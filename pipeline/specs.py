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


SPECS = {
 'wasch': {
  'file': 'folge5_waschmaschine.mp4', 'light': ('Offen', 'heiß', 'sauber'),
  'scenes': [
   (['Deine Waschmaschine', 'riecht muffig?'], {'muffig'}),
   (['Das liegt an Feuchtigkeit', 'und Waschmittelresten,'], {'Feuchtigkeit'}),
   (['in denen sich Bakterien und Schimmel wohlfühlen.', 'Drei Dinge helfen.'], {'Schimmel'}),
   (['Erstens: Lass nach dem Waschen', 'Tür und Waschmittelfach offen,', 'damit alles trocknet.'], {'offen'}),
   (['Zweitens: Wasche etwa einmal im Monat', 'leer bei 60 Grad oder mehr.'], {'60', 'Grad'}),
   (['Drittens: Reinige Gummidichtung', 'und Flusensieb regelmäßig.'], {'Gummidichtung', 'Flusensieb'}),
   (['Merk dir:', 'Offen lassen, heiß waschen, sauber machen.'], {'Offen', 'heiß', 'sauber'}),
  ],
  'ill': [
   sh(lambda c, t: washer(c, 380, 390, 1.3, t, stink=True)),
   sh(lambda c, t: (washer(c, 380, 390, 1.2, t), [drop(c, 250 + k * 130, 280 + ((t * 0.5 + k * 0.3) % 1) * 300, 1.0) for k in range(3)])),
   sh(lambda c, t: (washer(c, 380, 390, 1.3, t, stink=True), [c.ell(380 + 100 * 1.3 * math.cos(a), 430 + 100 * 1.3 * math.sin(a), 13, fill=DARKG) for a in (0.4, 1.7, 2.9, 4.3, 5.4)])),
   sh(lambda c, t: (washer(c, 380, 390, 1.3, t, door=True, drawer=True), badge(c, 1, t))),
   sh(lambda c, t: (washer(c, 380, 340, 1.1, t), pill(c, 380, 640, 300, 92, '60 °C', 60, NAVY, ORANGE), badge(c, 2, t))),
   sh(lambda c, t: (washer(c, 380, 390, 1.3, t, glow=True), sparkle(c, 560, 220 + math.sin(t * 4) * 10, 36), sparkle(c, 200, 520, 28), badge(c, 3, t))),
  ],
  'tiles': [lambda c, x, y, s: washer(c, x, y, 0.3 * s, door=True), lambda c, x, y, s: pill(c, x, y, 150 * s, 76 * s, '60°', 50 * s, NAVY, ORANGE), lambda c, x, y, s: washer(c, x, y, 0.3 * s, glow=True)],
 },
 'hick': {
  'file': 'folge6_schluckauf.mp4', 'light': ('Trinken', 'Luft', 'ruhig'),
  'scenes': [
   (['Schluckauf und er', 'geht nicht weg?'], {'Schluckauf'}),
   (['Dabei zieht sich dein Zwerchfell', 'ruckartig zusammen,'], {'Zwerchfell'}),
   (['und die Stimmritze schließt sich.', 'Daher das Hick.', 'Drei Dinge kannst du probieren.'], {'Hick'}),
   (['Erstens: Trink langsam', 'kleine Schlucke Wasser.'], {'Wasser'}),
   (['Zweitens: Halte etwa zehn Sekunden', 'die Luft an.'], {'zehn', 'Luft'}),
   (['Drittens: Atme ruhig und tief,', 'in den Bauch.'], {'Bauch'}),
   (['Merk dir:', 'Trinken, Luft anhalten, ruhig atmen.'], {'Trinken', 'Luft', 'ruhig'}),
  ],
  'ill': [
   sh(hickface),
   sh(lambda c, t: (diaphragm(c, 380, 400, 1.45, t), pill(c, 380, 90, 380, 84, 'Zwerchfell', 50, NAVY, ORANGE))),
   sh(gate),
   sh(lambda c, t: (glass(c, 380, 390, 1.5, min(0.3 + t * 0.1, 0.6)), badge(c, 1, t))),
   sh(lambda c, t: (face(c, 380, 330, 1.5, 'flat', cheeks=True), pill(c, 380, 640, 260, 90, '10 s', 60, NAVY, ORANGE), badge(c, 2, t))),
   sh(lambda c, t: (belly(c, 380, 390, 1.5, t), badge(c, 3, t))),
  ],
  'tiles': [lambda c, x, y, s: glass(c, x, y, 0.34 * s, 0.6), lambda c, x, y, s: face(c, x, y, 0.5 * s, 'flat', cheeks=True), lambda c, x, y, s: belly(c, x, y, 0.36 * s, 0)],
 },
 'brille': {
  'file': 'folge7_brille.mp4', 'light': ('Spülmittel', 'Nase', 'warm'),
  'scenes': [
   (['Deine Brille beschlägt,', 'sobald du reinkommst?'], {'beschlägt'}),
   (['Warme, feuchte Luft trifft', 'auf kaltes Glas'], {'Warme', 'kaltes'}),
   (['und wird dort zu winzigen Tröpfchen.', 'Drei Dinge helfen.'], {'Tröpfchen'}),
   (['Erstens: Putz die Gläser mit etwas Spülmittel', 'und lass einen dünnen Film trocknen.'], {'Spülmittel'}),
   (['Zweitens: Zieh Maske oder Schal', 'fest über die Nase,', 'damit deine Atemluft nicht nach oben strömt.'], {'Nase'}),
   (['Drittens: Nimm die Brille im warmen Raum kurz ab', 'und lass sie warm werden.'], {'warm', 'warmen'}),
   (['Merk dir:', 'Spülmittel, Nase abdecken, warm werden lassen.'], {'Spülmittel', 'Nase', 'warm'}),
  ],
  'ill': [
   sh(lambda c, t: glasses(c, 380, 360, 1.6, fog=min(t / 1.5, 1))),
   sh(warmcold),
   sh(lambda c, t: glasses(c, 380, 380, 1.6, fog=1)),
   sh(lambda c, t: (glasses(c, 380, 380, 1.5, fog=0), bubbles(c, t), sparkle(c, 600, 240, 34), badge(c, 1, t))),
   sh(facemask),
   sh(lambda c, t: (glassclear(c, t), badge(c, 3, t))),
  ],
  'tiles': [lambda c, x, y, s: [c.ell(x - 40 * s + k * 40 * s, y - 20 * s + (k % 2) * 40 * s, (26 - k * 4) * s, out=WATER, w=6 * s) for k in range(3)], lambda c, x, y, s: (face(c, x, y - 10 * s, 0.5 * s), mask(c, x, y - 10 * s, 0.5 * s)), lambda c, x, y, s: (glasses(c, x, y + 10 * s, 0.34 * s, 0), sun(c, x + 50 * s, y - 70 * s, 18 * s))],
 },
 'fenster': {
  'file': 'folge8_fenster.mp4', 'light': ('Stoßlüften', 'Durchzug', 'nicht'),
  'scenes': [
   (['Deine Fenster sind', 'morgens nass?'], {'nass'}),
   (['Warme Raumluft enthält viel Feuchtigkeit', 'und schlägt sich an der kalten Scheibe nieder.'], {'Feuchtigkeit', 'Scheibe'}),
   (['Bleibt die Feuchtigkeit im Raum,', 'kann Schimmel entstehen.', 'Drei Dinge helfen.'], {'Schimmel'}),
   (['Erstens: Lüfte mehrmals am Tag', 'fünf bis zehn Minuten', 'mit weit offenem Fenster.'], {'weit', 'offenem'}),
   (['Zweitens: Öffne gegenüberliegende Fenster', 'für Durchzug.'], {'Durchzug'}),
   (['Drittens: Heize alle Räume wenigstens etwas,', 'damit die Wände nicht auskühlen.'], {'Heize', 'auskühlen'}),
   (['Merk dir:', 'Stoßlüften, Durchzug, nicht auskühlen.'], {'Stoßlüften', 'Durchzug', 'auskühlen'}),
  ],
  'ill': [
   sh(lambda c, t: window(c, 380, 370, 1.35, mist=min(t / 1.5, 1))),
   sh(windowwarm),
   sh(lambda c, t: window(c, 440, 370, 1.3, mist=0.9, mold=True)),
   sh(lambda c, t: (window(c, 380, 360, 1.3, open_=True), airflow(c, 140, 620, 360, t), pill(c, 380, 660, 470, 80, '5 bis 10 Min', 46, NAVY, ORANGE), badge(c, 1, t))),
   sh(twowin),
   sh(lambda c, t: (radiator(c, 380, 420, 1.5, t), badge(c, 3, t))),
  ],
  'tiles': [lambda c, x, y, s: window(c, x, y, 0.3 * s, open_=True), lambda c, x, y, s: [c.line([(x - 55 * s, y + (k - 1) * 34 * s), (x + 40 * s, y + (k - 1) * 34 * s)], ORANGE, 9 * s) for k in range(3)], lambda c, x, y, s: radiator(c, x, y + 10 * s, 0.3 * s)],
 },
 'banane': {
  'file': 'folge9_bananen.mp4', 'light': ('Stiele', 'Abstand', 'einzeln'),
  'scenes': [
   (['Deine Bananen werden', 'viel zu schnell braun?'], {'braun'}),
   (['Reife Bananen geben ein Gas', 'namens Ethylen ab,'], {'Ethylen'}),
   (['und das lässt Obst schneller reifen.', 'Drei Dinge helfen.'], {'reifen'}),
   (['Erstens: Wickle die Stiele in Folie.'], {'Stiele', 'Folie'}),
   (['Zweitens: Leg Bananen nicht neben Äpfel,', 'denn auch die geben viel Ethylen ab.'], {'Äpfel'}),
   (['Drittens: Trenne die Bananen voneinander,', 'wenn du sie gekauft hast.'], {'Trenne'}),
   (['Merk dir:', 'Stiele einpacken, Abstand zu Äpfeln, einzeln lagern.'], {'Stiele', 'Abstand', 'einzeln'}),
  ],
  'ill': [
   sh(lambda c, t: bunch(c, 380, 390, 1.15, p=min(t / 2.0, 1))),
   sh(lambda c, t: (bunch(c, 330, 440, 0.95, 0.2), puffs(c, 560, 260, 1.0, t))),
   sh(lambda c, t: (bunch(c, 330, 440, 0.95, min(t / 2.5, 1) * 0.9), puffs(c, 560, 260, 1.0, t))),
   sh(lambda c, t: (bunch(c, 330, 400, 1.15, 0.0, foil=True), sparkle(c, 600, 160, 34), badge(c, 1, t))),
   sh(bananacross),
   sh(spreadbananas),
  ],
  'tiles': [lambda c, x, y, s: bunch(c, x - 20 * s, y + 10 * s, 0.27 * s, 0.0, foil=True), lambda c, x, y, s: (apple(c, x, y, 0.55 * s), c.line([(x - 60 * s, y - 60 * s), (x + 60 * s, y + 60 * s)], RED, 12 * s), c.line([(x + 60 * s, y - 60 * s), (x - 60 * s, y + 60 * s)], RED, 12 * s)), lambda c, x, y, s: bunch(c, x, y, 0.27 * s, 0.0, spread=50 * s)],
 },
 'finger': {
  'file': 'folge10_finger.mp4', 'light': ('Nerven', 'Minuten', 'vielleicht'),
  'scenes': [
   (['Warum werden deine Finger', 'im Wasser schrumpelig?'], {'schrumpelig'}),
   (['Die Haut quillt nicht einfach auf.', 'Dein Nervensystem zieht die Blutgefäße', 'in den Fingern zusammen,'], {'Nervensystem'}),
   (['und dadurch wirft die Haut Falten.', 'Drei Dinge sind spannend.'], {'Falten'}),
   (['Erstens: Es passiert erst', 'nach einigen Minuten im Wasser.'], {'Minuten'}),
   (['Zweitens: Es betrifft nur', 'Hände und Füße.'], {'Hände', 'Füße'}),
   (['Drittens: Vielleicht helfen die Rillen', 'beim Greifen auf nassem Untergrund,', 'ganz sicher weiß man das aber nicht.'], {'Vielleicht', 'Greifen'}),
   (['Merk dir:', 'Nerven, Minuten, vielleicht mehr Halt.'], {'Nerven', 'Minuten', 'vielleicht'}),
  ],
  'ill': [
   sh(lambda c, t: (hand(c, 380, 420, 1.5, wr=eout(min(t / 2.0, 1))), [drop(c, 250 + k * 130, 120 + ((t * 0.5 + k * 0.3) % 1) * 120, 1.0) for k in range(3)])),
   sh(lambda c, t: (hand(c, 290, 430, 1.2), bolt(c, 590, 300, 1.7 if int(t * 4) % 2 else 1.5))),
   sh(lambda c, t: (hand(c, 380, 420, 1.5, wr=1.0), [c.line([(380 + sg * (200 - 20 * math.sin(t * 5)), 360), (380 + sg * (150 - 20 * math.sin(t * 5)), 360)], ORANGE, 14) for sg in (-1, 1)])),
   sh(lambda c, t: (clock(c, 380, 350, 190, t), pill(c, 380, 650, 360, 84, 'nach Minuten', 46, NAVY, ORANGE), badge(c, 1, t))),
   sh(lambda c, t: (hand(c, 240, 420, 1.0, wr=1.0), foot(c, 540, 400, 1.0, wr=1.0), badge(c, 2, t))),
   sh(lambda c, t: (hand(c, 380, 420, 1.4, wr=1.0), c.text(590, 190, '?', 170, ORANGE), badge(c, 3, t))),
  ],
  'tiles': [lambda c, x, y, s: bolt(c, x, y, 0.9 * s), lambda c, x, y, s: clock(c, x, y + 10 * s, 55 * s, 0), lambda c, x, y, s: c.text(x, y, '?', 140 * s, ORANGE)],
 },
 'kaffee': {
  'file': 'folge11_kaffee.mp4', 'light': ('Licht', 'Wasser', 'Kaffee'),
  'scenes': [
   (['Du trinkst Kaffee und', 'wirst trotzdem nicht wach?'], {'wach'}),
   (['Koffein braucht eine Weile,', 'bis es richtig wirkt,'], {'Koffein'}),
   (['oft eine halbe Stunde oder länger.', 'Drei Dinge helfen.'], {'Stunde'}),
   (['Erstens: Geh früh ans Tageslicht.'], {'Tageslicht'}),
   (['Zweitens: Trink vorher', 'ein Glas Wasser.'], {'Wasser'}),
   (['Drittens: Wenn dein Magen empfindlich ist,', 'trink den Kaffee zum Frühstück.'], {'Frühstück'}),
   (['Merk dir:', 'Licht, Wasser, Kaffee zum Frühstück.'], {'Licht', 'Wasser', 'Kaffee'}),
  ],
  'ill': [
   sh(lambda c, t: (cup(c, 380, 400, 1.5, t), [c.text(560 + k * 40, 190 - k * 50 + math.sin(t * 3 + k) * 6, 'z', 50 + k * 18, ORANGE) for k in range(3)])),
   sh(lambda c, t: (cup(c, 300, 430, 1.2, t), clock(c, 580, 250, 100, t))),
   sh(lambda c, t: (clock(c, 380, 330, 200, t), pill(c, 380, 650, 300, 90, '30 Min', 58, NAVY, ORANGE))),
   sh(lambda c, t: (sun(c, 380, 350, 130, t), badge(c, 1, t))),
   sh(lambda c, t: (glass(c, 380, 390, 1.5, min(0.15 + t * 0.3, 0.8)), badge(c, 2, t))),
   sh(lambda c, t: (cup(c, 230, 420, 1.0, t), toast(c, 520, 410, 1.0), badge(c, 3, t))),
  ],
  'tiles': [lambda c, x, y, s: sun(c, x, y, 36 * s, 0), lambda c, x, y, s: glass(c, x, y, 0.34 * s, 0.6), lambda c, x, y, s: cup(c, x, y, 0.4 * s)],
 },
 'standby': {
  'file': 'folge12_standby.mp4', 'light': ('Leiste', 'Ladegerät', 'ganz'),
  'scenes': [
   (['Dein Fernseher ist aus', 'und verbraucht trotzdem Strom?'], {'Strom'}),
   (['Im Standby bleiben Geräte bereit', 'und ziehen rund um die Uhr', 'ein wenig Strom.'], {'Standby'}),
   (['Das summiert sich über das Jahr.', 'Drei Dinge helfen.'], {'summiert'}),
   (['Erstens: Nutze eine Steckdosenleiste', 'mit Schalter.'], {'Steckdosenleiste'}),
   (['Zweitens: Zieh Ladegeräte ab,', 'wenn nichts lädt.'], {'Ladegeräte'}),
   (['Drittens: Schalte Geräte richtig aus,', 'statt sie im Standby zu lassen.'], {'aus'}),
   (['Merk dir:', 'Leiste, Ladegerät, ganz aus.'], {'Leiste', 'Ladegerät', 'aus'}),
  ],
  'ill': [
   sh(lambda c, t: (tv(c, 380, 380, 1.5, led=int(t * 2) % 2 == 0), bolt(c, 620, 160, 0.9))),
   sh(lambda c, t: (tv(c, 300, 400, 1.2, led=True), clock(c, 600, 300, 95, t))),
   sh(lambda c, t: coins(c, 380, 620, 1.7, min(1 + t * 2.5, 12))),
   sh(lambda c, t: (strip(c, 430, 380, 1.2, on=t < 1.4), badge(c, 1, t))),
   sh(lambda c, t: (c.rr(150, 215, 270, 340, 16, fill=(235, 235, 240), out=NAVY, w=8), charger(c, 210, 400, 1.4, off=300 * eout(min(t / 1.2, 1))), badge(c, 2, t))),
   sh(lambda c, t: (tv(c, 380, 380, 1.5, led=False), c.line([(520, 130), (570, 180), (660, 80)], GREEN, 24), badge(c, 3, t))),
  ],
  'tiles': [lambda c, x, y, s: strip(c, x + 20 * s, y, 0.3 * s, on=False), lambda c, x, y, s: charger(c, x, y, 0.5 * s), lambda c, x, y, s: tv(c, x, y, 0.3 * s, led=False)],
 },
}
