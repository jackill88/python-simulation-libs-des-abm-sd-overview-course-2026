"""Paths for dev (repo checkout) and packaged Android builds."""

from __future__ import annotations

import os
import re
import shutil
from pathlib import Path

FLET_APP_DIR = Path(__file__).resolve().parent
REPO_ROOT = FLET_APP_DIR.parent
# Readable on APK: regular app files (not Flutter asset bundle).
BUNDLED_COURSE = FLET_APP_DIR / "bundled_course"
# Populated by prepare_assets; used by Flet's asset bundler (images/fonts).
ASSETS_COURSE = FLET_APP_DIR / "assets" / "course"
MODULE_PATTERN = re.compile(r"^(\d{2})_.+")
_COURSE_CACHE_DIRNAME = "course_content"


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


def _can_read_course_tree(root: Path) -> bool:
    """True when at least one markdown file under root is readable."""
    try:
        for path in root.rglob("*.md"):
            path.read_text(encoding="utf-8")
            return True
    except OSError:
        return False
    return False


def _copy_course_tree(source: Path, dest: Path) -> None:
    if dest.exists():
        shutil.rmtree(dest)
    shutil.copytree(source, dest)


def _materialize_if_needed(source: Path) -> Path:
    """
    On Android, markdown under Flutter ``assets/`` is not always readable via
    ``Path.read_text``. Copy a readable tree into app storage when needed.
    """
    if not _has_course_modules(source):
        return source

    if _can_read_course_tree(source):
        return source

    cache_root = get_app_data_dir() / _COURSE_CACHE_DIRNAME
    if _has_course_modules(cache_root) and _can_read_course_tree(cache_root):
        return cache_root

    # Last attempt: copy from source (may still fail if source is unreadable).
    try:
        _copy_course_tree(source, cache_root)
    except OSError:
        return source

    if _can_read_course_tree(cache_root):
        return cache_root
    return source


def _course_root_candidates() -> list[Path]:
    """Search order: APK-friendly paths first, then dev checkout."""
    candidates: list[Path] = []

    if _has_course_modules(BUNDLED_COURSE):
        candidates.append(BUNDLED_COURSE)

    env_assets = os.environ.get("FLET_ASSETS_DIR")
    if env_assets:
        assets_course = Path(env_assets) / "course"
        if _has_course_modules(assets_course):
            candidates.append(assets_course)

    if _has_course_modules(ASSETS_COURSE):
        candidates.append(ASSETS_COURSE)

    if _has_course_modules(REPO_ROOT):
        candidates.append(REPO_ROOT)

    if not candidates:
        candidates.append(BUNDLED_COURSE)

    return candidates


def get_course_root() -> Path:
    """Resolve course markdown root for desktop and packaged Android builds."""
    for candidate in _course_root_candidates():
        return _materialize_if_needed(candidate)
    return BUNDLED_COURSE
