"""Accès à la base SQLite."""
import sqlite3

import pandas as pd

from src.config import DB_PATH, ROOT

SCHEMA_PATH = ROOT / "sql" / "schema.sql"


def get_connection() -> sqlite3.Connection:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    return sqlite3.connect(DB_PATH)


def init_db() -> None:
    conn = get_connection()
    conn.executescript(SCHEMA_PATH.read_text(encoding="utf-8"))
    conn.commit()
    conn.close()


def upsert(table: str, df: pd.DataFrame) -> int:
    """INSERT OR REPLACE d'un DataFrame (clé primaire définie dans schema.sql)."""
    if df.empty:
        return 0
    df = df.copy()
    for c in df.columns:
        if pd.api.types.is_datetime64_any_dtype(df[c]):
            df[c] = df[c].dt.strftime("%Y-%m-%d")
    cols = ", ".join(df.columns)
    placeholders = ", ".join("?" * len(df.columns))
    rows = [
        tuple(None if pd.isna(v) else (v.item() if hasattr(v, "item") else v) for v in r)
        for r in df.itertuples(index=False, name=None)
    ]
    conn = get_connection()
    conn.executemany(f"INSERT OR REPLACE INTO {table} ({cols}) VALUES ({placeholders})", rows)
    conn.commit()
    conn.close()
    return len(rows)


def read_sql(query: str, params: tuple = ()) -> pd.DataFrame:
    conn = get_connection()
    try:
        return pd.read_sql_query(query, conn, params=params)
    finally:
        conn.close()
