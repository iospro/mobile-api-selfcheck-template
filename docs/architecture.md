# Architecture

```text
run_all.py
  -> test-configs/default.yml
  -> contracts/methods/*.yml
  -> FixtureTransport
  -> domains/test_*.py
  -> ApiMethodSpec
  -> envelope parser
  -> DTO validators
  -> ConsoleReporter + MarkdownReporter
```

`test-configs/default.yml` intentionally keeps production-like keys
(`base_url`, `pat_token_alias`) for shape parity, even though offline transport
does not use network/auth.

The important part is that transport is replaceable. This demo reads fixtures,
but the same domain validators can be used with a real HTTP transport.

This demo keeps offline safety:

- no network calls;
- no state-changing write chains;
- deterministic fixtures for all scenarios.

Method contracts (`contracts/methods/*.yml`) are checked before DTO validation,
so structure drift is visible even in lightweight demo mode.
