# Stack pack: TypeScript / Node back-end — STUB

> **Status: stub.** Seeded from framework idiom (NestJS-leaning), not yet battle-tested on a real grill. Fill from real Node-backend grills before relying on it; mark a lens `N/A` if the app doesn't adopt the pattern. See [dotnet.md](./dotnet.md) for the worked reference — a Node back-end's layering is far closer to .NET than to the front-end `ts-web.md`.

Load when recon detects `tsconfig.json` + Node-server deps (`@nestjs/*` / `express` / `fastify` / `koa`, an ORM like Prisma/TypeORM, **no DOM**). This is the **back-end** TypeScript stack — distinct from `ts-web.md`.

Layering vocabulary (NestJS / layered Node): `Module → Controller → Provider/Service (DI) → Repository`, optionally a hexagonal `Domain ← Application (use-cases) ← Infrastructure (ORM, HTTP, queue)` split. Cross-cutting via guards / interceptors / pipes / filters / middleware.

## Naming vs responsibility

- A `…Service` god-provider owning transport + domain mapping + persistence — split into use-case service / repository / outbound gateway. <!-- TODO -->
- A transport-shaped provider (`…ApiService`, `…HttpClient`) injected straight into a controller instead of behind a domain-named port. <!-- TODO -->
- A controller carrying business logic — it should validate, delegate, map; the smell is decision-making in the handler. <!-- TODO -->
- A provider named for its DI token / location rather than its role. <!-- TODO -->

## Folder placement

- By-kind buckets (`controllers/`, `services/`, `dtos/` at root) in a feature/domain-module repo — NestJS favours a module per feature. Count siblings, pick the dominant. <!-- TODO -->
- A feature module reaching into another module's provider that isn't in its `exports`. <!-- TODO -->
- A `shared`/`common` module importing a feature module (upward dependency). <!-- TODO -->

## Layer assignment

- Business logic in controllers, guards, or interceptors instead of providers / use-cases. <!-- TODO -->
- Repository / ORM calls directly in a controller. <!-- TODO -->
- Cross-cutting concerns (auth, logging, transactions, retries) hand-rolled per handler instead of a guard / interceptor / middleware at the right level. <!-- TODO -->
- One ORM entity serving as the domain model *and* the API DTO — no separation. <!-- TODO -->

## Value-type placement

- A request/response DTO (class-validator) used as the domain type, or a domain/ORM entity serialized straight to the wire — keep wire DTO and domain type distinct, map between them. <!-- TODO -->
- An enum backing a persisted column placed in a controller/DTO file rather than the domain. <!-- TODO -->
- A shared value concept duplicated across modules vs one domain type. <!-- TODO -->

## Port shape

- Aux-param idiom: Node has no `CancellationToken` — pass an `AbortSignal` / deadline to outbound calls and set a client timeout; **flag unbounded outbound calls**. Provider deps come via DI, not `new`. <!-- TODO -->
- Return type: distinguish expected-absence (`null`/`undefined`) from failure (thrown `HttpException` / a `Result` type); `Promise`-returning. <!-- TODO -->
- Parameter shape: primitive id vs domain object distributes lookup/mapping across layers, same as elsewhere. <!-- TODO -->

## Config and secret flow

- `@nestjs/config` (or a typed config module) with validated, namespaced config vs `process.env.X` read deep in providers. <!-- TODO -->
- Env validated at boot (zod/Joi schema) vs unchecked `process.env.X!`. <!-- TODO -->
- **Real secrets** here (unlike the front-end, they don't ship to a client) — but they must come from env / a secret manager, never committed `.env`. <!-- TODO -->

## Cross-service transport

A Node back-end has **real** service-to-service hops (not the front-end's single backend call). Grill request shape, contract location (caller- / callee-owned / shared lib), and failure mode on rename. Typed client + **runtime validation (zod) on responses** — Node gives no compile-time guarantee across the wire. Never inherit a sibling route's shape by default. <!-- TODO -->

**Producer note:** this back-end often *produces* the contract a front-end (or another service) consumes. A response-DTO change must sweep those consumers — see the implementation pack's *Impact sweep / contract drift*.
