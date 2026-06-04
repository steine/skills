# skills

Architectural grills for Matt Pocock's engineering skill suite.
I use Matt's skill suite extensively in my workflow, but I felt the architectural dimension was sometimes lacking in the result. 

## Origin & when to use

These extend [Matt Pocock's engineering skill suite](https://github.com/mattpocock/skills) (`grill-with-docs`, `to-prd`, `to-issues`) in the architectural dimension.

The two skills live in two different phases:

### Refinement → Definition of Ready

```
grab PBI → /grill-with-docs → /grill-architecture* → /to-prd → /to-issues
```

- **`grill-architecture`** ← *macro lenses.* Pressure-test the cross-cutting decisions — naming, layering, folder placement, port shape, config flow — and land ADRs so every issue inherits settled architecture.

### Sprint / implementation → per slice, per dev

```
grab issue → /grill-implementation → implement → [/grill-implementation on the diff] → PR
```

- **`grill-implementation`** ← *micro lenses.* At issue pickup, once the architecture is settled, vet the slice's concrete mechanics — reuse of existing affordances, read-path minimalism, spec-gaps, impact sweep, cross-boundary contract drift.


## What's in it

One plugin, **grill-skills**, bundling two skills that are a deliberate split of one concern:

| Skill | Altitude | When | Output |
|-------|----------|------|--------|
| `grill-architecture` | Macro — hard-to-reverse decisions | Refinement, before `to-prd` | Revised plan + **ADRs** |
| `grill-implementation` | Micro — reversible per-slice mechanics | Sprint, at issue pickup (opt. pre-PR) | **Fix-now list** (no ADRs) |

Both pressure-test against the codebase via composable per-stack packs (.NET + TS/React; Angular/Ruby/Go stubs). For the internal structure and how to extend it, see [plugins/grill-skills/MAINTAINERS.md](plugins/grill-skills/MAINTAINERS.md).

## Install

```
/plugin marketplace add steine/skills
/plugin install grill-skills@steine-skills
```

Skills are then invoked namespaced: `/grill-skills:grill-architecture`, `/grill-skills:grill-implementation`.

## Update

Third-party marketplaces don't auto-update by default. Pull the latest after a push:

```
/plugin marketplace update steine-skills
```

(Or enable auto-update for this marketplace in `/plugin` → Marketplaces — it then refreshes installed plugins at startup.)