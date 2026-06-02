---
name: grill-architecture
description: Architectural pressure-test of a plan or issue before implementation. Challenges every prescribed type, folder, config-flow, layer assignment, and cross-cutting placement against codebase precedent, framework idiom, and layering principles. Use at two granularities — (1) after to-prd, before to-issues, for cross-cutting architectural ADRs that the issue decomposition inherits; (2) at issue-start, before code, for slice-specific decisions inheriting prior ADRs. Output: revised plan + ADRs for hard-to-reverse picks. For reversible per-slice implementation mechanics once the architecture is settled — reuse of domain affordances, minimal read-path projections, interface spec-gaps, schema-change impact sweep, cross-workspace compat — use grill-implementation instead.
---

<what-to-do>

Interview the user relentlessly about every architectural prescription in this plan. For each named type, folder, config section, layer assignment, and cross-cutting concern, ask whether its location and shape match the codebase and framework. For each question, provide your recommended answer.

Ask questions one at a time. If a question can be answered by exploring the codebase, explore instead of asking.

</what-to-do>

<supporting-info>

## Codebase awareness

Walk these before grilling:

1. **Existing precedents.** For each external system or cross-cutting pattern in the spec, find any sibling implementation. Note folder, type names, layer split, config shape.
2. **Folder conventions.** Sample 2–3 existing modules. Feature folders or by-kind (`/Interfaces`, `/Services`, `/Models`)? Pick the dominant.
3. **Framework idioms.** Identify the framework. Note conventional answers for config flow, DI scope, typed clients, cross-cutting handlers, secret layering.
4. **Existing ADRs.** Read `docs/adr/`. Do not re-litigate prior decisions.
5. **Responsibility count per type.** For each spec-named type, list its responsibilities (transport / policy / mapping / persistence / etc.). >1 distinct responsibility → tag as first Q to grill.
6. **Issue-tree scope.** If the spec has a parent issue / epic / project, read it for inherited scope (deferred items, explicit out-of-scope, parent-level ADRs). Cite when auto-resolving via parent scope: "answered upstream by `<parent ref>`."

Recon findings are agent-internal working memory. Surface only a short bullet list in the preamble (one bullet per significant finding — key sources read, precedents verified, ADR state, entity/lookup facts that drive auto-resolves); reserve detailed precedents for the Q that consumes them.

**Recon bullets are one-liners.** Pack topic + load-bearing fact(s) per bullet. Drop prose connectives ("already wired", "exists at", parenthetical asides), drop file paths that aren't load-bearing, drop redundant qualifier clauses. Keep only facts that an auto-resolve or a Q recommendation will cite. Aim ~50% denser than narrative prose.

Output a preamble per **Preamble structure** below.

## Preamble structure

### Dependency annotation

Each Q carries a `deps:` tag:

- `deps: recon` — answerable from recon alone
- `deps: Qn` — single upstream
- `deps: Q1, Q3, ...` — multi-dep

When upstream Qs settle in a way that shifts a downstream Q's option space, **restate** the downstream Q with the new constraints — don't re-grill from scratch.

Cross-layer types (result records, port interfaces, value objects crossing layers) typically have multi-deps. Result-type homes depend on layering AND naming, not naming alone. When in doubt, add the upstream dep.

### Auto-resolve recon-answered Qs

If recon establishes a dominant precedent (single dominant convention, ≥2 examples, no conflicting signal), state the answer in the preamble as auto-applied: `(Reason: <one-line reason>)`. User can override.

### Guard against auto-resolving architectural questions

Before auto-resolving, run the relevant `## During the session` lens's smell list. If any smell could fire, grill instead.

Never auto-resolve:

- Responsibility split / layering
- Naming role / vocabulary (transport- vs domain-shaped)
- Config-flow ownership (composition root vs service)
- Cross-cutting placement (flags, persistence side-effects, retries, observability)
- Cross-service wire shape (`[FromBody]` record vs query-string scalars vs path params) when the slice introduces an HTTP hop between two services in the same repo
- Any Q where a `## During the session` smell rule could plausibly apply

When a Q has both a shape dimension AND an ownership dimension, split: shape part auto-resolvable from precedent; ownership part always grilled.

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

Slate entries are short **topic labels** (2–5 words naming what'll be decided), not mini-option lists or trade-off summaries. The full Q — options, smell check, recommendation, sub-picks — emits when Q1 starts grilling. Don't preview options in the slate; the user sees them when the Q fires.

Detailed recon (file paths, code excerpts, multi-line precedent dumps) belongs inside the Q that consumes it — not in the preamble. Each Q's recommendation should cite the specific precedent / spec line / smell rule it leans on; that's where detail pays its way.

## Grill order

Topological order: deps before dependents. Layering Q is the root. If the spec lists naming or flag placement first, do not grill them in that order — grill the layering question they presuppose.

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

When a slice introduces an HTTP / RPC / queue hop between two services *in the same repo*, grill three coupled dimensions: request shape, contract location, and failure mode on rename.

**Request shape:**

- `[FromBody]` record — JSON property binding; missing required field on a non-nullable record param fails loudly with a 400.
- Query-string scalars — name-based binding; missing or misnamed parameters silently bind to `default` (`Guid.Empty`, `null`, `0`). Silent no-ops in production.
- Path parameters with route constraints (`{id:guid}`) — malformed / missing values 404 at routing time.

**Contract location:**

- Caller-owned — each side defines its own DTO; JSON aligns at the wire. Cheap but no compile-time enforcement.
- Callee-owned — server publishes a Contracts project; caller depends on it. Rename breaks the build on both sides.
- Shared in Common.\* — everyone can import. Tempting but erodes service boundaries; usually wrong for directed RPC.

**Failure mode on rename:**

- Compile error (typed contract package) > test failure (record + integration test) > runtime trace (record + unit-test-only) > silent no-op (string-concat URL or scalar param). Lower-numbered modes are categorically better; design for compile-time when the surface will grow.

Watch for:

- Reusing a legacy user-route's query-string + scalar shape for a new service-to-service route in the same controller class. The two routes share class real estate but serve different callers (XHR-from-MVC vs typed HttpClient), different auth contexts, different blast radii. Inheritance of shape is path-dependence.
- Hand-rolled URL strings in HTTP clients (`$"/path?id={x}&name={y}"`) — each literal is a free-floating contract assumption; renames on the server don't ripple back to the client.
- "Match the existing controller's shape" recommendations without distinguishing whether the existing shape is *load-bearing for legacy callers* (back-compat) vs. *accidental* (legacy choice that doesn't need to propagate).
- Test fakes that short-circuit the transport (e.g. a hand-rolled `Recording*HttpClient` mocking the typed-client interface) — they let wire-shape bugs ship because the unit test doesn't exercise the URL/body construction. Pair with at least one `WebApplicationFactory` integration test.

Recommendation skew: for new internal-service routes, default to `[FromBody]` records over query-string scalars; defer shared-contract package extraction until the 2nd or 3rd hop, but pre-design for it (records on both sides, same shape, ready to consolidate). Never auto-resolve in favour of inheriting the legacy sibling route's shape.

### Implementation-mechanics lenses live in grill-implementation

This skill stops at the hard-to-reverse, ADR-worthy decisions: naming, folder, layer, value-type placement, port shape, config/secret flow. The reversible per-slice mechanics — reuse of existing domain affordances, minimal read-path projections, the interface spec-gap checklist (`CancellationToken`, exception/idempotency/observability contracts), the cross-cutting impact sweep on schema changes, and cross-workspace dependency-graph compat — are a separate altitude with a separate output (a fix-now list, no ADRs). They belong to the **grill-implementation** skill, run at issue-start once these architectural decisions are settled.

Don't run those lenses here. If one surfaces a genuinely architectural question (a derivation that should become a domain method, a port whose shape redistributes responsibility across layers), pull it back up into the relevant macro lens above. Otherwise leave it for grill-implementation.

### Surface coupled decisions

Naming, layering, folder, flag placement, config flow are usually one braided problem. Treat as a tree, not a queue.

When one decision settles, enumerate next coupled decisions. Before each Q, list adjacent commitments: "this Q presumes A, B, C — confirm or address first."

When listing options, include at least one that changes type count or layer count, not just relocates. Heuristic: "would this Q dissolve if we split the type?" If yes, surface that as an option.

Sub-concerns ≠ option modifiers. When recommending an option, distinguish the decision ("service owns its config") from sub-concerns that apply to all options (secret handling, env-specific defaults). Call sub-concerns out separately, not as caveats.

Bundle small divergences from precedent (typed vs named, timeouts, headers, lifetime, log levels) into one "divergence cluster" Q if each takes <2 sentences AND none unlocks coupled decisions downstream. Never bundle a divergence cluster with a load-bearing layering or naming decision — different cognitive modes.

### Cross-reference with code; verify in-grill

Before recommending a change naming a specific precedent, verify it exists and is current. Memory ≠ `ls` / `grep` confirmation.

If a Q depends on a verifiable fact (file exists, attribute present, provider registered, default value), verify with Bash / Read inside the grill — don't punt to "check this later."

Uncertain about a fact? Verify before recommending. Don't ship with `?` or "I think." Grills produce decisions, not best-guess assertions.

### Cite applied rules

When a Q's answer follows from a previously-applied lens or a prior session decision, cite it briefly rather than re-derive. "Answered by the enum-placement rule. Confirm?" beats re-running the full argument.

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
