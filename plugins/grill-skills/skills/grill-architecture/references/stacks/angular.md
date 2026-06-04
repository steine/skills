# Stack pack overlay: Angular — STUB

> **Status: stub.** Seeded with real Angular tells per lens so the structure (and the bite) is visible, but not battle-tested. Fill in from real Angular-codebase grills before relying on it; mark a lens `N/A` if the target app doesn't adopt the relevant pattern. See [react.md](./react.md) for the worked overlay shape.

**Overlay — load *with* [ts-web.md](./ts-web.md), not instead of it.** Triggered when `@angular/core` is in deps. `ts-web.md` carries the universal layers (transport, domain, server/client state, DTO placement, shared-package, folders); this overlay carries Angular's **view-logic layer** and the per-lens tells `ts-web.md` defers.

Angular's view-logic layer is **services + dependency injection**, often fronted by **facades**. The common reference model is three layers: **Core** (state, API services, business logic), **Abstraction / Facade** (exposes observable streams + methods, hides implementation, owns optimistic/pessimistic sync and `shareReplay()` caching), **Presentation** (components display + delegate up). Cross-feature state between sibling lazy features is forbidden — extract to `core/`. ([Dev-Academy — Angular Architecture Best Practices](https://dev-academy.com/angular-architecture-best-practices/).)

## Naming vs responsibility

- A `…Service` that's really several responsibilities — transport + domain mapping + state — instead of split Core service / Facade. The god-service is the Angular analogue of the god-class. <!-- TODO: facade-vs-service naming tells -->
- A transport-shaped service name (`…ApiService`) exposed to components directly instead of behind a capability facade. <!-- TODO -->

## Layer assignment — the view-logic tells

- **Business logic in components** instead of services — *"all business rules, decision-making, and data operations should be placed in services."* The component should display and delegate.
- **Nested `.subscribe()`** instead of composing streams with RxJS operators (`switchMap`/`combineLatest`) + the `async` pipe — manual subscription management is the smell.
- **Manual `.subscribe()` with no teardown** (pre-`takeUntilDestroyed`) — a subscription leak; or state held in component fields that a facade stream should own. <!-- TODO: signals-era tells (signal vs observable state) -->
- **Server state copied into component fields / a `BehaviorSubject`** kept in sync by hand, when a facade + cache (`shareReplay`) or `@tanstack/angular-query` should own it. <!-- TODO -->
- Smart/dumb split ignored — a presentational component reaching into a store/service instead of taking `@Input()` / emitting `@Output()`. <!-- TODO -->

## Port shape — the service/facade contract

- Return shape: `Observable<T>` with a distinct error channel, not a swallowed error; expected-absence vs failure distinguished. <!-- TODO -->
- **Cancellation idiom:** RxJS unsubscription / `switchMap` cancelling the prior inner request — the Angular analogue of an abort signal. Flag boundary calls with no cancellation path. <!-- TODO -->
- Idempotency/dedupe for state-changing operations. <!-- TODO -->

## Config and secret flow

- Config via an `InjectionToken` provided at the root, or `environment.ts`, not read ad-hoc deep in services. <!-- TODO -->
- Build-time public config only in the bundle; no real secret in `environment.*.ts` (it ships to the client). <!-- TODO -->

## Value-type placement

Covered by `ts-web.md` (DTO/type home, shared-vs-feature, feature-leak-into-shared). No Angular-specific tell unless the slice introduces a shared `InjectionToken`/module that has leaked a domain concept. <!-- TODO: NgModule vs standalone boundary tells -->

## State management (NgRx, if adopted)

- Server responses living in the NgRx store as the source of truth instead of a server-cache — the store is client state; borrowed server data belongs in a cache layer. <!-- TODO -->
- Business logic in components/effects instead of selectors + services. <!-- TODO: actions/reducers/selectors/effects placement tells -->

(Implementation-altitude Angular tells live in grill-implementation's own `references/stacks/angular.md`.)
