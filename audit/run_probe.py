"""Run a batch of read-only requests against the production SmartScout API and save trimmed responses.

Input : audit/requests/<batch>.jsonl   lines: {"id": "...", "method": "GET|POST", "path": "/api/...", "body": {...}, "tag": "..."}
Output: audit/results/<batch>.jsonl    lines: {"id","tag","method","path","body","status","ms","resp"|"error"}
"""
import json, os, sys, time, urllib.request, urllib.error
from concurrent.futures import ThreadPoolExecutor

API = os.environ.get("API", "https://football-recruitment-engine-production.up.railway.app")
CONC = int(os.environ.get("CONC", "5"))
PLAYER_KEYS = ["sportmonks_id", "name", "team_name", "league_name", "position", "detailed_position", "position_group",
               "nationality", "age", "height", "preferred_foot", "contract_expiry", "market_value", "is_loan",
               "is_injured", "injury_description", "archetype_match", "scores", "highlighted_stats", "rank",
               "availability_label", "value_tier_rank", "value_tier_total", "image_url", "similarity_score"]
STAT_KEYS = ["minutes_played", "appearances", "goals_p90", "assists_p90", "key_passes_p90", "successful_dribbles_p90",
             "tackles_p90", "interceptions_p90", "aerials_won_p90", "duels_won_pct", "accurate_pass_pct", "xg_p90",
             "shots_p90", "clearances_p90", "saves_p90", "accurate_crosses_p90", "rating"]


def trim_player(p):
    out = {k: p.get(k) for k in PLAYER_KEYS if k in p}
    st = p.get("stats") or {}
    out["stats"] = {k: st.get(k) for k in STAT_KEYS if k in st}
    return out


def trim(resp):
    if isinstance(resp, dict):
        r = dict(resp)
        for key in ("players", "results", "candidates", "similar"):
            if isinstance(r.get(key), list):
                r[key] = [trim_player(p) if isinstance(p, dict) else p for p in r[key][:25]]
        s = json.dumps(r, ensure_ascii=False)
        if len(s) > 60000:
            return {"_truncated": True, "head": s[:60000]}
        return r
    s = json.dumps(resp, ensure_ascii=False)
    return resp if len(s) <= 60000 else {"_truncated": True, "head": s[:60000]}


def run(req):
    url = API + req["path"]
    data = json.dumps(req.get("body")).encode() if req.get("body") is not None else None
    hdr = {"Content-Type": "application/json"} if data else {}
    t = time.time()
    out = {k: req.get(k) for k in ("id", "tag", "method", "path", "body")}
    for attempt in range(3):
        try:
            r = urllib.request.urlopen(urllib.request.Request(url, data=data, headers=hdr, method=req.get("method", "GET")), timeout=240)
            body = r.read().decode("utf-8", "replace")
            out["status"] = r.status
            try:
                out["resp"] = trim(json.loads(body))
            except Exception:
                out["resp"] = body[:5000]
            break
        except urllib.error.HTTPError as e:
            out["status"] = e.code
            out["error"] = e.read().decode("utf-8", "replace")[:3000]
            if e.code not in (502, 503, 504):
                break
        except Exception as e:
            out["status"] = None
            out["error"] = f"{type(e).__name__}: {e}"
        time.sleep(5 * (attempt + 1))
    out["ms"] = int((time.time() - t) * 1000)
    return out


def main(batch_path):
    reqs = [json.loads(l) for l in open(batch_path) if l.strip()]
    name = os.path.splitext(os.path.basename(batch_path))[0]
    os.makedirs("results", exist_ok=True)
    out_path = f"results/{name}.jsonl"
    done = 0
    with open(out_path, "w") as f, ThreadPoolExecutor(CONC) as ex:
        for res in ex.map(run, reqs):
            f.write(json.dumps(res, ensure_ascii=False) + "\n")
            done += 1
            if done % 50 == 0:
                print(f"{name}: {done}/{len(reqs)}", flush=True)
    print(f"{name}: wrote {done} results → {out_path}", flush=True)


if __name__ == "__main__":
    for p in sys.argv[1:]:
        main(p)
