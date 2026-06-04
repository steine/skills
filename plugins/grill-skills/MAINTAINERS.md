# Maintaining grill-skills

Audience: maintainers and agents **editing** these skills. To *invoke* a skill, read its `SKILL.md` instead — this doc is about how the skills are built and how to change them safely.

## 1. Architecture: spine + packs

Each skill is a stack-agnostic **spine** (its `SKILL.md`) plus per-stack **packs** (`references/stacks/*.md`).

- The **spine** carries each lens's *principle* — stack-neutral, e.g. "a read should move only what the consumer uses."
- A **pack** carries the concrete *tells* for one stack — e.g. `.AsNoTracking()` / `[Projectable]` for .NET, `res.json() as T` for TS.
- Packs **compose** one level deeper for front-ends: a **language pack** (`ts.md`) + a **framework overlay** (`react.md` / `angular.md`), loaded together.

Recursion: `spine → language pack → framework overlay`. The spine says *what to check*; the pack says *what it looks like here*.

**Loading.** The spine detects the stack during recon and reads the matching pack(s): `*.csproj`/`*.sln` → `dotnet.md`; `tsconfig.json` / front-end `package.json` → `ts.md` + an overlay (`react` dep → `react.md`, `@angular/core` → `angular.md`); `Gemfile` → `ruby.md`; `go.mod` → `go.md`. A repo spanning back-end + front-end loads two.

## 2. Two skills, two altitudes

| | `grill-architecture` | `grill-implementation` |
|--|--|--|
| Altitude | hard-to-reverse decisions | reversible, slice-local mechanics |
| Output | revised plan + **ADRs** | **fix-now list** (no ADRs) |
| Packs | architecture lenses | implementation lenses |

Firewall: codebase-wide consolidation is **neither** skill's job — it's punted up to `improve-codebase-architecture`. `grill-implementation` stays inside one slice; if a decision there feels ADR-worthy, it belonged to `grill-architecture`.

The front-end layering the spine re-anchors onto: `presentation ← view-logic ← state (server/client) ← domain ← transport ← shared` (dependencies point down).

## 3. ⚠️ Invariants — break these and it ships broken

- **Self-containment.** Each skill owns its OWN `references/stacks/`. A `SKILL.md` reference resolves relative to *that skill's own directory*, loaded on demand; cross-directory references (a sibling skill OR a plugin-root shared dir) are undocumented and **break when the plugin is installed from a marketplace**. Never link `../other-skill/...` or a plugin-root path — only `./references/...`.
  - **Corollary — do NOT "DRY" the packs.** The `dotnet.md` / `ts.md` tells are *intentionally* restated in both skills (one architecture pack, one implementation pack). The handful of idioms duplicated across the two (e.g. `CancellationToken`, DTO shape) is the accepted cost of self-containment. A single "shared pack" file is the exact bug already removed once — don't reintroduce it.
- **Domain-agnostic.** No org / product / system names anywhere — these skills ship to other teams. Evals use fictional `Acme.*`. When a real-world finding motivates a lens, encode the *generic pattern*, never the specific instance.
- **Taxonomy = stack axis only.** One pack per stack. A front-end/back-end split was considered and rejected: tier equals stack only by org coincidence (mono-stack), it re-binds the skills to one org's stack choices, and it keeps the irreducible per-stack axis underneath anyway.
- **`N/A` over force-fit.** If a lens doesn't bind to a stack or a slice, say `N/A` with a one-line reason. Don't invent a tell to fill a section.

## 4. Adding a stack

1. Write **two** files: `grill-architecture/references/stacks/<stack>.md` (architecture lenses) and `grill-implementation/references/stacks/<stack>.md` (implementation lenses). Use `dotnet.md` as the worked reference for both.
2. Wire **detection** in both `SKILL.md`s — marker file → pack link, using `./references/stacks/...` only.
3. **Stub-then-fill.** Seed a few real tells per lens, mark `> **Status: stub.**` with `<!-- TODO -->` markers, and fill from real grills before relying on it. `ruby` / `go` are stubs today; `angular` is a stub overlay.
4. Front-end stack with more than one framework sharing the language? Split into a language pack + framework overlay (see `ts.md` + `react.md` / `angular.md`).

## 5. How the skills are improved

- **Evals.** Each skill has `evals/evals.json` (positive cases the grill *should* catch). `grill-implementation` also has `evals/evals-negative.json` (traps it should *not* over-fire on — e.g. scope-creep that should be punted, not ballooned). **Add an eval whenever you add a lens.** Run them via the `skill-creator` eval harness.
- **The meta-method (how this set was built and should keep growing):** grill **real merges** in a target repo to find where a skill stays silent or cargo-cults a bad precedent; isolate the *generic* pattern behind the miss; encode it as a spine principle + pack tells + an eval. A new lens must **earn its noise** — most of the time conforming to clean precedent is correct, so verify that conforming was the *wrong* call in the motivating case before adding the lens. (The cross-boundary contract-drift lens came from exactly this loop.)
