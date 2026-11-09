"""
Lab: Call Centre System Dynamics
Module 05: System Dynamics

Theory: theory/02_stocks_flows_notation.md, theory/04_euler_and_time_step.md

Integrate backlog and staffing stocks with Euler steps.

Run: pytest tests/05_system_dynamics/test_call_centre_sd.py -v
"""

from __future__ import annotations


def sd_euler_step(state: dict[str, float], params: dict[str, float], dt: float) -> dict[str, float]:
    """Advance backlog, staffed_agents, and answered_today by one Euler step."""
    pass


def run_call_centre_sd(
    initial: dict[str, float],
    params: dict[str, float],
    *,
    steps: int,
    dt: float,
) -> dict[str, float | list[float]]:
    """
    Run the SD model for `steps` steps.

    Returns final_backlog, final_staffed, answered_today, backlog_history.
    """
    pass
