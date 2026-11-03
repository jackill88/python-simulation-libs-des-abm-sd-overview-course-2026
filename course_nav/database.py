"""SQLite progress tracking for course modules."""

from __future__ import annotations

import sqlite3
from dataclasses import dataclass
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Optional

_DEFAULT_DB_DIR = Path(__file__).resolve().parent.parent / "data"
DB_DIR = _DEFAULT_DB_DIR
DB_PATH = DB_DIR / "progress.db"


def configure_db_dir(path: Path) -> None:
    """Override the SQLite directory (e.g. Flet app storage on Android)."""
    global DB_DIR, DB_PATH
    DB_DIR = path
    DB_PATH = path / "progress.db"


class ModuleStatus(str, Enum):
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"


@dataclass
class ModuleProgress:
    module_id: str
    status: ModuleStatus
    started_at: Optional[str]
    completed_at: Optional[str]
    last_accessed_at: Optional[str]


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def get_connection() -> sqlite3.Connection:
    DB_DIR.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db(module_ids: list[str]) -> None:
    with get_connection() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS module_progress (
                module_id TEXT PRIMARY KEY,
                status TEXT NOT NULL DEFAULT 'not_started',
                started_at TEXT,
                completed_at TEXT,
                last_accessed_at TEXT
            )
            """
        )
        for module_id in module_ids:
            conn.execute(
                """
                INSERT OR IGNORE INTO module_progress (module_id, status)
                VALUES (?, ?)
                """,
                (module_id, ModuleStatus.NOT_STARTED.value),
            )
        conn.commit()


def get_all_progress() -> dict[str, ModuleProgress]:
    with get_connection() as conn:
        rows = conn.execute("SELECT * FROM module_progress").fetchall()
    return {
        row["module_id"]: ModuleProgress(
            module_id=row["module_id"],
            status=ModuleStatus(row["status"]),
            started_at=row["started_at"],
            completed_at=row["completed_at"],
            last_accessed_at=row["last_accessed_at"],
        )
        for row in rows
    }


def get_progress(module_id: str) -> ModuleProgress:
    progress = get_all_progress().get(module_id)
    if progress is None:
        raise KeyError(f"Unknown module: {module_id}")
    return progress


def touch_module(module_id: str) -> None:
    """Mark a module as started on first open; update last-accessed time otherwise."""
    now = _now()
    with get_connection() as conn:
        row = conn.execute(
            "SELECT status FROM module_progress WHERE module_id = ?",
            (module_id,),
        ).fetchone()
        if row is None:
            return
        status = row["status"]
        if status == ModuleStatus.NOT_STARTED.value:
            conn.execute(
                """
                UPDATE module_progress
                SET status = ?, started_at = ?, last_accessed_at = ?
                WHERE module_id = ?
                """,
                (ModuleStatus.IN_PROGRESS.value, now, now, module_id),
            )
        else:
            conn.execute(
                """
                UPDATE module_progress
                SET last_accessed_at = ?
                WHERE module_id = ?
                """,
                (now, module_id),
            )
        conn.commit()


def set_module_status(module_id: str, status: ModuleStatus) -> None:
    now = _now()
    with get_connection() as conn:
        if status == ModuleStatus.NOT_STARTED:
            conn.execute(
                """
                UPDATE module_progress
                SET status = ?, started_at = NULL, completed_at = NULL,
                    last_accessed_at = ?
                WHERE module_id = ?
                """,
                (status.value, now, module_id),
            )
        elif status == ModuleStatus.IN_PROGRESS:
            conn.execute(
                """
                UPDATE module_progress
                SET status = ?,
                    started_at = COALESCE(started_at, ?),
                    completed_at = NULL,
                    last_accessed_at = ?
                WHERE module_id = ?
                """,
                (status.value, now, now, module_id),
            )
        else:
            conn.execute(
                """
                UPDATE module_progress
                SET status = ?,
                    started_at = COALESCE(started_at, ?),
                    completed_at = ?,
                    last_accessed_at = ?
                WHERE module_id = ?
                """,
                (status.value, now, now, now, module_id),
            )
        conn.commit()


def completion_stats(module_ids: list[str]) -> tuple[int, int]:
    progress = get_all_progress()
    completed = sum(
        1
        for module_id in module_ids
        if progress.get(module_id)
        and progress[module_id].status == ModuleStatus.COMPLETED
    )
    return completed, len(module_ids)
