"""Flet offline bundle path resolution."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
FLET_APP = ROOT / "flet_app"
sys.path.insert(0, str(FLET_APP))

from config import BUNDLED_COURSE, get_course_root  # noqa: E402
from course_nav.course_loader import discover_modules  # noqa: E402


def test_bundled_course_has_modules_after_prepare():
    """bundled_course is the APK-readable tree (run prepare_assets before build)."""
    if not BUNDLED_COURSE.is_dir():
        return
    modules = discover_modules(BUNDLED_COURSE)
    assert len(modules) >= 7


def test_get_course_root_discovers_modules():
    root = get_course_root()
    modules = discover_modules(root)
    assert len(modules) >= 7
