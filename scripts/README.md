# Market Value Sync

Refreshes every player's `market_value` in Supabase from Transfermarkt, and
stores a `transfermarkt_id` + `club` so duplicate names don't cross-contaminate
and future runs are exact.

## How it works

1. **Linked players** (have a `transfermarkt_id`): one exact `/market_value`
   call → update the value.
2. **Unlinked players**: search Transfermarkt by name, disambiguate against the
   club we already hold, and on a confident match store the `transfermarkt_id` +
   club. Next run they're in the fast path above.
3. **Ambiguous / no match**: value left untouched, player written to
   `mv_review.json` (uploaded as a workflow artifact) for manual review. The
   sync never guesses a value.

## One-time setup

1. **Run the migration** (`scripts/migrations/001_add_transfermarkt_columns.sql`)
   in the Supabase SQL editor to add `transfermarkt_id` + `tm_synced_at`.
2. **Confirm the column mapping** at the top of `sync_market_values.py` matches
   the real `players` schema.
3. **Add GitHub secrets** (Settings → Secrets → Actions):
   - `SUPABASE_URL`, `SUPABASE_SERVICE_KEY` (already used by the old workflow)
   - `TM_API_BASE_URL` — your transfermarkt-api instance, e.g.
     `https://transfermarkt-api.fly.dev` (public, rate-limited) or your own.

## Running

- **Manually**: Actions → *Monthly Market Value Sync* → *Run workflow*. Start
  with `dry_run: true` and `limit: 50` to sanity-check matches, then run for
  real. Download the `mv-review-report` artifact to see skips.
- **Scheduled**: automatically at 03:00 UTC on the 1st of each month.

## Tests

`python scripts/test_matching.py` — offline tests for value parsing and the
duplicate-name disambiguation. No network/DB needed.
