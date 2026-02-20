"""
ARI Feedback Database — SQLite layer.

Stores teacher-submitted passage ratings for model retraining.
"""

import hashlib
import sqlite3
import uuid
from datetime import datetime, timezone
from pathlib import Path

import os
_db_env = os.environ.get("ARI_DB_PATH", "")
DB_PATH = Path(_db_env) if _db_env else Path(__file__).parent / "feedback.db"
MAX_DB_BYTES = 500 * 1024 * 1024  # 500 MB hard cap


def get_conn() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    """Create tables if they don't exist."""
    with get_conn() as conn:
        conn.executescript("""
            CREATE TABLE IF NOT EXISTS feedback (
                id              TEXT PRIMARY KEY,
                created_at      TEXT NOT NULL,
                text            TEXT NOT NULL,
                text_hash       TEXT NOT NULL,
                subject         TEXT,
                ari_grade_low   REAL,
                ari_grade_mid   REAL,
                ari_grade_high  REAL,
                teacher_grade   INTEGER NOT NULL,
                teacher_board   TEXT,
                reason          TEXT,
                source          TEXT DEFAULT 'web_tool'
            );

            CREATE INDEX IF NOT EXISTS idx_feedback_hash ON feedback(text_hash);
            CREATE INDEX IF NOT EXISTS idx_feedback_created ON feedback(created_at);

            CREATE TABLE IF NOT EXISTS rate_limit_log (
                id         INTEGER PRIMARY KEY AUTOINCREMENT,
                created_at TEXT NOT NULL,
                ip         TEXT NOT NULL,
                endpoint   TEXT NOT NULL
            );
        """)


def text_hash(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def db_size_ok() -> bool:
    """Return False if DB file exceeds MAX_DB_BYTES."""
    if DB_PATH.exists():
        return DB_PATH.stat().st_size < MAX_DB_BYTES
    return True


def insert_feedback(
    text: str,
    subject: str,
    ari_grade_low: float,
    ari_grade_mid: float,
    ari_grade_high: float,
    teacher_grade: int,
    teacher_board: str,
    reason: str,
) -> str:
    feedback_id = str(uuid.uuid4())
    h = text_hash(text)
    now = datetime.now(timezone.utc).isoformat()

    with get_conn() as conn:
        conn.execute(
            """INSERT INTO feedback
               (id, created_at, text, text_hash, subject,
                ari_grade_low, ari_grade_mid, ari_grade_high,
                teacher_grade, teacher_board, reason)
               VALUES (?,?,?,?,?,?,?,?,?,?,?)""",
            (
                feedback_id, now, text, h, subject,
                ari_grade_low, ari_grade_mid, ari_grade_high,
                teacher_grade, teacher_board, reason,
            ),
        )
    return feedback_id


def is_duplicate(text: str) -> bool:
    """Return True if this exact text was already submitted."""
    h = text_hash(text)
    with get_conn() as conn:
        row = conn.execute(
            "SELECT 1 FROM feedback WHERE text_hash = ? LIMIT 1", (h,)
        ).fetchone()
    return row is not None


def log_rate_limit(ip: str, endpoint: str) -> None:
    now = datetime.now(timezone.utc).isoformat()
    with get_conn() as conn:
        conn.execute(
            "INSERT INTO rate_limit_log (created_at, ip, endpoint) VALUES (?,?,?)",
            (now, ip, endpoint),
        )


def feedback_count() -> int:
    with get_conn() as conn:
        row = conn.execute("SELECT COUNT(*) FROM feedback").fetchone()
    return row[0]
