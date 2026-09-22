# Parcel API — demonstration starter

Δεν υλοποιεί ownership history ή transfer endpoints. Η απαίτηση βρίσκεται στο `DEMO-TICKET.md`. Πλήρες runbook: `../materials/demo-runbook.md`.

```bash
make up
make logs
# Μετά την επιτυχή εκκίνηση:
make seed
make verify
```

API docs: http://localhost:8000/docs. Μόνο local synthetic data. Τα credentials του Compose/read-only role είναι αποκλειστικά για το demo.

Μετά από αλλαγές τρέξτε `make up` για rebuild/recreate και ξανά verification. Το image περιλαμβάνει tests, Alembic και scripts. Το startup εκτελεί migrations. Source bind mount δεν αρκεί για server reload.

Το `make verify` τρέχει tests, lint και mypy. Το OpenAPI test είναι smoke test, όχι πλήρης backward compatibility έλεγχος. Το probe unit test ελέγχει μόνο το helper. Ownership integration tests προστίθενται μαζί με το feature.

Το `make race` απαιτεί history/transfer endpoints και history ως μικρό JSON array. Δημιουργεί disposable parcel, στέλνει 20 requests με διαφορετικά request IDs και απαιτεί επιτυχή requests και έναν active owner. Είναι smoke probe: δεν αποδεικνύει idempotency, πλήρες history ή race freedom.

## MCP

```bash
make readonly-role
uv sync --extra dev
```

Προσαρμόστε το `mcp-postgres.example.json` στον host και επιβεβαιώστε cwd. Αν χρειάζεται: `uv --directory /absolute/path/to/demo-api run --extra dev python tools/postgres_mcp.py`.

Tools: list_tables, describe_table, query_readonly. Ο server χρησιμοποιεί read-only transactions και SELECT grants. Το input filter δεν είναι πλήρης SQL security parser. Ο DB role περιορίζει table writes, όχι όλες τις δυνατότητες του agent runtime.

## Architecture

API: HTTP translation. Service: business rules/transactions. Repository: SQLAlchemy queries. Alembic: schema revisions. Δείτε `AGENTS.md` και `skills/database-migration/SKILL.md`.

`make down` σταματά το demo. `make reset` διαγράφει το volume του συγκεκριμένου Compose project και χρησιμοποιείται μόνο με disposable δεδομένα.
