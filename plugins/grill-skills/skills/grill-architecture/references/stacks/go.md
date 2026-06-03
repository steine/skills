# Stack pack: Go — STUB

> **Status: stub.** Seeded with a few real tells per lens so the structure (and the bite) is visible, but not yet battle-tested. Fill in from real Go-codebase grills before relying on it; mark a lens `N/A` if the target codebase is deliberately flat. See `dotnet.md` for the worked reference.

Layering note: Go favors small packages and consumer-defined interfaces over a formal Domain/Application/Infrastructure stack. Many services are deliberately flat-by-package. Apply the layering lenses only where the codebase has adopted boundaries; otherwise the lens collapses to package-boundary hygiene — say so.

## Naming vs responsibility

- **Interface defined producer-side** in the transport package instead of at the consumer — Go idiom is the consumer declares the small interface it needs. The transport-y `Client` name living in the domain package is the smell; prefer a consumer-side capability interface (`OrderRefReader`).
- Stuttering names (`fulfillment.FulfillmentClient`). <!-- TODO -->

## Folder placement

- A `models/` or `services/` by-kind package in a domain-package repo (Go prefers package-by-feature/domain). <!-- TODO: dominant-convention detection -->
- `internal/` boundary misuse — exporting what should be internal. <!-- TODO -->

## Layer assignment

- One struct's method doing HTTP + mapping + persistence. <!-- TODO -->
- Business policy in the HTTP handler instead of a domain service. <!-- TODO -->

## Value-type placement

- A typed enum (`type Status int` + `iota`) backing persisted state placed in the transport/handler package rather than the domain package. <!-- TODO -->
- A shared value concept duplicated across packages vs a single domain type. <!-- TODO -->

## Port shape

- Cancellation/deadline idiom: **`context.Context` as the first parameter** of every call that crosses a boundary (the Go analogue of `CancellationToken`). Flag boundary calls missing it.
- Return: `(T, error)` with wrapped errors (`fmt.Errorf("...: %w", err)`) vs swallowing; distinguish not-found from transport failure via sentinel/typed errors. <!-- TODO -->

## Config and secret flow

- Config read via `os.Getenv` scattered through packages vs a single parsed config struct injected from `main`. <!-- TODO -->
- Secrets in checked-in config vs env / secret manager. <!-- TODO -->

## Cross-service transport

- Hand-built URL strings in an `http.Client` call; no shared contract. Failure-mode ladder: a shared module type (compile error on both sides) > generated client > runtime. <!-- TODO: contract-location options in a Go monorepo / shared module -->
