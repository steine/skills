# Implementation pack: Ruby / Rails — STUB

> **Status: stub.** Fill from real Rails grills; mark a tell `N/A` if the app doesn't adopt the pattern. See [dotnet.md](./dotnet.md) for the worked reference. (Architecture tells live in grill-architecture's own `references/stacks/ruby.md`.)

- **Reuse:** an open-coded scope/predicate duplicating an existing model scope or concern method. <!-- TODO -->
- **Read-path:** `.all`/full-record load when a few columns are read → `select`/`pluck`; N+1 without `includes`. <!-- TODO -->
- **Spec-gap:** unbounded external call (no `Timeout`/client timeout); idempotency on state-changing actions; error contract (raise vs result). <!-- TODO -->
- **Impact sweep:** factories/fixtures, serializers/`as_json`, callbacks, migration + schema.rb, seeds with a hard-coded shape. <!-- TODO -->
