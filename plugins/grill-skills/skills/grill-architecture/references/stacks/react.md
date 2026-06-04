# Stack pack overlay: React

**Overlay — load *with* [ts.md](./ts.md), not instead of it.** Triggered when `react` / `react-dom` is in deps. `ts.md` carries the universal layers (transport, domain, server/client state, DTO placement, shared-package, folders); this overlay carries React's **view-logic layer** and the per-lens tells `ts.md` defers. Run each spine lens, apply the `ts.md` section, then layer these React tells on top.

(Implementation-altitude React tells live in grill-implementation's own `references/stacks/react.md`.)

React's view-logic layer is the **custom hook**. There is no DI container — dependencies come via props/context/import. The framework imposes one hard rule the lenses lean on: **components and hooks must be pure** — idempotent during render, no side effects in render, props/state/context treated as immutable ([react.dev/reference/rules](https://react.dev/reference/rules/components-and-hooks-must-be-pure)).

> **Legacy apps (React ≤16 / Redux-thunk / class components):** flag `status: legacy` and mark the modern tells below `N/A` rather than force-fitting — a pre-hooks/pre-TanStack app has its own (un-pursued) conventions. Note it and skip; don't grill it against patterns it predates.

## Naming vs responsibility

- **Data-access hook name must signal its mechanism.** A cached, declarative query hook and an imperative one-shot fetch are different contracts — naming them alike (`useGetX` returning a query *and* `useFetchX` returning a bare async thunk, side by side) hides which is which. Divergent fetch idioms across features (most use cached query hooks; one feature hand-rolls `fetch` in a thunk) is the tell.
- A `use…`-named function with **no React dependency** (no state/effect/context/ref) — it's a pure module wearing a hook costume; move it to the domain layer (`ts.md`) and call it.

## Layer assignment — the view-logic tells

- **Business logic inline in JSX** (the fat component): branching rules, money/date math, an IIFE computing state inside the render return. Extract to a pure module (`ts.md` domain layer) the component calls — logic the component owns can't be unit-tested without rendering.
- **Server state copied into client state via the React idioms:** `onSuccess`/`useEffect(() => setX(data))` syncing query data into `useState`/a store. `onSuccess` fires on *every* background refetch; the copy goes stale. Read from the cache; don't mirror it.
- **God component** — one component doing fetching + mutation + derivation + orchestration + rendering. Count the hooks it calls, the state pieces it holds, the responsibilities. Split container (orchestration/data) from presentational (props-in/events-out) per Abramov.
- **Imperative `fetch` in a component or `useEffect`** with manual loading/error booleans — re-implements caching, dedup, and refetch the query layer already gives you.
- **Cross-cutting error/loading placement:** with app-wide `useSuspenseQuery`, a thrown query needs an **error boundary** at the route/app level — without one, any failed read white-screens. Suspense boundary owns the loading state. These are app/route-layer concerns, not per-component `try/catch`.
- **A single configured `QueryClient` at the app root** (staleTime/retry/gc defaults, a global error handler), not a bare `new QueryClient()` with no defaults and not a client per module.

## Port shape — the hook contract

- A query hook should expose the **library's own state** (`data` / `isPending` / `isError`), not a hand-rolled `{ loading, error }` that re-invents it.
- **Query keys:** array form, structured **generic → specific** (`['orders','list',{filters}]`, `['orders','detail',id]`), from a **per-feature key factory colocated with the queries** — not a global key file, not ad-hoc inline arrays. Hierarchical keys are what make fuzzy invalidation (`invalidate(['orders'])`) work; put state that changes the data *into the key* so refetch is automatic. (TkDodo — [effective-react-query-keys](https://tkdodo.eu/blog/effective-react-query-keys); the [query-options API](https://tkdodo.eu/blog/the-query-options-api) colocates key+fn — don't over-engineer a separate factory.)
- **Mutations:** pick `invalidateQueries` *or* `setQueryData` for a key — not both on the same key (a patch immediately thrown away). State-changing ops get optimistic update + rollback (`onMutate`/`onError`).
- **`AbortSignal`** from the query wired into `fetch`, so an unmount / arg-change cancels the in-flight request.

## Config and secret flow

- Auth/SDK providers (MSAL, OAuth) composed once at the app root via a shared config factory, not re-instantiated per feature. Env reads go through the validated config module (`ts.md`), not `import.meta.env.X!` scattered in components.

## Value-type placement

Covered by `ts.md` (DTO/type home, shared-vs-feature, feature-leak-into-shared). No React-specific tell — say `N/A` unless the slice introduces a React-shaped shared primitive (a context value, a render-prop contract) that has leaked a domain concept.
