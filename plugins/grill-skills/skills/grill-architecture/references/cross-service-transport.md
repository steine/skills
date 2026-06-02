# Cross-service transport shape

Reference for the *Challenge cross-service transport shape* lens. Load when a slice introduces an HTTP / RPC / queue hop between two services **in the same repo**. Grill three coupled dimensions: request shape, contract location, failure mode on rename.

## Request shape

- `[FromBody]` record — JSON property binding; a missing required field on a non-nullable record param fails loudly with a 400.
- Query-string scalars — name-based binding; missing or misnamed parameters silently bind to `default` (`Guid.Empty`, `null`, `0`). Silent no-ops in production.
- Path parameters with route constraints (`{id:guid}`) — malformed / missing values 404 at routing time.

## Contract location

- Caller-owned — each side defines its own DTO; JSON aligns at the wire. Cheap, no compile-time enforcement.
- Callee-owned — server publishes a Contracts project; caller depends on it. Rename breaks the build on both sides.
- Shared in `Common.*` — everyone imports. Tempting but erodes service boundaries; usually wrong for directed RPC.

## Failure mode on rename

Compile error (typed contract package) > test failure (record + integration test) > runtime trace (record + unit-test-only) > silent no-op (string-concat URL or scalar param). Lower-numbered modes are categorically better; design for compile-time when the surface will grow.

## Watch for

- Reusing a legacy user-route's query-string + scalar shape for a new service-to-service route in the same controller class. The two routes share class real estate but serve different callers (XHR-from-MVC vs typed HttpClient), different auth contexts, different blast radii. Inheritance of shape is path-dependence.
- Hand-rolled URL strings in HTTP clients (`$"/path?id={x}&name={y}"`) — each literal is a free-floating contract assumption; renames on the server don't ripple back to the client.
- "Match the existing controller's shape" recommendations without distinguishing whether the existing shape is *load-bearing for legacy callers* (back-compat) vs. *accidental* (legacy choice that doesn't need to propagate).
- Test fakes that short-circuit the transport (e.g. a hand-rolled `Recording*HttpClient` mocking the typed-client interface) — they let wire-shape bugs ship because the unit test doesn't exercise the URL/body construction. Pair with at least one `WebApplicationFactory` integration test.

## Recommendation skew

For new internal-service routes, default to `[FromBody]` records over query-string scalars; defer shared-contract package extraction until the 2nd or 3rd hop, but pre-design for it (records on both sides, same shape, ready to consolidate). Never auto-resolve in favour of inheriting the legacy sibling route's shape.
