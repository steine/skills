# Implementation pack: .NET (CQRS, EF Core, ASP.NET)

The grill-implementation spine carries each lens's *principle*; this pack carries the concrete **.NET-idiom tells** for the implementation lenses. Load it when recon detects `*.csproj` / `*.sln`. Apply the matching section as you run each lens.

(Architecture-altitude tells — naming, folder, layer, value-type, port, config, transport — live in grill-architecture's own `references/stacks/dotnet.md`.)

## Reuse affordances

- Inline LINQ predicate duplicating a `[Projectable]` member or computed property already on the entity (`acr.IsActive` vs open-coded `!IsDeleted && StartDate <= today && …`).
- A derivation that has a name in the domain but isn't being called.
- A domain affordance with zero call sites — either this slice uses it, or it's dead code drifting from intent.
- Affordance idioms to grep on a touched entity: `[Projectable]` members, public computed properties, instance methods, extension methods.
- When a rule belongs on an entity but no helper exists, prefer an **instance method** (this stack is moving away from anemic entities — instance methods beat extension methods and feature statics).

## Read-path minimalism

- `.FirstOrDefaultAsync()` / `.ToListAsync()` returning a full entity when the caller reads N of M fields → project the subset.
- A read-only path with neither a projection nor `.AsNoTracking()`.
- A write handler loading a *related* entity only to copy a couple of scalars (`Id` + `Name`) → project those scalars instead.
- Asymmetry: the picker projects `(Id, Name)` but the writer loads the full entity for the same two fields — pick one contract.
- Name the fields the caller consumes vs the columns the SQL loads; the gap is the argument.

## Spec-gap checklist

- `CancellationToken` on every async method.
- Exception contract: which paths rethrow, which are caught-and-mapped.
- Ambient state: clock injected (`TimeProvider`) not wall-clock.
- Result types exhaustive over outcomes, including failure variants.
- `IDisposable` / `IAsyncDisposable` on types holding open resources.
- Observability surface (`ILogger<T>`, metrics, traces) the type needs.
- Idempotency / dedupe semantics for state-changing operations.

## Vacuous success

- `Enumerable.All(...)` (or `!Any(failed)`) over a collection that can be empty — `true` on empty.
- xUnit `[Theory]` fed by `[MemberData]` / `[ClassData]` from a query or discovery: assert the source's floor in its own `[Fact]`, so a shrunken source fails instead of running fewer cases.
- `catch { }` / `catch (Exception) { return HealthCheckResult.Healthy(); }` in a check or job — "couldn't check" reads as healthy.
- A background or reconciliation job that logs "completed" after processing 0 items, with no floor on the processed count.
- An early `return` on a missing precondition instead of `Skip` — the test reports as passed.
- Assertions any outcome satisfies: `Assert.NotNull(result)` on a non-nullable, `Assert.True(items.Count >= 0)`.
- A dependency stubbed to throw the very type the case asserts — `mock.Setup(...).ThrowsAsync(new InvalidOperationException())` under `Assert.ThrowsAsync<InvalidOperationException>` — so the handler's catch / log / count / rethrow can be deleted and the case stays green. Assert the wrapped exception type, the message the handler composes, its `InnerException`, or the metric / log it emitted.
- A mock returning the exact value the assertion checks, so the mapping or derivation under test never runs.
- An EF Core query exercised only against `UseInMemoryDatabase` (or SQLite in-memory): the in-memory provider evaluates expression trees the relational provider cannot translate — `??` over navigations, a subquery `.Contains(...)`, `[Projectable]` / computed members, client-evaluable method calls — so a green suite still throws on the first run in a deployed environment, and for a timer or job that is every invocation. Tell: the repo already has real-provider translation tests (a `*SqlTests` / `*SqlTranslationTests` class) that this slice's query didn't get.

## Impact sweep

- Factories and test fixtures that construct the entity.
- All `new <Entity>()` call sites (grep + count).
- Mappers touching the entity.
- View-models / DTOs auto-projecting entity properties — catch new columns leaking outward (**and into any hand-mirrored front-end DTO** — see the front-end impl pack's contract-drift tells).
- ORM model snapshot regen.
- The right migration project (multi-context repos).
- Seed data / fixtures with a hard-coded entity shape.

**Registration sites.** The tells above all fire on "a type changed"; these fire on "a resource was added". Grep the nearest sibling of the same kind by name and match its file set entry for entry:

- A new timer / `BackgroundService` / queue- or event-triggered function: its DI or host registration, and any **liveness or watchlist query** that enumerates the expected jobs by name.
- A new configuration value (`IOptions<T>` binding, app setting, connection string): the checked-in settings template (`local.settings.template.json`, `appsettings.Example.json`, `.env.example`) and the IaC / deployment parameter list. Absent there the knob is undiscoverable and runs at its code default in every environment — the slice's default quietly becomes the config, and whatever it tunes is never actually configured.
- A new alert rule / metric / dashboard under `infra/`: the monitoring doc or runbook table that states the rules, and the action / notification group the sibling rules point at.
- A new health check: its `AddHealthChecks()` registration, plus any probe or dashboard that names the expected checks.
- A new endpoint, authorization policy or feature flag: route registration, the policy list, the flag's per-environment default.

## Contract drift / cross-workspace compat

Front-end-side lenses — usually `N/A` for a pure .NET slice (the backend *is* the contract source, not a hand-mirror). A .NET VM change that a front-end re-declares is caught via **Impact sweep** above plus the front-end impl pack's contract-drift tells.
