# Implementation pack overlay: React

**Overlay — load *with* [ts-web.md](./ts-web.md), not instead of it.** Triggered when `react` / `react-dom` is in deps. `ts-web.md` carries the universal impl tells; this overlay carries React's view-logic slice-mechanics. Layer these on top of `ts-web.md`'s tells.

(Architecture-altitude React tells live in grill-architecture's own `references/stacks/react.md`.)

> **Legacy apps (React ≤16 / Redux-thunk / class components):** flag `status: legacy` and mark the modern tells below `N/A` rather than force-fitting — a pre-hooks/pre-TanStack app predates these patterns.

- **Reuse:** a bespoke fetch hook duplicating an existing shared query hook / query-options factory; query + auth + error hand-rolled in a hook instead of the shared client.
- **Read-path:** duplicate `useQuery` calls for the same data across components → reuse the **query key** (one cache entry), not a second fetch; fetch-all-then-filter inside the component → push to request params.
- **Spec-gap:** `AbortSignal` taken from the query's `signal` and passed into `fetch`; no manual `.subscribe`/teardown (the query lib owns it); state-changing mutations have `onMutate` + `onError` rollback.
- Return/loading/error shape of the hook is an architecture concern → grill-architecture's react overlay *Port shape*.
