"""Erzeugt Cover (1080x1920 JPG) aus einem Videoframe plus großem Titel.
Aufruf: python3 pipeline/cover.py <video.mp4> <cover.jpg> "<Titel>" <flat|3d> [sekunde]"""
import sys, subprocess, tempfile, os
from PIL import Image, ImageDraw, ImageFont

FD = '/usr/share/fonts/opentype/inter/'
W, H = 1080, 1920


def make(video, out, title, stil, sec=1.6):
    with tempfile.TemporaryDirectory() as td:
        png = os.path.join(td, 'f.png')
        subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-ss', str(sec), '-i', video, '-frames:v', '1', png], check=True)
        im = Image.open(png).convert('RGB')
    d = ImageDraw.Draw(im)
    if stil == '3d':
        bg, fg, acc, y0 = (3, 4, 7), (245, 247, 250), (255, 196, 64), 1395
    else:
        bg, fg, acc, y0 = (251, 247, 240), (20, 33, 61), (242, 140, 40), 1236
    d.rectangle([0, y0, W, H], fill=bg)
    # Titel: 1 bis 2 Zeilen, automatisch kleiner, bis es passt
    size = 150
    while True:
        f = ImageFont.truetype(FD + 'Inter-ExtraBold.otf', size)
        words = title.split(); lines = []; cur = ''
        for w in words:
            t = (cur + ' ' + w).strip()
            if f.getlength(t) <= 960 or not cur: cur = t
            else: lines.append(cur); cur = w
        lines.append(cur)
        if len(lines) <= 2 and max(f.getlength(x) for x in lines) <= 960: break
        size -= 6
    lh = int(size * 1.12)
    ty = y0 + 50
    d.rounded_rectangle([60, ty - 14, 76, ty + lh * len(lines) - 10], radius=8, fill=acc)
    for i, ln in enumerate(lines):
        d.text((110, ty + i * lh), ln, font=f, fill=fg if i < len(lines) - 1 or len(lines) == 1 else acc, anchor='lt')
    im.save(out, quality=90)


if __name__ == '__main__':
    v, o, t, s = sys.argv[1:5]
    make(v, o, t, s, float(sys.argv[5]) if len(sys.argv) > 5 else 1.6)
