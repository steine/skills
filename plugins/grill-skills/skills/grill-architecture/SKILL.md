---
name: grill-architecture
description: Architectural pressure-test of a plan or issue before implementation. Targets layered/hexagonal .NET codebases (CQRS, EF Core, ASP.NET). Challenges every prescribed type, folder, config-flow, layer assignment, and cross-cutting placement against codebase precedent, .NET framework idiom, and layering principles. Use at two granularities — (1) after to-prd, before to-issues, for cross-cutting architectural ADRs that the issue decomposition inherits; (2) at issue-start, before code, for slice-specific decisions inheriting prior ADRs. Output: revised plan + ADRs for hard-to-reverse picks. For reversible per-slice implementation mechanics once the architecture is settled — reuse of domain affordances, minimal read-path projections, interface spec-gaps, schema-change impact sweep, cross-workspace compat — use grill-implementation instead.
---

<what-to-do>

Interview the user relentlessly about every architectural prescription in this plan. For each named type, folder, config section, layer assignment, and cross-cutting concern, ask whether its location and shape match the codebase and framework. For each question, provide your recommended answer.

Ask questions one at a time. If a question can be answered by exploring the codebase, explore instead of asking.

</what-to-do>

<supporting-info>

## Target

Layered/hexagonal **.NET** codebases — CQRS, EF Core, ASP.NET. The lens *principles* (naming-vs-responsibility, folder convention, layer ownership, value-type scope, port shape, config flow, cross-service transport) port to any Domain/Application/Infrastructure split; the **smell lists are .NET-idiom** — treat them as the canonical examples and map to your stack.

## Codebase awareness

Walk these before grilling:

1. **Existing precedents.** For each external system or cross-cutting pattern in the spec, find any sibling implementation. Note folder, type names, layer split, config shape.
2. **Folder conventions.** Sample 2–3 existing modules. Feature folders or by-kind (`/Interfaces`, `/Services`, `/Models`)? Pick the dominant.
3. **Framework idioms.** Identify the framework. Note conventional answers for config flow, DI scope, typed clients, cross-cutting handlers, secret layering.
4. **Existing ADRs.** Read `docs/adr/`. Do not re-litigate prior decisions.
5. **Responsibility count per type.** For each spec-named type, list its responsibilities (transport / policy / mapping / persistence / etc.). >1 distinct responsibility → tag as first Q to grill.
6. **Issue-tree scope.** If the spec has a parent issue / epic / project, read it for inherited scope (deferred items, explicit out-of-scope, parent-level ADRs). Cite when auto-resolving via parent scope: "answered upstream by `<parent ref>`."

Recon is agent-internal. Surface it in the preamble as **one-liner bullets** — topic + load-bearing fact per bullet (sources read, precedents verified, ADR state, entity/lookup facts that drive auto-resolves). Drop prose connectives, non-load-bearing paths, redundant qualifiers; keep only facts an auto-resolve or a Q recommendation will cite. Reserve detailed precedents (file paths, code excerpts) for the Q that consumes them.

## Preamble structure

**Dependency tags.** Each Q carries `deps:` — `recon` (answerable from recon alone), `Qn` (single upstream), or `Q1, Q3, …` (multi-dep). Cross-layer types (result records, port interfaces, value objects) are usually multi-dep — result-type homes depend on layering AND naming; when in doubt add the upstream dep. When an upstream Q shifts a downstream Q's option space, **restate** the downstream Q with the new constraints — don't re-grill from scratch.

**Auto-resolve.** When recon gives a dominant precedent (≥2 examples, no conflicting signal), state the answer as applied with `(Reason: <one-line>)`; user can override. First run the relevant `## During the session` lens's smell list — if any smell could fire, grill instead. When a Q has both a shape dimension and an ownership dimension, split: shape auto-resolvable from precedent, ownership always grilled.

**Never auto-resolve:**

- Responsibility split / layering
- Naming role / vocabulary (transport- vs domain-shaped)
- Config-flow ownership (composition root vs service)
- Cross-cutting placement (flags, persistence side-effects, retries, observability)
- Cross-service wire shape (`[FromBody]` record vs query-string scalars vs path params) when the slice introduces an HTTP hop between two services in the same repo
- Any Q where a `## During the session` smell rule could plausibly apply

### Preamble format

```
Recon:
- <parent / sibling issues read>
- <module / project shape relevant to this spec>
- <auth / framework wiring state>
- <entity + lookup facts that drive auto-resolves>
- <ADR state>
- <anything else load-bearing for the slate>


Auto-resolved:
- A1  <decision>                       (Reason: <one-line reason>)
- A2  <decision>                       (Reason: <one-line reason>)

Grill slate (topo order):
Q1  <topic label, 2-5 words>           deps: recon          [ROOT]
Q2  <topic label, 2-5 words>           deps: Q1
Q3  <topic label, 2-5 words>           deps: Q1
Q4  <topic label, 2-5 words>           deps: Q1, Q3
...

Proceed with Q1?
```

Slate entries are short **topic labels** (2–5 words), not option lists or trade-off summaries — the full Q (options, smell check, recommendation, sub-picks) emits only when that Q fires. Each Q's recommendation cites the specific precedent / spec line / smell rule it leans on; that's where the detailed recon pays its way.

## Grill order

Topological: deps before dependents. The layering Q is the root. If the spec lists naming or flag placement first, don't grill them in that order — grill the layering question they presuppose.

## During the session

### Challenge naming against responsibility

Does the name describe role, or where it lives / who consumes it?

Watch for:

- Consumer / project prefix duplicating namespace
- Role mismatch — "Client" promising transport while returning domain shape
- Lock to one vendor / product when more impls may follow
- Stripping vendor name on a vendor-specific impl
- Application interfaces wearing transport vocab (`IXyzApiClient` in Application leaks transport upward — prefer `IXyzGateway` / `IXyzDispatcher` at the App boundary; reserve transport-shaped names for Infrastructure)

### Challenge folder placement against convention

Does this match the codebase's folder convention, or invent a new one?

Watch for:

- Folder-by-kind buckets (`/Interfaces`, `/Services`, `/Models`, `/Handlers`) in feature-folder repos
- Folders named after consumer when sibling folders are named after target system / capability
- New features nested under a dominant existing feature folder — default to sibling at parent level; only nest when genuinely subordinate

When multiple sub-conventions co-exist (e.g., dedicated `Enums/` vs alongside-entity), surface as a sub-pick. Right answer is usually the dominant one — count occurrences.

### Challenge layer assignment

For each responsibility — transport, policy, domain mapping, persistence, flags, retries, observability — which layer owns it, and why?

Watch for:

- One class owning transport + policy + domain mapping
- Feature flags in transport classes instead of the application layer
- Persistence side-effects inside infrastructure adapters
- Cross-cutting concerns at the wrong abstraction level

Precedent informs options, never justifies a recommendation by itself. "Match the sibling" is path-dependence, not architecture.

### Challenge value-type placement

For each enum, value object, or DTO: feature-scoped, domain-scoped, or contract-scoped?

Watch for:

- Enums backing EF columns / persisted state placed in a feature folder — belong in the domain layer
- DTOs shared across features placed in one feature folder — hoist to shared types
- Transport-shape contracts (request/response records) in Application or Domain — belong in Infrastructure under the transport adapter

### Challenge port shape at definition

When introducing a port, grill all three in one stroke:

1. Return type
2. Parameter shape — primitive ID vs domain record vs wire record
3. Auxiliary params (`CancellationToken`, observability handles)

Parameter shape distributes responsibility. Primitive ID → adapter owns lookup + mapping + transport. Domain record → dispatcher owns lookup + build; adapter owns mapping + transport only.

### Challenge config and secret flow

For each config key and secret: who reads it, who owns it, idiomatic for the framework?

Watch for:

- Composition root forwarding service-specific config the service could read directly
- Double-sourcing — service reads its own config AND host forwards the same keys
- Secrets co-mingled with non-secret config in the wrong layer

### Challenge cross-service transport shape

When a slice introduces an HTTP / RPC / queue hop between two services *in the same repo*, grill three coupled dimensions: request shape (`[FromBody]` record vs query-string scalars vs path params), contract location (caller- vs callee-owned vs shared), and failure mode on rename (compile error > test failure > runtime trace > silent no-op). Default new internal routes to `[FromBody]` records; never inherit a legacy sibling route's shape by default.

Load **REFERENCE:** [cross-service-transport.md](./references/cross-service-transport.md) for the full option trade-offs and watch-for list when this lens fires.

### Stay at architectural altitude

This skill stops at hard-to-reverse, ADR-worthy decisions: naming, folder, layer, value-type placement, port shape, config/secret flow. Reversible per-slice mechanics (reuse, projection, spec-gaps, impact sweep, workspace compat) belong to **grill-implementation**, run later. Don't run them here. If one surfaces a genuinely architectural question — a derivation that should become a domain method, a port shape that redistributes responsibility across layers — pull it up into the relevant macro lens above; otherwise leave it for grill-implementation.

### Surface coupled decisions

Naming, layering, folder, flag placement, config flow are usually one braided problem. Treat as a tree, not a queue.

When one decision settles, enumerate next coupled decisions. Before each Q, list adjacent commitments: "this Q presumes A, B, C — confirm or address first."

When listing options, include at least one that changes type count or layer count, not just relocates. Heuristic: "would this Q dissolve if we split the type?" If yes, surface that as an option.

Sub-concerns ≠ option modifiers. When recommending an option, distinguish the decision ("service owns its config") from sub-concerns that apply to all options (secret handling, env-specific defaults). Call sub-concerns out separately, not as caveats.

Bundle small divergences from precedent (typed vs named, timeouts, headers, lifetime, log levels) into one "divergence cluster" Q if each takes <2 sentences AND none unlocks coupled decisions downstream. Never bundle a divergence cluster with a load-bearing layering or naming decision — different cognitive modes.

### Verify in-grill, cite applied rules

Lenses turn on facts — does the precedent exist, is the attribute present, is the provider registered, what's the default value. Verify with Bash / Read / grep before recommending; memory is not confirmation. Don't ship with `?`, "I think", or "check this later" — grills produce decisions. When a Q's answer follows from a lens already applied or a prior session decision, cite it briefly ("Answered by the enum-placement rule. Confirm?") rather than re-derive.

### Update ADRs inline

When a decision settles and meets the ADR gate, draft the ADR right there. Don't batch.

## Closing the session

When the grill is done, produce a summary:

1. **Revised file map** — every file affected, labeled (NEW / changed / regenerated / N/A)
2. **Settled decisions indexed back to question numbers**
3. **Divergences from the source issue** — for tracker update
4. **ADRs landed** — list with one-line summary each
5. **Offer next step** — rewrite issue body, generate task list, or stop

## Offer ADRs sparingly

Offer an ADR only when all three are true:

1. **Hard to reverse** — cost of changing later is meaningful
2. **Surprising without context** — a future reader will wonder why
3. **The result of a real trade-off** — genuine alternatives existed

If any of the three is missing, skip the ADR. Use the format in [ADR-FORMAT.md](./ADR-FORMAT.md).

</supporting-info>
