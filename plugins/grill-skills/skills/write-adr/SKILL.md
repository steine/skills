---
name: write-adr
description: Write, supersede, or retire an Architecture Decision Record. Use whenever anything under an ADR folder (e.g. `docs/adr/`) is created or changed, when the user asks to record a decision, or when another skill (e.g. grill-architecture) settles a decision that might deserve an ADR. Gates whether the decision is ADR-worthy at all, keeps each record to one decision on about one page, supersedes instead of editing accepted records, and self-reviews the draft against known ADR anti-patterns before showing it.
---

<what-to-do>

Turn one settled decision into one short, durable record — or conclude that it isn't an ADR and say where it belongs instead. Work through the steps below in order. Ask the user whenever a step needs a judgement; the decision and its acceptance are theirs, the drafting is yours.

</what-to-do>

<supporting-info>

## 0. Find the governing rules

Before anything else, look for the repo's own ADR rules: a `README.md` in the ADR folder, and any ADR guidance in the agent instruction files (`AGENTS.md`, `CLAUDE.md`, files they link). **Repo rules win over this skill** wherever they conflict — numbering format, status vocabulary, frontmatter fields, glossary conventions. Everything below is the baseline for what the repo doesn't say.

Then read the accepted ADRs that touch the same area. You need them for step 3.

## 1. Gate — is this an ADR at all?

All three must hold. Put them to the user as questions, with your read of each:

1. **Hard to reverse** — changing course later costs something real (data already shaped by it, external systems depending on it, a quarter of rework).
2. **Surprising without context** — a reasonable reader would assume the opposite, or look at the result and ask "why on earth like this?"
3. **A real trade-off** — there were genuine alternatives, and this one won for stated reasons.

If any fails, it is not an ADR. Say where the content belongs instead: the PR description (how it was built), the ticket (what was asked), the domain glossary (what a term means now), or the code itself (a name, a type, a test). A decision that is easy to reverse gets reversed, not recorded.

What typically qualifies: architectural shape, integration patterns between contexts, technology with lock-in, ownership and boundary calls (the explicit no's too), deliberate deviations from the obvious path, constraints invisible in the code, and rejections a future reader would otherwise re-propose.

What typically doesn't: a helper's placement, a naming rule local to one module, a UI affordance, a validation message, a bug fix, the mechanics of one slice.

## 2. One decision per record

Write the decision as a single "We will …" sentence. If you need two sentences on unrelated subjects, you have two ADRs — split them and gate each separately.

Signals of a bundled record: a Decisions list whose bullets could each be reversed independently; a title joined by "and"; sections on schema, handlers, UI and auth in one file. Bundles are what later force partial supersession — split now so each piece can be replaced on its own.

## 3. Relate it to what exists

Decide which case applies and tell the user:

- **New** — nothing accepted covers it.
- **Replaces an accepted ADR wholesale** — write the new record, and set the old one's frontmatter to `status: superseded by ADR-NNNN`. That status line is the only edit to the old file.
- **Replaces part of an accepted ADR** — treat this as a smell: the old record bundled decisions. Prefer superseding it wholesale and briefly restating, in the new record or in separate new records, the parts that still hold. Only if that is disproportionate, leave the old one `accepted` and add `superseded-in-part-by: [ADR-NNNN]` to its frontmatter, with the new record naming exactly which of its decisions it replaces.
- **No longer relevant, nothing replaces it** — `status: deprecated`, with one line saying why.

Never edit an accepted record's body to reflect a later change, and never add "Amended by" banners. In-place edits are only for what was wrong on the day it was written — a typo, a broken link. The set of accepted records should read as the current truth without following chains.

## 4. Write it

```md
---
status: proposed
---

# {The decision, stated as a claim}

{Context: the forces at play — one short paragraph. What made this a question now.}

{Decision: "We will …" in full sentences, active voice. Why this option won.}

## Considered alternatives

{Only real ones, each with why it lost. Omit the section if the rejection is obvious.}

## Consequences

{What becomes easier and what becomes harder — the costs, not just the wins.}
```

- **Length.** Aim for well under a page. A single paragraph is a valid ADR. Going past a page needs a reason — a genuinely wicked problem — not thoroughness.
- **Decisions, not specs.** No code blocks, schema DDL, route/handler/file listings, test names, migration steps, or Added/Changed/Removed changelogs — the code, its tests and the PR carry those exactly and won't drift. Name a concrete identifier only when the identifier itself *is* the decision (a column's nullability, an endpoint's verb, which system owns a record).
- **Domain language.** If the repo has a glossary, use its terms and avoid the synonyms it rules out.
- **Journal voice.** Record what was decided and why, as a team would tell it. Avoid a rulebook tone of "must" and "never" unless the constraint itself is the decision.
- **Status.** Draft as `proposed`. Set `accepted` only after the user has confirmed the decision.
- **Numbering.** Highest existing number plus one, unless the repo says otherwise. Rescan right before merging — a concurrent branch may have taken it. Never renumber or rename after merge.

If the repo has a glossary that restates the decision (or the one it replaces), update the fact there and repoint its citation. The glossary states current behaviour; it must not keep a claim the new record just reversed.

## 5. Self-review before showing it

Check the draft against each anti-pattern and fix before presenting:

| Anti-pattern | Check |
|---|---|
| **Mega-ADR / Maze** | One decision, one topic. No detail dump the code already shows. |
| **Blueprint or policy in disguise** | Reads as a decision journal, not a manual or a law. |
| **Fairy tale / Free lunch** | Consequences include real costs. |
| **Sprint / Dummy alternative** | Alternatives are ones someone would actually propose — or the section is omitted with good reason. |
| **Sales pitch** | No unsupported superlatives; claims are factual. |
| **Stale neighbour** | Every accepted record this one contradicts is superseded or marked in part. |

Then show the user the draft, the relation outcome from step 3 (which files change status), and the glossary edits, in one message. Write nothing until they confirm.

## Sources

- Nygard, *Documenting Architecture Decisions* (2011) — one or two pages; supersede, don't rewrite.
- Fowler, *Architecture Decision Record* — typically a single page; accepted records are never reopened.
- Zimmermann, *How to create ADRs — and how not to* (2023) — the anti-pattern catalogue used in step 5.

</supporting-info>
