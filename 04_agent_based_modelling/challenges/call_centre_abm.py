"""
Project: Call Centre ABM with Mesa
Module 04: Agent-Based Modelling

Theory: theory/03_mesa_structure.md, theory/05_patience_abandonment_calibration.md

Model callers and agents as individuals with patience and service rules.

Run: pytest tests/04_agent_based_modelling/test_call_centre_abm.py -v
"""

from __future__ import annotations


def run_call_centre_abm(
    *,
    n_agents: int,
    steps: int,
    arrival_prob: float,
    service_prob: float,
    default_patience: int,
    seed: int,
) -> dict[str, int | float]:
    """
    Run a discrete-time ABM for `steps` ticks.

    Returns dict with keys: served, abandoned, abandon_rate, waiting.
    """
    pass
