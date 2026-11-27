import numpy as np, math, cv2
from engine import *

# id: FLOOR WALL ENAMEL BRASS STEEL CLOTH DROP BLACK COPPER GAUGE RED YELLOW AIR
FLOOR, WALL, ENAMEL, BRASS, STEEL, CLOTH, DROP, BLACK, COPPER, GAUGE, RED, YELLOW, AIR = range(13)
TABLE = np.array([
    (0.05, 0.06, 0.08, 20, 0.15, 0.04),   # floor
    (0.07, 0.085, 0.11, 12, 0.05, 0.02),  # wall
    (0.92, 0.93, 0.95, 40, 0.5, 0.10),    # enamel
    (0.85, 0.60, 0.18, 60, 0.9, 0.45),    # brass
    (0.80, 0.82, 0.86, 80, 0.9, 0.62),    # steel
    (0.42, 0.46, 0.52, 6, 0.04, 0.02),    # cloth
    (0.30, 0.60, 0.95, 120, 1.2, 0.5),    # drop
    (0.035, 0.035, 0.04, 50, 0.5, 0.12),  # black
    (0.80, 0.42, 0.25, 60, 0.8, 0.40),    # copper
    (0.93, 0.93, 0.90, 20, 0.1, 0.05),    # gauge dial
    (0.80, 0.10, 0.07, 70, 0.8, 0.3),     # red
    (0.95, 0.75, 0.10, 40, 0.5, 0.15),    # yellow
    (0.75, 0.88, 1.00, 90, 1.0, 0.4),     # air bubble
], f32)

LIGHT = (-0.55, 1.0, 0.75)


def lookup(idx):
    T = TABLE[idx]
    return {'base': T[:, :3].copy(), 'gloss': T[:, 3], 'spec': T[:, 4], 'refl': T[:, 5]}


def ease(x):
    x = min(max(x, 0.0), 1.0); return x * x * (3 - 2 * x)


class Cam:
    @staticmethod
    def orbit(tgt, ang, dist, h, fl=2.0):
        return ((tgt[0] + math.sin(ang) * dist, h, tgt[2] + math.cos(ang) * dist), tgt, fl)


# =================================== HEIZUNG ===================================
class Heiz(Scene):
    light = LIGHT
    spot = (0.4, 0, 0.0); spot_k = 0.07

    def __init__(self, k):
        self.k = k

    # --- Geometrie ---
    def radiator(self, p):
        panel = rbox(p, (0, 1.3, -0.30), (1.6, 0.95, 0.07), 0.03)
        q = p.copy()
        xi = np.clip(np.round((p[:, 0] + 1.4) / 0.35), 0, 8)
        q[:, 0] = p[:, 0] - (-1.4 + xi * 0.35)
        ribs = rbox(q, (0, 1.3, -0.17), (0.14, 0.90, 0.13), 0.065)
        top = rbox(p, (0, 2.20, -0.22), (1.64, 0.07, 0.11), 0.04)
        bot = rbox(p, (0, 0.40, -0.22), (1.64, 0.07, 0.11), 0.04)
        pipes = np.minimum(cyl(p, (-1.35, 0.18, -0.22), 0.05, 0.2, 1, 0.01), cyl(p, (1.35, 0.18, -0.22), 0.05, 0.2, 1, 0.01))
        return np.minimum(np.minimum(panel, ribs), np.minimum(np.minimum(top, bot), pipes))

    def valve(self, p, ang):
        body = cyl(p, (1.78, 2.2, -0.22), 0.085, 0.13, 0, 0.02)
        nut = cyl(p, (1.93, 2.2, -0.22), 0.055, 0.04, 0, 0.01)
        q = rot(p, (1.97, 2.2, -0.22), ang, 0)
        head = rbox(q, (1.97, 2.2, -0.22), (0.03, 0.045, 0.045), 0.008)
        return np.minimum(np.minimum(body, nut), head)

    def sdf(self, p, t):
        k = self.k
        ds = [p[:, 1], p[:, 2] + 0.45, self.radiator(p)]
        ids = [FLOOR, WALL, ENAMEL]
        if k in (3, 4):
            ang = 0.0 if k == 3 else -min(t / 1.4, 1) * 2.6
            ds.append(self.valve(p, ang)); ids.append(BRASS)
        if k == 3:
            off = (1 - ease(t / 0.9)) * 1.3
            ds.append(rbox(p, (2.0 + off, 1.93, -0.12), (0.3, 0.045, 0.22), 0.03)); ids.append(CLOTH)
        if k == 4:
            ds.append(rbox(p, (2.0, 1.93, -0.12), (0.3, 0.045, 0.22), 0.03)); ids.append(CLOTH)
            ang = -min(t / 1.4, 1) * 2.6
            sh = cyl(p, (2.28, 2.2, -0.22), 0.028, 0.30, 0, 0.005)
            hq = rot(p, (2.0, 2.2, -0.22), ang, 0)
            hd = rbox(hq, (2.0, 2.2 + 0.0, -0.22), (0.035, 0.24, 0.035), 0.012)
            # Schluessel: Hebel vor dem Schaft, dreht mit
            hq2 = rot(p, (2.55, 2.2, -0.22), ang, 0)
            hd2 = rbox(hq2, (2.55, 2.2, -0.22), (0.035, 0.30, 0.035), 0.012)
            ds.append(np.minimum(sh, hd2)); ids.append(STEEL)
            for j in range(3):
                ph = (t * 1.1 + j / 3.0) % 1.0
                on = t > 1.2
                dp = sph(p, (1.97, 2.12 - ph * 0.17, -0.22), 0.026 if on else 0.0001)
                ds.append(dp); ids.append(DROP)
        if k == 1:
            for j in range(7):
                ph = (t * 0.28 + j * 0.173) % 1.0
                x = -1.4 + (j * 3 % 9) * 0.35
                y = 0.9 + ph * 1.2
                ds.append(sph(p, (x, y, 0.02), 0.07 + 0.025 * (j % 2))); ids.append(AIR)
        if k == 5:
            ds = [p[:, 1], p[:, 2] + 0.45]
            ids = [FLOOR, WALL]
            gc = (0, 1.7, 0)
            ds.append(cyl(p, gc, 0.88, 0.12, 2, 0.04)); ids.append(STEEL)
            ds.append(cyl(p, (0, 1.7, 0.128), 0.74, 0.012, 2, 0.004)); ids.append(GAUGE)
            ds.append(cyl(p, (0, 0.85, -0.05), 0.09, 0.85, 1, 0.01)); ids.append(COPPER)
            ds.append(cyl(p, (0, 1.17, -0.05), 0.15, 0.06, 1, 0.01)); ids.append(BRASS)
        D = np.stack(ds, -1)
        a = D.argmin(-1)
        return D.min(-1), np.array(ids)[a]

    def cam(self, t):
        k = self.k
        if k == 0: return Cam.orbit((0, 1.25, 0), 0.55 + 0.07 * t, 4.6, 1.8)
        if k == 1: return Cam.orbit((0.2, 1.6, -0.1), 0.25 + 0.04 * t, 3.5, 1.9)
        if k == 2: return Cam.orbit((0, 1.25, 0), -0.45 + 0.06 * t, 4.6, 1.4)
        if k == 3: return Cam.orbit((1.9, 2.05, -0.15), 0.65 + 0.04 * t, 3.2, 2.5)
        if k == 4: return Cam.orbit((2.0, 2.0, -0.15), 0.55 + 0.04 * t, 3.3, 2.4)
        if k == 5: return Cam.orbit((0.1, 1.45, 0), 0.30 + 0.04 * t, 4.0, 1.9)
        return Cam.orbit((0, 1.25, 0), 0.7 - 0.08 * t, 4.5, 1.7)

    def warm(self, t):
        k = self.k
        if k in (0, 1, 2): return 0.50 + 0.03 * math.sin(t * 1.3)
        if k in (3, 4): return 0.5
        return 1.1

    def gauge_val(self, t):
        return 0.35 + (1.5 - 0.35) * ease(t / 1.6) + 0.05 * math.sin(t * 5) * math.exp(-t * 1.5)

    def mat(self, p, idx, n, t):
        m = lookup(idx)
        fl = idx == FLOOR
        m['base'][fl] = floor_mat(p[fl], n[fl])
        em = np.zeros((len(idx), 3), f32)
        rad = (idx == ENAMEL) | (idx == BRASS) & False
        if self.k != 5 and rad.any():
            q = p[rad]; nn = n[rad]
            yn = np.clip((q[:, 1] - 0.35) / 1.9, 0, 1)
            w = self.warm(t)
            hot = np.clip((w - yn) / 0.16 + 0.5, 0, 1)
            amp = 0.55 + (0.12 * math.sin(t * 2.0) if self.k >= 6 else 0)
            hotc = np.array([1.0, 0.40, 0.07], f32); coldc = np.array([0.10, 0.30, 0.95], f32)
            front = (0.45 + 0.55 * np.clip(nn[:, 2], 0, 1))[:, None]
            em[rad] = (hot[:, None] * hotc * amp + (1 - hot[:, None]) * coldc * amp * 0.45) * front
        if self.k == 1:
            a = idx == AIR
            em[a] = np.array([0.25, 0.45, 0.9], f32) * 0.8
        if self.k == 4 or self.k == 3:
            d = idx == DROP
            em[d] = np.array([0.1, 0.25, 0.5], f32)
        if self.k == 5:
            g = idx == GAUGE
            if g.any():
                x = p[g, 0]; y = p[g, 1] - 1.7
                r = np.sqrt(x * x + y * y)
                ang = np.degrees(np.arctan2(x, y))  # 0=oben, + = im Uhrzeigersinn
                col = np.tile(np.array([0.93, 0.93, 0.90], f32), (g.sum(), 1))
                val = np.clip((ang + 135) / 270 * 4, -1, 5)
                inarc = (np.abs(ang) <= 135)
                green = inarc & (val >= 1.0) & (val <= 2.0) & (r > 0.50) & (r < 0.61)
                yellow = inarc & (val > 2.0) & (val <= 3.0) & (r > 0.50) & (r < 0.61)
                redz = inarc & (val > 3.0) & (r > 0.50) & (r < 0.61)
                col[green] = (0.15, 0.65, 0.25); col[yellow] = (0.9, 0.7, 0.1); col[redz] = (0.8, 0.12, 0.1)
                tick = inarc & (r > 0.62) & (r < 0.70)
                frac = (val / 0.5) % 1
                major = (np.abs(val - np.round(val)) < 0.02)
                tk = tick & ((np.minimum(frac, 1 - frac) < 0.04) | major)
                col[tk] = (0.08, 0.08, 0.1)
                # Nadel
                va = self.gauge_val(t)
                na = math.radians(-135 + 270 * va / 4)
                dx, dy = math.sin(na), math.cos(na)
                s = x * dx + y * dy
                dist = np.abs(-x * dy + y * dx)
                nd = (s > -0.12) & (s < 0.58) & (dist < 0.018 + 0.012 * (1 - np.clip(s / 0.58, 0, 1)))
                col[nd] = (0.85, 0.08, 0.05)
                col[r < 0.065] = (0.1, 0.1, 0.12)
                m['base'][g] = col
        return {**m, 'emit': em}

    def post(self, img, proj, t):
        return img


# =================================== KOCHER ===================================
class Koch(Scene):
    light = LIGHT
    spot = (0.0, 0, 0.0); spot_k = 0.16

    def __init__(self, k):
        self.k = k

    def kettle_sdf(self, p, open_):
        outer = cyl(p, (0, 0.62, 0), 0.78, 0.50, 1, 0.04)
        if open_:
            inner = cyl(p, (0, 0.78, 0), 0.69, 0.60, 1, 0.01)
            body = np.maximum(outer, -inner)
        else:
            body = outer
        base = cyl(p, (0, 0.08, 0), 0.90, 0.08, 1, 0.03)
        ds = [body, base]; ids = [STEEL, BLACK]
        # Henkel (Torus-Hälfte rechts)
        q = np.stack([p[:, 0] - 0.78, p[:, 1] - 0.66, p[:, 2]], -1)
        tor = np.sqrt((np.sqrt(q[:, 0] ** 2 + q[:, 1] ** 2) - 0.44) ** 2 + q[:, 2] ** 2) - 0.065
        tor = np.maximum(tor, -(p[:, 0] - 0.75))
        ds.append(tor); ids.append(BLACK)
        ds.append(rbox(p, (-0.84, 1.02, 0), (0.2, 0.1, 0.2), 0.05)); ids.append(STEEL)
        if not open_:
            ds.append(ell(p, (0, 1.12, 0), (0.74, 0.15, 0.74))); ids.append(BLACK)
            ds.append(sph(p, (0, 1.30, 0), 0.09)); ids.append(BLACK)
        return ds, ids

    def sdf(self, p, t):
        k = self.k
        ds = [p[:, 1], p[:, 2] + 3.2]
        ids = [FLOOR, WALL]
        if k == 5:
            th = ease(t / 1.1) * math.radians(42)
            pv = (-0.9, 0.0, 0.0)
            q = rot(p, pv, th, 2)
            kd, ki = self.kettle_sdf(q, False)
            self.th = th
            # Strahl
            tip = self.spout_tip(th)
            for j in range(16):
                s = ((j / 16.0) + t * 1.6) % 1.0
                pos = (tip[0] - 0.55 * s, tip[1] - 2.2 * s * s - 0.08 * s, 0)
                if pos[1] < 0.03: pos = (pos[0], 0.03, 0)
                if t > 0.7: kd.append(sph(p, pos, 0.035)); ki.append(DROP)
        else:
            kd, ki = self.kettle_sdf(p, k in (1, 3))
        ds += kd; ids += ki
        if k == 3:
            ds.append(ell(p, (0, 2.0, 0), (0.36, 0.28, 0.28))); ids.append(YELLOW)
            for j in range(4):
                ph = (t * 0.9 + j / 4.0) % 1.0
                ds.append(sph(p, (0.05 * (j % 2 - 0.5), 1.7 - ph * 0.9, 0.04 * j - 0.06), 0.035)); ids.append(DROP)
        D = np.stack(ds, -1)
        a = D.argmin(-1)
        return D.min(-1), np.array(ids)[a]

    def spout_tip(self, th):
        c, s = math.cos(th), math.sin(th)
        x0, y0 = -1.04 + 0.9, 1.02
        return (-0.9 + c * x0 - s * y0, 0.0 + s * x0 + c * y0, 0)

    def cam(self, t):
        k = self.k
        if k == 0: return Cam.orbit((0, 0.7, 0), 0.5 + 0.08 * t, 3.9, 1.6)
        if k == 1: return Cam.orbit((0, 0.8, 0), 0.4 + 0.05 * t, 2.8, 3.2)
        if k == 2: return Cam.orbit((0, 0.85, 0), -0.4 + 0.06 * t, 4.0, 1.3)
        if k == 3: return Cam.orbit((0, 1.1, 0), 0.5 + 0.05 * t, 4.6, 2.5)
        if k == 4: return Cam.orbit((0, 0.85, 0), 0.7 - 0.06 * t, 4.0, 1.2)
        if k == 5: return Cam.orbit((-0.3, 0.8, 0), 0.0 + 0.02 * t, 4.8, 1.2)
        return Cam.orbit((0, 0.7, 0), 0.9 + 0.1 * t, 3.9, 1.6)

    def mat(self, p, idx, n, t):
        m = lookup(idx)
        fl = idx == FLOOR
        m['base'][fl] = floor_mat(p[fl], n[fl])
        em = np.zeros((len(idx), 3), f32)
        k = self.k
        if k in (1, 3):
            st = (idx == STEEL) & (np.hypot(p[:, 0], p[:, 2]) < 0.715) & (p[:, 1] < 1.0)
            if st.any():
                q = p[st]
                nz = (np.sin(q[:, 0] * 23) * np.sin(q[:, 2] * 19) + np.sin(q[:, 1] * 31 + q[:, 0] * 7)) * 0.5
                chalk = np.array([0.93, 0.91, 0.84], f32) * (0.82 + 0.18 * nz[:, None])
                amt = 1.0 if k == 1 else max(0.0, 1.0 - t * 0.35)
                m['base'][st] = chalk * amt + m['base'][st] * (1 - amt)
                m['spec'][st] = 0.08; m['gloss'][st] = 8; m['refl'][st] = 0.03
        if k in (2, 4):
            b = idx == BLACK
            glow = (0.5 + 0.5 * math.sin(t * 3)) * 0.35 + 0.5
            ring = b & (p[:, 1] < 0.12)
            em[ring] = np.array([1.0, 0.35, 0.05], f32) * glow * 0.9
        if k == 3:
            d = idx == DROP
            em[d] = np.array([0.25, 0.22, 0.05], f32)
        if k == 5:
            d = idx == DROP
            em[d] = np.array([0.1, 0.25, 0.5], f32)
        return {**m, 'emit': em}

    def post(self, img, proj, t):
        k = self.k
        H, W = img.shape[:2]
        layer = np.zeros((H, W), f32)
        if k in (2, 4):
            for j in range(7):
                ph = (t * 0.45 + j / 7.0) % 1.0
                P = (-1.05 - 0.15 * ph, 1.15 + ph * 1.5, 0.0 + 0.1 * math.sin(ph * 6 + j))
                x, y, sc = proj(P)
                rad = (0.12 + 0.30 * ph) * sc
                a = 0.55 * (1 - ph) ** 1.2 * min(ph * 6, 1)
                cv2.circle(layer, (int(x), int(y)), max(1, int(rad)), a, -1, cv2.LINE_AA)
            layer = cv2.GaussianBlur(layer, (0, 0), max(2, W * 0.035))
            img = img + layer[..., None] * np.array([0.8, 0.88, 1.0], f32)
        if k == 6:
            glints = [((-0.45, 0.95, 0.72), 0.0), ((0.35, 0.6, 0.75), 1.3), ((0.1, 1.12, 0.45), 2.4)]
            for P, ph in glints:
                x, y, sc = proj(P)
                a = max(0.0, math.sin(t * 2.6 + ph)) ** 2
                if a > 0.02:
                    L = int(0.20 * sc * a) + 2
                    cv2.line(layer, (int(x - L), int(y)), (int(x + L), int(y)), a, 2, cv2.LINE_AA)
                    cv2.line(layer, (int(x), int(y - L)), (int(x), int(y + L)), a, 2, cv2.LINE_AA)
            layer = cv2.GaussianBlur(layer, (0, 0), 1.5) * 2.0
            img = img + layer[..., None]
        return np.clip(img, 0, 1)


def make(video, k):
    return Heiz(k) if video == 'heizung' else Koch(k)


if __name__ == '__main__':
    import sys, time
    from PIL import Image
    video = sys.argv[1]
    W, H = 189, 220
    times = [1.5, 1.2, 1.5, 1.6, 2.2, 1.8, 1.5]
    if len(sys.argv) > 2:
        sel = [int(x) for x in sys.argv[2].split(',')]
    else:
        sel = range(7)
    tiles = []
    t0 = time.time()
    for k in sel:
        im = render(make(video, k), times[k], W, H)
        tiles.append(im)
        print(k, round(time.time() - t0, 1), flush=True)
    sheet = np.concatenate(tiles, axis=1)
    Image.fromarray(sheet).resize((sheet.shape[1] * 2, sheet.shape[0] * 2), Image.LANCZOS).save(f'sheet_{video}.png')
