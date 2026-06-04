---
name: grill-implementation
description: Implementation-level pressure-test of a single slice's draft before (or just after) writing code. Validates a slice's concrete mechanics against the codebase via composable per-stack packs (.NET + TS/React complete; Angular/Ruby/Go stubs) — reuse of existing affordances, read-path minimalism, interface spec-gaps (cancellation, result/error contract, observability, idempotency), the cross-cutting impact of any type/schema change, cross-boundary contract drift where a front-end re-declares a server DTO by hand, and cross-workspace dependency-graph compatibility. Use at issue-start once the architecture is settled (ADRs/grill-architecture done) and you're about to implement — or on a fresh diff you want vetted before PR. Inherits prior architectural decisions; does not re-litigate naming, folder, layer, or port-shape. Output: a corrected slice plan and a fix-now list. No ADRs.
---

<what-to-do>

Pressure-test the concrete mechanics of one slice — the code you're about to write, or just wrote — against what the codebase already provides. For each derived value, read query, new interface, schema change, and cross-workspace import in the slice, ask whether it reuses what exists, moves only what it reads, closes the gaps the spec omitted, and survives the dependency graph it touches.

Ask questions one at a time. If a question is answerable by grepping or reading the codebase, do that instead of asking — these are factual checks, not preferences.

This skill is **validation**, not discovery. It takes the slice's prescription as input and vets it. It does not wander the codebase hunting for unrelated improvements (that's `improve-codebase-architecture`), and it does not re-open layering / naming / folder / port-shape (that's `grill-architecture`, and those are inherited as settled). Stay inside the slice.

</what-to-do>

<supporting-info>

## Stack packs

The lens *principles* below (reuse, read-path minimalism, spec-gaps, impact sweep, contract drift, workspace compat) are **stack-agnostic**. The concrete **tells live in per-stack packs** in this skill's own `references/stacks/` (self-contained — grill-architecture keeps its own architecture-altitude packs separately):

- `*.csproj` / `*.sln` → [references/stacks/dotnet.md](./references/stacks/dotnet.md) — complete
- `tsconfig.json` / front-end `package.json` → [references/stacks/ts.md](./references/stacks/ts.md) — complete; **compose with a framework overlay**: `react` dep → [react.md](./references/stacks/react.md), `@angular/core` dep → [angular.md](./references/stacks/angular.md)
- `Gemfile` → [references/stacks/ruby.md](./references/stacks/ruby.md) — stub; `go.mod` → [references/stacks/go.md](./references/stacks/go.md) — stub

Detect the stack during recon and **load the matching pack now**; packs compose, so a TS front-end loads `ts.md` *and* its overlay. A slice that spans back-end and front-end may load two packs. If the stack isn't covered, use the .NET pack as the worked example and flag the gap. If a lens doesn't bind to this slice, say so rather than force-fit.

## Stay at slice altitude

`grill-architecture` settled the hard-to-reverse picks (naming, folder, layer, port shape) upstream — inherit them, don't re-open them. This skill validates the slice's reversible mechanics and produces a fix list, no ADRs.

The firewall against `improve-codebase-architecture`: this skill asks "does *this slice* reuse the affordance that already exists?" — slice-local, one call site. The codebase-wide question ("should these N call sites consolidate into one deep module?") is out of scope; punt it up rather than expanding the slice.

## Recon before grilling

Walk these first — they're cheap and they collapse most questions into auto-resolves:

1. **Inherited decisions.** Read the parent issue / epic and `docs/adr/` for the area. Layering, naming, and folder placement are settled upstream — note them so you don't re-grill, and so reuse questions cite the right home.
2. **Affordances on touched modules.** For each entity/module the slice touches, grep for existing helpers, computed members, utilities, or clients that already name the rule or own the behaviour (the pack lists the stack's affordance idioms). Anything the draft open-codes that already exists is a reuse candidate.
3. **Sibling read/write paths.** Find the nearest existing read and write in the same feature. Note whether the read moves only what its caller consumes, and the stack's over-fetch idiom (the pack lists tells). The slice should match the sharper of the two, not the looser.
4. **Workspace edges.** If the slice introduces an import from a shared workspace lib (`workspaces:` package, `file:`-linked dep) that this consumer doesn't already pull through, flag it now — first crossings reshape the dependency graph and surface latent version/tsconfig mismatches.
5. **Cross-boundary contracts.** If the slice changes a server VM/DTO, grep the front-end for a hand-mirrored type (often a `// Mirrors <Namespace>.<Vm>` comment, or a `res.json() as T` cast). No compiler edge crosses the HTTP boundary, so the mirror drifts silently — note it now so the change-shape question knows to sweep it.

Surface recon as a short bullet list in the preamble — one line per load-bearing finding (affordance found, sibling read shape, ADR state, workspace edge). Pack topic + fact per bullet; drop prose connectives and non-load-bearing paths. Detailed excerpts belong inside the question that consumes them.

## Preamble format

```
Recon:
- <inherited ADRs / parent scope relevant to this slice>
- <affordances found on touched modules>
- <sibling read/write shape>
- <workspace edges / cross-boundary contracts, if any>

Auto-resolved:
- A1  <decision>                       (Reason: <one-line reason>)

Grill slate:
Q1  <topic label, 2-5 words>
Q2  <topic label, 2-5 words>
...

Proceed with Q1?
```

Auto-resolve a question only when recon gives a single dominant signal with no conflict — e.g. the sibling read path already moves only what's consumed and the slice just needs to match it. When a real trade-off exists (reuse vs inline a rule that's subtly different here; lean vs full read when the writer also mutates), grill it.

## During the session — the lenses

Run the lenses that apply to the slice. Not every slice hits every lens; skip the ones with nothing to bite on, and say so rather than padding. Each lens below is the stack-agnostic *principle*; the concrete tells (and recommendation skew) for the detected stack live under the matching heading in the loaded pack — **run the lens, then apply the pack's same-named section.**

### Reuse affordances

When the draft encodes a derived predicate, mapping, or computed value inline — or hand-rolls boilerplate (a fetch, an auth header, a client) — check whether a named affordance already exists. Reuse beats reinvent: a rule named in one place changes in one place. → **Pack: *Reuse affordances*** for the stack's affordance idioms and dead-affordance tells.

If the rule conceptually belongs on an entity/module but no affordance exists yet, offer "add it there" as an option — not just "inline it." But keep it slice-local: add the one affordance this slice needs, don't refactor every sibling that open-codes it — that's an `improve-codebase-architecture` job.

### Read-path minimalism

A read should move only the fields/rows the consumer uses — **volume, not shape** (shape is the contract lens). Over-fetch is waste and, on a mutable backend read, accidental-mutation risk. Route findings: **slice-local** where the slice controls the fetch; **blocker** where the fix is a leaner endpoint/contract upstream; **`N/A`** where the read is already lean or its shape is fixed upstream. → **Pack: *Read-path minimalism*** for the stack's tells.

### Spec-gap checklist on every interface

For each interface or type the slice defines — including any this grill introduces — check the gaps a spec almost always omits, because they're costly to retrofit once callers exist: cancellation, exception/error contract, ambient state (clock), exhaustive result/outcome types, resource disposal, observability, idempotency. The pack carries the stack's concrete checklist (the idiom for each gap). → **Pack: *Spec-gap checklist*.**

When a question introduces a new type the spec didn't name, run this checklist against it before moving on — the gap won't surface on its own, precisely because the spec never anticipated the type.

### Cross-cutting impact sweep

For each schema / type / contract change in the slice, sweep the blast radius before finalizing; mark each item mandatory / optional / N/A. Post-merge discovery costs far more than pre-implementation discovery. → **Pack: *Impact sweep*** for the stack's call-site / fixture / mapping / migration tells.

### Cross-boundary contract drift

When the slice changes a server VM/DTO that a front-end re-declares **by hand**, the mirror does not move with it — no compiler edge crosses the HTTP boundary, so a rename/retype/added-field drifts silently until it fails at runtime. The `res.json() as T` cast is the tell: it manufactures confidence the wire never earned. For each server contract the slice touches, sweep its hand-mirror.

Watch for:

- A server field renamed, added, removed, or retyped, with a hand-written front-end type mirroring it (often a `// Mirrors <Namespace>.<Vm>` comment) that the slice leaves untouched
- A declared type the wire can't deliver — `Date` on a field that serializes as an ISO string (so `.getTime()` / `<` sorts lie), an enum union for a value the server sends as an int, a non-null field the server may omit
- An `res.json() as T` boundary with no runtime parse (zod/io-ts) — a renamed field arrives as `undefined`, not a compile error
- Asymmetry: the server's read VM gains a column the front-end type and render path never learn of (dead data), or the front-end still expects a field the server stopped sending

When flagging, name the server field + its wire type against the front-end's declared type. The mismatch is the argument. Fix options: validate/parse at the boundary, or — if hand-mirroring stays — treat the mirror as a contract the slice must edit in lockstep, and flag it as a blocker when it spans repos. Keep it slice-local: fix the one contract this slice's change touches; "adopt codegen / a shared validated http client" across all call sites is an `improve-codebase-architecture` punt. → **Pack (front-end): *Impact sweep + contract drift*** for the stack's mirror tells.

### Cross-workspace dependency-graph compat

When the slice adds an import from a shared workspace lib that this consumer didn't previously pull through its barrel, treat it as a **first-crossing** event — importing reshapes the graph tsc and the bundler traverse, so latent version/tsconfig mismatches surface only once the new path crosses the boundary. Probe with a POC import + `tsc -b` / `npm run build` against the consumer before signing off; static recon can't see what tsc refuses to compile once the graph shifts.

Load **REFERENCE:** [workspace-compat.md](./references/workspace-compat.md) for the watch-for list and the collision options when this lens fires.

## Verify facts in-grill

These lenses turn on facts — does the affordance exist, is the column persisted, does the sibling over-fetch, what version is hoisted. Verify with Bash / Read / grep inside the grill before recommending. Memory is not confirmation; don't ship a recommendation with "I think" or punt to "check later." A grill produces decisions.

When an answer follows from a lens already applied earlier in the session, cite it briefly rather than re-derive: "Same as the read shape we settled on Q2 — match it. Confirm?"

## Closing the session

When the grill is done, produce:

1. **Fix-now list** — concrete changes to the slice, each tied to the question that surfaced it and the lens it came from. This is the deliverable; keep it actionable.
2. **Blockers split out** — anything that can't be fixed inside this slice (a workspace version unify, a leaner endpoint upstream, a missing precondition). Flag for the tracker as a separate item.
3. **Punted-up items** — codebase-wide consolidation noticed but deliberately left for `improve-codebase-architecture`, so it's recorded rather than lost.
4. **Offer next step** — apply the fixes, update the issue body, or stop.

No ADRs. If a decision here feels ADR-worthy, it was probably an architecture question in disguise — route it back to `grill-architecture`.

</supporting-info>
