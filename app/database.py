"""Small PostgreSQL connection helpers for the application."""

import os

import psycopg
from psycopg.rows import dict_row


def get_database_url() -> str:
    """Return the configured database URL or raise a clear startup error."""
    database_url = os.getenv("DATABASE_URL")

    if not database_url:
        raise RuntimeError(
            "DATABASE_URL is not configured. Copy .env.example to .env "
            "and set your PostgreSQL connection string."
        )

    return database_url


def get_connection(database_url: str | None = None) -> psycopg.Connection:
    """Open one short-lived database connection for a service operation."""
    return psycopg.connect(
        database_url or get_database_url(),
        row_factory=dict_row,
    )
