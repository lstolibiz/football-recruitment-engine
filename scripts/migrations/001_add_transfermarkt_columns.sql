-- Adds the sync bookkeeping column the market-value sync writes.
-- `transfermarkt_id`, `name`, `team_name`, `market_value` already exist on the
-- players table, so only `tm_synced_at` is new here.
-- Safe to run repeatedly (IF NOT EXISTS). Run once in the Supabase SQL editor.

alter table public.players
  add column if not exists tm_synced_at timestamptz;

-- Fast lookups on the TM id once players are linked.
create index if not exists players_transfermarkt_id_idx
  on public.players (transfermarkt_id);
