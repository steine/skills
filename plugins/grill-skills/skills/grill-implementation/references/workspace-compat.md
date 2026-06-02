# Cross-workspace dependency-graph compat

Reference for the *Cross-workspace dependency-graph compat* lens. Load when a slice adds an import from a shared workspace lib that this consumer didn't previously pull through its barrel. Treat it as a **first-crossing** event: importing reshapes the graph the typechecker and bundler traverse, so latent mismatches dormant in static reads surface the moment a new path crosses the boundary.

## Watch for

- Mismatched runtime/types versions across workspaces (React 18 vs 19) deduped via npm hoist — the first stricter-consumer import surfaces cross-version type collisions tsc never visited.
- Shared lib shipping `.tsx` source vs a built `dist/` — `skipLibCheck` masks `.d.ts` only; sources get type-checked under the importer's stricter flags.
- The consumer's stricter tsconfig (`verbatimModuleSyntax`, `erasableSyntaxOnly`, `noUnusedLocals`) traversing into a lib not written for it.
- Peer deps the shared lib doesn't declare, relying on root hoist.

## Probe before signing off

Run a minimum-viable POC import + `npm run build` / `tsc -b` against the consumer. Static recon can't see what tsc refuses to compile once the graph shifts.

On collision, the options are:

- Unify versions monorepo-wide — a blocker slice.
- Ship `dist/` from the shared lib — a separate slice.
- Relax the consumer's tsconfig — local, loses strictness.
- Inline rather than import — local, duplicates.
