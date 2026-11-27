import json, os, sys, base64, urllib.request, urllib.error
exec(open('lib.py').read().replace('def sceneF', 'def _x'), {}) if False else None
ns = {'math': __import__('math'), 'ORANGE': 0, 'RED': 0, 'NAVY': 0, 'WHITE': 0, 'SKY': 0, 'WATER': 0, 'PEACH': 0, 'GREY': 0, 'GREEN': 0, 'BG': 0, 'C': object}
exec(open('lib.py').read(), ns)
ns['eob'] = ns['eout'] = lambda x: x
exec(open('specs2.py').read(), ns)
SPECS = ns['SPECS']
OUT = 'work'
for vid in sys.argv[1:]:
    sc = [' '.join(s[0]) for s in SPECS[vid]['scenes']]
    text = '[excited] ' + sc[0] + ' [short pause] ' + sc[1] + ' ' + sc[2] + ' [short pause] ' + ' '.join(sc[3:6]) + ' [warmly] ' + sc[6]
    req = urllib.request.Request(
        "https://api.elevenlabs.io/v1/text-to-speech/ZS4LV6KFpS6qQd2D5m9U/with-timestamps?output_format=mp3_44100_128",
        data=json.dumps({"text": text, "model_id": "eleven_v4", "language_code": "de"}).encode(),
        headers={"xi-api-key": os.environ["XI"], "Content-Type": "application/json"})
    try:
        r = json.load(urllib.request.urlopen(req, timeout=120))
    except urllib.error.HTTPError as e:
        print(vid, "HTTP", e.code, e.read()[:200].decode()); continue
    open(f"{OUT}/voice_{vid}.mp3", "wb").write(base64.b64decode(r["audio_base64"]))
    json.dump(r["alignment"], open(f"{OUT}/align_{vid}.json", "w"))
    print(vid, "ok", len(text.split()), "Wörter", flush=True)
