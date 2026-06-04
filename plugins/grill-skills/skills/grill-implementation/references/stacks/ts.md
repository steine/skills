# Implementation pack: TypeScript / front-end (language pack)

The grill-implementation spine carries each lens's *principle*; this pack carries the **TypeScript/SPA-idiom tells** for the implementation lenses — independent of UI framework. Load it when recon detects `tsconfig.json` / a front-end `package.json`. It is the **language pack** — compose with a framework overlay:

- `react`/`react-dom` in deps → also load [react.md](./react.md)
- `@angular/core` in deps → also load [angular.md](./angular.md)

(Architecture-altitude tells live in grill-architecture's own `references/stacks/ts.md`.)

## Reuse affordances

- A hand-rolled fetch / auth-header / error block when a shared http client (or `apiFetch` wrapper) already exists — or *should*: repeated boilerplate across call sites is the tell that the affordance is missing.
- An inline data transform duplicating a pure util / domain function that already names the rule.
- A bespoke fetch hook when a shared query hook / query-options factory already covers the same read.
- A shared affordance (util, client, hook) with zero call sites — use it or it's dead.

## Read-path minimalism

- Calling a fat endpoint (full payload) when the screen renders N of M fields → leaner endpoint / field selection. Often a **blocker** (needs a backend change), not a slice-local fix.
- Fetching a whole collection then filtering / sorting / paginating **client-side** when the server supports query params → push it to the request (**slice-local**).
- Duplicate fetches of the same data across components instead of one shared query (over-fetch by duplication → query-key reuse; see the framework overlay's *Port shape*).
- `N/A` when the read is already lean or the endpoint shape is fixed upstream.

## Spec-gap checklist

- `AbortSignal` wired into `fetch`, cancelling on unmount / argument change.
- Error and loading states surfaced, not a swallowed `catch {}`.
- Injected clock / config rather than ambient `Date.now()` where determinism matters.
- Idempotency / dedupe for state-changing mutations.
- Cleanup of subscriptions / effects on unmount.
- Framework return-shape / hook-contract gaps → **overlay**.

## Impact sweep + contract drift

- The **hand-mirrored server DTO** (the `// Mirrors <Vm>` type) updated in lockstep with the server change — the `res.json() as T` cast hides drift. (Full lens: the SKILL's *Cross-boundary contract drift*.)
- A declared type the wire can't deliver — `Date` on an ISO-string field (so `<` sorts / `.getTime()` lie), an enum union for an int the server sends, a non-null field the server may omit.
- Components / selectors consuming the changed type.
- Query keys / cache entries keyed on the old shape.
- Generated-client regen, if codegen is in use.

## Cross-workspace dependency-graph compat

- A first-crossing import from a shared workspace lib → probe with `tsc -b` / build before signing off (see the SKILL's *Cross-workspace compat* + workspace-compat.md).
