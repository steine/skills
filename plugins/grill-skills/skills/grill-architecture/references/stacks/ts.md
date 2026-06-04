# Stack pack: TypeScript / front-end (language pack)

The grill-architecture spine carries each lens's *principle*; this pack carries the **TypeScript/SPA-idiom tells** that hold regardless of UI framework. Load it when recon detects `tsconfig.json` / a `package.json` with a front-end toolchain (Vite, webpack, Next, Angular CLI). It is the **language pack** — compose it with a framework overlay:

- `react`/`react-dom` in deps → also load [react.md](./react.md)
- `@angular/core` in deps → also load [angular.md](./angular.md)

(Implementation-altitude tells — reuse, read-path minimalism, spec-gaps, impact sweep, contract drift — live in grill-implementation's own `references/stacks/ts.md`.)

The universal concerns (transport boundary, domain logic, server/client state, DTO placement, shared-package boundary, feature-slice folders) live here. The framework overlay carries the **view-logic layer** idiom — React custom-hooks vs Angular services + DI + facades — plus naming/port-shape/return-shape tells for that layer.

## Re-anchored layering vocabulary

A front-end has no `Domain ← Application ← Infrastructure` stack; it has an implicit downward-only layering (dependencies point down; features never import features; shared never imports features):

`Presentation (components/templates)` ← `View-logic (hooks / services+facades)` ← `State: server-state cache / client-state` ← `Domain (pure framework-free modules)` ← `Transport boundary (typed + runtime-validated client)` ← `Shared / foundation (design system, config, utils)`

Run each spine lens, then apply the matching section. Mark a lens `N/A` (with a one-liner) rather than force-fit a deliberately flat app.

## Naming vs responsibility

- A module/type named for **where it lives or who calls it** rather than its role.
- A `…Dto` / `…Response` (wire shape) used directly as the in-app domain type — transport vocabulary leaking inward; map it to a domain type at the boundary.
- A data-access unit named for the transport verb (`fetchOrders`) when siblings name for the resource/role — inconsistent access vocabulary across the feature.
- View-logic naming (query vs imperative-thunk hook; service vs facade) → **framework overlay**.

## Folder placement

- By-kind top-level buckets (`components/`, `hooks/`, `utils/` holding *everything*) in a feature-organised repo — you can't tell what the app does from the tree.
- An **off-convention island**: a feature missing the dominant `api` / `model` / `ui` segments its siblings share, or inventing its own data-fetching pattern while every other feature uses the shared one.
- A feature importing another feature's internals instead of its public `index.ts`.
- `shared` / foundation importing **from** a feature (upward dependency — inverts the layering).
- Sample 2–3 sibling features; count the dominant segment layout and match it.

## Layer assignment

- **Business/domain logic inline in presentation** — branching rules, money/date math, filtering/sorting computed inside component markup instead of a pure module the component calls. Pure logic should be unit-testable without rendering.
- **Server state copied into client state** — server data synced into local/store state via an effect or success-callback. Defeats the cache: a background refetch won't update the copy. Server-state (a borrowed, stale-while-revalidate snapshot) and app-owned client state are **different layers** — keep them separate.
- A view-logic unit (hook/service) that is really a dumping ground of framework-free domain logic — it should delegate to a pure module.
- A domain rule duplicated across several components instead of one shared pure function.
- View-logic mechanism (hooks vs services+DI+facades) → **framework overlay**.

## Value-type placement

- A hand-written type **mirroring a server contract** used as the domain type across the app — wire shape and domain shape should be distinct; map at the transport boundary (see *Cross-service transport*).
- A type shared across features sitting in one feature's `types/` — hoist to a shared/entities home.
- A persisted/enumerated domain concept hand-rolled as ad-hoc string unions in several features vs one shared type.
- A **feature/domain concept leaked into the shared package** — a "primitive" component that knows a domain entity, calls an API, or reads a feature store. Shared = business-agnostic only.

## Port shape

Universal part of the data-access contract (framework return-shape idiom → overlay):

- Distinguishes **expected absence** (empty/`null`) from **failure** (error) — not one opaque `null` for both.
- **Cancellation/abort** of in-flight requests on unmount or argument change (`AbortSignal`).
- **Idempotency / dedupe** semantics for mutations that change server state.
- A surfaced **error and loading** state, not a swallowed `catch {}`.

## Config and secret flow

- Env vars read ad-hoc deep in modules (`import.meta.env.X` / `process.env.X`) vs one validated config module.
- **Non-null-asserting (`!`) an env or token read that can genuinely be absent** — masks a real null (e.g. an auth token that can fail to resolve, then ships `Bearer null`).
- Build-time public config (`VITE_*` / `NG_*`) co-mingled with anything secret — **front-end bundles ship to the client; no real secret belongs in one**. Secrets stay server-side.
- Auth/SDK config (MSAL, OAuth client) duplicated per app instead of a shared config factory.

## Cross-service transport — the network boundary

The front-end's one "service hop" is the call to its backend. This is the **hard-to-reverse strategy** for crossing the network edge:

- **Type source:** generated from the server contract (OpenAPI → `openapi-typescript` / `orval`) vs hand-written types. Hand-mirroring drifts the moment the backend changes.
- **Runtime validation:** parse responses at the edge (`zod` `safeParse`) vs trusting `(await res.json()) as T`. The cast is **a lie the compiler believes** — a renamed or omitted field is `undefined` at runtime with green CI. Validate once at the boundary so internal code works with verified data.
- **Contract ownership:** generated-from-spec (single source of truth) vs hand-mirrored (a contract two repos must edit in lockstep).
- **One client vs scattered boilerplate:** a shared client/interceptor owning auth header, base URL, and error mapping vs the same fetch block copy-pasted across call sites.

Failure-mode ladder, best → worst: compile error (generated types) > runtime parse error (zod at the edge) > silent `undefined` (`as T`). Default new apps to generated-types + edge-validation; never hand-mirror by default.

This lens sets the **strategy** (set once, ADR-worthy). The **per-slice conformance** check — a slice changed a server VM and the hand-mirror now lies — is grill-implementation's *Cross-boundary contract drift* lens, which inherits this decision.
