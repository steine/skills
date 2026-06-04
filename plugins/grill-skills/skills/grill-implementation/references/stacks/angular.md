# Implementation pack overlay: Angular — STUB

> **Status: stub.** Seeded with real tells so the structure is visible, not battle-tested. Fill from real Angular grills before relying on it; mark a tell `N/A` if the app doesn't adopt the pattern.

**Overlay — load *with* [ts-web.md](./ts-web.md), not instead of it.** Triggered when `@angular/core` is in deps. `ts-web.md` carries the universal impl tells; this overlay carries Angular's view-logic slice-mechanics.

(Architecture-altitude Angular tells live in grill-architecture's own `references/stacks/angular.md`.)

- **Reuse:** a bespoke service method duplicating an existing facade stream / shared data-access service. <!-- TODO -->
- **Read-path:** fetch-all-then-filter in a component vs server query params; duplicate HTTP calls instead of a `shareReplay()`-cached facade stream. <!-- TODO -->
- **Spec-gap:** unsubscription / `takeUntilDestroyed` teardown; `switchMap` cancelling the prior request; idempotency on state-changing calls. <!-- TODO -->
- Observable return/error shape is an architecture concern → grill-architecture's angular overlay *Port shape*. <!-- TODO -->
