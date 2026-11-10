# Python Stack & Conventions

This course standardises on a small Python stack so DES, ABM, and SD challenges share patterns: **SimPy** for events, **Mesa 2.x** for agents, **pydantic** for data shapes, **pytest** for checks, and explicit **random seeds** everywhere stochasticity appears.

## Stack at a glance

| Package | Version target | Role in Northline |
|---------|----------------|---------------------|
| `simpy` | 4.x | DES event engine |
| `mesa` | 2.x | ABM schedulers & model class |
| `pydantic` | 2.x | `CallCentreSnapshot` and config objects |
| `pytest` | 8.x | Challenge autograding |
| `numpy` | 2.x | SD Euler integration |

Install from the repo root:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Project layout

```
python-simulation-libs-des-abm-sd-overview-course-2026/
├── 01_get_started/
│   ├── theory/
│   └── challenges/
├── 02_the_call_centre/
├── shared/
│   └── models.py          # shared pydantic types
├── tests/
│   └── 02_the_call_centre/
└── _scripts/
    ├── theory_content/    # source markdown (this tree)
    └── bootstrap_course.py
```

**Convention:** challenge docstrings cite theory filenames. **Do not** edit tests to “make green” unless the spec is wrong—fix your implementation.

## SimPy (DES)

- One `simpy.Environment()` per **replication**.
- Use `random.Random(seed)` — **not** global `random` — so pytest and parallel runs stay isolated.

```python
import random
import simpy

def build_env(seed: int = 42):
    rng = random.Random(seed)
    env = simpy.Environment()
    agents = simpy.Resource(env, capacity=4)  # Northline c=4
    return env, agents, rng
```

| API | Use for Northline |
|-----|-------------------|
| `env.process(fn())` | Arrival generator, per-call handler |
| `yield env.timeout(t)` | Hold until service completes |
| `with resource.request() as req: yield req` | Join queue, seize agent |

Mention `PriorityResource` only when VIP calls skip the line—out of scope for baseline labs.

## Mesa 2.x (ABM)

Mesa 2 uses a **`Model`** class, **`Agent`** subclasses, and a **`AgentSet`** (or legacy scheduler patterns in older examples—follow the module stub).

```python
# Illustrative structure — align with your challenge file
from mesa import Agent, Model

class Caller(Agent):
    def __init__(self, model, patience_min: float):
        super().__init__(model)
        self.patience_min = patience_min
        self.waited = 0.0
```

| Concept | Northline mapping |
|---------|-------------------|
| Agent | Caller or service agent |
| Step | Tick queue, update patience, attempt match |
| DataCollector | ASA, abandons per tick |

## Pydantic

Use models at **I/O boundaries**:

```python
from shared.models import CallCentreSnapshot

snap = CallCentreSnapshot(backlog=3.0, staffed_agents=4.0, answered_today=120.0)
```

Validation errors should surface bad parameters before a long DES run.

## Pytest conventions

| Pattern | Why |
|---------|-----|
| `tests/<module>/test_*.py` | Mirrors course modules |
| Fixed seeds in tests | Deterministic CI |
| `-v` locally | See which KPI helper failed |

```bash
pytest tests/02_the_call_centre/test_queueing_metrics.py -v
```

Tests check **pure functions** first; integration tests may run short simulations with caps on event count.

## Randomness & seeds

| Rule | Detail |
|------|--------|
| One seed per replication | Change seed → new sample path |
| Document seed in results tables | “500 reps, seeds 0..499” |
| Never mix `numpy.random` and `random` without intent | SD module may use NumPy; DES uses `random.Random` |

```python
def run_replication(rep_id: int):
    seed = 10_000 + rep_id
    rng = random.Random(seed)
    # pass rng into all stochastic draws
```

## Style & typing

- `from __future__ import annotations` in challenge files.
- Type hints on public functions (challenges already stubbed).
- Units in variable names when ambiguous: `mean_service_min`, `arrival_rate_per_min`.

## Key takeaway

The stack is deliberately minimal: **SimPy** owns continuous time events, **Mesa** owns heterogeneous callers, **pydantic** keeps snapshots honest, and **pytest** locks down formulas before you trust a storyline about Northline Support.
