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

## Impact sweep

- Factories and test fixtures that construct the entity.
- All `new <Entity>()` call sites (grep + count).
- Mappers touching the entity.
- View-models / DTOs auto-projecting entity properties — catch new columns leaking outward (**and into any hand-mirrored front-end DTO** — see the front-end impl pack's contract-drift tells).
- ORM model snapshot regen.
- The right migration project (multi-context repos).
- Seed data / fixtures with a hard-coded entity shape.

## Contract drift / cross-workspace compat

Front-end-side lenses — usually `N/A` for a pure .NET slice (the backend *is* the contract source, not a hand-mirror). A .NET VM change that a front-end re-declares is caught via **Impact sweep** above plus the front-end impl pack's contract-drift tells.
