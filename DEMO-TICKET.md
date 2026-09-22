# Feature ticket: parcel ownership history

The API currently stores only the current owner on `parcel.owner_tax_number`.

## Required behavior

1. Existing Parcel API consumers remain compatible.
2. Ownership transfers preserve previous owners.
3. Add `GET /parcels/{id}/ownership-history`.
4. Add `POST /parcels/{id}/transfer`.
5. History items contain `owner_tax_number`, `valid_from`, and `valid_until`.
6. A parcel has at most one active owner.
7. Concurrent transfers never produce multiple active owners.
8. Migration and deployment work while the previous application version is still running.

## Clarification expected

Ask before choosing semantics for authorization, timestamps, equal effective times, request retries, and idempotency.

## Evidence expected

- backward-compatible OpenAPI contract;
- Alembic migration and deployment order;
- integration tests for history and transfer;
- a concurrency test that can fail against an unsafe implementation;
- rollback limits and residual risk.

