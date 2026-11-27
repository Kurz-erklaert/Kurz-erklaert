"""Baut auswertung.xlsx aus insights.json, queue.json, posted.json (Übersicht, Reels, Verlauf, Warteschlange, Info).
Aufruf: python3 agenten/baue_excel.py [ausgabe.xlsx]"""
import json, sys, datetime as dt
from openpyxl import Workbook
from openpyxl.chart import BarChart, LineChart, Reference, Series
from openpyxl.chart.axis import DateAxis
from openpyxl.formatting.rule import DataBarRule
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter as L

out = sys.argv[1] if len(sys.argv) > 1 else 'auswertung.xlsx'
ins = json.load(open('insights.json')); q = json.load(open('queue.json')); posted = json.load(open('posted.json'))
LEN = 28.0
NAVY, ORANGE = '1F2A44', 'F28C28'
STIL = [('flat', 'Flat hell', '8FA3C7'), ('flat-dunkel', 'Flat dunkel', '2B3A67'), ('3d', '3D', 'F28C28')]
thin = Side(style='thin', color='D9DEE8'); box = Border(left=thin, right=thin, top=thin, bottom=thin)
head_font = Font(bold=True, color='FFFFFF', name='Calibri', size=11); head_fill = PatternFill('solid', fgColor=NAVY)

def hdr(ws, row, cols, height=34):
    for c in range(1, cols + 1):
        x = ws.cell(row, c); x.font = head_font; x.fill = head_fill; x.alignment = Alignment(wrap_text=True, horizontal='center', vertical='center'); x.border = box
    ws.row_dimensions[row].height = height

def match(cap):
    for e in q:
        if e['caption'][:40] == cap[:40]: return e
    return {}

# ---------- Reels ----------
ws = wb = Workbook(); ov = wb.active; ov.title = 'Übersicht'
ws = wb.create_sheet('Reels')
cols = ['Veröffentlicht', 'Video', 'Stil', 'Variante', 'Aufrufe', 'Reichweite', 'Likes', 'Kommentare', 'Shares', 'Gespeichert', 'Ø Wiedergabe (s)',
        'Wiedergabe % der Länge', 'Saves + Shares je 100 Aufrufe', 'Alter (Std.)', 'Link', 'flat', 'flat-dunkel', '3d', 'Zeitpunkt']
ws.append(cols); hdr(ws, 1, len(cols), 48)
rows = []
for r in sorted(ins['reels'], key=lambda r: r['timestamp']):
    if r['timestamp'] < '2026-11-26': continue
    e = match(r.get('caption_anfang', '')); i = r['insights']
    t = dt.datetime.strptime(r['timestamp'], '%Y-%m-%dT%H:%M:%S%z').astimezone(dt.timezone(dt.timedelta(hours=1))).replace(tzinfo=None)
    rows.append([t, (e.get('video') or '(Reel ohne Videozuordnung)')[:40].replace('videos/', '').replace('.mp4', ''), e.get('stil', '?'), e.get('variante', ''),
                 i.get('views') or 0, i.get('reach') or 0, i.get('likes') or 0, i.get('comments') or 0, i.get('shares') or 0, i.get('saved') or 0,
                 round((i.get('ig_reels_avg_watch_time') or 0) / 1000, 1), r['permalink']])
n_last = max(len(rows) + 1, 2)
for n, row in enumerate(rows, start=2):
    ws.append(row[:11] + [None, None, None, row[11]])
    ws.cell(n, 12, f'=IF(E{n}>0,K{n}/{LEN},"")').number_format = '0%'
    ws.cell(n, 13, f'=IF(E{n}>0,(J{n}+I{n})/E{n}*100,"")').number_format = '0.0'
    ws.cell(n, 14, f'=ROUND((NOW()-A{n})*24,0)').number_format = '0'
    for k, (key, _, _) in enumerate(STIL):
        ws.cell(n, 16 + k, f'=IF($C{n}="{key}",$E{n},0)')
    ws.cell(n, 1).number_format = 'dd.mm.yy hh:mm'
    ws.cell(n, 19, row[0].strftime('%d.%m. %H:%M'))
    fill = PatternFill('solid', fgColor='F5F7FB' if n % 2 == 0 else 'FFFFFF')
    for c in range(1, 16):
        x = ws.cell(n, c); x.fill = fill; x.border = box
        x.alignment = Alignment(horizontal='left' if c in (2, 15) else 'center', vertical='center')
    key = row[2]; colr = {k: c for k, _, c in STIL}.get(key, 'CCCCCC')
    ws.cell(n, 3).fill = PatternFill('solid', fgColor=colr); ws.cell(n, 3).font = Font(bold=True, color='FFFFFF' if key != 'flat' else '1F2A44')
    ws.cell(n, 15).hyperlink = row[11]; ws.cell(n, 15).value = 'öffnen'; ws.cell(n, 15).font = Font(color='0563C1', underline='single')
for k, w in enumerate([17, 24, 13, 9, 10, 11, 8, 12, 8, 12, 13, 15, 17, 10, 10, 6, 11, 6], 1): ws.column_dimensions[L(k)].width = w
for c in (16, 17, 18, 19):
    ws.column_dimensions[L(c)].width = 22 if c == 19 else 11
    ws.cell(1, c).fill = PatternFill('solid', fgColor='98A2B3')
    for rr in range(2, n_last + 1): ws.cell(rr, c).font = Font(color='98A2B3', size=9)
ws.cell(1, 16).value = 'Flat hell'; ws.cell(1, 17).value = 'Flat dunkel'; ws.cell(1, 18).value = '3D'; ws.cell(1, 19).value = 'Zeitpunkt (Achse)'
ws.freeze_panes = 'C2'
if rows:
    ws.conditional_formatting.add(f'E2:E{n_last}', DataBarRule(start_type='num', start_value=0, end_type='max', color='8FA3C7'))
    ws.conditional_formatting.add(f'F2:F{n_last}', DataBarRule(start_type='num', start_value=0, end_type='max', color='B8C4DD'))

# ---------- Übersicht ----------
ov.sheet_view.showGridLines = False
ov['B2'] = 'Kurz erklärt: Alltag, Auswertung'; ov['B2'].font = Font(bold=True, size=20, color=NAVY)
ov['B3'] = f'Datenstand: {ins.get("abgerufen", "")[:16].replace("T", " ")} UTC · Quelle: Instagram-Kennzahlen · Reels ab 26.11.2026'; ov['B3'].font = Font(italic=True, color='667085')
kp = [('Reels', f'=COUNTA(Reels!B2:B{n_last})', '0'), ('Aufrufe gesamt', f'=SUM(Reels!E2:E{n_last})', '#,##0'),
      ('Ø Aufrufe je Reel', f'=IFERROR(AVERAGE(Reels!E2:E{n_last}),0)', '0.0'), ('Ø Wiedergabe (s)', f'=IFERROR(AVERAGE(Reels!K2:K{n_last}),0)', '0.0'),
      ('Gespeichert gesamt', f'=SUM(Reels!J2:J{n_last})', '0'), ('Shares gesamt', f'=SUM(Reels!I2:I{n_last})', '0')]
for k, (lab, fm, nf) in enumerate(kp):
    c = 2 + k * 2
    ov.merge_cells(start_row=5, start_column=c, end_row=5, end_column=c + 1); ov.merge_cells(start_row=6, start_column=c, end_row=6, end_column=c + 1)
    a = ov.cell(5, c, lab); a.font = Font(color='FFFFFF', size=10); a.fill = head_fill; a.alignment = Alignment(horizontal='center')
    ov.cell(5, c + 1).fill = head_fill
    b = ov.cell(6, c, fm); b.number_format = nf; b.font = Font(bold=True, size=18, color=NAVY); b.alignment = Alignment(horizontal='center'); b.fill = PatternFill('solid', fgColor='EEF2FA')
    ov.cell(6, c + 1).fill = PatternFill('solid', fgColor='EEF2FA')
ov.row_dimensions[6].height = 34
for c in range(1, 16): ov.column_dimensions[L(c)].width = 13
ov.column_dimensions['A'].width = 3
ov['B8'] = 'Stilvergleich'; ov['B8'].font = Font(bold=True, size=14, color=NAVY)
heads = ['Stil', 'Reels', 'Ø Aufrufe', 'Ø Reichweite', 'Ø Wiedergabe (s)', 'Saves+Shares je 100']
for k, h in enumerate(heads): ov.cell(9, 2 + k, h)
hdr(ov, 9, 7, 32); ov.cell(9, 1).fill = PatternFill(); ov.cell(9, 1).border = Border()
for r_i, (key, lab, colr) in enumerate(STIL, start=10):
    ov.cell(r_i, 2, lab); ov.cell(r_i, 2).font = Font(bold=True, color='FFFFFF' if key != 'flat' else NAVY); ov.cell(r_i, 2).fill = PatternFill('solid', fgColor=colr)
    ov.cell(r_i, 8, key).font = Font(color='FFFFFF', size=8)
    rng = lambda col: f'Reels!{col}2:{col}{n_last}'
    ov.cell(r_i, 3, f'=COUNTIFS({rng("C")},$H{r_i})')
    for c_i, col in zip((4, 5, 6, 7), 'EFKM'):
        ov.cell(r_i, c_i, f'=IFERROR(AVERAGEIFS({rng(col)},{rng("C")},$H{r_i}),0)').number_format = '0.0'
    for c_i in range(2, 8):
        ov.cell(r_i, c_i).border = box
        if c_i > 2: ov.cell(r_i, c_i).alignment = Alignment(horizontal='center')
ov.column_dimensions['H'].width = 3
ov['B13'] = 'Hinweis: Bei wenigen Reels je Gruppe sind die Werte nur Tendenzen. Entscheidung erst ab 6 Reels je Gruppe und mindestens 72 Stunden Laufzeit.'
ov['B13'].font = Font(italic=True, color='667085', size=9)

def style_chart(ch, title, xt=None, yt=None, w=17, h=8.5, plot_h=0.62, labels_below=False):
    from openpyxl.chart.layout import Layout, ManualLayout
    ch.title = title; ch.width = w; ch.height = h
    ch.title.overlay = False
    ch.x_axis.delete = False; ch.y_axis.delete = False
    ch.x_axis.title = None  # Achsentitel unten entfallen: Beschriftung erklärt sich selbst, verhindert Überlagerung
    if yt:
        ch.y_axis.title = yt; ch.y_axis.title.overlay = False
    if ch.legend is not None:
        ch.legend.position = 'b'; ch.legend.overlay = False
    ch.layout = Layout(manualLayout=ManualLayout(layoutTarget='inner', xMode='edge', yMode='edge', x=0.12, y=0.16, w=0.84, h=plot_h))

def bar_by_style(col, title, ytitle, anchor):
    ch = BarChart(); ch.type = 'col'; ch.varyColors = False
    ch.add_data(Reference(ov, min_col=col, min_row=9, max_row=12), titles_from_data=True)
    ch.set_categories(Reference(ov, min_col=2, min_row=10, max_row=12)); ch.legend = None
    s = ch.series[0]; s.graphicalProperties.solidFill = NAVY
    from openpyxl.chart.series import DataPoint
    for idx, (_, _, colr) in enumerate(STIL):
        dp = DataPoint(idx=idx); dp.graphicalProperties.solidFill = colr; s.dPt.append(dp)
    style_chart(ch, title, None, ytitle, 12, 8, 0.6); ov.add_chart(ch, anchor)
bar_by_style(4, 'Ø Aufrufe je Stil', 'Aufrufe', 'B15'); bar_by_style(6, 'Ø Wiedergabe je Stil', 'Sekunden', 'H15'); bar_by_style(7, 'Saves + Shares je 100 Aufrufe', 'je 100', 'N15')

# ---------- Verlauf (Zeitachse) ----------
g = wb.create_sheet('Verlauf'); g.sheet_view.showGridLines = False
g['B2'] = 'Verlauf über die Zeit'; g['B2'].font = Font(bold=True, size=18, color=NAVY)
g['B3'] = 'Jeder Punkt oder Balken ist ein Reel. Die waagerechte Achse ist die Zeitleiste: links das älteste, rechts das neueste Reel.'; g['B3'].font = Font(italic=True, color='667085')
def time_chart(kind, cols_, title, ytitle, anchor, colors):
    ch = LineChart() if kind == 'line' else BarChart()
    if kind == 'bar': ch.type = 'col'; ch.overlap = 100 if len(cols_) > 1 and cols_[0] >= 16 else None
    for c, colr in zip(cols_, colors):
        ch.add_data(Reference(ws, min_col=c, min_row=1, max_row=n_last), titles_from_data=True)
        s = ch.series[-1]
        if kind == 'line':
            s.graphicalProperties.line.solidFill = colr; s.graphicalProperties.line.width = 28000; s.marker.symbol = 'circle'; s.marker.size = 8
            s.marker.graphicalProperties.solidFill = colr; s.smooth = False
        else: s.graphicalProperties.solidFill = colr
    ch.set_categories(Reference(ws, min_col=19, min_row=2, max_row=n_last))
    style_chart(ch, title, None, ytitle, 25, 11, 0.5); 
    ch.x_axis.delete = False; ch.y_axis.delete = False
    ch.plotVisOnly = False
    from openpyxl.chart.text import RichText
    from openpyxl.drawing.text import Paragraph, ParagraphProperties, CharacterProperties, RichTextProperties
    ch.x_axis.txPr = RichText(bodyPr=RichTextProperties(rot=-5400000, vert='horz'), p=[Paragraph(pPr=ParagraphProperties(defRPr=CharacterProperties(sz=800)), endParaRPr=CharacterProperties())])
    ch.x_axis.tickLblSkip = 1 if n_last <= 25 else max(1, n_last // 20)
    g.add_chart(ch, anchor)
time_chart('line', [5, 6], 'Aufrufe und Reichweite je Reel', 'Anzahl', 'B5', [NAVY, ORANGE])
time_chart('bar', [16, 17, 18], 'Aufrufe je Reel, nach Stil eingefärbt', 'Aufrufe', 'B27', [c for _, _, c in STIL])
time_chart('line', [11], 'Ø Wiedergabezeit je Reel', 'Sekunden', 'B49', [NAVY])
time_chart('bar', [9, 10], 'Shares und Gespeichert je Reel', 'Anzahl', 'B71', [ORANGE, NAVY])

# ---------- Warteschlange ----------
w = wb.create_sheet('Warteschlange'); w.append(['Platz', 'Video', 'Stil', 'Variante', 'Status']); hdr(w, 1, 5, 28)
n = 0
for e in q:
    done = e['video'] in posted; n += 0 if done else 1
    w.append([n if not done else '', e['video'].replace('videos/', '').replace('.mp4', ''), e.get('stil'), e.get('variante'), 'veröffentlicht' if done else 'offen'])
    r = w.max_row; colr = {k: c for k, _, c in STIL}.get(e.get('stil'), 'CCCCCC')
    for c in range(1, 6): w.cell(r, c).border = box; w.cell(r, c).alignment = Alignment(horizontal='center')
    w.cell(r, 3).fill = PatternFill('solid', fgColor=colr); w.cell(r, 3).font = Font(bold=True, color='FFFFFF' if e.get('stil') != 'flat' else NAVY)
    if done:
        for c in (1, 2, 4, 5): w.cell(r, c).font = Font(color='98A2B3')
for k, wd in enumerate([8, 26, 14, 10, 16], 1): w.column_dimensions[L(k)].width = wd
w.freeze_panes = 'A2'

i = wb.create_sheet('Info')
for line in ['Quelle: insights.json (Instagram Graph API), Zuordnung zu Videos über den Anfang der Caption.', f'Stand der Daten: {ins.get("abgerufen")}',
             'Wiedergabe in % nutzt eine mittlere Länge von 28 s (Näherung).', 'Kleine Stichproben: Werte sind Tendenzen, keine Beweise.',
             'Die Datei wird automatisch überschrieben. Eigene Berechnungen bitte in einer Kopie machen.']:
    i.append([line])
i.column_dimensions['A'].width = 100
wb.save(out); print('geschrieben', out, len(rows), 'Reels')
