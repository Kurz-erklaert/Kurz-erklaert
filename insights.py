"""Holt Reel-Kennzahlen von Instagram und speichert sie in insights.json."""
import json, os, sys, urllib.request, urllib.parse, urllib.error, datetime

HOST = os.environ.get("IG_HOST", "https://graph.facebook.com")
VER = os.environ.get("IG_VERSION", "v21.0")
TOKEN = os.environ["IG_TOKEN"]
UID = os.environ["IG_USER_ID"]


def get(path, params):
    url = f"{HOST}/{VER}/{path}?" + urllib.parse.urlencode(dict(params, access_token=TOKEN))
    try:
        with urllib.request.urlopen(url, timeout=60) as r:
            return json.load(r)
    except urllib.error.HTTPError as e:
        return {"error": e.read().decode()[:300]}


METRICS = ["views", "reach", "likes", "comments", "shares", "saved", "total_interactions",
           "ig_reels_avg_watch_time", "ig_reels_video_view_total_time"]

acc = get(UID, {"fields": "username,followers_count,media_count"})
# Token-Info (Ablaufdatum, Gültigkeit); fehlertolerant, nicht jeder Tokentyp erlaubt das
tok = get("debug_token", {"input_token": TOKEN})
tinfo = tok.get("data") if "data" in tok else {"fehler": (tok.get("error") or "")[:200]}
if isinstance(tinfo, dict):
    tinfo = {k: tinfo.get(k) for k in ("is_valid", "type", "expires_at", "data_access_expires_at", "scopes", "fehler")}
media = get(f"{UID}/media", {"fields": "id,caption,timestamp,permalink,media_product_type,like_count,comments_count", "limit": 50})
out = {"abgerufen": datetime.datetime.utcnow().isoformat() + "Z", "konto": acc, "token_info": tinfo, "reels": []}
jetzt = datetime.datetime.utcnow()
for m in media.get("data", []):
    if m.get("media_product_type") != "REELS":
        continue
    row = {k: m.get(k) for k in ("id", "timestamp", "permalink", "like_count", "comments_count")}
    row["caption_anfang"] = (m.get("caption") or "")[:60]
    ins = {}
    for met in METRICS:  # jede Kennzahl einzeln, damit ein Fehler nicht alles stoppt
        r = get(f"{m['id']}/insights", {"metric": met})
        if "data" in r and r["data"]:
            ins[met] = r["data"][0]["values"][0]["value"]
        else:
            ins[met] = None
            row.setdefault("fehler", {})[met] = (r.get("error") or "")[:120]
    row["insights"] = ins
    # Kommentare der letzten 14 Tage (für den Community-Agenten); Fehler (fehlende Berechtigung) werden nur vermerkt
    try:
        alter = jetzt - datetime.datetime.strptime(m["timestamp"][:19], "%Y-%m-%dT%H:%M:%S")
    except Exception:
        alter = datetime.timedelta(days=99)
    if alter.days <= 14 and (m.get("comments_count") or 0) > 0:
        c = get(f"{m['id']}/comments", {"fields": "id,text,username,timestamp,like_count,replies{id,text,username,timestamp}", "limit": 30})
        if "data" in c:
            row["kommentare"] = c["data"]
        else:
            row["kommentare_fehler"] = (c.get("error") or "")[:160]
    out["reels"].append(row)
if "error" in media:
    out["fehler"] = media["error"]
json.dump(out, open("insights.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("Reels:", len(out["reels"]), "| Fehler:", out.get("fehler"))
