"""Test utilities shared by course test files."""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path
from typing import Any


def load_challenge(module_dir: str, challenge_file: str, module_name: str | None = None) -> Any:
    """Dynamically load a challenge .py file from a course module."""
    root = Path(__file__).resolve().parents[1]
    path = root / module_dir / "challenges" / challenge_file
    name = module_name or path.stem
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Cannot load challenge: {path}")
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod
