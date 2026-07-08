-- Adds the columns the market-value sync relies on.
-- Safe to run repeatedly (IF NOT EXISTS). Run once in the Supabase SQL editor
-- (or via the CLI) before the first sync.
--
-- NOTE: adjust the table name if `players` differs in your schema.

alter table public.players
  add column if not exists transfermarkt_id text,
  add column if not exists tm_synced_at timestamptz;

-- Fast lookups / dedupe on the TM id once players are linked.
create index if not exists players_transfermarkt_id_idx
  on public.players (transfermarkt_id);

-- If your table has no `club` column yet, uncomment to add one:
-- alter table public.players add column if not exists club text;
