#!/usr/bin/env python3
"""Generate course markdown content for Python Simulation Libraries overview."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.strip() + "\n", encoding="utf-8")
    print(f"  wrote {path.relative_to(ROOT)}")


ROOT_README = """# Python Simulation Libraries: DES, ABM & System Dynamics

A self-paced, test-driven course on **three simulation paradigms in Python**, using one shared scenario: the imaginary **Northline Support** call centre.

## Learning Objectives

After finishing this course, you will be able to:

- Frame operational questions (KPIs, stability, time grain) before choosing a library
- Build a **discrete-event** call-centre model with **SimPy**
- Build an **agent-based** model with **Mesa** (callers, agents, patience)
- Build a **system dynamics** backlog/staffing model with Euler integration
- Compare outputs across paradigms on a normalized scorecard

## Libraries

| Paradigm | Library | Role in course |
|----------|---------|----------------|
| Discrete-Event Simulation (DES) | [SimPy](https://simpy.readthedocs.io/) | Event calendar, queues, agents as resources |
| Agent-Based Modelling (ABM) | [Mesa](https://mesa.readthedocs.io/) | Individual callers & agents, discrete ticks |
| System Dynamics (SD) | NumPy-style equations (pure Python) | Stocks, flows, hiring/attrition feedback |

Supporting tools: **pytest** (verify labs), **Pydantic** (typed snapshots), **Streamlit/Flet** (course navigator apps — same layout as the AI backend course).

## Course Structure

| Module | Topic | Challenges |
|--------|-------|------------|
| [01_get_started](01_get_started/README.md) | Get Started | — |
| [02_the_call_centre](02_the_call_centre/README.md) | The Call Centre Story | 1 lab |
| [03_discrete_event_simulation](03_discrete_event_simulation/README.md) | Discrete-Event Simulation (SimPy) | 1 project |
| [04_agent_based_modelling](04_agent_based_modelling/README.md) | Agent-Based Modelling (Mesa) | 1 project |
| [05_system_dynamics](05_system_dynamics/README.md) | System Dynamics | 1 lab |
| [06_comparing_paradigms](06_comparing_paradigms/README.md) | Comparing Paradigms | 1 capstone |
| [07_wrapping_up](07_wrapping_up/README.md) | Wrapping Up | — |

Each module contains:

- **`theory/`** — Markdown lessons with explanations and Python examples
- **`quizzes/`** — Self-check multiple-choice quizzes
- **`challenges/`** — Python files with function stubs (where applicable)

Tests live in **`tests/`**, organized by module.

## Getting Started

```bash
pip install -r requirements.txt
pytest -v
```

When **all tests pass**, you have completed the hands-on parts of the course.

Maintainers can sanity-check content:

```bash
python3 _scripts/verify_course.py
python3 _scripts/verify_tests.py
```

## Course Navigator App

### Streamlit (desktop / browser)

```bash
pip install -r requirements-app.txt
streamlit run app/main.py
```

### Flet (Android APK)

```bash
pip install -r requirements-flet.txt
flet run flet_app/main.py

# Build offline APK (optional)
python flet_app/prepare_assets.py
flet build apk
```
"""


MODULES: dict[str, dict] = {
    "01_get_started": {
        "readme": """# Module 01: Get Started

Welcome to the Northline Support simulation track.

## Learning Objectives

- Understand how theory, quizzes, and pytest challenges fit together
- Know which Python libraries map to DES, ABM, and SD

## Lessons

| # | Topic | Theory |
|---|-------|--------|
| 1 | Course Overview | [theory/01_course_overview.md](theory/01_course_overview.md) |

## Suggested Study Path

1. Read the course overview
2. Continue to Module 02 for the shared call-centre scenario
""",
        "theory": {
            "01_course_overview.md": """# Course Overview

You will model **Northline Support**, an imaginary customer service centre, three different ways.

## Why three paradigms?

| Paradigm | Question it loves | Call-centre example |
|----------|-------------------|---------------------|
| DES (SimPy) | *When* does congestion happen? | Wait times, queue spikes at peak hour |
| ABM (Mesa) | *Who* does what, and how do rules interact? | Patient vs impatient callers, skilled agents |
| SD | *How* do policies play out over months? | Hiring, attrition, backlog feedback |

## How this course works

| Component | Purpose |
|-----------|---------|
| Theory lessons | Concepts with runnable Python snippets |
| Quizzes | Self-check before moving on |
| Challenges | Implement stubs; `pytest` verifies correctness |
| Streamlit app | Browse content on desktop |
| Flet APK | Offline Android navigator with interactive quizzes |

## Prerequisites

- Comfortable Python (functions, classes, dicts)
- Basic probability (averages, random seeds)
- Familiarity with pytest is helpful but not required

## Suggested pace

| Module | Focus |
|--------|-------|
| 02 | Scenario + queueing metrics lab |
| 03–05 | One paradigm per module (theory + quiz + challenge) |
| 06 | Compare paradigms capstone |
| 07 | Wrap-up reading |

Start with **Module 02: The Call Centre Story**.
""",
        },
    },
    "02_the_call_centre": {
        "readme": """# Module 02: The Call Centre Story

Define Northline Support and the queueing metrics that every model will reference.

## Learning Objectives

- Describe the imaginary centre, its KPIs, and offered load
- Compute traffic intensity and stability before simulating
- Implement the queueing metrics lab

## Lessons

| # | Topic | Theory |
|---|-------|--------|
| 1 | Meet Northline Support | [theory/01_meet_northline.md](theory/01_meet_northline.md) |
| 2 | Queueing Basics | [theory/02_queueing_basics.md](theory/02_queueing_basics.md) |
| 3 | Choosing a Simulation Lens | [theory/03_choosing_a_lens.md](theory/03_choosing_a_lens.md) |

## Quiz

[quizzes/module_quiz.md](quizzes/module_quiz.md)

## Challenge

Implement [challenges/queueing_metrics.py](challenges/queueing_metrics.py) and run:

```bash
pytest tests/02_the_call_centre/test_queueing_metrics.py -v
```
""",
        "theory": {
            "01_meet_northline.md": """# Meet Northline Support

**Northline Support** handles billing and technical questions by phone. Operations leadership tracks:

- **Mean wait time** — how long callers wait before an agent answers
- **Abandon rate** — share of callers who hang up while waiting
- **Service level** — % answered within a target (e.g. 80% within 30 seconds)

Parameters we reuse across modules:

| Symbol | Meaning | Example |
|--------|---------|---------|
| λ | Arrival rate (calls / minute) | 10 |
| μ | Service rate per agent | 3 |
| c | Agents logged in | 4 |

Imaginary does not mean toy: the **structure** matches real centres even when numbers are didactic.
""",
            "02_queueing_basics.md": """# Queueing Basics

Before SimPy or Mesa, check **capacity sanity**.

## Traffic intensity

For c identical agents with exponential service at rate μ and Poisson arrivals at rate λ:

```python
A = lambda_rate / (c * mu_rate)  # offered load per server pool
```

When **A < 1**, the system can keep up on average (stable queue). When **A ≥ 1**, backlog grows without bound in the long run unless you add capacity or shed load.

## Snapshot helper

Your lab returns a `CallCentreSnapshot` — a typed view of staffing and a simple backlog proxy when load exceeds capacity:

```python
from shared.models import CallCentreSnapshot

snap = CallCentreSnapshot(backlog=0.0, staffed_agents=4, answered_today=0.0)
```

Use snapshots to guard impossible parameters before launching heavy simulations.
""",
            "03_choosing_a_lens.md": """# Choosing a Simulation Lens

Ask three questions:

1. **Time grain** — Events (DES), ticks (ABM), or continuous flows (SD)?
2. **Entity detail** — Do individuals matter, or only aggregates?
3. **Horizon** — Peak hour, shift, or multi-month hiring policy?

| If your priority is… | Start with… |
|----------------------|-------------|
| Precise wait times & staffing what-if | DES (Module 03) |
| Behaviour rules (patience, skills) | ABM (Module 04) |
| Hiring/attrition feedback | SD (Module 05) |

You will implement all three, then normalize KPIs in Module 06.
""",
        },
    },
    "03_discrete_event_simulation": {
        "readme": """# Module 03: Discrete-Event Simulation (SimPy)

Model Northline as arriving calls, a FIFO wait line, and c parallel agents.

## Learning Objectives

- Explain events, processes, and resources in SimPy
- Implement reproducible M/M/c-style DES for the call centre

## Lessons

| # | Topic | Theory |
|---|-------|--------|
| 1 | Why DES for Call Centres | [theory/01_why_des.md](theory/01_why_des.md) |
| 2 | SimPy Processes & Resources | [theory/02_simpy_processes.md](theory/02_simpy_processes.md) |

## Quiz

[quizzes/module_quiz.md](quizzes/module_quiz.md)

## Challenge

[challenges/call_centre_des.py](challenges/call_centre_des.py)

```bash
pytest tests/03_discrete_event_simulation/test_call_centre_des.py -v
```
""",
        "theory": {
            "01_why_des.md": """# Why DES for Call Centres

Call centres are classic **queueing systems**: random arrivals, limited servers, waiting, abandonment.

DES records **exact times** when:

- a call arrives
- a call enters service
- service completes

That event log yields empirical wait-time distributions — something aggregate spreadsheets hide.
""",
            "02_simpy_processes.md": """# SimPy Processes & Resources

Minimal pattern for Northline:

```python
import random
import simpy

def run_once(seed: int = 42):
    rng = random.Random(seed)
    env = simpy.Environment()
    agents = simpy.Resource(env, capacity=2)

    def handle_call():
        with agents.request() as req:
            yield req
            yield env.timeout(rng.expovariate(1 / 3.0))  # mean service 3 min

    def arrivals():
        for _ in range(5):
            yield env.timeout(rng.expovariate(1 / 4.0))  # mean inter-arrival 4 min
            env.process(handle_call())

    env.process(arrivals())
    env.run()
```

Your project generalizes this with metrics: `calls_served`, `mean_wait`, `max_queue`.
""",
        },
    },
    "04_agent_based_modelling": {
        "readme": """# Module 04: Agent-Based Modelling (Mesa)

Model callers and agents as individuals on a discrete time grid.

## Learning Objectives

- Structure a Mesa model with agents and a scheduler
- Encode patience and service success as micro-rules

## Lessons

| # | Topic | Theory |
|---|-------|--------|
| 1 | Why ABM for Call Centres | [theory/01_why_abm.md](theory/01_why_abm.md) |
| 2 | Mesa Agents and Steps | [theory/02_mesa_agents_and_steps.md](theory/02_mesa_agents_and_steps.md) |

## Quiz

[quizzes/module_quiz.md](quizzes/module_quiz.md)

## Challenge

[challenges/call_centre_abm.py](challenges/call_centre_abm.py)

```bash
pytest tests/04_agent_based_modelling/test_call_centre_abm.py -v
```
""",
        "theory": {
            "01_why_abm.md": """# Why ABM for Call Centres

Not every caller is identical:

- Some abandon after 30 seconds; others wait five minutes
- Agents differ in handle time and upsell behaviour
- Supervisors change routing rules mid-shift

ABM encodes these **heterogeneous rules** explicitly. Macro KPIs emerge from micro interactions.
""",
            "02_mesa_agents_and_steps.md": """# Mesa Agents and Steps

Course pattern (Mesa 2.x API):

```python
from mesa import Agent, Model
from mesa.time import RandomActivation

class Caller(Agent):
    def __init__(self, unique_id, model, patience):
        super().__init__(unique_id, model)
        self.patience = patience
        self.waited = 0

class CallCentreModel(Model):
    def __init__(self, n_agents, seed):
        super().__init__()
        self.schedule = RandomActivation(self)
        self.random = __import__("random").Random(seed)
        # add agents, waiting list, counters ...

    def step(self):
        # arrivals, service attempts, abandon checks
        self.schedule.step()
```

Your challenge wraps a full model in `run_call_centre_abm(...)`.
""",
        },
    },
    "05_system_dynamics": {
        "readme": """# Module 05: System Dynamics

Track backlog and staffing as stocks with continuous flows.

## Learning Objectives

- Draw stock–flow diagrams for Northline
- Integrate with explicit Euler steps in Python

## Lessons

| # | Topic | Theory |
|---|-------|--------|
| 1 | Why SD for Workforce Loops | [theory/01_why_sd.md](theory/01_why_sd.md) |
| 2 | Stocks, Flows, and Euler Steps | [theory/02_stocks_flows_and_euler.md](theory/02_stocks_flows_and_euler.md) |

## Quiz

[quizzes/module_quiz.md](quizzes/module_quiz.md)

## Challenge

[challenges/call_centre_sd.py](challenges/call_centre_sd.py)

```bash
pytest tests/05_system_dynamics/test_call_centre_sd.py -v
```
""",
        "theory": {
            "01_why_sd.md": """# Why SD for Workforce Loops

Intraday DES answers “what happens this peak hour?” **System dynamics** answers “what if we hire slower but attrition drops?”

Stocks might include:

- **Backlog** of waiting work
- **Staffed agents**
- (Extension) **Morale** affecting attrition

Flows connect HR policy to customer experience with visible feedback loops.
""",
            "02_stocks_flows_and_euler.md": """# Stocks, Flows, and Euler Steps

```python
def step(state, params, dt):
    arrivals = params["arrival_rate"] * dt
    capacity = state["staffed_agents"] * params["service_rate_per_agent"] * dt
    served = min(state["backlog"] + arrivals, capacity)
    backlog = max(0.0, state["backlog"] + arrivals - served)
    return {**state, "backlog": backlog, "answered_today": state["answered_today"] + served}
```

Choose `dt` small enough that flows do not jump wildly per step. Compare SD curves qualitatively to DES/ABM KPIs in Module 06.
""",
        },
    },
    "06_comparing_paradigms": {
        "readme": """# Module 06: Comparing Paradigms

Normalize DES, ABM, and SD outputs onto one scorecard.

## Learning Objectives

- Explain trade-offs between event, agent, and stock-flow views
- Implement KPI normalization for cross-paradigm comparison

## Lessons

| # | Topic | Theory |
|---|-------|--------|
| 1 | Three Lenses, Same Call Centre | [theory/01_three_lenses_same_call_centre.md](theory/01_three_lenses_same_call_centre.md) |
| 2 | Building a Comparison Brief | [theory/02_comparison_brief.md](theory/02_comparison_brief.md) |

## Quiz

[quizzes/module_quiz.md](quizzes/module_quiz.md)

## Challenge

[challenges/compare_paradigms.py](challenges/compare_paradigms.py)

```bash
pytest tests/06_comparing_paradigms/test_compare_paradigms.py -v
```
""",
        "theory": {
            "01_three_lenses_same_call_centre.md": """# Three Lenses, Same Call Centre

| Lens | Strength | Blind spot |
|------|----------|------------|
| DES | Timing of queues | Long HR feedback |
| ABM | Individual rules | Calibration of micro-rules |
| SD | Policy feedback | Intraday event detail |

None replaces the others — they **answer different questions**.
""",
            "02_comparison_brief.md": """# Building a Comparison Brief

When presenting to stakeholders:

1. State the **decision** (staffing, hiring, IVR deflection)
2. Show **assumptions** per paradigm
3. Present **normalized KPIs** — throughput, delay proxy, peak queue/backlog
4. Discuss **uncertainty** (seeds, time step, rule variants)

Your capstone function `normalize_simulation_metrics` is the engineering adapter between teams.
""",
        },
    },
    "07_wrapping_up": {
        "readme": """# Module 07: Wrapping Up

Consolidate what you built and plan next experiments.

## Lessons

| # | Topic | Theory |
|---|-------|--------|
| 1 | Conclusion | [theory/01_conclusion.md](theory/01_conclusion.md) |

## Next steps

- Extend Northline with shift schedules (DES) or skills (ABM)
- Add morale feedback in SD
- Export Mesa/ SimPy metrics to a shared dashboard
""",
        "theory": {
            "01_conclusion.md": """# Conclusion

You modeled **Northline Support** with:

- **SimPy** for event-level queues
- **Mesa** for caller/agent rules
- **System dynamics** for backlog and staffing stocks

The engineering lesson is not “pick the coolest library” — it is **match the paradigm to the decision**, document assumptions, and compare KPIs honestly.

Keep `pytest` green, keep seeds fixed while debugging, and treat simulation output as **evidence**, not prophecy.
""",
        },
    },
}


def main() -> None:
    from quiz_content import QUIZZES  # noqa: PLC0415

    print("Bootstrapping simulation course content...")
    write(ROOT / "README.md", ROOT_README)

    for module_id, content in sorted(MODULES.items()):
        module_dir = ROOT / module_id
        write(module_dir / "README.md", content["readme"])
        for filename, text in content.get("theory", {}).items():
            write(module_dir / "theory" / filename, text)
        if module_id in QUIZZES:
            write(module_dir / "quizzes" / "module_quiz.md", QUIZZES[module_id])

    print("Done.")


if __name__ == "__main__":
    main()
