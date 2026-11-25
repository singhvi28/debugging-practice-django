# Buglyst Medium — Django Mini-Labs

Tiny Django practice labs adapted from the FastAPI versions in the parent repo's [`buglyst-medium/`](../../buglyst-medium/). Each folder plants **one bug**; pytest asserts the correct behavior.

Source questions: [QUESTIONS.md](QUESTIONS.md).

## How to run a lab

Prefer the shared parent `.venv` — do **not** create a venv per lab:

```bash
cd labs/<lab-folder>
pip install -r requirements.txt   # once, into the shared env
pytest -v
```

Fix the code until tests pass. No answer keys.

## Labs

| ID | Folder | Title |
|----|--------|-------|
| 04 | [labs/004-accessdenied-at-3am](labs/004-accessdenied-at-3am) | AccessDenied at 3AM |
| 05 | [labs/005-silent-timeout](labs/005-silent-timeout) | The Silent Timeout |
| 06 | [labs/006-cache-stampede](labs/006-cache-stampede) | Cache Stampede |
| 07 | [labs/007-nplus1-that-wasnt](labs/007-nplus1-that-wasnt) | The N+1 That Wasn't |
| 09 | [labs/009-flaky-retry](labs/009-flaky-retry) | The Flaky Retry |
| 11 | [labs/011-timezone-trap](labs/011-timezone-trap) | The Timezone Trap |
| 14 | [labs/014-cors-origin-parsing](labs/014-cors-origin-parsing) | CORS origin parsing bug |
| 16 | [labs/016-stale-confirmation](labs/016-stale-confirmation) | The stale confirmation |
| 19 | [labs/019-log-ate-the-request](labs/019-log-ate-the-request) | The log that ate the request |
| 21 | [labs/021-permission-outlived-user](labs/021-permission-outlived-user) | The Permission That Outlived the User |
| 22 | [labs/022-invoice-forgot-quantity](labs/022-invoice-forgot-quantity) | The Invoice That Forgot Quantity |
| 23 | [labs/023-file-left-the-vault](labs/023-file-left-the-vault) | The File That Left the Vault |
| 24 | [labs/024-dashboard-averaged-averages](labs/024-dashboard-averaged-averages) | The Dashboard That Averaged Averages |
| 26 | [labs/026-header-vanished-mid-flight](labs/026-header-vanished-mid-flight) | The Header That Vanished Mid-Flight |
| 27 | [labs/027-query-loaded-the-world](labs/027-query-loaded-the-world) | The Query That Loaded the World |
| 28 | [labs/028-event-fired-twice](labs/028-event-fired-twice) | The Event That Fired Twice |
| 29 | [labs/029-config-swallowed-prod](labs/029-config-swallowed-prod) | The Config That Swallowed Prod |
| 30 | [labs/030-filter-swallowed-false](labs/030-filter-swallowed-false) | The Filter That Swallowed False |
| 31 | [labs/031-token-never-expired](labs/031-token-never-expired) | The Token That Never Expired |
| 32 | [labs/032-redirect-left-the-building](labs/032-redirect-left-the-building) | The Redirect That Left the Building |
| 33 | [labs/033-rate-limit-counted-everyone](labs/033-rate-limit-counted-everyone) | The Rate Limit That Counted Everyone |
| 34 | [labs/034-lock-never-let-go](labs/034-lock-never-let-go) | The Lock That Never Let Go |
| 35 | [labs/035-webhook-trusted-silence](labs/035-webhook-trusted-silence) | The Webhook That Trusted Silence |
| 39 | [labs/039-payment-dedupe-amount-mismatch](labs/039-payment-dedupe-amount-mismatch) | Payment dedupe ignores amount mismatch |
| 40 | [labs/040-dedupe-cache-evicts-eagerly](labs/040-dedupe-cache-evicts-eagerly) | Dedupe cache evicts too eagerly |
| 41 | [labs/041-webhook-signature-tolerance](labs/041-webhook-signature-tolerance) | Webhook signature tolerance too wide |
| 42 | [labs/042-idempotency-fingerprint-key-order](labs/042-idempotency-fingerprint-key-order) | Idempotency fingerprint key-order sensitive |
| 49 | [labs/049-backoff-overflow](labs/049-backoff-overflow) | Backoff Overflow at High Attempts |
| 50 | [labs/050-jitter-can-go-negative](labs/050-jitter-can-go-negative) | Jitter Can Go Negative |
| 51 | [labs/051-retry-budget-shared](labs/051-retry-budget-shared) | Retry Budget Shared Across Callers |
| 52 | [labs/052-circuit-half-open-floods](labs/052-circuit-half-open-floods) | Circuit Half-Open Floods Requests |
| 58 | [labs/058-negative-cache-poisoning](labs/058-negative-cache-poisoning) | Negative cache poisoning |
| 59 | [labs/059-swr-serves-stale-forever](labs/059-swr-serves-stale-forever) | Stale-while-revalidate serves stale forever |
| 60 | [labs/060-lru-evicts-wrong-tenant](labs/060-lru-evicts-wrong-tenant) | LRU evicts the wrong tenant |
| 61 | [labs/061-tenant-prefix-skipped-on-read](labs/061-tenant-prefix-skipped-on-read) | Tenant prefix skipped on read |
| 69 | [labs/069-two-for-one-email](labs/069-two-for-one-email) | Two For One Email |
| 70 | [labs/070-lock-wrong-axis](labs/070-lock-wrong-axis) | Lock Around the Wrong Axis |
| 71 | [labs/071-order-stayed-open](labs/071-order-stayed-open) | The Order That Stayed Open |
| 72 | [labs/072-phantom-read](labs/072-phantom-read) | The Phantom Read |
| 79 | [labs/079-token-bucket-refills-every-request](labs/079-token-bucket-refills-every-request) | Token bucket refills on every request |
| 80 | [labs/080-preflight-omits-expose-headers](labs/080-preflight-omits-expose-headers) | Preflight omits Access-Control-Expose-Headers |
| 81 | [labs/081-rate-limit-bucket-shared](labs/081-rate-limit-bucket-shared) | Rate-limit bucket shared across users |
| 82 | [labs/082-cursor-non-unique-column](labs/082-cursor-non-unique-column) | Cursor built from a non-unique column |
| 88 | [labs/088-dotenv-empty-string-truthy](labs/088-dotenv-empty-string-truthy) | Dotenv Empty String Truthy |
| 89 | [labs/089-frozen-config-at-import](labs/089-frozen-config-at-import) | Frozen Config At Import Time |
| 93 | [labs/093-region-fallback-shadow](labs/093-region-fallback-shadow) | Region Fallback Shadow |
| 94 | [labs/094-migrate-skips-on-equal-version](labs/094-migrate-skips-on-equal-version) | Migrate Skips On Equal Version |
| 98 | [labs/098-lowercase-header-lookup](labs/098-lowercase-header-lookup) | Lowercase header lookup |
| 99 | [labs/099-unencoded-query-params](labs/099-unencoded-query-params) | Unencoded query params |
| 102 | [labs/102-content-type-charset-lie](labs/102-content-type-charset-lie) | Content-Type charset lie |
| 103 | [labs/103-dns-cache-ignores-ttl](labs/103-dns-cache-ignores-ttl) | DNS cache ignores TTL |
| 108 | [labs/108-nplus1-silently-drops-rows](labs/108-nplus1-silently-drops-rows) | N+1 that silently drops rows |
| 109 | [labs/109-pagination-skips-timestamp-ties](labs/109-pagination-skips-timestamp-ties) | Pagination skips rows on timestamp ties |
| 112 | [labs/112-memoization-object-identity](labs/112-memoization-object-identity) | Memoization keyed on object identity |
| 113 | [labs/113-ttl-refreshed-on-every-read](labs/113-ttl-refreshed-on-every-read) | TTL refreshed on every read |
| 118 | [labs/118-loop-mutates-source-array](labs/118-loop-mutates-source-array) | Loop Mutates the Source Array |
| 119 | [labs/119-permit-released-twice](labs/119-permit-released-twice) | Permit Released Twice on Success |
| 122 | [labs/122-spy-counter-survives-reset](labs/122-spy-counter-survives-reset) | Spy Counter Survives Reset |
| 124 | [labs/124-week-started-a-day-late](labs/124-week-started-a-day-late) | The Week That Started A Day Late |
| 127 | [labs/127-payment-key-in-logs](labs/127-payment-key-in-logs) | The Payment Key That Ended Up In The Logs |
| 130 | [labs/130-artifact-belonged-to-yesterday](labs/130-artifact-belonged-to-yesterday) | The Artifact That Belonged To Yesterday |
| 131 | [labs/131-pr-build-held-production-key](labs/131-pr-build-held-production-key) | The PR Build That Held A Production Key |
| 133 | [labs/133-duplicate-webhook-processing](labs/133-duplicate-webhook-processing) | Duplicate webhook processing |
| 136 | [labs/136-xgroup-entriesread-zero](labs/136-xgroup-entriesread-zero) | Zero-value entries-read argument omitted from XGROUP tokens |
| 138 | [labs/138-idempotency-key-ignored](labs/138-idempotency-key-ignored) | Idempotency key ignored |
