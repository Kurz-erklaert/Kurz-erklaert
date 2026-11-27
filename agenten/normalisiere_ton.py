#!/usr/bin/env python3
"""Normalisiert die Lautstärke eines Videos auf etwa -15 LUFS (Bild bleibt unverändert, nur Ton wird neu kodiert).
Aufruf: python3 agenten/normalisiere_ton.py <video.mp4> [...]   (überschreibt die Datei)"""
import json, os, re, subprocess, sys

I, TP, LRA = -15.0, -1.5, 9.0


def norm(path):
    r = subprocess.run(['ffmpeg', '-nostats', '-i', path, '-af', f'loudnorm=I={I}:TP={TP}:LRA={LRA}:print_format=json', '-f', 'null', '-'], capture_output=True, text=True)
    m = json.loads(re.search(r'\{[^{}]*"input_i"[^{}]*\}', r.stderr, re.S).group(0))
    af = (f'loudnorm=I={I}:TP={TP}:LRA={LRA}:measured_I={m["input_i"]}:measured_TP={m["input_tp"]}:measured_LRA={m["input_lra"]}:'
          f'measured_thresh={m["input_thresh"]}:offset={m["target_offset"]}:linear=true')
    tmp = path[:-4] + '_norm.mp4'
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', path, '-map', '0:v', '-map', '0:a', '-c:v', 'copy', '-af', af, '-ar', '44100', '-c:a', 'aac', '-b:a', '192k', tmp], check=True)
    os.replace(tmp, path)
    print(f'{path}: {m["input_i"]} LUFS -> ca. {I} LUFS')


if __name__ == '__main__':
    for f in sys.argv[1:]:
        norm(f)
