# Implementation pack: Ruby / Rails — STUB

> **Status: stub.** Fill from real Rails grills; mark a tell `N/A` if the app doesn't adopt the pattern. See [dotnet.md](./dotnet.md) for the worked reference. (Architecture tells live in grill-architecture's own `references/stacks/ruby.md`.)

- **Reuse:** an open-coded scope/predicate duplicating an existing model scope or concern method. <!-- TODO -->
- **Read-path:** `.all`/full-record load when a few columns are read → `select`/`pluck`; N+1 without `includes`. <!-- TODO -->
- **Spec-gap:** unbounded external call (no `Timeout`/client timeout); idempotency on state-changing actions; error contract (raise vs result). <!-- TODO -->
- **Vacuous success:** `all?` is true on empty; `rescue => e` returning ok in a check or job; RSpec examples generated from a list that can come back empty; `and_raise(SomeError)` under `expect { }.to raise_error(SomeError)` — the rescue-and-wrap under test can be deleted and it stays green; model specs against sqlite while production is Postgres (collation, `ILIKE`, JSON operators). <!-- TODO -->
- **Impact sweep:** factories/fixtures, serializers/`as_json`, callbacks, migration + schema.rb, seeds with a hard-coded shape; **registration sites** for a non-type resource the slice adds (a job in `sidekiq.yml` / the cron schedule, an ENV key in `.env.example` and credentials, an alert rule in the doc that lists them) — grep the nearest sibling of that kind and match every file that names it. <!-- TODO -->
