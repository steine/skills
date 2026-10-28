---
name: review
description: "Review a finished implementation — your own branch before opening the PR, or someone else's PR. Runs the `code-review` skill (standards + spec, from Matt Pocock's suite), then presents the findings per axis with a recommendation on each — fix now, allow, verify first, or your call — so it's clear what to fix before the change goes in. Use when finalizing a branch before the PR, reviewing a teammate's PR, or when the user asks what still has to change."
---

<what-to-do>

Run the two-axis review, then say what each finding means for *this* change. A list of findings without recommendations leaves the reader to infer which ones matter — and a gap that should have been fixed now gets shipped as "non-blocking". Work through the steps below in order. The final call is the user's; the recommendations are yours.

`code-review` owns the findings. This skill owns presenting them and recommending, for each one, whether to fix it now or allow it into the codebase. Never add a finding of your own — not from earlier runs, not from your own reading of the diff. If the review missed something, that's a gap in `code-review`, not something to patch here.

</what-to-do>

<supporting-info>

## 0. Find the governing rules

Look for the repo's own review rules: anything in the agent instruction files (`AGENTS.md`, `CLAUDE.md`, files they link), `CONTRIBUTING.md`, or a workflow doc that says what must be fixed before a change ships. **Repo rules win over this skill** wherever they conflict. Everything below is the baseline for what the repo doesn't say.

## 1. Pin what's under review

- **Your own branch** (the default): the fixed point is the merge-base with the main branch, unless the user names another. Uncommitted changes count — ask the user to commit or stash them, or review them alongside.
- **Someone else's PR**: don't check it out over the user's work. Fetch its head as a ref (on GitHub, `git fetch origin pull/<n>/head:refs/remotes/pr/<n>`) and review `<base>...pr/<n>`. Read the PR description and the whole discussion: conversation comments, submitted reviews, and inline review threads, resolved ones included. On GitHub, `gh pr view <n> --comments` covers the first two; inline threads and their resolved state need the API, e.g. the GraphQL `reviewThreads` connection.

## 2. Run the review

Invoke the `code-review` skill with that fixed point and follow its process through both sub-agents and the two-axis report. If it isn't available, stop and tell the user it comes from [mattpocock/skills](https://github.com/mattpocock/skills).

Do **not** present `code-review`'s aggregate. Its two-axis report and closing summary are input to steps 3–5; step 5's layout replaces them.

## 3. Check findings before tagging them

Sub-agents can be wrong, and a fix-now tag costs real work. Before tagging:

- **Check against the code** any finding that would be fix-now: confirm the behaviour it claims. Drop it if the code says otherwise.
- **Check against what's already written** — the issue, the commit messages, and the PR description if there is one. Drop a finding they refute (an "unannounced" change that is announced, a path reported as verified).
- **Check against the PR discussion.** Match each finding to any comment or thread that already raised it, and show the link next to the finding:
  - *Answered* — a reply explains why it isn't a problem, and the code bears that out → drop it, citing the thread.
  - *Fixed* — a thread asked for it and a later commit did it → the code check above drops it.
  - *Punted* — someone agreed to defer it ("follow-up", "non-blocking", "out of scope") → still give it a recommendation. An earlier punt doesn't close a gap; if you recommend fix now, say that it disagrees with the punt in that thread so the user can decide with both in view.

  A comment raising something the review didn't find is not a finding here.
- **Keep** a finding that's merely acknowledged as a known limit. Writing a gap down doesn't close it; it still gets a recommendation.
- **Hold** a finding when the code and the written record disagree — the code supports it, but the PR description or a thread reports the opposite as tested. Neither wins; it becomes *Verify first* in step 4.

These checks can drop or hold a finding, never add one. Say which findings you dropped and why, in one line each.

## 4. Give every finding one recommendation

- **Fix now** — the finding falls within the issue's stated purpose **and** the fix is cheap. This includes:
  - a gap against the purpose itself, not just the listed requirements. If the issue says the change *replaces* something (a manual check, an old path), anything that lets the replacement silently cover less than what it replaces is in scope;
  - a breach of a documented repo standard;
  - a claim the change makes false — in a README, a runbook, a PR description. A list that's merely incomplete isn't false.

  "The failure is unlikely", "rare in practice" and "strictly better than before" are **not** reasons to downgrade. If it's in purpose and cheap, it's fixed now.
- **Allow** — the default, left unmarked in the output: let it into the codebase as it is: judgement calls, baseline smells, naming, helper shape, a known limit nothing can fix (say why). When it's a real gap outside the issue's purpose, add a proposed ticket: title and one-line scope.
- **Verify first** — a held finding from step 3. Name the one check that settles it and what the recommendation becomes either way.
- **Your call** — in purpose but not cheap. Lay out the two options — fix now, or cut it into a ticket (proposed title) — and don't decide it yourself.

A finding can carry two when it splits — e.g. *Fix now* for a false README claim plus *Your call* for the stricter check behind it.

## 5. Present per axis

Keep the axes apart so the reader stays in one kind of problem at a time: all of Standards, then all of Spec. Inside each axis, group and order findings by the severity label `code-review`'s sub-agent gave them (hard violation, missing, looks wrong, judgement call, nit — whatever it used). Don't re-grade them; severity is the review's, the recommendation is yours.

```markdown
**Review: <PR n or branch> · <issue id> <issue title>**
`<fixed point>...<head>` · <n> commits · <n> files · <n> threads read

# Standards
**<severity label>**
- **S1** <finding, one line>. `<file:line>`
- **S2** …

**<next severity label>**
- …

**Dropped:** <id> <finding> (<reason or thread link>) · …

# Spec
**<severity label>**
- **P1** <finding, one line>. `<file:line>`
  → **Fix now:** <what to change>
  → **Your call:** <option A>, or ticket "<title>"
- **P2** <finding, one line>. `<file:line>` · [thread](<link>)
  → **Verify first:** <check>. <outcome if X → recommendation>; <outcome if Y → recommendation>.

**Dropped:** <id> <finding> (<reason or thread link>) · …

# Next
**Fix now:** <ids, Standards first, joined by ` · `>
**Verify first:** <ids> (<the check>)
**Your call:** <ids>

<one or two lines — see below>
```

- **The axis heading is only the axis name** — no verdict or counts under it; Next carries the totals. An axis with no findings at all is the heading plus "No findings."
- **One line per finding**, plus a `file:line` or thread link. A finding with no `→` line is allowed — don't print *Allow*. Add a short reason in parentheses only when allowing something the issue asked for. *Fix now*, *Verify first*, *Your call* and a proposed *Ticket* go on indented `→` lines.
- **Emit the template as rendered markdown**, not inside a code block, and never as tables — tables squeeze the finding text and push the recommendation out of reading order. Each axis is the only top-level heading, so the reader sees where one kind of problem ends and the next begins; no `---` rules, they add clutter. The review title stays a bold line so it doesn't compete with the axes.
- **Cut "no problem" text.** No met requirements, passing standards, "done well" notes or scope checks that found nothing — only findings and their recommendations.
- **Dropped findings** close their own axis in one line, each with its reason, so the reader can see nothing went missing. Leave the line out when the axis dropped nothing.
- **Next** is its own section after both axes — it's about the whole review, not one axis. It opens with the action list: one line per group (*Fix now*, *Verify first*, *Your call*), finding ids only, Standards ids before Spec ids, joined by ` · ` — no bullets. Leave out a group with no ids; if all three are empty, the line is "**Fix now:** nothing". The reasons and exact changes stay on the findings; Next only points to them.
- Notes on how this skill or `code-review` performed don't belong in the review. Raise them separately if at all.

**Next** depends on whose change it is:

- **Your own branch** — offer to apply the fix-now items. Anything the user accepts as a known limit goes into a ready-to-paste *Limits* section for the PR description.
- **Someone else's PR** — fix-now items and proposed tickets go in the review comment. Direction-level ideas (a different overall approach, a shared abstraction elsewhere) go in a **separate** comment marked non-blocking, so they read as context rather than added scope. The author owns their issue and PR; whether to accept a proposal, and any tracker updates, are theirs. If the PR is already merged, fix-now items become a fix-up PR. Confirm with the user before posting anything.

</supporting-info>
