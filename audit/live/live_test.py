"""Live end-to-end test of every SmartScout feature against production, as a real signed-in test account.

Runs on GitHub Actions (production is not reachable from the dev sandbox). Needs repository secrets
TEST_USER_EMAIL / TEST_USER_PASSWORD for an approved test account on the 'elite' plan.
Input : audit/live/plan.json (built from the audit agents' request files)
Output: results/live-<stamp>.jsonl (one line per request) + results/live-<stamp>-summary.json
Side effects are limited to the test account: a saved squad (created then deleted), settings, events,
a handful of cached scouting reports. contact-agent is never called (it sends real emails).
"""
import json, os, sys, time, random, threading, urllib.request, urllib.error
from concurrent.futures import ThreadPoolExecutor

API = os.environ.get("API", "https://football-recruitment-engine-production.up.railway.app")
AUTH = "https://qimgcswndezrhoiokphu.supabase.co/auth/v1/token?grant_type=password"
ANON = os.environ.get("SUPABASE_ANON_KEY", "")     # public key the website ships to every browser
EMAIL, PASSWORD = os.environ.get("TEST_USER_EMAIL", ""), os.environ.get("TEST_USER_PASSWORD", "")
STATIC_TOKEN = os.environ.get("STATIC_TOKEN")      # local dry runs only
STAMP = time.strftime("%Y%m%dT%H%M%SZ", time.gmtime())
OUT = f"results/live-{STAMP}.jsonl"
os.makedirs("results", exist_ok=True)
_lock = threading.Lock()
_tok = {"value": None, "at": 0.0}
_search_times: list[float] = []
SEARCH_PER_HOUR = int(os.environ.get("SEARCH_PER_HOUR", "450"))   # API allows 600/h per account


def token() -> str:
    with _lock:
        if STATIC_TOKEN:
            return STATIC_TOKEN
        if _tok["value"] and time.time() - _tok["at"] < 2400:
            return _tok["value"]
        req = urllib.request.Request(AUTH, data=json.dumps({"email": EMAIL, "password": PASSWORD}).encode(),
                                     headers={"apikey": ANON, "Content-Type": "application/json"}, method="POST")
        d = json.loads(urllib.request.urlopen(req, timeout=30).read())
        _tok.update(value=d["access_token"], at=time.time())
        return _tok["value"]


def pace_search():
    while True:
        with _lock:
            now = time.time()
            while _search_times and now - _search_times[0] > 3600:
                _search_times.pop(0)
            if len(_search_times) < SEARCH_PER_HOUR:
                _search_times.append(now)
                return
        time.sleep(5)


def call(method, path, body=None, auth=True, raw_token=None, timeout=240):
    hdr = {"Content-Type": "application/json"} if body is not None else {}
    if raw_token is not None:
        hdr["Authorization"] = raw_token
    elif auth:
        hdr["Authorization"] = "Bearer " + token()
    data = json.dumps(body).encode() if body is not None else None
    t = time.time()
    for attempt in range(3):
        try:
            r = urllib.request.urlopen(urllib.request.Request(API + path, data=data, headers=hdr, method=method), timeout=timeout)
            txt = r.read().decode("utf-8", "replace")
            try:
                return r.status, json.loads(txt), round((time.time() - t) * 1000)
            except Exception:
                return r.status, txt[:3000], round((time.time() - t) * 1000)
        except urllib.error.HTTPError as e:
            txt = e.read().decode("utf-8", "replace")[:3000]
            if e.code in (502, 503, 504) and attempt < 2:
                time.sleep(5 * (attempt + 1)); continue
            try:
                return e.code, json.loads(txt), round((time.time() - t) * 1000)
            except Exception:
                return e.code, txt, round((time.time() - t) * 1000)
        except Exception as e:
            if attempt < 2:
                time.sleep(5 * (attempt + 1)); continue
            return 0, f"{type(e).__name__}: {e}", round((time.time() - t) * 1000)


def trim(resp, n=25):
    if isinstance(resp, dict):
        r = dict(resp)
        for k in ("players", "similar_players", "results", "candidates"):
            if isinstance(r.get(k), list):
                r[k] = r[k][:n]
        if isinstance(r.get("gaps"), list):
            r["gaps"] = [dict(g, top_candidates=(g.get("top_candidates") or [])[:5]) for g in r["gaps"]]
        s = json.dumps(r, ensure_ascii=False, default=str)
        return r if len(s) < 120000 else {"_truncated": True, "head": s[:120000]}
    return resp


def record(rec):
    with _lock, open(OUT, "a") as f:
        f.write(json.dumps(rec, ensure_ascii=False, default=str) + "\n")


def run(req, phase):
    if req["path"].startswith(("/api/search",)) and req.get("method") == "POST":
        pace_search()
    st, resp, ms = call(req.get("method", "GET"), req["path"], req.get("body"),
                        auth=req.get("auth", True), raw_token=req.get("raw_token"))
    rec = {"phase": phase, "id": req.get("id"), "tag": req.get("tag"), "method": req.get("method", "GET"),
           "path": req["path"], "body": req.get("body"), "note": req.get("_note"), "status": st, "ms": ms, "resp": trim(resp)}
    record(rec)
    return rec


def run_many(reqs, phase, conc=4):
    print(f"== {phase}: {len(reqs)} requests", flush=True)
    with ThreadPoolExecutor(conc) as ex:
        out = list(ex.map(lambda r: run(r, phase), reqs))
    bad = sum(1 for r in out if not (200 <= r["status"] < 300))
    print(f"   done: {len(out) - bad} ok, {bad} not-2xx", flush=True)
    return out


def main():
    plan = json.load(open(os.environ.get("PLAN") or os.path.join(os.path.dirname(__file__), "plan.json")))
    random.seed(7)
    # 1. security (no AI cost)
    forged = "Bearer eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ4IiwiZW1haWwiOiJ4QHguY29tIiwiZXhwIjo5OTk5OTk5OTk5fQ.c2lnbmF0dXJl"
    sec = [
        {"id": "sec-anon-stats", "tag": "expect-401", "path": "/api/stats", "auth": False},
        {"id": "sec-anon-search", "tag": "expect-401", "method": "POST", "path": "/api/search", "body": {"prompt": "striker"}, "auth": False},
        {"id": "sec-forged", "tag": "expect-401", "path": "/api/leagues", "raw_token": forged},
        {"id": "sec-docs", "tag": "expect-404", "path": "/docs", "auth": False},
        {"id": "sec-openapi", "tag": "expect-404", "path": "/openapi.json", "auth": False},
        {"id": "sec-admin-with-user-token", "tag": "expect-401/403", "path": "/api/admin/users"},
        {"id": "sec-agent-patch", "tag": "expect-401/403", "method": "PATCH", "path": "/api/players/1/agent?agent_email=x@example.com"},
        {"id": "sec-health", "tag": "expect-200", "path": "/api/health", "auth": False},
    ]
    run_many(sec, "security", conc=2)
    # 2. account + meta
    meta = [{"id": f"meta-{i}", "tag": "meta", "path": p} for i, p in enumerate(
        ["/api/auth/me", "/api/stats", "/api/leagues", "/api/archetypes", "/api/formations", "/api/squad-gap/formations",
         "/api/suggest?q=strik", "/api/suggest?q=bellingham", "/api/settings?session_id=live-test", "/api/reports",
         "/api/contact-requests", "/api/players?limit=5"])]
    run_many(meta, "meta", conc=3)
    # 3. searches (paced) + name/team lookups
    srch = run_many(plan["search"], "search", conc=4)
    run_many(plan["lookup"], "lookup", conc=4)
    # players seen in results -> detail sweep
    seen = {}
    for r in srch:
        if r["status"] == 200 and isinstance(r["resp"], dict):
            for p in (r["resp"].get("players") or [])[:3]:
                if p.get("sportmonks_id"):
                    seen[p["sportmonks_id"]] = p
    ids = random.sample(sorted(seen), min(40, len(seen)))
    detail = []
    for sid in ids:
        for suffix in ("rankings", "strengths-weaknesses", "similar", "injuries", "career", "age-curve"):
            detail.append({"id": f"detail-{sid}-{suffix}", "tag": f"detail-{suffix}", "path": f"/api/players/{sid}/{suffix}"})
    run_many(detail, "player-detail", conc=4)
    run_many(plan["similar"], "similar", conc=4)
    run_many(plan["outliers"], "outliers", conc=3)
    # refine: reuse real result sets from this run
    sets = [[p["sportmonks_id"] for p in (r["resp"].get("players") or [])] for r in srch
            if r["status"] == 200 and isinstance(r["resp"], dict) and len(r["resp"].get("players") or []) >= 10]
    refine = []
    for i, fu in enumerate(plan["refine_followups"]):
        if sets:
            refine.append({"id": f"refine-{i}", "tag": "refine", "method": "POST", "path": "/api/search/refine",
                           "body": {"player_ids": sets[i % len(sets)], "follow_up": fu}})
    run_many(refine, "refine", conc=3)
    # 4. AI features (capped)
    reports = plan["reports"] + [{"id": f"report-seen-{sid}", "tag": "scouting-report", "path": f"/api/players/{sid}/scouting-report"}
                                 for sid in ids[:3]]
    run_many(reports, "reports", conc=2)
    run_many(plan["help"], "help", conc=2)
    fit = []
    for sid in ids[:4]:
        p = seen[sid]
        fit.append({"id": f"fit-{sid}", "tag": "fit-note", "method": "POST", "path": "/api/generate-fit-note",
                    "body": {"candidate": p, "position_group": p.get("position_group") or p.get("position") or "Central Mid",
                             "squad": [], "weak_stats": [{"label": "Key Passes/90"}]}})
    run_many(fit, "fit-note", conc=2)
    ins = [{"id": f"ins-{sid}", "tag": "outlier-insight", "method": "POST", "path": "/api/outliers/insight",
            "body": {"player": seen[sid], "stat_percentile": 0.85, "mv_percentile": 0.3}} for sid in ids[4:6]]
    run_many(ins, "outlier-insight", conc=2)
    # squad gap: prepared requests + full XIs built from real squads
    forms = call("GET", "/api/formations")[1]
    forms = forms.get("formations", forms) if isinstance(forms, dict) else {}
    sg = list(plan["squad_gap"])
    for team in plan["full_xi_teams"]:
        st, players, _ = call("GET", "/api/teams/" + urllib.request.quote(team) + "/players")
        if isinstance(players, dict):
            players = [q for grp in (players.get("by_position") or {}).values() for q in grp]
        if st != 200 or not isinstance(players, list) or "4-3-3 (Attack)" not in forms:
            continue
        slots = forms["4-3-3 (Attack)"]["positions"]
        pool = sorted(players, key=lambda p: -(p.get("minutes_played") or 0))
        used, assign = set(), {}
        for s in slots:
            want = s.get("position_group")
            c = [p for p in pool if p.get("sportmonks_id") not in used and (p.get("position_group") == want)] or \
                [p for p in pool if p.get("sportmonks_id") not in used]
            if c:
                used.add(c[0]["sportmonks_id"]); assign.setdefault(want, []).append(c[0]["sportmonks_id"])
        for objective, drop_striker in (("starter", False), ("starter", True)):
            a = {k: list(v) for k, v in assign.items()}
            vacant = []
            if drop_striker and a.get("Striker"):
                a["Striker"] = []; vacant = ["Striker"]
            sg.append({"id": f"sg-xi-{team}-{'open-st' if drop_striker else 'full'}", "tag": "squad-gap-full-xi",
                       "method": "POST", "path": "/api/squad-gap",
                       "body": {"formation": "4-3-3 (Attack)", "squad_player_ids": [i for v in a.values() for i in v],
                                "squad_assignments": a, "vacant_position_groups": vacant, "recruitment_objective": objective}})
    run_many(sg, "squad-gap", conc=2)
    # 5. user data round trips (test account only)
    sess = "live-test-" + STAMP
    st, sq, _ = call("POST", "/api/squads", {"session_id": sess, "name": "Live test squad", "formation": "4-3-3 (Attack)",
                                             "slots": [{"position_group": "Striker", "sportmonks_id": ids[0] if ids else None}]})
    record({"phase": "user-data", "id": "squad-create", "status": st, "resp": sq})
    sid = sq.get("id") if isinstance(sq, dict) else None
    ud = [{"id": "squad-list", "tag": "squads", "path": f"/api/squads?session_id={sess}"},
          {"id": "settings-patch", "tag": "settings", "method": "PATCH", "path": "/api/settings",
           "body": {"session_id": sess, "default_min_minutes": 600}},
          {"id": "events-log", "tag": "events", "method": "POST", "path": "/api/events/log",
           "body": {"event_type": "search", "payload": {"source": "live-test"}}},
          {"id": "watchlist-alerts", "tag": "watchlist", "method": "POST", "path": "/api/watchlist/alerts",
           "body": {"items": [{"sportmonks_id": i, "player_name": seen[i].get("name"), "market_value": seen[i].get("market_value")} for i in ids[:10]]}}]
    if sid:
        ud += [{"id": "squad-get", "tag": "squads", "path": f"/api/squads/{sid}?session_id={sess}"},
               {"id": "squad-get-wrong-session", "tag": "expect-403/404", "path": f"/api/squads/{sid}?session_id=someone-else"},
               {"id": "squad-delete", "tag": "squads", "method": "DELETE", "path": f"/api/squads/{sid}?session_id={sess}"}]
    run_many(ud, "user-data", conc=1)
    # summary
    rows = [json.loads(l) for l in open(OUT)]
    summ = {}
    for r in rows:
        s = summ.setdefault(r["phase"], {"n": 0, "ok": 0, "statuses": {}, "ms": []})
        s["n"] += 1; s["ok"] += 200 <= (r.get("status") or 0) < 300
        s["statuses"][str(r.get("status"))] = s["statuses"].get(str(r.get("status")), 0) + 1
        s["ms"].append(r.get("ms") or 0)
    for s in summ.values():
        ms = sorted(s.pop("ms")); s["p50_ms"] = ms[len(ms) // 2] if ms else 0; s["p95_ms"] = ms[int(len(ms) * 0.95)] if ms else 0
    json.dump(summ, open(f"results/live-{STAMP}-summary.json", "w"), indent=1)
    print(json.dumps(summ, indent=1))
    for ph, s in summ.items():
        print(f"::notice::{ph}: {s['ok']}/{s['n']} ok, statuses {s['statuses']}, p50 {s['p50_ms']} ms")


if __name__ == "__main__":
    main()
