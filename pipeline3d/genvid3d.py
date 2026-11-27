import sys, os, json, math, subprocess, time
import numpy as np, cv2
from multiprocessing import Pool
from PIL import Image, ImageDraw, ImageFont
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

W, H, FPS = 1080, 1920, 30
RW, RH, RFPS = 378, 440, 10
R3H = 1257
SCR = '/tmp/claude-0/-home-claude/9933ae9d-2912-5ee4-8ee1-1140ae92f947/scratchpad'
WORK = SCR + '/work'
FD = '/usr/share/fonts/opentype/inter/'
AMBER = (255, 196, 64); WHITE = (245, 247, 250); GREENC = (90, 210, 130); BASE = (3, 4, 7)

TEXT = {
 'heizung': dict(
  scenes=[
   (['So wird deine kalte Heizung', 'wieder richtig warm.'], {'warm.'}),
   (['Meistens ist Luft', 'im Heizkörper.'], {'Luft'}),
   (['Sie steigt nach oben und verdrängt das heiße Wasser,', 'deshalb bleibt der Heizkörper oben kalt.', 'Drei Schritte helfen.'], {'Luft', 'kalt.'}),
   (['Erstens: Halte ein Tuch', 'unter das Entlüftungsventil.'], {'Tuch'}),
   (['Zweitens: Öffne es mit dem Schlüssel,', 'bis Wasser statt Luft kommt.'], {'Wasser'}),
   (['Drittens: Schließ es wieder', 'und prüfe den Druck der Anlage.'], {'Druck'}),
   (['Merk dir:', 'Tuch, öffnen, Druck prüfen.'], {'Tuch', 'öffnen', 'Druck'}),
  ],
  titles=['Heizung bleibt kalt –', 'Luft im Heizkörper', 'Oben kalt, unten warm', None, None, None, None],
  steps=['1. Tuch unterlegen', '2. Ventil öffnen', '3. Druck prüfen'],
  out='s3d_heizung.mp4'),
 'kocher': dict(
  scenes=[
   (['So wird dein Wasserkocher', 'in zehn Minuten kalkfrei.'], {'kalkfrei.'}),
   (['Der weiße Belag im Wasserkocher', 'ist Kalk aus dem Wasser.'], {'Kalk'}),
   (['Beim Erhitzen bleibt er zurück', 'und setzt sich fest.', 'Drei Schritte lösen ihn.'], {'Erhitzen', 'fest.'}),
   (['Erstens: Gib Wasser mit etwas', 'Zitronensäure oder Essig hinein.'], {'Zitronensäure', 'Essig'}),
   (['Zweitens: Koche es einmal auf', 'und lass es kurz wirken.'], {'Koche', 'wirken.'}),
   (['Drittens: Gieß alles weg', 'und spüle gründlich nach.'], {'spüle'}),
   (['Merk dir:', 'Säure, aufkochen, gut ausspülen.'], {'Säure', 'aufkochen', 'gut'}),
  ],
  titles=['Wasserkocher verkalkt?', 'Das ist Kalk', 'Hitze setzt ihn fest', None, None, None, None],
  steps=['1. Säure hineingeben', '2. Aufkochen', '3. Gut ausspülen'],
  out='s3d_kocher.mp4'),
}


def font(n, s):
    return ImageFont.truetype(FD + n, int(s))


def timing(vid):
    SC_TXT = TEXT[vid]['scenes']
    AUD = f'{WORK}/voice_{vid}.mp3'
    al = json.load(open(f'{WORK}/align_{vid}.json'))
    toks = []; cur = ''; st = en = None; inb = False
    for ch, a, b in zip(al['characters'], al['character_start_times_seconds'], al['character_end_times_seconds']):
        if ch == '[': inb = True; continue
        if ch == ']': inb = False; continue
        if inb: continue
        if ch.isspace():
            if cur: toks.append((cur, st, en)); cur = ''
            continue
        if not cur: st = a
        cur += ch; en = b
    if cur: toks.append((cur, st, en))
    ti = 0; SC = []
    for chunks, kw in SC_TXT:
        cs = []
        for c in chunks:
            ws = c.split(); seg = toks[ti:ti + len(ws)]
            assert [t[0] for t in seg] == ws, (ws, [t[0] for t in seg])
            ti += len(ws); cs.append(seg)
        SC.append((cs, {k.strip('.,:?!') for k in kw}))
    assert ti == len(toks)
    adur = float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', AUD], capture_output=True, text=True).stdout)
    bounds = [0.0] + [SC[i][0][0][0][1] - 0.15 for i in range(1, 7)]
    total = max(adur, toks[-1][2]) + 0.7
    fb = [round(b * FPS) for b in bounds] + [round(total * FPS)]
    return SC, fb, AUD


CF = font('Inter-ExtraBold.otf', 84)


def layout(seg, s0):
    sp_ = CF.getlength(' '); lines = []; cur = []; cw = 0
    for w, a, b in seg:
        wl = CF.getlength(w)
        if cur and cw + sp_ + wl > 960:
            lines.append(cur); cur = []; cw = 0
        cw += (sp_ if cur else 0) + wl; cur.append((w, wl, a - s0))
    lines.append(cur); out = []; lh = 112; y0 = 1560 - len(lines) * lh / 2
    for li, ln in enumerate(lines):
        tot = sum(x[1] for x in ln) + sp_ * (len(ln) - 1); x = (W - tot) / 2
        for w, wl, tw in ln:
            out.append((w, x, y0 + li * lh, tw)); x += wl + sp_
    return out


def job(a):
    vid, si, j = a
    import scenes3d
    from engine import render
    return render(scenes3d.make(vid, si), j / RFPS, RW, RH)


def render_lowres(vid, fb):
    jobs = []
    for si in range(7):
        dur = (fb[si + 1] - fb[si]) / FPS
        n = int(dur * RFPS) + 2
        jobs += [(vid, si, j) for j in range(n)]
    path = f'{WORK}/lr_{vid}.npz'
    if os.path.exists(path):
        z = np.load(path); return [z[f's{i}'] for i in range(7)]
    t0 = time.time(); out = []
    with Pool(2) as pool:
        for k, im in enumerate(pool.imap(job, jobs, chunksize=2)):
            out.append(im)
            if k % 20 == 0: print(vid, 'render', k, '/', len(jobs), round(time.time() - t0), 's', flush=True)
    res = []; pos = 0
    for si in range(7):
        n = int((fb[si + 1] - fb[si]) / FPS * RFPS) + 2
        res.append(np.stack(out[pos:pos + n])); pos += n
    np.savez(path, **{f's{i}': r for i, r in enumerate(res)})
    return res


def make_static():
    badge = Image.new('RGBA', (W, 260), (0, 0, 0, 0)); d = ImageDraw.Draw(badge)
    f = font('Inter-Bold.otf', 34); tx = 'KURZ ERKLÄRT  ·  ALLTAG'
    # Buchstabenabstand
    wtot = sum(f.getlength(c) + 3 for c in tx)
    d.rounded_rectangle([84, 90, 84 + wtot + 84, 90 + 62], radius=14, fill=(40, 30, 8, 150), outline=AMBER, width=2)
    d.ellipse([104, 111, 122, 129], fill=AMBER)
    x = 140
    for c in tx:
        d.text((x, 121), c, font=f, fill=AMBER, anchor='lm'); x += f.getlength(c) + 3
    return badge


BADGE = make_static()
GRAD = np.linspace(0, 1, 200)[:, None, None]


def frame3d(lr, si, t):
    arr = lr[si]; x = t * RFPS
    i0 = int(x); i1 = min(i0 + 1, len(arr) - 1); i0 = min(i0, len(arr) - 1); f = x - int(x)
    a = arr[i0].astype(np.float32) * (1 - f) + arr[i1].astype(np.float32) * f
    up = cv2.resize(a, (W, R3H), interpolation=cv2.INTER_CUBIC)
    bl = cv2.GaussianBlur(up, (0, 0), 3)
    up = np.clip(up + (up - bl) * 0.7, 0, 255)
    up += np.random.normal(0, 2.2, up.shape[:2])[..., None].astype(np.float32)
    # Vignette seitlich
    return up


def compose(vid, SC, lay, lr, si, t, dur, cfg):
    canvas = np.empty((H, W, 3), np.float32); canvas[:] = BASE
    up = frame3d(lr, si, t)
    fade = np.ones((R3H, 1, 1), np.float32)
    fade[-240:, 0, 0] = np.linspace(1, 0, 240) ** 1.4
    fade[:110, 0, 0] *= np.linspace(0, 1, 110)[:, None] [:, 0] ** 1.2 if False else np.linspace(0, 1, 110) ** 1.2
    OFF = 150
    canvas[OFF:OFF + R3H] = up * fade + np.array(BASE, np.float32) * (1 - fade)
    # sanfter Einblender am Szenenbeginn
    if t < 0.18:
        canvas[OFF:OFF + R3H] *= 0.55 + 0.45 * (t / 0.18)
    im = Image.fromarray(np.clip(canvas, 0, 255).astype(np.uint8)).convert('RGBA')
    im.alpha_composite(BADGE)
    d = ImageDraw.Draw(im)
    title = cfg['titles'][si]
    if title:
        p = min(1.0, t / 0.3)
        d.rectangle([84, 200, 92, 288], fill=AMBER + (int(255 * p),))
        d.text((118, 244), title, font=font('Inter-ExtraBold.otf', 66), fill=WHITE + (int(255 * p),), anchor='lm')
    elif si >= 3:
        st = cfg['steps']
        for i, s in enumerate(st):
            y = 232 + i * 82
            done = (si > 3 + i) or (si == 3 + i and t > dur * 0.55) or si == 6
            cur = (si == 3 + i)
            d.rounded_rectangle([108, y - 24, 156, y + 24], radius=10, outline=(GREENC if done else (190, 195, 205)) + (255,), width=4, fill=(30, 70, 45, 255) if done else (0, 0, 0, 0))
            if done:
                d.line([(118, y), (130, y + 12), (148, y - 12)], fill=GREENC + (255,), width=6, joint='curve')
            d.text((178, y), s, font=font('Inter-Bold.otf', 50), fill=(WHITE if (done or cur) else (150, 156, 168)) + (255,), anchor='lm')
    kw = SC[si][1]
    act = None
    for l in lay[si]:
        if l[0][3] <= t + 0.02: act = l
    if act:
        for w, wx, wy, tw in act:
            p = max(0.0, min(1.0, (t - tw) / 0.14))
            if p <= 0: continue
            col = AMBER if w.strip('.,:?!') in kw else WHITE
            d.text((wx, wy + (1 - p) * 20), w, font=CF, fill=col + (int(255 * p),), anchor='lt', stroke_width=7, stroke_fill=(2, 3, 6, int(255 * p)))
    return np.array(im.convert('RGB'))


def build(vid):
    cfg = TEXT[vid]
    SC, fb, AUD = timing(vid)
    print(vid, 'Szenen', [round((fb[i + 1] - fb[i]) / FPS, 2) for i in range(7)], flush=True)
    lr = render_lowres(vid, fb)
    S0 = [fb[i] / FPS for i in range(7)]
    lay = [[layout(seg, S0[i]) for seg in SC[i][0]] for i in range(7)]
    tmp = f'{WORK}/v3d_{vid}_tmp.mp4'
    p = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                          '-c:v', 'libx264', '-crf', '18', '-preset', 'veryfast', '-pix_fmt', 'yuv420p', tmp], stdin=subprocess.PIPE)
    for si in range(7):
        n = fb[si + 1] - fb[si]; dur = n / FPS
        for i in range(n):
            p.stdin.write(compose(vid, SC, lay, lr, si, i / FPS, dur, cfg).tobytes())
        print(vid, 'compose scene', si, flush=True)
    p.stdin.close(); assert p.wait() == 0
    out = f'{SCR}/{cfg["out"]}'
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', tmp, '-i', AUD, '-map', '0:v', '-map', '1:a', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '192k', out], check=True)
    print(vid, 'FERTIG', out, flush=True)


if __name__ == '__main__':
    if sys.argv[1] == 'still':
        vid = sys.argv[2]
        cfg = TEXT[vid]; SC, fb, AUD = timing(vid)
        S0 = [fb[i] / FPS for i in range(7)]
        lay = [[layout(seg, S0[i]) for seg in SC[i][0]] for i in range(7)]
        import scenes3d
        from engine import render
        pts = [(0, 1.5), (2, 2.5), (3, 2.0), (4, 2.2), (5, 2.0), (6, 2.0)]
        lr = [None] * 7
        sel = []
        for si, t in pts:
            lr[si] = np.stack([render(scenes3d.make(vid, si), t, RW, RH)] * 3)
        tiles = []
        for si, t in pts:
            dur = (fb[si + 1] - fb[si]) / FPS
            fr = compose(vid, SC, lay, lr, si, 0.0 + min(t, 1.4) * 0 + 1.4 if False else min(t + S0[si] * 0, dur - 0.05), dur, cfg)
            tiles.append(Image.fromarray(fr).resize((360, 640), Image.LANCZOS))
        sheet = Image.new('RGB', (360 * len(tiles), 640))
        for i, tl in enumerate(tiles): sheet.paste(tl, (i * 360, 0))
        sheet.save(f'{SCR}/r3d/still_{vid}.png')
    else:
        for vid in sys.argv[1:]:
            build(vid)
