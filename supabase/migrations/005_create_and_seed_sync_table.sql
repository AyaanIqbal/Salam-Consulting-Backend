create table if not exists sync_state (
  source text primary key,
  last_synced_at timestamptz null
);

insert into sync_state (source, last_synced_at)
values ('wix_contacts', null)
on conflict (source) do nothing;

insert into sync_state (source, last_synced_at)
values ('wix_orders', null)
on conflict (source) do nothing;