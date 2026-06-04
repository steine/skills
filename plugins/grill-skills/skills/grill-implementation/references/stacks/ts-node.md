# Implementation pack: TypeScript / Node back-end — STUB

> **Status: stub.** Seeded from framework idiom (NestJS-leaning), not yet battle-tested on a real grill. Fill from real Node-backend grills before relying on it; mark a tell `N/A` if the app doesn't adopt the pattern. See [dotnet.md](./dotnet.md) for the worked reference — a Node back-end's mechanics track .NET far more than the front-end `ts-web.md`.

Load when recon detects `tsconfig.json` + Node-server deps (`@nestjs/*` / `express` / `fastify` / `koa`, an ORM like Prisma/TypeORM, **no DOM**). This is the **back-end** TypeScript stack — distinct from `ts-web.md`.

(Architecture-altitude tells live in grill-architecture's own `references/stacks/ts-node.md`.)

## Reuse affordances

- An inline query/predicate duplicating an existing repository method or domain-entity method. <!-- TODO -->
- A hand-rolled outbound HTTP call duplicating an existing typed client / provider. <!-- TODO -->
- A provider / pipe / guard with zero injectors or call sites — dead code. <!-- TODO -->
- Affordance idioms to grep: repository methods, domain-entity methods, shared providers, custom pipes/guards/decorators. <!-- TODO -->

## Read-path minimalism

- An ORM full-entity load when few columns are read → `select` projection (Prisma `select`, TypeORM `select`/QueryBuilder). <!-- TODO -->
- N+1 with no `relations` / eager join. <!-- TODO -->
- Loading a full relation to copy one scalar. <!-- TODO -->
- A read endpoint returning ORM entities when a projected DTO suffices. <!-- TODO -->

## Spec-gap checklist

- Cancellation/timeout on outbound calls (no `CancellationToken` — use `AbortController` / client timeout). <!-- TODO -->
- Error contract: thrown `HttpException` vs caught-and-mapped; which exception filter catches it. <!-- TODO -->
- Clock injected vs ambient `new Date()` / `Date.now()`. <!-- TODO -->
- Result exhaustive over outcomes incl. failure variants. <!-- TODO -->
- Resource disposal (DB handles, streams) — `onModuleDestroy` / lifecycle hooks. <!-- TODO -->
- Observability (`Logger`, metrics, traces). <!-- TODO -->
- Idempotency / dedupe on state-changing endpoints, and behaviour under retry. <!-- TODO -->
- Transaction boundary for multi-write operations. <!-- TODO -->

## Impact sweep + contract drift (producer side)

- Factories / fixtures / seeders constructing the entity. <!-- TODO -->
- All `new <Entity>()` / `repository.create` call sites. <!-- TODO -->
- Entity→DTO mappers. <!-- TODO -->
- **Response DTOs auto-serializing entity props** — a new column leaks outward to every consumer. This back-end is usually the **producer**: sweep the front-end's hand-mirror of this DTO (and any other service's). Codegen contract → regen; hand-mirrored downstream → a cross-repo contract to update in lockstep, flag as a blocker. <!-- TODO -->
- Migration (Prisma/TypeORM migrate) + schema. <!-- TODO -->
- Seed data with a hard-coded shape. <!-- TODO -->

## Cross-workspace dependency-graph compat

- A first-crossing import from a shared workspace lib → probe with `tsc -b` / build before signing off (see the SKILL's *Cross-workspace compat* + workspace-compat.md). <!-- TODO -->
