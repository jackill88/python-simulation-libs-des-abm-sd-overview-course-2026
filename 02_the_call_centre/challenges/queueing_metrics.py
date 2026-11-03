"""
Lab: Queueing Metrics for Northline Support
Module 02: The Call Centre Story

Theory: theory/02_queueing_basics.md

Implement basic Erlang-style metrics for the imaginary Northline Support centre.

Run: pytest tests/02_the_call_centre/test_queueing_metrics.py -v
"""

from __future__ import annotations

from shared.models import CallCentreSnapshot


def traffic_intensity(arrival_rate: float, n_agents: int, service_rate: float) -> float:
    """Return offered load A = λ / (c · μ)."""
    pass


def is_system_stable(arrival_rate: float, n_agents: int, service_rate: float) -> bool:
    """Return True when the centre can theoretically keep up with arrivals."""
    pass


def validate_call_centre_params(
    arrival_rate: float,
    n_agents: int,
    service_rate: float,
) -> CallCentreSnapshot:
    """Return a nominal snapshot (staffing + backlog proxy) for sanity checks."""
    pass
