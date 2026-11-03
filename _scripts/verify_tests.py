#!/usr/bin/env python3
"""Run pytest with reference solutions patched in (maintainer tool)."""

from __future__ import annotations

import inspect
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "_scripts"))

import solutions as sol

IMPORT_PREFIX = {
    ("03_discrete_event_simulation", "call_centre_des.py"): (
        "import random\nfrom typing import Any\n\nimport simpy\n"
    ),
    ("04_agent_based_modelling", "call_centre_abm.py"): (
        "import random\n\nfrom mesa import Agent, Model\nfrom mesa.time import RandomActivation\n"
    ),
}

CHALLENGE_MAP = {
    ("02_the_call_centre", "queueing_metrics.py"): [
        "traffic_intensity",
        "is_system_stable",
        "validate_call_centre_params",
    ],
    ("03_discrete_event_simulation", "call_centre_des.py"): [
        "run_call_centre_des",
    ],
    ("04_agent_based_modelling", "call_centre_abm.py"): [
        "run_call_centre_abm",
    ],
    ("05_system_dynamics", "call_centre_sd.py"): [
        "sd_euler_step",
        "run_call_centre_sd",
    ],
    ("06_comparing_paradigms", "compare_paradigms.py"): [
        "normalize_simulation_metrics",
    ],
}


def main() -> int:
    backups: dict[Path, str] = {}
    for (mod, fname), names in CHALLENGE_MAP.items():
        path = ROOT / mod / "challenges" / fname
        original = path.read_text()
        backups[path] = original
        header = original.split("\ndef ", 1)[0].rstrip()
        prefix = IMPORT_PREFIX.get((mod, fname), "")
        parts = [header, ""]
        if prefix:
            parts = [prefix.rstrip(), ""]
        for name in names:
            parts.append(inspect.getsource(getattr(sol, name)).rstrip())
        path.write_text("\n\n".join(parts) + "\n")

    result = subprocess.run(
        [sys.executable, "-m", "pytest", "-q"],
        cwd=ROOT,
    )

    for path, content in backups.items():
        path.write_text(content)

    return result.returncode


if __name__ == "__main__":
    raise SystemExit(main())
