"""Veröffentlicht das nächste Video aus queue.json als Instagram Reel."""
import json, os, sys, time, urllib.request, urllib.parse, urllib.error
from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo

HOST = os.environ.get("IG_HOST", "https://graph.facebook.com")
VER = os.environ.get("IG_VERSION", "v21.0")
TOKEN = os.environ["IG_TOKEN"]
UID = os.environ["IG_USER_ID"]
REPO = os.environ["GITHUB_REPOSITORY"]
BRANCH = os.environ.get("GITHUB_REF_NAME", "main")
DRY = os.environ.get("DRY_RUN") == "1"


def call(method, path, params, fatal=True):
    params = dict(params, access_token=TOKEN)
    url = f"{HOST}/{VER}/{path}"
    data = urllib.parse.urlencode(params).encode() if method == "POST" else None
    if method == "GET":
        url += "?" + urllib.parse.urlencode(params)
    try:
        with urllib.request.urlopen(urllib.request.Request(url, data=data, method=method), timeout=60) as r:
            return json.load(r)
    except urllib.error.HTTPError as e:
        msg = e.read().decode()[:500]
        print("API-Fehler:", msg)
        if fatal: sys.exit(1)
        return {"error": msg}


queue = json.load(open("queue.json", encoding="utf-8"))
posted = json.load(open("posted.json"))
try:
    posted_at = json.load(open("posted_at.json"))
except FileNotFoundError:
    posted_at = {}

TZ = ZoneInfo("Europe/Berlin")
START = datetime(2026, 11, 27, 18, 30, tzinfo=TZ)   # erster Slot des Dauerbetriebs (Folge 2)
SLOTS = ((8, 0), (18, 30))
MIN_GAP = timedelta(hours=3)


def slots_due(now):
    n, d = 0, START.date()
    while d <= now.date():
        for h, m in SLOTS:
            sl = datetime(d.year, d.month, d.day, h, m, tzinfo=TZ)
            if START <= sl <= now:
                n += 1
        d += timedelta(days=1)
    return n


if os.environ.get("GITHUB_EVENT_NAME") == "schedule" or os.environ.get("FORCE_SLOT_CHECK") == "1":
    now = datetime.fromisoformat(os.environ["NOW_ISO"]) if os.environ.get("NOW_ISO") else datetime.now(TZ)
    expected = 1 + slots_due(now)       # Folge 1 wurde vorab als Test gepostet
    if len(posted) >= expected:
        print(f"Kein Slot fällig (gepostet {len(posted)}, erwartet {expected}, jetzt {now:%d.%m. %H:%M})."); sys.exit(0)
    last = max((datetime.fromisoformat(v) for v in posted_at.values()), default=None)
    if last and now - last < MIN_GAP:
        print(f"Slot fällig, aber letztes Video erst vor {now - last}. Warte."); sys.exit(0)
    print(f"Slot fällig (gepostet {len(posted)}, erwartet {expected}).")
todo = [x for x in queue if x["video"] not in posted]
if not todo:
    print("Warteschlange leer."); sys.exit(0)
item = todo[0]
video_url = f"https://raw.githubusercontent.com/{REPO}/{BRANCH}/{item['video']}"
print("Nächstes Video:", item["video"], video_url)
if DRY:
    print("DRY_RUN, kein Upload."); sys.exit(0)

params = {"media_type": "REELS", "video_url": video_url, "caption": item["caption"], "share_to_feed": "true"}
if item.get("cover") and os.path.exists(item["cover"]):
    params["cover_url"] = f"https://raw.githubusercontent.com/{REPO}/{BRANCH}/{item['cover']}"
    c = call("POST", f"{UID}/media", params, fatal=False)
    if "id" not in c:   # Cover abgelehnt: ohne Cover erneut versuchen, damit nichts ausfällt
        print("Cover wurde abgelehnt, veröffentliche ohne Cover.")
        params.pop("cover_url"); c = call("POST", f"{UID}/media", params)
else:
    c = call("POST", f"{UID}/media", params)
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
posted_at[item["video"]] = datetime.now(timezone.utc).isoformat()
json.dump(posted_at, open("posted_at.json", "w"), indent=1)
