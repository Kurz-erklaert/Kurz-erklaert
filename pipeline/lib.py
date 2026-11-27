YEL = (247, 206, 70); BRN = (120, 80, 40); STEEL = (222, 228, 238); PUFF = (205, 232, 190)
ICE = (110, 190, 235); WOOD = (196, 146, 92); DARKG = (100, 125, 90); MIST = (236, 243, 249); CRUMB = (248, 228, 185)


def lerp(a, b, p):
    p = max(0.0, min(1.0, p))
    return tuple(int(a[i] + (b[i] - a[i]) * p) for i in range(3))


def badge(c, n, t):
    s = eob((t - 0.15) / 0.35)
    if s <= 0.05:
        return
    c.ell(95, 95, 58 * s, fill=ORANGE)
    c.text(95, 98, str(n), 76 * s, WHITE)


def pill(c, cx, cy, w, h, txt, size, fill, tc):
    c.rr(cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2, h / 2, fill=fill)
    c.text(cx, cy + 3, txt, size, tc)


def snow(c, cx, cy, r, col, w):
    for i in range(6):
        a = i * math.pi / 3
        c.line([(cx, cy), (cx + math.cos(a) * r, cy + math.sin(a) * r)], col, w)
        mx, my = cx + math.cos(a) * r * .62, cy + math.sin(a) * r * .62
        for sg in (-1, 1):
            b = a + sg * 0.75
            c.line([(mx, my), (mx + math.cos(b) * r * .3, my + math.sin(b) * r * .3)], col, w * .8)


def drop(c, x, y, s=1.0):
    c.poly([(x, y - 34 * s), (x - 17 * s, y + 2 * s), (x + 17 * s, y + 2 * s)], WATER)
    c.ell(x, y + 6 * s, 17 * s, fill=WATER)


def sun(c, cx, cy, r, t=0):
    for i in range(10):
        a = t * .5 + i * math.pi / 5
        c.line([(cx + math.cos(a) * r * 1.3, cy + math.sin(a) * r * 1.3), (cx + math.cos(a) * r * 1.75, cy + math.sin(a) * r * 1.75)], ORANGE, r * .16)
    c.ell(cx, cy, r, fill=ORANGE)


def wavy(c, x, y, s, t, col=PUFF, n=5, w=9):
    pts = [(x + math.sin(i * 1.1 + t * 4) * 14 * s, y - i * 20 * s) for i in range(n)]
    c.line(pts, col, w * s)


def sparkle(c, x, y, r, col=ORANGE, w=8):
    c.line([(x - r, y), (x + r, y)], col, w); c.line([(x, y - r), (x, y + r)], col, w)
    c.line([(x - r * .6, y - r * .6), (x + r * .6, y + r * .6)], col, w * .7); c.line([(x - r * .6, y + r * .6), (x + r * .6, y - r * .6)], col, w * .7)


def bolt(c, x, y, s, col=ORANGE):
    c.poly([(x + 10 * s, y - 90 * s), (x - 40 * s, y + 10 * s), (x - 5 * s, y + 10 * s), (x - 20 * s, y + 90 * s), (x + 40 * s, y - 20 * s), (x + 5 * s, y - 20 * s)], col)


def coins(c, cx, cy, s, n):
    for k in range(int(n)):
        c.rr(cx - 70 * s, cy - k * 24 * s - 15 * s, cx + 70 * s, cy - k * 24 * s + 15 * s, 15 * s, fill=YEL, out=NAVY, w=6)


def washer(c, cx, cy, s, t=0, door=False, stink=False, drawer=False, glow=False):
    c.rr(cx - 150 * s, cy - 190 * s, cx + 150 * s, cy + 190 * s, 30 * s, fill=(232, 236, 244), out=NAVY, w=10)
    c.line([(cx - 150 * s, cy - 110 * s), (cx + 150 * s, cy - 110 * s)], NAVY, 8 * s)
    c.ell(cx + 100 * s, cy - 150 * s, 16 * s, fill=ORANGE)
    dx = -62 * s if drawer else 0
    c.rr(cx - 130 * s + dx, cy - 168 * s, cx - 30 * s + dx, cy - 128 * s, 10 * s, fill=WHITE, out=NAVY, w=7)
    if door:
        c.ell(cx, cy + 40 * s, 92 * s, fill=NAVY)
        c.ell(cx - 112 * s, cy + 40 * s, 34 * s, fill=(190, 215, 235), out=NAVY, w=8)
    else:
        c.ell(cx, cy + 40 * s, 100 * s, fill=(190, 215, 235), out=NAVY, w=12)
        c.ell(cx, cy + 40 * s, 64 * s, fill=(130, 170, 205))
    if stink:
        for k in (-60, 0, 60):
            wavy(c, cx + k * s, cy - 200 * s, s, t + k, PUFF)
    if glow:
        c.ell(cx, cy + 40 * s, 125 * s, out=ORANGE, w=10 * s)


def face(c, cx, cy, s, mouth='smile', cheeks=False):
    if cheeks:
        for sg in (-1, 1):
            c.ell(cx + sg * 92 * s, cy + 30 * s, 40 * s, fill=PEACH, out=NAVY, w=7)
    c.ell(cx, cy, 100 * s, fill=PEACH, out=NAVY, w=9)
    for ex in (-36, 36):
        c.ell(cx + ex * s, cy - 20 * s, 9 * s, fill=NAVY)
    if mouth == 'o':
        c.ell(cx, cy + 45 * s, 20 * s, fill=NAVY)
    elif mouth == 'smile':
        c.arc(cx, cy + 25 * s, 36 * s, 20, 160, NAVY, 7 * s)
    else:
        c.line([(cx - 22 * s, cy + 52 * s), (cx + 22 * s, cy + 52 * s)], NAVY, 7 * s)


def mask(c, cx, cy, s):
    for sg in (-1, 1):
        c.line([(cx + sg * 78 * s, cy + 25 * s), (cx + sg * 108 * s, cy + 2 * s)], NAVY, 7 * s)
    c.rr(cx - 78 * s, cy + 5 * s, cx + 78 * s, cy + 82 * s, 36 * s, fill=WHITE, out=NAVY, w=7)


def glass(c, cx, cy, s, p):
    top, bot = cy - 160 * s, cy + 160 * s
    xl = lambda y: cx - 65 * s + 17 * s * (y - top) / (bot - top)
    xr = lambda y: cx + 65 * s - 17 * s * (y - top) / (bot - top)
    c.poly([(cx - 65 * s, top), (cx + 65 * s, top), (cx + 48 * s, bot), (cx - 48 * s, bot)], (238, 246, 252))
    yw = bot - (bot - top) * max(p, 0.02)
    c.poly([(xl(yw), yw), (xr(yw), yw), (cx + 48 * s, bot), (cx - 48 * s, bot)], WATER)
    c.line([(cx - 65 * s, top), (cx - 48 * s, bot), (cx + 48 * s, bot), (cx + 65 * s, top)], NAVY, 10 * s)


def glasses(c, cx, cy, s, fog=0.0):
    col = lerp(SKY, (244, 247, 251), fog)
    c.line([(cx - 185 * s, cy - 10 * s), (cx - 240 * s, cy - 45 * s)], NAVY, 11 * s)
    c.line([(cx + 185 * s, cy - 10 * s), (cx + 240 * s, cy - 45 * s)], NAVY, 11 * s)
    for sg in (-1, 1):
        c.ell(cx + sg * 100 * s, cy, 85 * s, fill=col, out=NAVY, w=12 * s)
    c.line([(cx - 18 * s, cy - 10 * s), (cx, cy - 26 * s), (cx + 18 * s, cy - 10 * s)], NAVY, 10 * s)
    if fog > 0.35:
        for dx, dy, r in ((-130, -30, 9), (-85, 20, 7), (-60, -45, 8), (80, -25, 8), (120, 25, 9), (60, 40, 7), (-110, 40, 6), (105, -50, 6)):
            drop(c, cx + dx * s, cy + dy * s, r / 14 * s * 1.3)


def window(c, cx, cy, s, mist=0.0, open_=False, mold=False):
    col = lerp(SKY, MIST, mist)
    c.rr(cx - 130 * s, cy - 170 * s, cx + 130 * s, cy + 170 * s, 10 * s, fill=(255, 255, 255) if open_ else col, out=NAVY, w=12 * s)
    if not open_:
        c.line([(cx, cy - 170 * s), (cx, cy + 170 * s)], NAVY, 10 * s); c.line([(cx - 130 * s, cy), (cx + 130 * s, cy)], NAVY, 10 * s)
        if mist > 0.4:
            for dx, dy in ((-80, -90), (-50, -20), (60, -110), (85, -30), (-90, 60), (30, 80), (70, 110), (-30, 120)):
                drop(c, cx + dx * s, cy + dy * s, 0.8 * s)
    c.rr(cx - 155 * s, cy + 170 * s, cx + 155 * s, cy + 195 * s, 8 * s, fill=NAVY)
    if mold:
        for dx, dy, r in ((-165, -110, 24), (-195, -75, 17), (-160, -60, 14), (-188, -135, 12)):
            c.ell(cx + dx * s, cy + dy * s, r * s, fill=DARKG)


def airflow(c, x0, x1, y, t):
    for k in range(3):
        yy = y + (k - 1) * 70
        xh = x0 + ((t * 0.7 + k * 0.33) % 1) * (x1 - x0)
        c.line([(xh - 110, yy), (xh, yy)], ORANGE, 12)
        c.poly([(xh + 2, yy - 24), (xh + 38, yy), (xh + 2, yy + 24)], ORANGE)


def radiator(c, cx, cy, s, t=0):
    c.rr(cx - 160 * s, cy - 110 * s, cx + 160 * s, cy + 110 * s, 22 * s, fill=(240, 240, 245), out=NAVY, w=10)
    for k in range(6):
        c.line([(cx - 125 * s + k * 50 * s, cy - 80 * s), (cx - 125 * s + k * 50 * s, cy + 80 * s)], NAVY, 8 * s)
    for k in (-90, 0, 90):
        wavy(c, cx + k * s, cy - 125 * s, s, t + k, ORANGE, n=4)


def banana(c, cx, cy, s, p=0.0, col=None):
    col = col or lerp(YEL, BRN, p)
    pts = [(cx + 190 * s * math.cos(math.radians(a)), cy - 110 * s + 190 * s * math.sin(math.radians(a))) for a in range(30, 151, 8)]
    c.line(pts, NAVY, 84 * s); c.line(pts, col, 64 * s)
    c.ell(pts[0][0], pts[0][1], 13 * s, fill=BRN)
    c.rr(pts[-1][0] - 16 * s, pts[-1][1] - 42 * s, pts[-1][0] + 18 * s, pts[-1][1] - 8 * s, 6 * s, fill=BRN)


def bunch(c, cx, cy, s, p=0.0, foil=False, spread=0.0):
    for k in range(3):
        banana(c, cx + (k - 1) * spread, cy + (k - 1) * (55 * s) * (1 - min(spread / 140, 0.0)), s, p)
    if foil:
        c.rr(cx + 125 * s, cy - 175 * s, cx + 215 * s, cy + 25 * s, 12 * s, fill=STEEL, out=NAVY, w=7)


def apple(c, cx, cy, s):
    c.ell(cx, cy, 75 * s, fill=RED, out=NAVY, w=9 * s)
    c.line([(cx, cy - 70 * s), (cx + 8 * s, cy - 105 * s)], NAVY, 8 * s)
    c.ell(cx + 36 * s, cy - 92 * s, 22 * s, fill=GREEN, out=NAVY, w=6 * s)


def puffs(c, cx, cy, s, t, n=5):
    for k in range(n):
        ph = (t * 0.45 + k / n) % 1
        c.ell(cx + math.sin(k * 2.3 + t) * 60 * s, cy - ph * 230 * s, (16 + 22 * ph) * s, fill=PUFF)


def hand(c, cx, cy, s, wr=0.0):
    for k, h in enumerate((150, 175, 175, 150)):
        x = cx - 72 * s + k * 48 * s
        c.rr(x - 20 * s, cy - h * s, x + 20 * s, cy + 30 * s, 20 * s, fill=PEACH, out=NAVY, w=8)
        for j in range(4):
            if wr > j / 4 + 0.1:
                yy = cy - (h - 25 - j * 28) * s
                c.line([(x - 12 * s, yy), (x + 12 * s, yy)], NAVY, 4 * s)
    c.rr(cx - 95 * s, cy - 20 * s, cx + 80 * s, cy + 160 * s, 36 * s, fill=PEACH, out=NAVY, w=8)
    c.rr(cx - 150 * s, cy + 10 * s, cx - 60 * s, cy + 60 * s, 25 * s, fill=PEACH, out=NAVY, w=8)


def foot(c, cx, cy, s, wr=0.0):
    c.rr(cx - 70 * s, cy - 60 * s, cx + 60 * s, cy + 150 * s, 50 * s, fill=PEACH, out=NAVY, w=8)
    for k in range(5):
        c.ell(cx - 55 * s + k * 28 * s, cy - 70 * s - (4 - k if k > 2 else k) * 4 * s, 17 * s, fill=PEACH, out=NAVY, w=6)
    for j in range(4):
        if wr > j / 4 + 0.1:
            c.line([(cx - 30 * s, cy - 10 * s + j * 30 * s), (cx + 30 * s, cy - 10 * s + j * 30 * s)], NAVY, 4 * s)


def cup(c, cx, cy, s, t=0):
    c.ell(cx + 105 * s, cy + 10 * s, 40 * s, out=NAVY, w=12 * s)
    c.rr(cx - 95 * s, cy - 60 * s, cx + 95 * s, cy + 90 * s, 42 * s, fill=WHITE, out=NAVY, w=10)
    c.rr(cx - 80 * s, cy - 52 * s, cx + 80 * s, cy - 20 * s, 14 * s, fill=(120, 80, 50))
    c.rr(cx - 125 * s, cy + 92 * s, cx + 125 * s, cy + 112 * s, 10 * s, fill=NAVY)
    for k in (-35, 20):
        wavy(c, cx + k * s, cy - 75 * s, s, t + k, (200, 195, 190), n=4)


def toast(c, cx, cy, s):
    c.rr(cx - 90 * s, cy - 90 * s, cx + 90 * s, cy + 80 * s, 50 * s, fill=CRUMB, out=NAVY, w=9)
    c.rr(cx - 62 * s, cy - 62 * s, cx + 62 * s, cy + 52 * s, 36 * s, fill=lerp(CRUMB, WHITE, 0.5))


def strip(c, cx, cy, s, on=True):
    c.line([(cx - 190 * s, cy), (cx - 250 * s, cy + 40 * s), (cx - 300 * s, cy + 10 * s)], NAVY, 8 * s)
    c.rr(cx - 190 * s, cy - 45 * s, cx + 190 * s, cy + 45 * s, 20 * s, fill=(235, 235, 240), out=NAVY, w=9)
    for k in range(4):
        c.rr(cx - 150 * s + k * 70 * s, cy - 20 * s, cx - 105 * s + k * 70 * s, cy + 20 * s, 8 * s, fill=NAVY)
    c.rr(cx + 135 * s, cy - 22 * s, cx + 170 * s, cy + 22 * s, 8 * s, fill=GREEN if on else RED)


def tv(c, cx, cy, s, led=True, on=False):
    c.rr(cx - 170 * s, cy - 120 * s, cx + 170 * s, cy + 90 * s, 18 * s, fill=NAVY)
    c.rr(cx - 155 * s, cy - 105 * s, cx + 155 * s, cy + 70 * s, 10 * s, fill=(SKY if on else (30, 40, 70)))
    c.rr(cx - 60 * s, cy + 90 * s, cx + 60 * s, cy + 115 * s, 6 * s, fill=NAVY)
    if led:
        c.ell(cx + 130 * s, cy + 80 * s, 9 * s, fill=RED)


def charger(c, cx, cy, s, off=0.0):
    c.line([(cx + off * s, cy + 60 * s), (cx + off * s, cy + 110 * s), (cx + off * s + 70 * s, cy + 150 * s)], NAVY, 10 * s)
    for dx in (-20, 20):
        c.rr(cx + off * s + dx * s - 6 * s, cy - 95 * s, cx + off * s + dx * s + 6 * s, cy - 55 * s, 3 * s, fill=STEEL, out=NAVY, w=4)
    c.rr(cx + off * s - 45 * s, cy - 60 * s, cx + off * s + 45 * s, cy + 60 * s, 14 * s, fill=WHITE, out=NAVY, w=8)


def diaphragm(c, cx, cy, s, t):
    c.rr(cx - 100 * s, cy - 170 * s, cx + 100 * s, cy + 170 * s, 60 * s, fill=PEACH, out=NAVY, w=9)
    off = math.sin(t * 8) * 18 * s
    c.arc(cx, cy + 70 * s + off, 90 * s, 200, 340, ORANGE, 14 * s)
    c.arc(cx, cy + 70 * s + off, 74 * s, 200, 340, ORANGE, 8 * s)


def belly(c, cx, cy, s, t):
    c.rr(cx - 100 * s, cy - 170 * s, cx + 100 * s, cy + 170 * s, 60 * s, fill=PEACH, out=NAVY, w=9)
    r = (62 + 16 * math.sin(t * 2.2)) * s
    c.ell(cx, cy + 50 * s, r, fill=lerp(PEACH, ORANGE, 0.45), out=NAVY, w=7)


def sceneF(fn):
    def g(t):
        c = C(); fn(c, t); return c.out()
    return g


def tilesF(tiles):
    def g(t):
        c = C()
        for i, cx in enumerate((130, 380, 630)):
            on = t >= LIGHT[i]
            s = 1.0
            if on:
                u = (t - LIGHT[i]) / 0.35
                s = 1.0 + (0.12 * math.sin(min(1, u) * math.pi) + 0.04)
            hw, hh = 105 * s, 135 * s
            if on:
                c.rr(cx - hw, 380 - hh, cx + hw, 380 + hh, 40, fill=PEACH, out=ORANGE, w=10)
            else:
                c.rr(cx - hw, 380 - hh, cx + hw, 380 + hh, 40, fill=(242, 236, 225))
            tiles[i](c, cx, 380, s)
        return c.out()
    return g
