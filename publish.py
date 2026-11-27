"""Veröffentlicht das nächste Video aus queue.json als Instagram Reel."""
import json, os, sys, time, urllib.request, urllib.parse, urllib.error

HOST = os.environ.get("IG_HOST", "https://graph.facebook.com")
VER = os.environ.get("IG_VERSION", "v21.0")
TOKEN = os.environ["IG_TOKEN"]
UID = os.environ["IG_USER_ID"]
REPO = os.environ["GITHUB_REPOSITORY"]
BRANCH = os.environ.get("GITHUB_REF_NAME", "main")
DRY = os.environ.get("DRY_RUN") == "1"


def call(method, path, params):
    params = dict(params, access_token=TOKEN)
    url = f"{HOST}/{VER}/{path}"
    data = urllib.parse.urlencode(params).encode() if method == "POST" else None
    if method == "GET":
        url += "?" + urllib.parse.urlencode(params)
    try:
        with urllib.request.urlopen(urllib.request.Request(url, data=data, method=method), timeout=60) as r:
            return json.load(r)
    except urllib.error.HTTPError as e:
        print("API-Fehler:", e.read().decode()[:500]); sys.exit(1)


queue = json.load(open("queue.json", encoding="utf-8"))
posted = json.load(open("posted.json"))
todo = [x for x in queue if x["video"] not in posted]
if not todo:
    print("Warteschlange leer."); sys.exit(0)
item = todo[0]
video_url = f"https://raw.githubusercontent.com/{REPO}/{BRANCH}/{item['video']}"
print("Nächstes Video:", item["video"], video_url)
if DRY:
    print("DRY_RUN, kein Upload."); sys.exit(0)

c = call("POST", f"{UID}/media", {"media_type": "REELS", "video_url": video_url,
                                  "caption": item["caption"], "share_to_feed": "true"})
cid = c["id"]
for _ in range(40):
    s = call("GET", cid, {"fields": "status_code,status"})
    print("Status:", s)
    if s.get("status_code") == "FINISHED": break
    if s.get("status_code") in ("ERROR", "EXPIRED"): sys.exit("Verarbeitung fehlgeschlagen")
    time.sleep(15)
else:
    sys.exit("Zeitüberschreitung")
p = call("POST", f"{UID}/media_publish", {"creation_id": cid})
print("Veröffentlicht:", p)
posted.append(item["video"])
json.dump(posted, open("posted.json", "w"), indent=1)
