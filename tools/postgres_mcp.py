from __future__ import annotations

import json
import os
import re
from typing import Any

import asyncpg
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("parcel-postgres-readonly")
DATABASE_URL = os.environ.get(
    "MCP_DATABASE_URL",
    "postgresql://agent_readonly:workshop-readonly@localhost:5432/parcels",
)


async def fetch(sql: str, *args: object) -> list[dict[str, Any]]:
    connection = await asyncpg.connect(DATABASE_URL)
    try:
        async with connection.transaction(readonly=True):
            rows = await connection.fetch(sql, *args)
            return [dict(row) for row in rows]
    finally:
        await connection.close()


def encode(rows: list[dict[str, Any]]) -> str:
    return json.dumps(rows, default=str, indent=2)


@mcp.tool()
async def list_tables() -> str:
    """List tables in the public schema."""
    rows = await fetch(
        """
        SELECT table_name
        FROM information_schema.tables
        WHERE table_schema = 'public' AND table_type = 'BASE TABLE'
        ORDER BY table_name
        """
    )
    return encode(rows)


@mcp.tool()
async def describe_table(table_name: str) -> str:
    """Describe columns and indexes for one public table."""
    columns = await fetch(
        """
        SELECT column_name, data_type, is_nullable
        FROM information_schema.columns
        WHERE table_schema = 'public' AND table_name = $1
        ORDER BY ordinal_position
        """,
        table_name,
    )
    indexes = await fetch(
        """
        SELECT indexname, indexdef
        FROM pg_indexes
        WHERE schemaname = 'public' AND tablename = $1
        ORDER BY indexname
        """,
        table_name,
    )
    return json.dumps({"columns": columns, "indexes": indexes}, default=str, indent=2)


@mcp.tool()
async def query_readonly(sql: str, limit: int = 100) -> str:
    """Run one bounded SELECT or EXPLAIN statement in a read-only transaction."""
    statement = sql.strip().rstrip(";")
    if ";" in statement:
        raise ValueError("Only one statement is allowed")
    if not re.match(r"^(SELECT|EXPLAIN)\b", statement, re.IGNORECASE):
        raise ValueError("Only SELECT and EXPLAIN are allowed")
    safe_limit = max(1, min(limit, 500))
    if statement.upper().startswith("EXPLAIN"):
        return encode(await fetch(statement))
    bounded = f"SELECT * FROM ({statement}) AS agent_query LIMIT {safe_limit}"
    return encode(await fetch(bounded))


if __name__ == "__main__":
    mcp.run(transport="stdio")

