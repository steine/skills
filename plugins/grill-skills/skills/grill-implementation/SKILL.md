---
name: grill-implementation
description: Implementation-level pressure-test of a single slice's draft before (or just after) writing code. Targets .NET slices (EF Core, CQRS) with TS/npm-workspace front-ends. Validates the slice's concrete mechanics against the codebase — reuse of existing domain affordances, minimal read-path projections, interface spec-gaps (CancellationToken, result types, observability, idempotency), the cross-cutting impact of any schema/type change, and cross-workspace dependency-graph compatibility. Use at issue-start once the architecture is settled (ADRs/grill-architecture done) and you're about to implement — or on a fresh diff you want vetted before PR. Inherits prior architectural decisions; does not re-litigate naming, folder, layer, or port-shape. Output: a corrected slice plan and a fix-now list. No ADRs.
---

<what-to-do>

Pressure-test the concrete mechanics of one slice — the code you're about to write, or just wrote — against what the codebase already provides. For each derived value, read query, new interface, schema change, and cross-workspace import in the slice, ask whether it reuses what exists, loads only what it reads, closes the gaps the spec omitted, and survives the dependency graph it touches.

Ask questions one at a time. If a question is answerable by grepping or reading the codebase, do that instead of asking — these are factual checks, not preferences.

This skill is **validation**, not discovery. It takes the slice's prescription as input and vets it. It does not wander the codebase hunting for unrelated improvements (that's `improve-codebase-architecture`), and it does not re-open layering / naming / folder / port-shape (that's `grill-architecture`, and those are inherited as settled). Stay inside the slice.

</what-to-do>

<supporting-info>

## Target

**.NET** slices — EF Core, CQRS — with **TS/npm-workspace** front-ends (the cross-workspace lens). Lens principles port to any layered codebase; the smell lists (`.AsNoTracking()`, `[Projectable]`, `CancellationToken`, tsconfig/npm hoist) are stack-idiom — adapt them to yours.

## Stay at slice altitude

`grill-architecture` settled the hard-to-reverse picks (naming, folder, layer, port shape) upstream — inherit them, don't re-open them. This skill validates the slice's reversible mechanics and produces a fix list, no ADRs.

The firewall against `improve-codebase-architecture`: this skill asks "does *this slice* reuse the affordance that already exists?" — slice-local, one call site. The codebase-wide question ("should these N call sites consolidate into one deep module?") is out of scope; punt it up rather than expanding the slice.

## Recon before grilling

Walk these first — they're cheap and they collapse most questions into auto-resolves:

1. **Inherited decisions.** Read the parent issue / epic and `docs/adr/` for the area. Layering, naming, and folder placement are settled upstream — note them so you don't re-grill, and so reuse questions cite the right home.
2. **Domain affordances on touched entities.** For each entity the slice touches, grep for `[Projectable]` members, public computed properties, instance methods, and extension methods. Anything rule-shaped is a candidate the slice should reuse instead of open-coding.
3. **Sibling read/write paths.** Find the nearest existing query and command in the same feature. Note whether reads project to a subset or load full entities, and whether they use `.AsNoTracking()`. The slice should match the sharper of the two, not the looser.
4. **Workspace edges.** If the slice introduces an import from a shared workspace lib (`workspaces:` package, `file:`-linked dep) that this consumer doesn't already pull through, flag it now — first crossings reshape the dependency graph and surface latent version/tsconfig mismatches.

Surface recon as a short bullet list in the preamble — one line per load-bearing finding (affordance found, sibling projection shape, ADR state, workspace edge). Pack topic + fact per bullet; drop prose connectives and non-load-bearing paths. Detailed excerpts belong inside the question that consumes them.

## Preamble format

```
Recon:
- <inherited ADRs / parent scope relevant to this slice>
- <domain affordances found on touched entities>
- <sibling read/write projection + tracking shape>
- <workspace edges, if any>

Auto-resolved:
- A1  <decision>                       (Reason: <one-line reason>)

Grill slate:
Q1  <topic label, 2-5 words>
Q2  <topic label, 2-5 words>
...

Proceed with Q1?
```

Auto-resolve a question only when recon gives a single dominant signal with no conflict — e.g. the sibling read path already projects and the slice just needs to match it. When a real trade-off exists (reuse vs inline a rule that's subtly different here; project vs load when the writer also mutates), grill it.

## During the session — the lenses

Run the lenses that apply to the slice. Not every slice hits every lens; skip the ones with nothing to bite on, and say so rather than padding.

### Reuse existing domain affordances

When the draft encodes a derived predicate, mapping, or computed value inline, check the entity/domain folder for a helper that already names that rule. Reuse beats reinvent — and a rule with a name in one place is a rule that changes in one place.

Watch for:

- Inline LINQ predicate duplicating a `[Projectable]` member or computed property already on the entity (`acr.IsActive` vs open-coded `!IsDeleted && StartDate <= today && …`)
- A derivation that has a name in the domain but isn't being called
- A domain affordance defined with zero call sites — either this slice should use it, or it's dead code documenting intent that drifts from reality

If the rule conceptually belongs on an entity but no helper exists yet, offer "add it to the entity" as an option — not just "inline it" or "static helper." (This repo is moving away from anemic entities; instance methods on entities beat extension methods and feature statics.) But keep it slice-local: add the one affordance this slice needs, don't refactor every sibling that open-codes it — that's an `improve-codebase-architecture` job.

### Minimal projection on read paths

For each query whose result the caller only reads from, ask whether it should be a column-subset projection rather than a full tracked-entity load. Full loads cost wasteful SQL, a needless change-tracker entry, and accidental-mutation risk.

Watch for:

- `.FirstOrDefaultAsync()` / `.ToListAsync()` returning a full entity when the caller reads N of M fields
- A read-only path with neither a projection nor `.AsNoTracking()`
- A write handler loading a *related* entity only to copy a couple of scalars (`Id` + `Name`) onto the entity it actually mutates — project those scalars instead
- Asymmetry between read and write endpoints — the picker projects to `(Id, Name)` but the writer loads the full entity for the same two fields. Pick one contract.

When flagging, name the fields the caller actually consumes versus the fields the SQL would load. The gap is the argument.

### Spec-gap checklist on every interface

For each interface or class the slice defines — including any this grill introduces — check the gaps a spec almost always omits, because they're costly to retrofit once callers exist:

- `CancellationToken` on every async method
- Exception contract: which paths rethrow, which are caught-and-mapped
- Ambient state: timestamps/clock injected (`TimeProvider`) or wall-clock
- Result types exhaustive over outcomes, including failure variants
- `IDisposable` / `IAsyncDisposable` on types holding open resources
- Observability surface (`ILogger<T>`, metrics, traces) the type needs
- Idempotency / dedupe semantics for state-changing operations

When a question introduces a new type the spec didn't name, run this checklist against it before moving on — the gap won't surface on its own, precisely because the spec never anticipated the type.

### Cross-cutting impact sweep

For each schema / mapping / domain-type change in the slice, sweep the blast radius before finalizing. Post-merge discovery costs far more than pre-implementation discovery. Mark each item mandatory / optional / N/A:

- Factories and test fixtures that construct the entity
- All `new <Entity>()` call sites (grep + count)
- Mappers touching the entity
- View-models / DTOs auto-projecting entity properties — catch new columns leaking outward
- ORM model snapshot regen
- The right migration project (multi-context repos)
- Seed data / fixtures with a hard-coded entity shape

### Cross-workspace dependency-graph compat

When the slice adds an import from a shared workspace lib that this consumer didn't previously pull through its barrel, treat it as a **first-crossing** event — importing reshapes the graph tsc and the bundler traverse, so latent version/tsconfig mismatches surface only once the new path crosses the boundary. Probe with a POC import + `tsc -b` / `npm run build` against the consumer before signing off; static recon can't see what tsc refuses to compile once the graph shifts.

Load **REFERENCE:** [workspace-compat.md](./references/workspace-compat.md) for the watch-for list and the collision options when this lens fires.

## Verify facts in-grill

These lenses turn on facts — does the affordance exist, is the column persisted, does the sibling project, what version is hoisted. Verify with Bash / Read / grep inside the grill before recommending. Memory is not confirmation; don't ship a recommendation with "I think" or punt to "check later." A grill produces decisions.

When an answer follows from a lens already applied earlier in the session, cite it briefly rather than re-derive: "Same as the projection call we made on Q2 — match it. Confirm?"

## Closing the session

When the grill is done, produce:

1. **Fix-now list** — concrete changes to the slice, each tied to the question that surfaced it and the lens it came from. This is the deliverable; keep it actionable.
2. **Blockers split out** — anything that can't be fixed inside this slice (a workspace version unify, a missing precondition). Flag for the tracker as a separate item.
3. **Punted-up items** — codebase-wide consolidation noticed but deliberately left for `improve-codebase-architecture`, so it's recorded rather than lost.
4. **Offer next step** — apply the fixes, update the issue body, or stop.

No ADRs. If a decision here feels ADR-worthy, it was probably an architecture question in disguise — route it back to `grill-architecture`.

</supporting-info>
