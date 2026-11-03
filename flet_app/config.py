"""Paths for dev (repo checkout) and packaged Android builds."""

from __future__ import annotations

import os
import re
from pathlib import Path

FLET_APP_DIR = Path(__file__).resolve().parent
REPO_ROOT = FLET_APP_DIR.parent
BUNDLED_COURSE = FLET_APP_DIR / "assets" / "course"
MODULE_PATTERN = re.compile(r"^(\d{2})_.+")


def get_app_data_dir() -> Path:
    """Writable storage for progress.db (required on Android)."""
    env_dir = os.environ.get("FLET_APP_STORAGE_DATA")
    if env_dir:
        return Path(env_dir)
    return REPO_ROOT / "data"


def _has_course_modules(root: Path) -> bool:
    if not root.is_dir():
        return False
    return any(
        p.is_dir() and MODULE_PATTERN.match(p.name)
        for p in root.iterdir()
    )


def get_course_root() -> Path:
    """Course content: bundled assets in APK, repo root during development."""
    if _has_course_modules(BUNDLED_COURSE):
        return BUNDLED_COURSE
    if _has_course_modules(REPO_ROOT):
        return REPO_ROOT
    return BUNDLED_COURSE
