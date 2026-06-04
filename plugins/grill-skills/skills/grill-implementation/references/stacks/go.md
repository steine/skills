# Implementation pack: Go — STUB

> **Status: stub.** Fill from real Go grills; mark a tell `N/A` if the package is deliberately flat. See [dotnet.md](./dotnet.md) for the worked reference. (Architecture tells live in grill-architecture's own `references/stacks/go.md`.)

- **Reuse:** an open-coded helper duplicating an existing package function / method. <!-- TODO -->
- **Read-path:** `SELECT *` / full-row scan when few columns are used; loading a slice to read one field. <!-- TODO -->
- **Spec-gap:** **`context.Context` first param** on every boundary call; `(T, error)` with wrapped errors; sentinel/typed not-found vs transport failure; idempotency. <!-- TODO -->
- **Impact sweep:** constructors/test fixtures, struct-literal call sites, mappers, migration, seed data. <!-- TODO -->
