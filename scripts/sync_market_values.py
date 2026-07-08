"""
Sync every player's market value from Transfermarkt.

Flow per player:
  * Already linked (has transfermarkt_id): exact /market_value lookup -> update.
  * Not linked yet: search by name, disambiguate by club, and on a confident
    match store the transfermarkt_id + club so future runs are exact.
  * Ambiguous / no match: leave the value untouched and write the player to a
    review report (never guess a value).

Because the transfermarkt_id is persisted on first confident match, the run is
resumable and cheap after the initial pass.

Environment:
  SUPABASE_URL           (required)  your Supabase project URL
  SUPABASE_SERVICE_KEY   (required)  service-role key (server-side only)
  TM_API_BASE_URL        (required)  base URL of your transfermarkt-api instance
  TM_DELAY               (optional)  seconds between TM calls (default 0.5)
  SYNC_LIMIT             (optional)  cap number of players processed (testing)
  DRY_RUN                (optional)  "1" = compute + report, write nothing
"""

from __future__ import annotations

import json
import os
import sys
import time
from datetime import datetime, timezone

from supabase import create_client

from matching import match_player
from tm_client import TransfermarktClient

# ============================================================================
# COLUMN MAPPING  —  the ONLY thing to confirm against your real schema.
# Defaults are inferred from the app's `pipeline` table + frontend Player type.
# Adjust the right-hand strings to match `players` exactly, then this runs.
# ============================================================================
TABLE = "players"
COL_PK = "id"                       # primary key used for updates
COL_NAME = "name"                   # player full name
COL_CLUB = "team_name"              # current club (used to disambiguate)
COL_MARKET_VALUE = "market_value"   # numeric euros — the column we update
COL_TM_ID = "transfermarkt_id"      # existing column; cached TM player id
# Optional: set to None if you don't want a per-row sync timestamp written.
COL_TM_SYNCED_AT = "tm_synced_at"
# ============================================================================

PAGE_SIZE = 1000
REVIEW_PATH = os.environ.get("REVIEW_PATH", "mv_review.json")


def env(name: str, required: bool = True, default: str | None = None) -> str | None:
    val = os.environ.get(name, default)
    if required and not val:
        sys.exit(f"Missing required env var: {name}")
    return val


def fetch_all_players(sb) -> list[dict]:
    """Page through the whole players table."""
    cols = [COL_PK, COL_NAME, COL_CLUB, COL_MARKET_VALUE, COL_TM_ID]
    select = ",".join(dict.fromkeys(cols))  # de-dupe, keep order
    rows: list[dict] = []
    start = 0
    while True:
        resp = (
            sb.table(TABLE)
            .select(select)
            .range(start, start + PAGE_SIZE - 1)
            .execute()
        )
        batch = resp.data or []
        rows.extend(batch)
        if len(batch) < PAGE_SIZE:
            break
        start += PAGE_SIZE
    return rows


def main() -> int:
    supabase_url = env("SUPABASE_URL")
    service_key = env("SUPABASE_SERVICE_KEY")
    tm_base = env("TM_API_BASE_URL")
    delay = float(env("TM_DELAY", required=False, default="0.5"))
    limit = env("SYNC_LIMIT", required=False)
    dry_run = env("DRY_RUN", required=False, default="0") == "1"

    sb = create_client(supabase_url, service_key)
    players = fetch_all_players(sb)
    if limit:
        players = players[: int(limit)]

    print(f"Loaded {len(players)} players. dry_run={dry_run}", flush=True)

    stats = {
        "total": len(players),
        "updated": 0,
        "linked": 0,      # newly matched to a TM id this run
        "exact": 0,       # updated via cached TM id
        "unchanged": 0,
        "skipped": 0,
        "errors": 0,
    }
    review: list[dict] = []

    with TransfermarktClient(tm_base, delay=delay) as tm:
        for i, p in enumerate(players, 1):
            pk = p.get(COL_PK)
            name = p.get(COL_NAME)
            club = p.get(COL_CLUB)
            tm_id = p.get(COL_TM_ID)
            old_value = p.get(COL_MARKET_VALUE)

            if not name:
                stats["skipped"] += 1
                review.append({"id": pk, "reason": "missing_name"})
                continue

            try:
                if tm_id:
                    new_value = tm.market_value(str(tm_id))
                    matched_club = club
                    outcome = "exact"
                else:
                    candidates = tm.search(name)
                    result = match_player(name, club, candidates)
                    if not result.candidate:
                        stats["skipped"] += 1
                        review.append(
                            {"id": pk, "name": name, "club": club,
                             "reason": result.reason,
                             "candidates": [
                                 {"tm_id": c.tm_id, "name": c.name,
                                  "club": c.club_name, "mv": c.market_value}
                                 for c in candidates[:5]
                             ]}
                        )
                        continue
                    cand = result.candidate
                    tm_id = cand.tm_id
                    matched_club = cand.club_name or club
                    new_value = cand.market_value
                    outcome = "linked"
            except Exception as e:  # noqa: BLE001 — never let one player kill the run
                stats["errors"] += 1
                review.append({"id": pk, "name": name, "reason": f"error: {e}"})
                continue

            if new_value is None:
                stats["skipped"] += 1
                review.append({"id": pk, "name": name, "club": club,
                               "reason": "no_market_value_from_tm"})
                continue

            update: dict = {COL_MARKET_VALUE: new_value}
            if COL_TM_ID:
                update[COL_TM_ID] = tm_id
            if COL_CLUB and matched_club:
                update[COL_CLUB] = matched_club
            if COL_TM_SYNCED_AT:
                update[COL_TM_SYNCED_AT] = datetime.now(timezone.utc).isoformat()

            changed = new_value != old_value
            if not dry_run:
                sb.table(TABLE).update(update).eq(COL_PK, pk).execute()

            stats[outcome] += 1
            if changed:
                stats["updated"] += 1
            else:
                stats["unchanged"] += 1

            if i % 250 == 0:
                print(f"  {i}/{len(players)}  {json.dumps(stats)}", flush=True)

    stats["skipped_review_count"] = len(review)
    print("DONE:", json.dumps(stats, indent=2), flush=True)

    with open(REVIEW_PATH, "w", encoding="utf-8") as f:
        json.dump(
            {"generated_at": datetime.now(timezone.utc).isoformat(),
             "stats": stats, "review": review},
            f, ensure_ascii=False, indent=2,
        )
    print(f"Review report ({len(review)} players) -> {REVIEW_PATH}", flush=True)
    return 0


if __name__ == "__main__":
    start = time.time()
    code = main()
    print(f"Elapsed: {time.time() - start:.0f}s", flush=True)
    sys.exit(code)
