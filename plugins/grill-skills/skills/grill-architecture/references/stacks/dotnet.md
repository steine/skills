# Stack pack: .NET (CQRS, EF Core, ASP.NET)

The grill-architecture spine carries each lens's *principle*; this pack carries the concrete **.NET-idiom tells** and recommendation skew for each lens. Load it when recon detects `*.csproj` / `*.sln`. Apply the matching section as you run each lens.

Layering vocabulary assumed: `Domain` (entities, value objects, domain services) ← `Application` (feature handlers, ports) ← `Infrastructure` (EF, HTTP adapters, transport). Feature-folder convention under `Application/Features/<Feature>/`.

## Naming vs responsibility

- Consumer / project prefix duplicating the namespace.
- Role mismatch — `Client` promising transport while returning a domain shape.
- Lock to one vendor / product when more impls may follow.
- Stripping the vendor name on a vendor-specific impl.
- **Application interfaces wearing transport vocab** — `IXyzApiClient` in Application leaks transport upward. Prefer `IXyzGateway` / `IXyzDispatcher` at the App boundary; reserve transport-shaped names (`…ApiClient`, `…HttpClient`) for the Infrastructure impl.

## Folder placement

- Folder-by-kind buckets (`/Interfaces`, `/Services`, `/Models`, `/Handlers`) in a feature-folder repo.
- Folders named after the consumer when sibling folders are named after target system / capability.
- When multiple sub-conventions co-exist (dedicated `Enums/` vs alongside-entity), surface as a sub-pick; count occurrences and pick the dominant.

## Layer assignment

- One class owning transport + policy + domain mapping.
- Feature flags in transport classes instead of the Application layer.
- Persistence side-effects inside Infrastructure adapters.
- Cross-cutting concerns (retries, observability) at the wrong abstraction level.

## Value-type placement

- Enums backing EF columns / persisted state placed in a feature folder — belong in the Domain layer.
- DTOs shared across features placed in one feature folder — hoist to shared types.
- Transport-shape contracts (request/response records) in Application or Domain — belong in Infrastructure under the transport adapter.

## Port shape

- Auxiliary param idiom: **`CancellationToken` on every async method**; observability handles (`ILogger<T>`) injected, not passed.
- Parameter shape distributes responsibility: a primitive ID → the adapter owns lookup + mapping + transport; a domain record → the dispatcher owns lookup + build, the adapter owns mapping + transport only.
- Return type: nullable for expected-absence vs a result type when failure variants must be distinguished.

## Config and secret flow

- Composition root (`Program.cs`) forwarding service-specific config the service could read directly via `IOptions<T>`.
- Double-sourcing — service reads its own config (`IConfiguration`) AND the host forwards the same keys.
- Secrets co-mingled with non-secret config in `appsettings.json` — source from User Secrets (dev) / env / Key Vault (deployed).
- Resilience (retry/timeout) folded into the transport class instead of an `IHttpClientFactory` + resilience handler at the wiring layer.

## Cross-service transport

Request shape (`[FromBody]` record vs query-string scalars vs path params), contract location (caller- vs callee-owned vs `Common.*` shared), failure mode on rename. Default new internal routes to `[FromBody]` records; never inherit a legacy sibling route's shape by default.

Full option trade-offs + watch-for list: **REFERENCE:** [../cross-service-transport.md](../cross-service-transport.md).
