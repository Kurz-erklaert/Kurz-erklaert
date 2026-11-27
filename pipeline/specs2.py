OUTDIR = '/home/claude/kurz-erklaert/videos/'


def sh(fn):
    return sceneF(fn)


# ---------- neue Icons ----------
def lemon(c, cx, cy, s):
    c.ell(cx, cy, 70 * s, fill=(247, 214, 80), out=NAVY, w=8 * s)
    c.ell(cx - 66 * s, cy, 14 * s, fill=(247, 214, 80), out=NAVY, w=6 * s)
    c.ell(cx + 66 * s, cy, 14 * s, fill=(247, 214, 80), out=NAVY, w=6 * s)
    c.arc(cx - 10 * s, cy - 6 * s, 40 * s, 200, 290, WHITE, 8 * s)


def applecut(c, cx, cy, s, brown=0.0):
    c.ell(cx, cy, 75 * s, fill=RED, out=NAVY, w=9 * s)
    c.ell(cx, cy, 60 * s, fill=lerp((252, 244, 214), BRN, brown))
    c.ell(cx - 12 * s, cy + 4 * s, 7 * s, fill=NAVY)
    c.ell(cx + 12 * s, cy + 4 * s, 7 * s, fill=NAVY)


def box(c, cx, cy, s, lid=True):
    c.rr(cx - 140 * s, cy - 40 * s, cx + 140 * s, cy + 90 * s, 22 * s, fill=(235, 245, 252), out=NAVY, w=9 * s)
    if lid:
        c.rr(cx - 150 * s, cy - 78 * s, cx + 150 * s, cy - 38 * s, 14 * s, fill=WATER, out=NAVY, w=9 * s)
    for dx in (-60, 0, 60):
        c.ell(cx + dx * s, cy + 25 * s, 24 * s, fill=(252, 244, 214), out=NAVY, w=5 * s) if not lid else None


def bun(c, cx, cy, s, crumbs=False, warm=0.0):
    col = lerp(CRUMB, (222, 160, 90), 0.5 + 0.4 * warm)
    c.ell(cx, cy, 110 * s, fill=col, out=NAVY, w=9 * s)
    for dx in (-50, 0, 50):
        c.line([(cx + dx * s - 14 * s, cy - 40 * s), (cx + dx * s + 14 * s, cy + 20 * s)], NAVY, 7 * s)
    if crumbs:
        for dx, dy in ((-150, 90), (-110, 130), (140, 100), (100, 140), (0, 150)):
            c.ell(cx + dx * s, cy + dy * s, 7 * s, fill=BRN)


def phone(c, cx, cy, s, level=0.5, hot=False, bolt_=False):
    c.rr(cx - 95 * s, cy - 170 * s, cx + 95 * s, cy + 170 * s, 30 * s, fill=NAVY)
    c.rr(cx - 80 * s, cy - 150 * s, cx + 80 * s, cy + 150 * s, 18 * s, fill=(255, 235, 230) if hot else SKY)
    col = RED if level < 0.25 or hot else GREEN
    c.rr(cx - 50 * s, cy - 20 * s, cx + 50 * s, cy + 50 * s, 10 * s, out=NAVY, w=7 * s)
    c.rr(cx - 42 * s, cy - 12 * s, cx - 42 * s + max(8, 84 * level) * s, cy + 42 * s, 6 * s, fill=col)
    if bolt_:
        bolt(c, cx, cy - 90 * s, 0.9 * s)


def mirror(c, cx, cy, s, mist=0.0):
    c.rr(cx - 130 * s, cy - 170 * s, cx + 130 * s, cy + 170 * s, 60 * s, fill=lerp(SKY, MIST, mist), out=NAVY, w=12 * s)
    if mist < 0.5:
        c.line([(cx - 70 * s, cy - 100 * s), (cx - 20 * s, cy - 130 * s)], WHITE, 12 * s)
        c.line([(cx - 90 * s, cy - 60 * s), (cx - 50 * s, cy - 85 * s)], WHITE, 8 * s)
    else:
        for dx, dy in ((-60, -80), (30, -110), (70, -20), (-70, 40), (20, 90), (80, 110)):
            drop(c, cx + dx * s, cy + dy * s, 0.8 * s)


def kettle(c, cx, cy, s, t=0, chalk=0.0, steam=False):
    c.line([(cx + 105 * s, cy - 30 * s), (cx + 170 * s, cy - 50 * s), (cx + 150 * s, cy + 60 * s)], NAVY, 14 * s)
    c.line([(cx - 105 * s, cy - 40 * s), (cx - 150 * s, cy - 70 * s)], NAVY, 14 * s)
    c.rr(cx - 110 * s, cy - 110 * s, cx + 110 * s, cy + 100 * s, 40 * s, fill=WHITE, out=NAVY, w=10 * s)
    if chalk > 0:
        for k in range(5):
            c.ell(cx - 70 * s + k * 35 * s, cy + 80 * s, (10 + 14 * chalk) * s, fill=(225, 222, 214), out=NAVY, w=3 * s)
    c.rr(cx - 125 * s, cy + 100 * s, cx + 125 * s, cy + 125 * s, 10 * s, fill=NAVY)
    if steam:
        for k in (-40, 30):
            wavy(c, cx + k * s, cy - 125 * s, s, t + k, (200, 195, 190), n=4)


def gauge(c, cx, cy, s, t=0):
    c.ell(cx, cy, 110 * s, fill=WHITE, out=NAVY, w=10 * s)
    c.arc(cx, cy, 80 * s, 150, 390, GREEN, 14 * s)
    a = math.radians(200 + 60 * math.sin(t * 1.5) * 0.3 + 40)
    c.line([(cx, cy), (cx + 76 * s * math.cos(a), cy + 76 * s * math.sin(a))], RED, 9 * s)
    c.ell(cx, cy, 11 * s, fill=NAVY)


def showerhead(c, cx, cy, s, t=0):
    c.rr(cx - 120 * s, cy - 20 * s, cx + 120 * s, cy + 30 * s, 24 * s, fill=STEEL, out=NAVY, w=8 * s)
    c.line([(cx - 120 * s, cy - 10 * s), (cx - 190 * s, cy - 110 * s)], NAVY, 14 * s)
    for k in range(6):
        ph = (t * 0.7 + k / 6) % 1
        c.ell(cx - 90 * s + k * 36 * s, cy + 50 * s + ph * 260 * s, 9 * s, fill=WATER)


SPECS = {
 'apfel': {
  'file': OUTDIR + 's2_01_apfel.mp4', 'light': ('Zitrone', 'Dose', 'spät'), 'variant': 'A',
  'scenes': [
   (['Dieser Fehler macht', 'deinen Apfel braun.'], {'Fehler'}),
   (['Schneidest du einen Apfel auf,', 'kommt Luft an das Fruchtfleisch.'], {'Luft'}),
   (['Ein Stoff im Apfel reagiert mit Sauerstoff,', 'und die Schnittfläche wird braun.', 'Drei Tricks helfen.'], {'Sauerstoff', 'braun'}),
   (['Erstens: Träufle etwas Zitronensaft', 'auf die Schnittfläche.'], {'Zitronensaft'}),
   (['Zweitens: Pack die Stücke', 'luftdicht in eine Dose.'], {'luftdicht', 'Dose'}),
   (['Drittens: Schneide den Apfel', 'erst kurz vor dem Essen auf.'], {'kurz'}),
   (['Merk dir:', 'Zitrone, Dose, spät schneiden.'], {'Zitrone', 'Dose', 'spät'}),
  ],
  'ill': [
   sh(lambda c, t: (applecut(c, 380, 390, 2.0, min(t / 3.0, 1) * 0.9), pill(c, 380, 90, 420, 90, 'Fehler?', 56, RED, WHITE))),
   sh(lambda c, t: (applecut(c, 380, 420, 1.9), puffs(c, 380, 290, 1.0, t, n=5), pill(c, 380, 90, 300, 84, 'Luft', 52, NAVY, ORANGE))),
   sh(lambda c, t: (applecut(c, 380, 400, 2.0, min(t / 2.5, 1)), pill(c, 380, 90, 400, 84, 'Sauerstoff', 50, NAVY, ORANGE))),
   sh(lambda c, t: (applecut(c, 380, 470, 1.6), lemon(c, 380, 190, 1.1), [drop(c, 380 + (k - 1) * 40, 270 + ((t * 0.7 + k * 0.3) % 1) * 140, 0.6) for k in range(3)], badge(c, 1, t))),
   sh(lambda c, t: (box(c, 380, 400, 1.7, lid=t > 1.0), badge(c, 2, t))),
   sh(lambda c, t: (apple(c, 380, 390, 2.0), pill(c, 380, 640, 430, 90, 'kurz vorher', 54, NAVY, ORANGE), badge(c, 3, t))),
  ],
  'tiles': [lambda c, x, y, s: lemon(c, x, y, 0.8 * s), lambda c, x, y, s: box(c, x, y, 0.5 * s), lambda c, x, y, s: applecut(c, x, y, 0.8 * s)],
 },
 'heizung': {
  'file': OUTDIR + 's2_02_heizung.mp4', 'light': ('Tuch', 'öffnen', 'Druck'), 'variant': 'B',
  'scenes': [
   (['So wird deine kalte Heizung', 'wieder richtig warm.'], {'warm.'}),
   (['Meistens ist Luft', 'im Heizkörper.'], {'Luft'}),
   (['Sie steigt nach oben und verdrängt das heiße Wasser,', 'deshalb bleibt der Heizkörper oben kalt.', 'Drei Schritte helfen.'], {'Luft', 'kalt.'}),
   (['Erstens: Halte ein Tuch', 'unter das Entlüftungsventil.'], {'Tuch'}),
   (['Zweitens: Öffne es mit dem Schlüssel,', 'bis Wasser statt Luft kommt.'], {'Wasser'}),
   (['Drittens: Schließ es wieder', 'und prüfe den Druck der Anlage.'], {'Druck'}),
   (['Merk dir:', 'Tuch, öffnen, Druck prüfen.'], {'Tuch', 'öffnen', 'Druck'}),
  ],
  'ill': [
   sh(lambda c, t: (radiator(c, 380, 400, 1.7, t), sparkle(c, 640, 230 + math.sin(t * 4) * 8, 34), sparkle(c, 130, 260, 26))),
   sh(lambda c, t: (radiator(c, 380, 420, 1.7, t * 0.0), [c.ell(260 + k * 60 + math.sin(t * 2 + k) * 10, 520 - ((t * 0.4 + k / 5) % 1) * 190, 14 + 4 * (k % 2), out=WATER, w=5) for k in range(5)])),
   sh(lambda c, t: (radiator(c, 380, 400, 1.7, 0.0), snow(c, 380, 190, 70, ICE, 9), wavy(c, 380, 640, 1.6, t, ORANGE, n=6))),
   sh(lambda c, t: (c.rr(150, 300, 610, 470, 30, fill=SKY, out=NAVY, w=9), c.rr(330, 190, 430, 300, 18, fill=STEEL, out=NAVY, w=8), badge(c, 1, t))),
   sh(lambda c, t: (c.rr(280, 120, 480, 320, 34, fill=STEEL, out=NAVY, w=10), c.ell(380, 220, 40, fill=NAVY), c.arc(380, 220, 120, 20 + t * 60, 200 + t * 60, ORANGE, 16), [drop(c, 380, 360 + ((t * 0.6 + k * 0.5) % 1) * 280, 1.3) for k in range(2)], badge(c, 2, t))),
   sh(lambda c, t: (gauge(c, 380, 350, 1.7, t), badge(c, 3, t))),
  ],
  'tiles': [lambda c, x, y, s: c.rr(x - 75 * s, y - 40 * s, x + 75 * s, y + 40 * s, 14 * s, fill=SKY, out=NAVY, w=6), lambda c, x, y, s: (c.rr(x - 30 * s, y - 60 * s, x + 30 * s, y + 10 * s, 10 * s, fill=STEEL, out=NAVY, w=6), drop(c, x, y + 60 * s, 0.9 * s)), lambda c, x, y, s: gauge(c, x, y, 0.5 * s)],
 },
 'broetchen': {
  'file': OUTDIR + 's2_03_broetchen.mp4', 'light': ('Wasser', 'Hitze', 'sofort'), 'variant': 'A',
  'scenes': [
   (['Wirf trockene Brötchen', 'nie weg!'], {'nie'}),
   (['Brötchen von gestern', 'sind hart und zäh.'], {'hart'}),
   (['Die Stärke im Brötchen verfestigt sich,', 'und es wird trocken.', 'Mit drei Schritten wird es wieder knusprig.'], {'Stärke', 'trocken.'}),
   (['Erstens: Halte das Brötchen', 'kurz unter den Wasserhahn.'], {'Wasserhahn.'}),
   (['Zweitens: Backe es bei etwa 180 Grad', 'ungefähr zehn Minuten.'], {'180', 'zehn'}),
   (['Drittens: Iss es sofort,', 'solange es warm ist.'], {'sofort,'}),
   (['Merk dir:', 'Wasser, Hitze, sofort essen.'], {'Wasser', 'Hitze', 'sofort'}),
  ],
  'ill': [
   sh(lambda c, t: (bun(c, 380, 400, 1.7), c.line([(200, 220), (560, 580)], RED, 26) if t > 0.8 else None, c.line([(560, 220), (200, 580)], RED, 26) if t > 0.8 else None)),
   sh(lambda c, t: bun(c, 380, 400, 1.7, crumbs=True)),
   sh(lambda c, t: (bun(c, 380, 400, 1.7, crumbs=True), pill(c, 380, 640, 360, 84, 'Stärke', 52, NAVY, ORANGE))),
   sh(lambda c, t: (bun(c, 380, 500, 1.2), [drop(c, 380 + (k - 1) * 50, 140 + ((t * 0.7 + k * 0.3) % 1) * 200, 0.9) for k in range(3)], c.rr(330, 60, 430, 110, 14, fill=STEEL, out=NAVY, w=8), badge(c, 1, t))),
   sh(lambda c, t: (c.rr(110, 150, 650, 560, 36, fill=(236, 236, 242), out=NAVY, w=10), bun(c, 380, 400, 0.9, warm=min(t / 2.0, 1)), pill(c, 380, 640, 360, 84, '180 °C', 54, NAVY, ORANGE), badge(c, 2, t))),
   sh(lambda c, t: (bun(c, 380, 430, 1.6, warm=1.0), wavy(c, 330, 240, 1.4, t, (200, 195, 190), n=4), sparkle(c, 590, 230 + math.sin(t * 4) * 8, 34), badge(c, 3, t))),
  ],
  'tiles': [lambda c, x, y, s: drop(c, x, y + 10 * s, 1.8 * s), lambda c, x, y, s: pill(c, x, y, 150 * s, 76 * s, '180°', 50 * s, NAVY, ORANGE), lambda c, x, y, s: bun(c, x, y, 0.55 * s, warm=1.0)],
 },
 'handy': {
  'file': OUTDIR + 's2_04_handy.mp4', 'light': ('Kühl', 'Mitte', 'Strom'), 'variant': 'B',
  'scenes': [
   (['So hält dein Handy-Akku', 'deutlich länger.'], {'länger.'}),
   (['Ein Handy-Akku altert schneller,', 'wenn er heiß wird.'], {'heiß'}),
   (['Auch ständig volle oder ganz leere Ladung', 'belastet ihn.', 'Drei Gewohnheiten helfen.'], {'volle', 'leere'}),
   (['Erstens: Lass dein Handy', 'nicht in der Sonne liegen.'], {'Sonne'}),
   (['Zweitens: Lade es möglichst', 'zwischen zwanzig und achtzig Prozent.'], {'zwanzig', 'achtzig'}),
   (['Drittens: Schalte bei Bedarf', 'den Energiesparmodus ein.'], {'Energiesparmodus'}),
   (['Merk dir:', 'Kühl halten, Mitte laden, Strom sparen.'], {'Kühl', 'Mitte', 'Strom'}),
  ],
  'ill': [
   sh(lambda c, t: (phone(c, 380, 390, 1.5, 0.35 + 0.6 * min(t / 3.0, 1)), sparkle(c, 590, 200 + math.sin(t * 4) * 8, 34), sparkle(c, 160, 300, 26))),
   sh(lambda c, t: (phone(c, 380, 420, 1.4, 0.4, hot=True), sun(c, 590, 160, 50, t), wavy(c, 330, 250, 1.2, t, RED, n=4))),
   sh(lambda c, t: (phone(c, 380, 400, 1.5, 0.05 + 0.9 * abs(math.sin(t * 1.2)), bolt_=True))),
   sh(lambda c, t: (phone(c, 380, 430, 1.3, 0.5), sun(c, 590, 150, 50, t), c.line([(520, 80), (660, 220)], RED, 22), c.line([(660, 80), (520, 220)], RED, 22), badge(c, 1, t))),
   sh(lambda c, t: (phone(c, 380, 360, 1.4, 0.55), pill(c, 380, 650, 460, 84, '20 – 80 %', 54, NAVY, ORANGE), badge(c, 2, t))),
   sh(lambda c, t: (phone(c, 380, 370, 1.4, 0.7), c.ell(380, 440, 36, fill=GREEN), pill(c, 380, 650, 460, 84, 'Sparmodus', 50, NAVY, ORANGE), badge(c, 3, t))),
  ],
  'tiles': [lambda c, x, y, s: (sun(c, x, y, 40 * s, 0), c.line([(x - 50 * s, y - 50 * s), (x + 50 * s, y + 50 * s)], RED, 12 * s)), lambda c, x, y, s: pill(c, x, y, 160 * s, 76 * s, '50 %', 50 * s, NAVY, ORANGE), lambda c, x, y, s: phone(c, x, y, 0.4 * s, 0.7)],
 },
 'spiegel': {
  'file': OUTDIR + 's2_05_spiegel.mp4', 'light': ('Lüften', 'Spülmittel', 'kühler'), 'variant': 'A',
  'scenes': [
   (['Dieser Fehler lässt deinen', 'Badspiegel beschlagen.'], {'Fehler'}),
   (['Beim Duschen entsteht', 'warmer Wasserdampf.'], {'Wasserdampf.'}),
   (['Er trifft auf die kältere Spiegelfläche', 'und wird zu winzigen Tröpfchen.', 'Drei Dinge helfen.'], {'kältere', 'Tröpfchen.'}),
   (['Erstens: Lüfte nach dem Duschen', 'fünf Minuten lang.'], {'Lüfte', 'fünf'}),
   (['Zweitens: Reibe den Spiegel', 'mit einem Hauch Spülmittel ein.'], {'Spülmittel'}),
   (['Drittens: Dusche etwas kühler,', 'dann entsteht weniger Dampf.'], {'kühler,'}),
   (['Merk dir:', 'Lüften, Spülmittel, kühler duschen.'], {'Lüften', 'Spülmittel', 'kühler'}),
  ],
  'ill': [
   sh(lambda c, t: (mirror(c, 380, 390, 1.6, min(t / 2.0, 1)), pill(c, 380, 90, 380, 90, 'Fehler?', 56, RED, WHITE))),
   sh(lambda c, t: (showerhead(c, 380, 200, 1.3, t), wavy(c, 330, 640, 1.5, t, (200, 195, 190), n=5))),
   sh(lambda c, t: (mirror(c, 380, 390, 1.6, min(t / 1.5, 1)), wavy(c, 130, 620, 1.5, t, ORANGE, n=6))),
   sh(lambda c, t: (window(c, 380, 380, 1.3, open_=True), airflow(c, 200, 560, 380, t), badge(c, 1, t))),
   sh(lambda c, t: (mirror(c, 380, 390, 1.6, max(0.0, 1 - t / 1.2)), sparkle(c, 580, 250, 34), sparkle(c, 200, 520, 26), badge(c, 2, t))),
   sh(lambda c, t: (showerhead(c, 380, 200, 1.3, t), snow(c, 600, 120, 50, ICE, 9), badge(c, 3, t))),
  ],
  'tiles': [lambda c, x, y, s: window(c, x, y, 0.3 * s, open_=True), lambda c, x, y, s: mirror(c, x, y, 0.38 * s, 0.0), lambda c, x, y, s: (snow(c, x, y, 55 * s, ICE, 9 * s))],
 },
 'kocher': {
  'file': OUTDIR + 's2_06_kocher.mp4', 'light': ('Säure', 'aufkochen', 'gut'), 'variant': 'B',
  'scenes': [
   (['So wird dein Wasserkocher', 'in zehn Minuten kalkfrei.'], {'kalkfrei.'}),
   (['Der weiße Belag im Wasserkocher', 'ist Kalk aus dem Wasser.'], {'Kalk'}),
   (['Beim Erhitzen bleibt er zurück', 'und setzt sich fest.', 'Drei Schritte lösen ihn.'], {'Erhitzen', 'fest.'}),
   (['Erstens: Gib Wasser mit etwas', 'Zitronensäure oder Essig hinein.'], {'Zitronensäure', 'Essig'}),
   (['Zweitens: Koche es einmal auf', 'und lass es kurz wirken.'], {'Koche', 'wirken.'}),
   (['Drittens: Gieß alles weg', 'und spüle gründlich nach.'], {'spüle'}),
   (['Merk dir:', 'Säure, aufkochen, gut ausspülen.'], {'Säure', 'aufkochen', 'gut'}),
  ],
  'ill': [
   sh(lambda c, t: (kettle(c, 380, 400, 1.6, t, chalk=max(0.0, 1 - t / 3.0)), sparkle(c, 600, 200 + math.sin(t * 4) * 8, 34), sparkle(c, 150, 260, 26))),
   sh(lambda c, t: (kettle(c, 380, 400, 1.6, t, chalk=1.0), pill(c, 380, 90, 300, 84, 'Kalk', 52, NAVY, ORANGE))),
   sh(lambda c, t: (kettle(c, 380, 400, 1.6, t, chalk=min(t / 2.0, 1), steam=True), wavy(c, 130, 640, 1.4, t, ORANGE, n=6))),
   sh(lambda c, t: (kettle(c, 380, 470, 1.3, t, chalk=1.0), lemon(c, 380, 170, 1.0), [drop(c, 380 + (k - 1) * 30, 230 + ((t * 0.7 + k * 0.3) % 1) * 130, 0.6) for k in range(3)], badge(c, 1, t))),
   sh(lambda c, t: (kettle(c, 380, 420, 1.6, t, chalk=0.6, steam=True), [c.ell(300 + k * 80, 500 - ((t * 0.8 + k / 3) % 1) * 90, 12, out=WATER, w=4) for k in range(3)], badge(c, 2, t))),
   sh(lambda c, t: (kettle(c, 380, 400, 1.5, t, chalk=0.0), [drop(c, 640 + (k - 1) * 10, 360 + ((t * 0.7 + k * 0.4) % 1) * 280, 0.8) for k in range(2)], sparkle(c, 220, 250, 34), badge(c, 3, t))),
  ],
  'tiles': [lambda c, x, y, s: lemon(c, x, y, 0.8 * s), lambda c, x, y, s: kettle(c, x, y, 0.38 * s, 0, steam=True), lambda c, x, y, s: (kettle(c, x, y, 0.38 * s, 0), sparkle(c, x + 60 * s, y - 60 * s, 18 * s))],
 },
}
