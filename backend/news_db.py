"""
TruthLens - News Database Module
SQLite-backed store for real verified news headlines fetched from Inshorts.
Used for similarity-based verification against user input.
"""

import os
import sqlite3
import threading
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(__file__), 'saved_model', 'news_headlines.db')

# Thread-safe lock
_lock = threading.Lock()


def get_connection():
    """Return a new SQLite connection."""
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Create tables if they don't exist."""
    with _lock:
        conn = get_connection()
        conn.execute("""
            CREATE TABLE IF NOT EXISTS headlines (
                id        INTEGER PRIMARY KEY AUTOINCREMENT,
                title     TEXT    NOT NULL,
                category  TEXT,
                source    TEXT,
                url       TEXT,
                fetched_at TEXT
            )
        """)
        conn.execute("CREATE INDEX IF NOT EXISTS idx_title ON headlines(title)")
        conn.commit()
        conn.close()


def insert_headlines(articles: list):
    """
    Bulk-insert a list of article dicts.
    Skips duplicates (same title already in DB).
    """
    with _lock:
        conn = get_connection()
        now = datetime.utcnow().isoformat()
        inserted = 0

        for art in articles:
            title = (art.get('title') or '').strip()
            if not title:
                continue

            # Skip if title already exists
            exists = conn.execute(
                "SELECT 1 FROM headlines WHERE title = ?", (title,)
            ).fetchone()

            if not exists:
                conn.execute(
                    """INSERT INTO headlines (title, category, source, url, fetched_at)
                       VALUES (?, ?, ?, ?, ?)""",
                    (
                        title,
                        art.get('category', 'general'),
                        art.get('source', 'Inshorts'),
                        art.get('url', ''),
                        now
                    )
                )
                inserted += 1

        conn.commit()
        conn.close()
        return inserted


def get_all_headlines() -> list:
    """Return all stored headline strings."""
    conn = get_connection()
    rows = conn.execute("SELECT title FROM headlines").fetchall()
    conn.close()
    return [row['title'] for row in rows]


def get_headline_count() -> int:
    """Return total number of stored headlines."""
    conn = get_connection()
    count = conn.execute("SELECT COUNT(*) FROM headlines").fetchone()[0]
    conn.close()
    return count
