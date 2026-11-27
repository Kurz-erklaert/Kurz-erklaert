import sys, math, subprocess, os
from PIL import Image, ImageDraw, ImageFont

W, H, FPS = 1080, 1920, 30
NAVY = (232, 238, 248); ORANGE = (255, 170, 50); BG = (8, 10, 16)
PEACH = (40, 48, 70); SKY = (46, 78, 120); WATER = (70, 160, 225)
RED = (214, 64, 52); WHITE = (255, 255, 255); GREY = (44, 52, 72); GREEN = (140, 190, 120)
FD = '/usr/share/fonts/opentype/inter/'
OUT = '/tmp/claude-0/-home-claude/9933ae9d-2912-5ee4-8ee1-1140ae92f947/scratchpad/work'
os.makedirs(OUT, exist_ok=True)


def font(n, s):
    return ImageFont.truetype(FD + n, int(s))


def eob(x):
    x = max(0.0, min(1.0, x)); c1 = 1.70158; c3 = c1 + 1
    return 1 + c3 * (x - 1) ** 3 + c1 * (x - 1) ** 2


def eout(x):
    x = max(0.0, min(1.0, x)); return 1 - (1 - x) ** 2


SS = 2; IL = 760


class C:
    def __init__(s):
        s.im = Image.new('RGBA', (IL * SS, IL * SS), (0, 0, 0, 0)); s.d = ImageDraw.Draw(s.im)

    def ell(s, cx, cy, r, fill=None, out=None, w=0):
        s.d.ellipse([(cx - r) * SS, (cy - r) * SS, (cx + r) * SS, (cy + r) * SS], fill=fill, outline=out, width=max(1, int(w * SS)) if out else 0)

    def rr(s, x0, y0, x1, y1, r, fill=None, out=None, w=0):
        s.d.rounded_rectangle([x0 * SS, y0 * SS, x1 * SS, y1 * SS], radius=r * SS, fill=fill, outline=out, width=max(1, int(w * SS)) if out else 0)

    def line(s, pts, fill, w):
        s.d.line([(x * SS, y * SS) for x, y in pts], fill=fill, width=max(1, int(w * SS)), joint='curve')
        for x, y in (pts[0], pts[-1]):
            s.ell(x, y, w / 2, fill=fill)

    def poly(s, pts, fill):
        s.d.polygon([(x * SS, y * SS) for x, y in pts], fill=fill)

    def arc(s, cx, cy, r, a0, a1, fill, w):
        s.d.arc([(cx - r) * SS, (cy - r) * SS, (cx + r) * SS, (cy + r) * SS], a0, a1, fill=fill, width=max(1, int(w * SS)))

    def text(s, cx, cy, t, size, fill, fn='Inter-ExtraBold.otf'):
        s.d.text((cx * SS, cy * SS), t, font=font(fn, size * SS), fill=fill, anchor='mm')

    def out(s):
        return s.im.resize((IL, IL), Image.LANCZOS)


def clock(c, cx, cy, r, t=0, shake=0):
    sh = math.sin(t * 38) * shake
    c.line([(cx - r * .55, cy + r * .95), (cx - r * .8, cy + r * 1.2)], NAVY, r * .1)
    c.line([(cx + r * .55, cy + r * .95), (cx + r * .8, cy + r * 1.2)], NAVY, r * .1)
    for sg in (-1, 1):
        c.ell(cx + sg * r * .78 + sh * sg, cy - r * .78, r * .3, fill=ORANGE, out=NAVY, w=r * .07)
    c.line([(cx, cy - r * 1.0), (cx, cy - r * 1.2)], NAVY, r * .08)
    c.ell(cx, cy, r, fill=WHITE, out=NAVY, w=r * .1)
    for i in range(12):
        a = i * math.pi / 6
        c.line([(cx + math.sin(a) * r * .74, cy - math.cos(a) * r * .74), (cx + math.sin(a) * r * .84, cy - math.cos(a) * r * .84)], NAVY, r * .04)
    a = math.radians(240)
    c.line([(cx, cy), (cx + math.sin(a) * r * .5, cy - math.cos(a) * r * .5)], NAVY, r * .09)
    c.line([(cx, cy), (cx, cy - r * .68)], NAVY, r * .06)
    c.ell(cx, cy, r * .07, fill=ORANGE)


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

def sh(fn):
    return sceneF(fn)


def hickface(c, t):
    yb = -abs(math.sin(t * 5)) * 28
    face(c, 380, 340 + yb, 1.5, 'o')
    if math.sin(t * 5) > 0.5:
        pill(c, 380, 110, 330, 100, 'HICK!', 70, ORANGE, WHITE)


def gate(c, t):
    p = eout(min(t / 1.0, 1))
    face(c, 380, 280, 1.4, 'o')
    c.rr(240 + 90 * p, 520, 380, 566, 12, fill=ORANGE)
    c.rr(380, 520, 520 - 90 * p, 566, 12, fill=ORANGE)
    if t > 1.3:
        pill(c, 380, 650, 330, 90, 'HICK!', 62, ORANGE, WHITE)


def bubbles(c, t, x0=380):
    for k in range(7):
        ph = (t * 0.4 + k / 7) % 1
        c.ell(x0 - 170 + k * 56 + math.sin(k + t) * 12, 640 - ph * 520, 14 + 10 * (k % 3), out=WATER, w=6)


def glassclear(c, t):
    p = min(t / 2.0, 1)
    glasses(c, 380, 330, 1.4, fog=1 - p)
    sun(c, 600, 120, 46, t)


def facemask(c, t):
    face(c, 380, 330, 1.5)
    mask(c, 380, 330, 1.5)
    for k in range(3):
        ph = (t * 0.7 + k / 3) % 1
        y = 380 + k * 40
        c.line([(470 + ph * 100, y), (500 + ph * 100, y + 10 * (k - 1))], ORANGE, 11)
    badge(c, 2, t)


def warmcold(c, t):
    glasses(c, 400, 400, 1.3, fog=0.15)
    wavy(c, 130, 560, 1.4, t, ORANGE, n=6)
    snow(c, 520, 400, 52, ICE, 9)


def windowwarm(c, t):
    window(c, 440, 370, 1.3, mist=min(t / 1.2, 1))
    wavy(c, 130, 620, 1.5, t, ORANGE, n=7)


def twowin(c, t):
    window(c, 150, 380, 0.68, open_=True)
    window(c, 610, 380, 0.68, open_=True)
    airflow(c, 230, 530, 380, t)
    badge(c, 2, t)


def bananacross(c, t):
    apple(c, 190, 380, 1.1)
    bunch(c, 530, 400, 0.65, 0.0)
    puffs(c, 190, 300, 0.9, t, n=3)
    e = eout(min((t - 0.5) / 0.4, 1))
    if e > 0:
        c.line([(290, 260), (290 + 180 * e, 260 + 240 * e)], RED, 26)
        c.line([(470, 260), (470 - 180 * e, 260 + 240 * e)], RED, 26)
    badge(c, 3 - 1, t)


def spreadbananas(c, t):
    sp = 160 * eout(min(t / 1.2, 1))
    bunch(c, 380, 380, 0.75, 0.0, spread=sp)
    badge(c, 3, t)


exec(open('/tmp/claude-0/-home-claude/9933ae9d-2912-5ee4-8ee1-1140ae92f947/scratchpad/specs2.py').read())

VID = sys.argv[2]
SPEC = SPECS[VID]
SPEC['scenes'] = [(ch, {k.strip('.,:?!') for k in kw}) for ch, kw in SPEC['scenes']]
ILL = SPEC['ill'] + [tilesF(SPEC['tiles'])]
import json
AUD = OUT + f'/voice_{VID}.mp3'
al = json.load(open(OUT + f'/align_{VID}.json'))
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

SCENES = SPEC['scenes']
ti = 0; SC = []
for chunks, kw in SCENES:
    cs = []
    for c in chunks:
        ws = c.split(); seg = toks[ti:ti + len(ws)]
        assert [t[0] for t in seg] == ws, (ws, [t[0] for t in seg])
        ti += len(ws); cs.append(seg)
    SC.append((cs, kw))
assert ti == len(toks)
import subprocess as sp
adur = float(sp.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', AUD], capture_output=True, text=True).stdout)
bounds = [0.0] + [SC[i][0][0][0][1] - 0.15 for i in range(1, 7)]
total = max(adur, toks[-1][2]) + 0.7
fb = [round(b * FPS) for b in bounds] + [round(total * FPS)]
DURS = [(fb[i + 1] - fb[i]) / FPS for i in range(7)]
S0 = [fb[i] / FPS for i in range(7)]
LIGHT = [[t for t in SC[6][0][1] if t[0].startswith(w)][0][1] - S0[6] - 0.05 for w in SPEC['light']]
print('Szenen', [round(d, 2) for d in DURS], 'gesamt', round(total, 2), 'light', [round(x, 2) for x in LIGHT])

CF = font('Inter-ExtraBold.otf', 96)


def layout(seg, s0):
    sp_ = CF.getlength(' '); lines = []; cur = []; cw = 0
    for w, a, b in seg:
        wl = CF.getlength(w)
        if cur and cw + sp_ + wl > 940:
            lines.append(cur); cur = []; cw = 0
        cw += (sp_ if cur else 0) + wl; cur.append((w, wl, a - s0))
    lines.append(cur); out = []; lh = 128; y0 = 1380 - len(lines) * lh / 2
    for li, ln in enumerate(lines):
        tot = sum(x[1] for x in ln) + sp_ * (len(ln) - 1); x = (W - tot) / 2
        for w, wl, tw in ln:
            out.append((w, x, y0 + li * lh, tw)); x += wl + sp_
    return out


LAY = [[layout(seg, S0[i]) for seg in SC[i][0]] for i in range(7)]


def blend(a, b, p):
    return tuple(int(a[i] + (b[i] - a[i]) * p) for i in range(3))


def make_bg():
    im = Image.new('RGB', (W, H), BG); d = ImageDraw.Draw(im)
    f = font('Inter-Bold.otf', 40); tx = 'Kurz erklärt: Alltag'; w = f.getlength(tx)
    d.rounded_rectangle([(W - w) / 2 - 36, 236, (W + w) / 2 + 36, 312], radius=38, fill=PEACH)
    d.text((W / 2, 275), tx, font=f, fill=NAVY, anchor='mm')
    return im


BGIMG = make_bg()


def frame(si, t):
    f = BGIMG.copy()
    ill = ILL[si](t)
    sc = (0.72 + 0.28 * eob(t / 0.5)) * 1.2; a = min(t / 0.25, 1)
    ill2 = ill.resize((int(IL * sc), int(IL * sc)), Image.BILINEAR)
    if a < 1:
        ill2.putalpha(ill2.getchannel('A').point(lambda v: int(v * a)))
    x = (W - ill2.width) // 2; y = 310 + (int(IL * 1.2) - ill2.height) // 2 + int(math.sin(t * 2.2) * 6)
    f.paste(ill2, (x, y), ill2)
    d = ImageDraw.Draw(f); kw = SC[si][1]
    act = None
    for lay in LAY[si]:
        if lay[0][3] <= t + 0.02: act = lay
    if act:
        for w, wx, wy, tw in act:
            p = max(0.0, min(1.0, (t - tw) / 0.14))
            if p <= 0: continue
            col = ORANGE if w.strip('.,:?!') in kw else NAVY
            d.text((wx, wy + (1 - p) * 22), w, font=CF, fill=blend(BG, col, p), anchor='lt')
    return f


def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode:
        print(r.stderr[-1500:]); sys.exit(1)


if sys.argv[1] == 'preview':
    pts = [(0, 2.0), (1, 2.0), (2, 2.0), (3, 2.5), (4, 2.5), (5, 2.5), (6, 3.0)]
    sheet = Image.new('RGB', (360 * 4, 640 * 2), WHITE)
    for i, (si, t) in enumerate(pts):
        sheet.paste(frame(si, t).resize((360, 640), Image.LANCZOS), ((i % 4) * 360, (i // 4) * 640))
    sheet.save(f'{OUT}/sheet_{VID}.png')
else:
    files = []
    for si in range(7):
        final = f'{OUT}/{VID}_{si}.mp4'; tmp = f'{OUT}/{VID}_{si}_tmp.mp4'
        n = fb[si + 1] - fb[si]
        p = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                              '-c:v', 'libx264', '-crf', '18', '-preset', 'veryfast', '-pix_fmt', 'yuv420p', tmp], stdin=subprocess.PIPE)
        for i in range(n):
            p.stdin.write(frame(si, i / FPS).tobytes())
        p.stdin.close()
        if p.wait() == 0: os.rename(tmp, final)
        else: sys.exit('ffmpeg failed')
        files.append(final); print('scene', si, 'done', flush=True)
    with open(f'{OUT}/list_{VID}.txt', 'w') as fh:
        for fl in files: fh.write(f"file '{fl}'\n")
    run(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'concat', '-safe', '0', '-i', f'{OUT}/list_{VID}.txt', '-c', 'copy', f'{OUT}/joined_{VID}.mp4'])
    run(['ffmpeg', '-y', '-loglevel', 'error', '-i', f'{OUT}/joined_{VID}.mp4', '-i', AUD, '-map', '0:v', '-map', '1:a', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '192k',
         SPEC["file"]])
    print('fertig')
