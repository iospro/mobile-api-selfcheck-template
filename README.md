# mobile-api-selfcheck-template

Offline demo of mobile API contract selfchecks.

The template shows the same idea as the production `api-tests` project:

1. Read a test config from `test-configs/*.yml`.
2. Describe methods with `ApiMethodSpec`.
3. Validate method contracts from `contracts/methods/*.yml`.
4. Load fixed responses from local fixtures.
5. Parse `data/errors` envelope.
6. Validate payload as mobile DTOs expect it.
7. Print console report and write markdown report.

No network, tokens, product URLs or real customer data are used.

Note: `test-configs/default.yml` includes `base_url` and `pat_token_alias`
for config parity with production. In this offline template they are placeholders
and are not used for network/auth calls.

## Structure

```text
mobile-api-selfcheck-template/
  run_all.py
  test-configs/default.yml
  contracts/
    methods/
      chats/search.yml
      feed/list.yml
    dto/
      chat.yml
      feed_group.yml
  fixtures/
  domains/
  selfcheck/
```

## Run

```bash
python3 run_all.py --test-config default --scenario ok --trace
python3 run_all.py --test-config default --scenario dto-fail --trace
python3 run_all.py --test-config default --scenario envelope-error --trace
```

Custom report path:

```bash
python3 run_all.py --test-config default --scenario ok --report reports/ok.md
```

## Scenarios

- `ok` — all fixtures match DTO validators.
- `dto-fail` — envelope is valid, but nested DTO validation fails.
- `envelope-error` — API returns `errors` instead of `data`.

## Domains

- `Chats`: `GET /api/chats` with `limit`, `offset`, `queryString`.
- `Feed`: `POST /api/feed` with simple body (`limit`, `offset`).

## Config parity with production

- `base_url` — placeholder (`https://yoursite.ru`) for parity with real project config shape.
- `pat_token_alias` — placeholder alias (`YOURSITE_PAT_TOKEN`) for parity with PAT lookup flow.
- `report.path` and `domains.*` are used by the offline run.

See:

- `contracts/README.md`
- `test-configs/default.yml`
- `docs/dto_chats.md`
- `docs/dto_feed.md`
- `docs/architecture.md`
