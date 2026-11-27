"""Baut auswertung.xlsx aus insights.json, queue.json, posted.json (Tabellen + Excel-Diagramme).
Aufruf: python3 agenten/baue_excel.py [ausgabe.xlsx]"""
import json, sys, datetime as dt
from openpyxl import Workbook
from openpyxl.chart import BarChart, LineChart, Reference
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.utils import get_column_letter

out = sys.argv[1] if len(sys.argv) > 1 else 'auswertung.xlsx'
ins = json.load(open('insights.json')); q = json.load(open('queue.json')); posted = json.load(open('posted.json'))
LEN = 28.0  # mittlere Videolänge in s (Annäherung)

def match(cap):
    for e in q:
        if e['caption'][:40] == cap[:40]: return e
    return None

wb = Workbook(); ws = wb.active; ws.title = 'Reels'
hdr = ['Veröffentlicht', 'Video', 'Stil', 'Variante', 'Aufrufe', 'Reichweite', 'Likes', 'Kommentare', 'Shares', 'Gespeichert',
       'Ø Wiedergabe (s)', 'Wiedergabe % der Länge', 'Saves+Shares je 100 Aufrufe', 'Alter (h)', 'Link']
ws.append(hdr)
rows = []
for r in sorted(ins['reels'], key=lambda r: r['timestamp']):
    if r['timestamp'] < '2026-11-26': continue
    e = match(r.get('caption_anfang', '')) or {}
    i = r['insights']; t = dt.datetime.strptime(r['timestamp'], '%Y-%m-%dT%H:%M:%S%z')
    rows.append([t.astimezone(dt.timezone(dt.timedelta(hours=1))).replace(tzinfo=None), (e.get('video') or r.get('caption_anfang', ''))[:40].replace('videos/', ''),
                 e.get('stil', '?'), e.get('variante', ''), i.get('views'), i.get('reach'), i.get('likes'), i.get('comments'), i.get('shares'), i.get('saved'),
                 round((i.get('ig_reels_avg_watch_time') or 0) / 1000, 1), None, None, None, r['permalink']])
now = dt.datetime.now(dt.timezone.utc)
for n, row in enumerate(rows, start=2):
    ws.append(row)
    ws.cell(n, 12, f'=IF(E{n}>0,K{n}/{LEN},"")').number_format = '0%'
    ws.cell(n, 13, f'=IF(E{n}>0,(J{n}+I{n})/E{n}*100,"")').number_format = '0.0'
    ws.cell(n, 14, f'=ROUND((NOW()-A{n})*24,0)').number_format = '0'  # grob; Excel-Zeit lokal
    ws.cell(n, 1).number_format = 'dd.mm. hh:mm'
for c in ws[1]: c.font = Font(bold=True, color='FFFFFF'); c.fill = PatternFill('solid', fgColor='1F2A44'); c.alignment = Alignment(wrap_text=True, vertical='center')
for k, w in enumerate([15, 22, 12, 9, 10, 11, 8, 11, 8, 11, 12, 14, 16, 9, 40], 1): ws.column_dimensions[get_column_letter(k)].width = w
ws.freeze_panes = 'C2'; ws.row_dimensions[1].height = 45
last = len(rows) + 1

# Stilvergleich (Formeln, aktualisieren sich in Excel von selbst)
sv = wb.create_sheet('Stilvergleich')
sv.append(['Stil', 'Anzahl Reels', 'Ø Aufrufe', 'Ø Reichweite', 'Ø Wiedergabe (s)', 'Ø Saves+Shares je 100', 'Hinweis'])
for n, s in enumerate(['flat', 'flat-dunkel', '3d'], start=2):
    sv.append([s, f'=COUNTIFS(Reels!C2:C{last},A{n})', f'=IFERROR(AVERAGEIFS(Reels!E2:E{last},Reels!C2:C{last},A{n}),0)',
               f'=IFERROR(AVERAGEIFS(Reels!F2:F{last},Reels!C2:C{last},A{n}),0)', f'=IFERROR(AVERAGEIFS(Reels!K2:K{last},Reels!C2:C{last},A{n}),0)',
               f'=IFERROR(AVERAGEIFS(Reels!M2:M{last},Reels!C2:C{last},A{n}),0)', 'Tendenz erst ab 6 Reels je Gruppe und 72 h Laufzeit' if n == 2 else ''])
    for c in 'CDEF': sv[f'{c}{n}'].number_format = '0.0'
for c in sv[1]: c.font = Font(bold=True, color='FFFFFF'); c.fill = PatternFill('solid', fgColor='1F2A44')
for k, w in enumerate([14, 13, 12, 13, 16, 22, 50], 1): sv.column_dimensions[get_column_letter(k)].width = w

def bar(title, col, anchor, ytitle):
    ch = BarChart(); ch.type = 'col'; ch.title = title; ch.y_axis.title = ytitle; ch.height = 8; ch.width = 18
    ch.add_data(Reference(sv, min_col=col, min_row=1, max_row=4), titles_from_data=True); ch.set_categories(Reference(sv, min_col=1, min_row=2, max_row=4)); ch.legend = None
    sv.add_chart(ch, anchor)
bar('Ø Aufrufe je Stil', 3, 'A7', 'Aufrufe'); bar('Ø Wiedergabe (s) je Stil', 5, 'J7', 'Sekunden'); bar('Ø Saves+Shares je 100 Aufrufe', 6, 'A24', 'je 100')

# Verlauf
g = wb.create_sheet('Verlauf')
lc = LineChart(); lc.title = 'Aufrufe je Reel (chronologisch)'; lc.height = 9; lc.width = 26
lc.add_data(Reference(ws, min_col=5, min_row=1, max_row=last), titles_from_data=True); lc.add_data(Reference(ws, min_col=6, min_row=1, max_row=last), titles_from_data=True)
lc.set_categories(Reference(ws, min_col=2, min_row=2, max_row=last)); g.add_chart(lc, 'A1')
b = BarChart(); b.type = 'col'; b.title = 'Gespeichert und Shares je Reel'; b.height = 9; b.width = 26
b.add_data(Reference(ws, min_col=9, min_row=1, max_row=last), titles_from_data=True); b.add_data(Reference(ws, min_col=10, min_row=1, max_row=last), titles_from_data=True)
b.set_categories(Reference(ws, min_col=2, min_row=2, max_row=last)); g.add_chart(b, 'A20')

# Warteschlange
w = wb.create_sheet('Warteschlange'); w.append(['Platz', 'Video', 'Stil', 'Variante', 'Status'])
n = 0
for e in q:
    st = 'veröffentlicht' if e['video'] in posted else 'offen'
    if st == 'offen': n += 1
    w.append([n if st == 'offen' else '', e['video'].replace('videos/', ''), e.get('stil'), e.get('variante'), st])
for c in w[1]: c.font = Font(bold=True, color='FFFFFF'); c.fill = PatternFill('solid', fgColor='1F2A44')
for k, wd in enumerate([8, 26, 14, 10, 16], 1): w.column_dimensions[get_column_letter(k)].width = wd
i = wb.create_sheet('Info')
for line in [f'Stand der Daten: {ins.get("abgerufen")}', 'Quelle: insights.json (Instagram Graph API), Zuordnung zu Videos über den Caption-Anfang.',
             'Ø Wiedergabe in % nutzt eine mittlere Länge von 28 s (Näherung).', 'Kleine Stichproben: Werte sind Tendenzen, keine Beweise.']:
    i.append([line])
i.column_dimensions['A'].width = 100
wb.save(out); print('geschrieben', out, len(rows), 'Reels')
