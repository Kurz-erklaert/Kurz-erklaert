import numpy as np, cv2

f32 = np.float32


def norm(v):
    return v / np.maximum(np.linalg.norm(v, axis=-1, keepdims=True), 1e-9)


# ---------- SDF-Helfer (alle float32, p hat Form (N,3)) ----------
def rbox(p, c, b, r=0.03):
    q = np.abs(p - c) - (np.array(b, f32) - r)
    return np.linalg.norm(np.maximum(q, 0), axis=-1) + np.minimum(q.max(-1), 0) - r


def cyl(p, c, rad, h, axis=1, r=0.02):
    """Zylinder um Achse axis (0,1,2), Halbhoehe h."""
    q = p - c
    ax = q[..., axis]
    o = [i for i in range(3) if i != axis]
    rr = np.sqrt(q[..., o[0]] ** 2 + q[..., o[1]] ** 2)
    d0 = rr - rad + r
    d1 = np.abs(ax) - h + r
    return np.minimum(np.maximum(d0, d1), 0) + np.sqrt(np.maximum(d0, 0) ** 2 + np.maximum(d1, 0) ** 2) - r


def sph(p, c, r):
    return np.linalg.norm(p - c, axis=-1) - r


def ell(p, c, rad):
    q = (p - c) / np.array(rad, f32)
    k0 = np.linalg.norm(q, axis=-1)
    k1 = np.linalg.norm(q / np.array(rad, f32), axis=-1)
    return k0 * (k0 - 1.0) / np.maximum(k1, 1e-6)


def rot(p, c, ang, axis=2):
    """Punkte p um c um Achse drehen (inverse Drehung fuer SDF-Transformation)."""
    q = p - c
    ca, sa = np.cos(ang), np.sin(ang)
    o = [i for i in range(3) if i != axis]
    a, b = q[..., o[0]].copy(), q[..., o[1]].copy()
    q = q.copy()
    q[..., o[0]] = ca * a + sa * b
    q[..., o[1]] = -sa * a + ca * b
    return q + c


def smin(a, b, k=0.08):
    h = np.clip(0.5 + 0.5 * (b - a) / k, 0, 1)
    return b * (1 - h) + a * h - k * h * (1 - h)


class Scene:
    """Unterklassen liefern: sdf(p,t)->(d,idx), mat(p,idx,n,t)->dict, cam(t)->(ro,tgt,fov)"""
    spot = (0.0, 0.0, 0.0)
    spot_k = 0.12
    wall = False

    def sd(self, p, t):
        return self.sdf(p, t)[0]


def render(scene, t, W, H, ss=1):
    ys, xs = np.mgrid[0:H, 0:W].astype(f32)
    u = (xs / W - 0.5) * 2 * W / H
    v = -(ys / H - 0.5) * 2
    ro, tgt, fl = scene.cam(t)
    ro = np.array(ro, f32); tgt = np.array(tgt, f32)
    f = norm(tgt - ro); r = norm(np.cross(f, [0, 1, 0])); up = np.cross(r, f)
    rd = norm(f[None, None] * fl + u[..., None] * r + v[..., None] * up).reshape(-1, 3).astype(f32)
    N = rd.shape[0]
    tt = np.zeros(N, f32); hit = np.zeros(N, bool)
    alive = np.arange(N)
    for i in range(70):
        p = ro + rd[alive] * tt[alive, None]
        d = scene.sd(p, t)
        tt[alive] += d
        h = d < 0.0035
        far = tt[alive] > 22
        hit[alive[h]] = True
        alive = alive[~(h | far)]
        if len(alive) == 0:
            break
    hit[alive] = tt[alive] < 22
    hi = np.nonzero(hit)[0]
    img = np.zeros((N, 3), f32)
    emit_buf = np.zeros((N, 3), f32)
    bgv = background(W, H, scene)
    img[:] = bgv.reshape(-1, 3)
    if len(hi):
        p = ro + rd[hi] * tt[hi, None]
        d0, idx = scene.sdf(p, t)
        e = 2e-3
        n = norm(np.stack([scene.sd(p + [e, 0, 0], t) - scene.sd(p - [e, 0, 0], t),
                           scene.sd(p + [0, e, 0], t) - scene.sd(p - [0, e, 0], t),
                           scene.sd(p + [0, 0, e], t) - scene.sd(p - [0, 0, e], t)], -1).astype(f32))
        L = norm(np.array(scene.light, f32))
        sh = np.ones(len(hi), f32); tl = np.full(len(hi), 0.04, f32)
        for i in range(22):
            q = p + n * 0.012 + L * tl[:, None]
            dd = scene.sd(q, t)
            sh = np.minimum(sh, np.clip(9 * dd / tl, 0, 1)); tl += np.clip(dd, 0.04, 0.5)
        ao = np.ones(len(hi), f32)
        for k in range(1, 5):
            hh = 0.07 * k
            ao -= (hh - scene.sd(p + n * hh, t)) * 0.5 ** k * 3
        ao = np.clip(ao, 0, 1)
        m = scene.mat(p, idx, n, t)
        base = m['base']
        diff = np.clip((n * L).sum(-1), 0, 1)
        V = -rd[hi]
        Hh = norm(L + V)
        spec = np.clip((n * Hh).sum(-1), 0, 1) ** m['gloss'] * m['spec']
        fres = 0.04 + 0.96 * (1 - np.clip((n * V).sum(-1), 0, 1)) ** 5
        refl = rd[hi] - 2 * (rd[hi] * n).sum(-1, keepdims=True) * n
        env = (0.06 + 0.5 * np.clip(refl[:, 1:2] * 0.5 + 0.5, 0, 1) ** 2) * np.array([0.7, 0.82, 1.0], f32) \
            + 1.1 * np.clip(refl[:, 1:2] * 0.7 + 0.1 * refl[:, 0:1] - 0.15, 0, 1) ** 6 * np.array([1, 0.96, 0.9], f32)
        sp = np.exp(-(((p[:, 0] - scene.spot[0]) ** 2 + (p[:, 2] - scene.spot[2]) ** 2) * scene.spot_k))[:, None]
        sp = np.where(m.get('nospot', np.zeros(len(hi), bool))[:, None], 1.0, sp)
        key = np.array([1.0, 0.97, 0.92], f32)
        col = base * (0.10 * ao[:, None] + diff[:, None] * sh[:, None] * 0.95 * key) * sp
        col = col + (spec * sh)[:, None] * sp + env * (fres * 0.6 + m['refl'])[:, None] * ao[:, None] * sp
        em = m.get('emit', 0.0)
        col = col + em
        fog = np.exp(-np.clip(tt[hi], 0, 22) * 0.045)[:, None]
        col = col * fog + img[hi] * (1 - fog)
        img[hi] = col
        emit_buf[hi] = np.asarray(em) if np.ndim(em) else 0
    img = img.reshape(H, W, 3)
    eb = emit_buf.reshape(H, W, 3)
    if eb.max() > 0:
        k = max(3, int(H * 0.03) | 1)
        img = img + cv2.GaussianBlur(eb, (0, 0), k) * 0.9 + cv2.GaussianBlur(eb, (0, 0), k * 3) * 0.5
    img = np.clip(img, 0, 1) ** (1 / 2.2)
    if hasattr(scene, 'post'):
        def proj(P):
            P = np.array(P, f32); vv = P - ro
            z = vv @ f; x = vv @ r; y = vv @ up
            u_ = x * fl / z; v_ = y * fl / z
            return ((u_ / (2 * W / H) + 0.5) * W, (-v_ / 2 + 0.5) * H, fl / z * H / 2)
        img = scene.post(img, proj, t)
    return (np.clip(img, 0, 1) * 255).astype(np.uint8)


_bg_cache = {}


def background(W, H, scene):
    key = (W, H)
    if key not in _bg_cache:
        ys, xs = np.mgrid[0:H, 0:W].astype(f32)
        g = np.clip(1 - ((xs / W - 0.5) ** 2 * 1.2 + (ys / H - 0.35) ** 2 * 1.6) * 2.2, 0, 1)
        _bg_cache[key] = (np.array([0.012, 0.016, 0.026], f32) + 0.028 * g[..., None] * np.array([0.7, 0.9, 1.3], f32)).astype(f32)
    return _bg_cache[key]


def floor_mat(p, n, grid_scale=1.0):
    gx = np.abs(((p[:, 0] * grid_scale) % 1) - 0.5); gz = np.abs(((p[:, 2] * grid_scale) % 1) - 0.5)
    grid = np.maximum(gx, gz) > 0.488
    base = np.where(grid[:, None], 0.16, 0.045) * np.array([0.8, 0.95, 1.2], f32)
    return base.astype(f32)
