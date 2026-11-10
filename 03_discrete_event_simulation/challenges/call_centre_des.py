"""
Project: Call Centre DES with SimPy
Module 03: Discrete-Event Simulation

Theory: theory/03_simpy_processes.md, theory/05_statistics_warmup_run_length.md

Build an M/M/c-style model of Northline Support using SimPy.

Run: pytest tests/03_discrete_event_simulation/test_call_centre_des.py -v
"""

from __future__ import annotations


def run_call_centre_des(
    *,
    n_agents: int,
    mean_inter_arrival: float,
    mean_service_time: float,
    max_calls: int,
    seed: int,
) -> dict[str, float | int]:
    """
    Simulate incoming calls, waiting queue, and agent service times.

    Returns dict with keys: calls_served, mean_wait, max_queue.
    """
    pass
