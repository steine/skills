---
name: implement
description: "Implement a piece of work based on a spec or set of tickets, commit it, then run review on it and fix what it says must be fixed now."
disable-model-invocation: true
---

Implement the work described by the user in the spec or tickets.

If the user passes a ticket reference, fetch it from the issue tracker and state its title before starting. If the reference is ambiguous, ask.

Note the current `HEAD` before starting; it is the fixed point for the review.

Use Matt's `tdd` skill (`mattpocock-skills:tdd` when installed as his plugin) where possible, at pre-agreed seams.

Run typechecking regularly, single test files regularly, and the full test suite once at the end.

Commit your work to the current branch. Commit before reviewing: the review only sees commits.

Then use /grill-skills:review against that fixed point. Apply every *Fix now* item, commit, and re-run the review until none remain. Stop and ask the user about any *Verify first* or *Your call* item. Leave *Allow* findings as they are.

Adapted from the `implement` skill in [mattpocock/skills](https://github.com/mattpocock/skills) (MIT).
