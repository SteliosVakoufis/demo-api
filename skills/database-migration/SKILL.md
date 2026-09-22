---
name: database-migration
description: Plan and implement a deployed PostgreSQL schema or data migration.
---

# Database migration

1. Inspect schema, row counts, indexes, and dependencies.
2. State compatibility and locking risks before editing.
3. Separate expand, migrate, and contract phases.
4. Encode invariants as database constraints where possible.
5. Keep old and new application versions compatible during rollout.
6. Verify forward migration on representative data.
7. Test concurrency with separate database transactions.
8. Report deployment order, observability signals, rollback limits, and residual risk.

