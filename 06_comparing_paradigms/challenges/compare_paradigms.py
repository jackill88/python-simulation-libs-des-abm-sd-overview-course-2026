"""
Capstone: Compare DES, ABM, and SD Views
Module 06: Comparing Paradigms

Theory: theory/01_three_lenses_same_call_centre.md

Normalize outputs so you can compare paradigms on shared KPIs.

Run: pytest tests/06_comparing_paradigms/test_compare_paradigms.py -v
"""

from __future__ import annotations

from typing import Any


def normalize_simulation_metrics(paradigm: str, raw: dict[str, Any]) -> dict[str, float]:
    """
    Map paradigm-specific result dicts onto:
      throughput, mean_delay, peak_queue
    """
    pass
