#!/usr/bin/env python3
"""Prüft Skript-Dateien (plan/skripte/*.json) auf Format. Aufruf: python3 agenten/pruefe_skript.py [datei ...]
Ohne Argument werden alle Dateien in plan/skripte/ geprüft. Rückgabe 1 bei Fehlern."""
import json, re, sys, glob

STATUS = {"skript", "geprueft", "ueberarbeiten", "abgelehnt", "produziert"}
ERG = {"", "ok", "ueberarbeiten", "abgelehnt"}


def strip(w):
    return w.strip('.,:?!;')


def check(path):
    err = []
    try:
        s = json.load(open(path, encoding='utf-8'))
    except Exception as e:
        return [f'kein gültiges JSON: {e}']
    for k in ('id', 'thema', 'kategorie', 'variante', 'stil', 'scenes', 'merksatz_woerter', 'bildideen', 'caption', 'quellen', 'status', 'faktencheck'):
        if k not in s:
            err.append(f'Feld fehlt: {k}')
    if err:
        return err
    if not re.fullmatch(r's\d+_\d{2}_[a-z0-9_]+', s['id']):
        err.append('id muss wie s3_01_stichwort aussehen')
    if s['variante'] not in ('A', 'B'): err.append('variante muss A oder B sein')
    if s['stil'] not in ('flat', '3d'): err.append('stil muss flat oder 3d sein')
    if s['status'] not in STATUS: err.append('ungültiger status')
    if s['faktencheck'].get('ergebnis', '') not in ERG: err.append('ungültiges faktencheck.ergebnis')
    sc = s['scenes']
    if len(sc) != 7:
        err.append('genau 7 Szenen nötig'); return err
    words = 0
    for i, x in enumerate(sc):
        z = x.get('zeilen', [])
        if not 1 <= len(z) <= 3: err.append(f'Szene {i}: 1 bis 3 Zeilen')
        for line in z:
            lim = 52 if i == 2 else 38
            if len(line) > lim: err.append(f'Szene {i}: Zeile zu lang ({len(line)}>{lim}): {line}')
            if re.search(r'[\U0001F300-\U0001FAFF☀-➿]|\.\.\.|…', line): err.append(f'Szene {i}: Emoji oder Auslassungspunkte im Videotext')
        text = ' '.join(z); words += len(text.split())
        toks = {strip(w) for w in text.split()}
        if not 1 <= len(x.get('schluesselwoerter', [])) <= 3: err.append(f'Szene {i}: 1 bis 3 Schlüsselwörter')
        for kw in x.get('schluesselwoerter', []):
            if strip(kw) not in toks: err.append(f'Szene {i}: Schlüsselwort nicht im Text: {kw}')
    if not 55 <= words <= 80: err.append(f'Wortzahl {words}, erlaubt 55 bis 80')
    last = {strip(w) for w in ' '.join(sc[6]['zeilen']).split()}
    if len(s['merksatz_woerter']) != 3: err.append('merksatz_woerter: genau 3')
    for w in s['merksatz_woerter']:
        if strip(w) not in last: err.append(f'merksatz_wort nicht in Szene 6: {w}')
    if len(s['bildideen']) != 7: err.append('bildideen: genau 7')
    tags = re.findall(r'#\w+', s['caption'])
    if len(tags) != 5: err.append(f'Caption braucht genau 5 Hashtags, hat {len(tags)}')
    if not s['caption'].strip().splitlines()[-1].lstrip().startswith('#'): err.append('Hashtags gehören in die letzte Zeile')
    if '#' in ''.join(s['caption'].strip().splitlines()[:-1]): err.append('Hashtags nur in der letzten Zeile')
    if s['status'] == 'geprueft' and (not s['quellen'] or s['faktencheck'].get('ergebnis') != 'ok'):
        err.append('geprueft braucht quellen und faktencheck.ergebnis ok')
    return err


if __name__ == '__main__':
    files = sys.argv[1:] or sorted(glob.glob('plan/skripte/*.json'))
    bad = 0
    for f in files:
        e = check(f)
        print(('OK    ' if not e else 'FEHLER ') + f)
        for m in e: print('   -', m)
        bad += bool(e)
    sys.exit(1 if bad else 0)
