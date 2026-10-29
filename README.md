# skills

Architectural grills for Matt Pocock's engineering skill suite.
I use Matt's skill suite extensively in my workflow, but I felt the architectural dimension was sometimes lacking in the result. 

## Supported stacks

| Stack | Detected by | Coverage |
|-------|-------------|----------|
| .NET (CQRS / EF Core / ASP.NET) | `*.csproj` / `*.sln` | ✅ complete |
| TS front-end — React | `tsconfig.json` + `react` | ✅ complete |
| TS front-end — Angular | `tsconfig.json` + `@angular/core` | 🚧 stub |
| TS back-end — Node (NestJS / Express) | `tsconfig.json` + `@nestjs`/`express`, no DOM | 🚧 stub |
| Ruby / Rails | `Gemfile` | 🚧 stub |
| Go | `go.mod` | 🚧 stub |

Coverage applies to both skills (architecture + implementation). Stubs are seeded with real tells but not yet grill-tested — see [MAINTAINERS.md](plugins/grill-skills/MAINTAINERS.md) to fill or add one.

## Origin & when to use

These extend [Matt Pocock's engineering skill suite](https://github.com/mattpocock/skills) (`grilling`, `domain-modeling`, `implement`, `code-review`) in the architectural dimension.

The skills live in two different phases:

### Refinement → Definition of Ready

```
grab PBI → /grill-feature → /grill-architecture
```

- **`grill-feature`** ← *problem space.* Flesh out the stakeholder ask in the domain's language, land goal and scope, and split it into user stories — sliced by user value, never by layer — each with acceptance criteria. Architecture and implementation questions are parked for the grills that own them, not grilled here. Everything is drafted onto the feature ticket, the story split included; no story tickets yet, since architecture may still re-cut it.
- **`grill-architecture`** ← *macro lenses.* Pressure-test the cross-cutting decisions — naming, layering, folder placement, port shape, config flow — and land ADRs so every issue inherits settled architecture. Re-cuts the story split where a decision requires it, then creates the story tickets with their acceptance criteria and cross-system dependencies.

### Sprint / implementation → per slice, per dev

```
grab issue → /grill-implementation → /implement → PR
```

- **`grill-implementation`** ← *micro lenses.* At issue pickup, once the architecture is settled, vet the slice's concrete mechanics — reuse of existing affordances, read-path minimalism, spec-gaps, vacuous success, impact sweep, cross-boundary contract drift. If the story has acceptance criteria but no approach, drafts one first and grills that; then maps each criterion to test cases, the list `implement` builds against.
- **`implement`** ← *build.* Matt's `implement` with its last step swapped: commits, then runs `review` instead of `code-review` and applies the fix-now items, stopping to ask on anything that needs a decision.
- **`review`** ← *finish line.* Before opening the PR (or when reviewing someone else's), wraps Matt's `code-review` (standards + spec) and presents its findings per axis with a recommendation on each — fix now, allow, verify first, or your call — so an in-scope gap isn't shipped as "non-blocking".


## What's in it

One plugin, **grill-skills**, bundling a feature grill that lands the ask, two grill skills that are a deliberate split of one concern, the ADR writer they hand off to, an `implement` that ends in `review`, and a review wrapper for the finished implementation:

| Skill | Altitude | When | Output |
|-------|----------|------|--------|
| `grill-feature` | Problem space — what's asked and when it's done | Refinement, first step | Goal, scope, **user stories with acceptance criteria**, parked questions (no ADRs) |
| `grill-architecture` | Macro — hard-to-reverse decisions | Refinement, after `grill-feature` | Revised plan + **ADRs** |
| `grill-implementation` | Micro — reversible per-slice mechanics | Sprint, at issue pickup | Slice approach, **fix-now list**, tests traced to the acceptance criteria (no ADRs) |
| `write-adr` | Recording — one decision per ADR | Whenever an ADR is written, superseded or retired | Short ADR + status changes on the records it replaces |
| `implement` | Build — the slice, then its review | Sprint, after `grill-implementation` | Committed slice with its fix-now items applied |
| `review` | Finish line — what the change must still fix | Before opening the PR, or reviewing someone else's | Per-axis findings, each with a **fix now / allow** recommendation |

The two grills pressure-test against the codebase via composable per-stack packs (.NET + TS-web/React complete; TS-node/Angular/Ruby/Go stubs). For the internal structure and how to extend it, see [plugins/grill-skills/MAINTAINERS.md](plugins/grill-skills/MAINTAINERS.md).

## Install

```
/plugin marketplace add steine/skills
/plugin install grill-skills@steine-skills
```

Skills are then invoked namespaced: `/grill-skills:grill-feature`, `/grill-skills:grill-architecture`, `/grill-skills:grill-implementation`, `/grill-skills:write-adr`, `/grill-skills:implement`, `/grill-skills:review`.

`grill-feature` needs `grilling` and `domain-modeling`, `implement` needs `tdd`, and `review` needs `code-review`, all from [mattpocock/skills](https://github.com/mattpocock/skills). Install them as his plugin:

```
/plugin install mattpocock-skills@claude-plugins-official
```

The skills call his by their plugin names (`mattpocock-skills:code-review` and so on). That matters for `code-review` in particular: Claude Code ships its own `code-review` under the bare name, a bug-hunting review without the Standards and Spec axes `review` is built on.

## Update

Third-party marketplaces don't auto-update by default. Pull the latest after a push:

```
/plugin marketplace update steine-skills
```

(Or enable auto-update for this marketplace in `/plugin` → Marketplaces — it then refreshes installed plugins at startup.)