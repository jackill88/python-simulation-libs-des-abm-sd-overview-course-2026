#!/usr/bin/env python3
"""Reference solutions — used to verify tests; not part of the student path."""

from __future__ import annotations

import random
from typing import Any

import simpy
from mesa import Agent, Model
from mesa.time import RandomActivation

from shared.models import CallCentreSnapshot


def traffic_intensity(arrival_rate: float, n_agents: int, service_rate: float) -> float:
    """Erlang traffic intensity A = λ / (c · μ)."""
    if n_agents <= 0 or service_rate <= 0:
        raise ValueError("n_agents and service_rate must be positive")
    return arrival_rate / (n_agents * service_rate)


def is_system_stable(arrival_rate: float, n_agents: int, service_rate: float) -> bool:
    """Return True when offered load is strictly below capacity."""
    return traffic_intensity(arrival_rate, n_agents, service_rate) < 1.0


def validate_call_centre_params(
    arrival_rate: float,
    n_agents: int,
    service_rate: float,
) -> CallCentreSnapshot:
    """Build a snapshot of nominal steady-state staffing view for Northline Support."""
    if arrival_rate < 0 or service_rate < 0 or n_agents < 0:
        raise ValueError("rates and agent count must be non-negative")
    staffed = float(n_agents)
    # Nominal backlog proxy when unstable: show offered load minus capacity (floored at 0).
    capacity = staffed * service_rate
    backlog = max(0.0, arrival_rate - capacity) if capacity > 0 else arrival_rate
    return CallCentreSnapshot(
        backlog=backlog,
        staffed_agents=staffed,
        answered_today=0.0,
    )


def run_call_centre_des(
    *,
    n_agents: int,
    mean_inter_arrival: float,
    mean_service_time: float,
    max_calls: int,
    seed: int,
) -> dict[str, float | int]:
    """
    M/M/c-style call centre with Poisson arrivals and exponential service times.
    Uses SimPy resource with c agents.
    """
    if n_agents <= 0:
        raise ValueError("n_agents must be positive")
    if mean_inter_arrival <= 0 or mean_service_time <= 0:
        raise ValueError("mean times must be positive")
    if max_calls <= 0:
        raise ValueError("max_calls must be positive")

    rng = random.Random(seed)
    env = simpy.Environment()
    resource = simpy.Resource(env, capacity=n_agents)
    waits: list[float] = []
    queue_depths: list[int] = []

    def call_process(call_id: int) -> Any:
        arrival = env.now
        with resource.request() as request:
            queue_depths.append(len(resource.queue))
            yield request
            wait = env.now - arrival
            waits.append(wait)
            yield env.timeout(rng.expovariate(1.0 / mean_service_time))

    def arrival_process() -> Any:
        for call_id in range(max_calls):
            yield env.timeout(rng.expovariate(1.0 / mean_inter_arrival))
            env.process(call_process(call_id))

    env.process(arrival_process())
    env.run()

    mean_wait = sum(waits) / len(waits) if waits else 0.0
    return {
        "calls_served": len(waits),
        "mean_wait": mean_wait,
        "max_queue": max(queue_depths) if queue_depths else 0,
    }


def run_call_centre_abm(
    *,
    n_agents: int,
    steps: int,
    arrival_prob: float,
    service_prob: float,
    default_patience: int,
    seed: int,
) -> dict[str, int | float]:
    if steps <= 0:
        raise ValueError("steps must be positive")

    class _SupportAgent(Agent):
        def __init__(self, unique_id: int, model: Model) -> None:
            super().__init__(unique_id, model)

    class _Caller(Agent):
        def __init__(self, unique_id: int, model: Model, patience: int) -> None:
            super().__init__(unique_id, model)
            self.patience = patience
            self.waited = 0
            self.abandoned = False
            self.served = False

    class CallCentreModel(Model):
        def __init__(
            self,
            n_agents: int,
            arrival_prob: float,
            service_prob: float,
            default_patience: int,
            seed: int,
        ) -> None:
            super().__init__()
            self.n_agents = n_agents
            self.arrival_prob = arrival_prob
            self.service_prob = service_prob
            self.default_patience = default_patience
            self.random = random.Random(seed)
            self.schedule = RandomActivation(self)
            self.waiting: list[_Caller] = []
            self.served_count = 0
            self.abandoned_count = 0

            for i in range(n_agents):
                self.schedule.add(_SupportAgent(i, self))

            self._next_id = n_agents

        def step(self) -> None:
            if self.random.random() < self.arrival_prob:
                caller = _Caller(self._next_id, self, self.default_patience)
                self._next_id += 1
                self.waiting.append(caller)
                self.schedule.add(caller)

            free_agents = self.n_agents
            still_waiting: list[_Caller] = []
            for caller in self.waiting:
                if free_agents > 0 and self.random.random() < self.service_prob:
                    caller.served = True
                    self.served_count += 1
                    free_agents -= 1
                else:
                    caller.waited += 1
                    if caller.waited > caller.patience:
                        caller.abandoned = True
                        self.abandoned_count += 1
                    else:
                        still_waiting.append(caller)
            self.waiting = still_waiting
            self.schedule.step()

    model = CallCentreModel(
        n_agents=n_agents,
        arrival_prob=arrival_prob,
        service_prob=service_prob,
        default_patience=default_patience,
        seed=seed,
    )
    for _ in range(steps):
        model.step()
    total = model.served_count + model.abandoned_count
    abandon_rate = model.abandoned_count / total if total else 0.0
    return {
        "served": model.served_count,
        "abandoned": model.abandoned_count,
        "abandon_rate": abandon_rate,
        "waiting": len(model.waiting),
    }


def sd_euler_step(state: dict[str, float], params: dict[str, float], dt: float) -> dict[str, float]:
    """One Euler step for backlog / staffing stocks at Northline Support."""
    backlog = state["backlog"]
    staffed = state["staffed_agents"]
    answered = state.get("answered_today", 0.0)

    arrivals = params["arrival_rate"] * dt
    service_capacity = staffed * params["service_rate_per_agent"] * dt
    served = min(backlog + arrivals, service_capacity)
    new_backlog = max(0.0, backlog + arrivals - served)

    hiring = params.get("hiring_rate", 0.0) * dt
    attrition = params.get("attrition_rate", 0.0) * staffed * dt
    new_staffed = max(0.0, staffed + hiring - attrition)

    return {
        "backlog": new_backlog,
        "staffed_agents": new_staffed,
        "answered_today": answered + served,
    }


def run_call_centre_sd(
    initial: dict[str, float],
    params: dict[str, float],
    *,
    steps: int,
    dt: float,
) -> dict[str, float | list[float]]:
    if steps <= 0:
        raise ValueError("steps must be positive")
    if dt <= 0:
        raise ValueError("dt must be positive")

    state = dict(initial)
    backlog_history: list[float] = [state["backlog"]]
    for _ in range(steps):
        state = sd_euler_step(state, params, dt)
        backlog_history.append(state["backlog"])

    return {
        "final_backlog": state["backlog"],
        "final_staffed": state["staffed_agents"],
        "answered_today": state["answered_today"],
        "backlog_history": backlog_history,
    }


def normalize_simulation_metrics(paradigm: str, raw: dict[str, Any]) -> dict[str, float]:
    """Map DES / ABM / SD outputs onto shared KPI names for comparison."""
    key = paradigm.lower()
    if key == "des":
        return {
            "throughput": float(raw.get("calls_served", 0)),
            "mean_delay": float(raw.get("mean_wait", 0.0)),
            "peak_queue": float(raw.get("max_queue", 0)),
        }
    if key == "abm":
        served = float(raw.get("served", 0))
        abandon = float(raw.get("abandon_rate", 0.0))
        return {
            "throughput": served,
            "mean_delay": abandon,
            "peak_queue": float(raw.get("waiting", 0)),
        }
    if key == "sd":
        history = raw.get("backlog_history") or []
        peak = max(history) if history else float(raw.get("final_backlog", 0))
        return {
            "throughput": float(raw.get("answered_today", 0)),
            "mean_delay": float(raw.get("final_backlog", 0)),
            "peak_queue": peak,
        }
    raise ValueError(f"unknown paradigm: {paradigm}")
