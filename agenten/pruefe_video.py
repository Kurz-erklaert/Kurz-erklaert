#!/usr/bin/env python3
"""Technische Qualitätsprüfung für fertige Reels. Aufruf: python3 agenten/pruefe_video.py [video ...]
Ohne Argument alle Videos aus queue.json. Rückgabe 1, wenn ein harter Fehler gefunden wurde. Braucht ffmpeg/ffprobe."""
import json, re, subprocess, sys, os


def run(cmd):
    return subprocess.run(cmd, capture_output=True, text=True)


def check(path):
    fehler, warn, info = [], [], {}
    if not os.path.exists(path):
        return [f'Datei fehlt: {path}'], [], {}
    p = json.loads(run(['ffprobe', '-v', 'error', '-show_streams', '-show_format', '-of', 'json', path]).stdout or '{}')
    v = next((s for s in p.get('streams', []) if s['codec_type'] == 'video'), None)
    a = next((s for s in p.get('streams', []) if s['codec_type'] == 'audio'), None)
    if not v: return ['kein Videostream'], [], {}
    if not a: fehler.append('kein Tonstream')
    if (v['width'], v['height']) != (1080, 1920): fehler.append(f"Auflösung {v['width']}x{v['height']}, erwartet 1080x1920")
    if v['codec_name'] != 'h264': fehler.append(f"Videocodec {v['codec_name']}, erwartet h264")
    if a and a['codec_name'] != 'aac': warn.append(f"Audiocodec {a['codec_name']}, empfohlen aac")
    num, den = v['r_frame_rate'].split('/')
    fps = float(num) / float(den)
    if not 23 <= fps <= 61: fehler.append(f'Bildrate {fps:.1f}')
    dur = float(p['format']['duration']); info['dauer'] = round(dur, 1)
    if not 20 <= dur <= 40: fehler.append(f'Dauer {dur:.1f} s außerhalb 20 bis 40 s')
    elif not 24 <= dur <= 33: warn.append(f'Dauer {dur:.1f} s außerhalb der Wunschlänge 24 bis 33 s')
    mb = os.path.getsize(path) / 1e6; info['mb'] = round(mb, 1)
    if mb > 100: fehler.append(f'Datei {mb:.0f} MB, über 100 MB')
    if a:
        ad = float(a.get('duration') or dur)
        if abs(ad - float(v.get('duration') or dur)) > 1.0: warn.append(f'Ton und Bild unterschiedlich lang ({ad:.1f} / {float(v.get("duration") or dur):.1f} s)')
        r = run(['ffmpeg', '-nostats', '-i', path, '-af', 'ebur128=peak=true,silencedetect=n=-40dB:d=1.2', '-f', 'null', '-'])
        t = r.stderr
        m = re.findall(r'I:\s+(-?[\d.]+) LUFS', t); tp = re.findall(r'Peak:\s+(-?[\d.]+) dBFS', t)
        if m:
            lufs = float(m[-1]); info['lufs'] = lufs
            if lufs < -24: fehler.append(f'zu leise ({lufs} LUFS)')
            elif lufs < -20 or lufs > -9: warn.append(f'Lautstärke {lufs} LUFS (Ziel etwa -18 bis -12)')
        if tp and float(tp[-1]) > -0.1: warn.append(f'Übersteuerung (True Peak {tp[-1]} dBFS)')
        sil = re.findall(r'silence_start: ([\d.]+)', t)
        if sil and float(sil[0]) < 0.5: warn.append('Stille am Anfang')
        if len(sil) >= 3: warn.append(f'{len(sil)} lange Pausen (über 1,2 s)')
    # Schwarzbild in den ersten 1,5 Sekunden
    r = run(['ffmpeg', '-nostats', '-t', '1.5', '-i', path, '-vf', 'blackdetect=d=0.8:pix_th=0.06', '-f', 'null', '-'])
    if 'black_start' in r.stderr: fehler.append('schwarzes Bild am Anfang')
    return fehler, warn, info


if __name__ == '__main__':
    files = sys.argv[1:] or [e['video'] for e in json.load(open('queue.json', encoding='utf-8'))]
    bad = 0
    for f in files:
        e, w, i = check(f)
        print(('OK     ' if not e else 'FEHLER ') + f, i)
        for m in e: print('   - FEHLER:', m)
        for m in w: print('   - Hinweis:', m)
        bad += bool(e)
    sys.exit(1 if bad else 0)
