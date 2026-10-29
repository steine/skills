---
name: grill-feature
description: "Feature-level pressure-test of a stakeholder ask, the first step of refinement. Fleshes out what is asked and why, pins scope (in, and explicitly out), splits the feature into user stories by user value and drafts testable acceptance criteria per story, in the project's domain language. Runs a grilling session with the domain-modeling skill, but stays in the problem space: architecture questions (layers, type names, ports, config, transport) are parked for grill-architecture and implementation questions (reuse, queries, error contracts, tests) for grill-implementation. Use when a backlog item or stakeholder request needs fleshing out before grill-architecture. Output: goal, scope, story split with acceptance criteria, glossary updates, open stakeholder questions and parked questions, drafted onto the feature ticket. No ADRs."
---

<what-to-do>

Grill the user about the stakeholder's ask until the feature is clear enough to architect: what problem it solves and for whom, what is in and out of scope, which user stories it breaks into, and how anyone will know each story is done.

Invoke the `grilling` skill for the session mechanics and the `domain-modeling` skill for the glossary, both from [mattpocock/skills](https://github.com/mattpocock/skills) — `mattpocock-skills:grilling` and `mattpocock-skills:domain-modeling` when installed as his plugin — and follow both. Where they conflict with the scope rules below, the scope rules win. Use Matt's: another source may ship a skill under the same name (`anthropic-skills:grilling`, say) with a different session format, and it is not a substitute. If his aren't available, stop and tell the user where they come from.

This is the problem space. How the feature gets built has its own skills, later in refinement and in the sprint. Don't grill it here.

</what-to-do>

<supporting-info>

## Recon

Before the first round:

1. **The ask.** The backlog item, its parent epic, linked stakeholder notes. Note who asked, and in which words. Asks vary in quality — a one-liner is a starting point, not a gap to complain about.
2. **The glossary.** `GLOSSARY.md` (or `GLOSSARY-MAP.md` and the context it points to); repos set up before domain-modeling renamed it use `CONTEXT.md` / `CONTEXT-MAP.md` — use whichever exists. Note terms the ask uses that conflict with it or are missing from it.
3. **Current behaviour.** What the system does today in the area the ask touches, as observable behaviour — enough to tell what the ask changes. Read code for facts, not for design.
4. **Similar past work.** Earlier features and stories in the same area of the tracker: how their goals and scope were cut, how big their stories were, what their acceptance criteria looked like. Draft from them where they fit.
5. **The tracker's templates.** If the team has a feature or story template, read it now: its sections are where the output goes, and any notes on who writes what bind you.

## What to grill

- **Problem and outcome.** Who has the problem, what they do today, what changes for them once it ships. An ask phrased as a solution ("add a button that…") is traced back to the need behind it; the solution stays a candidate, not a given.
- **Scope.** What's in, and what's explicitly out. Write down every exclusion a reader might otherwise assume is included — the explicit no's are what stop scope creep at the PR.
- **Edge-case scenarios.** domain-modeling's scenario probing: each scenario that settles a boundary becomes an acceptance criterion or an out-of-scope line.
- **Domain language.** Per domain-modeling: challenge fuzzy and conflicting terms, update the glossary inline. A term in the ask that is ambiguous, overloaded or in conflict with the glossary is a root of the tree — every criterion downstream is written in it — so grill it in the first round, alongside the problem question, not at the end.

## Split into stories

Once scope settles, break the in-scope part into user stories. Each story is a slice of value a user or operator can see, that can be accepted on its own.

- **Slice by user value, never by layer.** A story named for a layer or a technology ("API for pausing", "pause button", "database column for paused state") is architecture leaking in. Re-cut it into slices that each deliver something observable end to end.
- **One story, one outcome.** If a story's acceptance criteria describe two outcomes a user could get separately, it's two stories. If a story can't be accepted until another ships, say so — it may belong with that one.
- **Not too small either.** A story that nobody would accept or demo on its own is a task. Fold it into the story it serves.

For each story, draft acceptance criteria. Each one observable by someone using or operating the system, stated in domain terms, and checkable: a reader can say pass or fail. Use Given/When/Then where the repo or tracker does. Watch for:

- a criterion that can't fail ("works correctly", "is user-friendly", "handles errors gracefully")
- a criterion that names a solution (an endpoint, a table, a component) instead of a behaviour
- a criterion that checks internal state (a stored field, a flag, a date the system computes) instead of what someone sees — it smuggles a data model into the story
- a criterion that restates the story or the goal instead of saying how to check it
- a happy path with no criterion for the edge cases the scenarios surfaced

The split is a draft. `grill-architecture` may re-cut it — an enabling story a decision requires, two stories that must ship together — and it edits the split directly rather than sending it back here, then creates the story tickets.

## Stay in the problem space

Out of scope here, whoever raises it:

- **Architecture** — layer ownership, type and module names, folder placement, ports and contracts, config flow, service-to-service transport, technology choice, cross-system dependencies → `grill-architecture`.
- **Implementation** — reuse of existing code, query shape, error and result contracts, cancellation, test design, migration mechanics → `grill-implementation`.

When one of your questions or one of the user's remarks lands there, don't ask it and don't answer it: add it to the parked list with one line of context and carry on with the frontier. If the user pushes, say which skill will take it up.

Two things look like solution talk but belong here:

- **A stakeholder-mandated constraint** ("must go through the existing payment provider", "has to work offline in the field app") is scope. Record it as a constraint, not a parked question.
- **What the system does today** is a fact, not a design. Establish it from the code, per domain-modeling's cross-reference with code.

**No ADRs.** domain-modeling offers them; here, decline. What was asked belongs in the ticket, what a term means belongs in the glossary, and a hard-to-reverse technical decision is architecture — park it.

## Who decides

Product decisions — the goal, the scope cut, the story split, what counts as done — are the stakeholder's and the team's. Everything you write is a draft for them to edit or approve; mark it as one. When the user can't answer a question, don't settle it for them: record it as an open stakeholder question with your recommended answer, and keep going with the rest of the frontier. A criterion that depends on an open question is marked provisional and names that question — otherwise your recommendation reads as settled, and the stakeholder's decision gets made by whoever reads the story first.

## Closing the session

Produce:

1. **Goal** — the ask in one to three sentences of domain language: who, what changes, why.
2. **Scope** — in; out (the explicit no's); constraints.
3. **Stories** — each with a one-line title, its numbered acceptance criteria, and where it sits in delivery order: which stories it needs first, or that it stands alone. Every story gets that line, not just the ones with a dependency — the order is what the team plans the sprint from.
4. **Glossary changes** — terms added to or changed in the glossary.
5. **Open stakeholder questions** — each with your recommended answer.
6. **Parked** — split into *for grill-architecture* and *for grill-implementation*.

Then offer to draft it onto the feature ticket. If the team has a feature template, fill its sections rather than this list's shape: goal and scope in theirs, the parked architecture questions in its architecture section if it has one. The story split — each story's title, acceptance criteria and parked implementation questions — goes on the feature too, marked as a draft. Don't create story tickets yet: `grill-architecture` may still re-cut the split, and tickets created now would have to be edited, merged or deleted. It creates them once the split is settled. Show the user the edit and get a yes before changing the ticket.

Then offer `grill-architecture`, or stop. If the user says there's nothing architectural to settle, offer to create the story tickets now instead — from the team's story template if it has one, each with its acceptance criteria and parked implementation questions, after a yes.

</supporting-info>
