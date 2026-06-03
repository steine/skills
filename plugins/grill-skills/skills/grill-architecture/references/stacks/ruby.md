# Stack pack: Ruby / Rails — STUB

> **Status: stub.** Seeded with a few real tells per lens so the structure (and the bite) is visible, but not yet battle-tested. Fill in from real Rails-codebase grills before relying on it; mark a lens `N/A` if the target codebase doesn't adopt the relevant layering. See `dotnet.md` for the worked reference.

Layering note: Rails has no enforced Domain/Application/Infrastructure split. Many apps are MVC-with-fat-models or service-object layered (`app/services`, `app/adapters`). The lens still applies *if* the codebase has adopted a layering; if it's deliberately flat MVC, say so per lens rather than force-fitting.

## Naming vs responsibility

- A `FooClient` class doing HTTP *and* domain mapping, consumed directly instead of injected — the duck-typed "port" is the collaborator you pass in; name it for the role (`FooGateway`), keep transport vocab on the adapter.
- A `FooService` god-object that's really several responsibilities. <!-- TODO: more tells -->

## Folder placement

- Service objects dumped in one fat `app/services/` bucket vs grouped by domain concept. <!-- TODO: dominant-convention detection in Rails repos -->
- Mixing concerns into `app/models/` (fat models) vs extracting. <!-- TODO -->

## Layer assignment

- ActiveRecord callbacks (`after_save`, `after_commit`) hiding persistence side-effects and policy inside the model — the Rails analogue of "persistence side-effects in the adapter". <!-- TODO -->
- Business policy in controllers instead of a service/interactor. <!-- TODO -->

## Value-type placement

- An enum (`enum status: {...}`) backing a DB column defined inline on the model — usually fine in Rails (model *is* the domain), but a shared value concept (Money) duplicated across models should be a value object (`app/values`). <!-- TODO -->

## Port shape

- Cancellation/deadline idiom: Ruby has no `CancellationToken`/`context` — it's `Timeout.timeout` / explicit timeout args / the HTTP client's own timeout. Flag unbounded external calls. <!-- TODO -->
- Parameter shape: primitive id vs domain object passed to the collaborator distributes lookup/mapping the same way as elsewhere. <!-- TODO -->

## Config and secret flow

- Config sprinkled via `ENV[...]` reads deep in classes vs centralized (`Rails.application.config` / `config/settings.yml`). <!-- TODO -->
- Secrets in `config/*.yml` plaintext vs Rails credentials / encrypted secrets / Vault. <!-- TODO -->

## Cross-service transport

- Hand-built URL strings in a `Net::HTTP`/Faraday call; no typed contract (Ruby has no compile-time check — the failure-mode ladder bottoms out at runtime/test, so an integration/contract test is the only guard). <!-- TODO: contract-location options in a Ruby monorepo -->
