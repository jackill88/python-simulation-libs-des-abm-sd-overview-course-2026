# Mesa Model Structure (2.x)

**Mesa** is the agent-based engine for Module 04. You will model **Northline Support** as a `Model` containing `Agent` instances, advanced by a **schedule** each time step.

This lesson maps Mesa vocabulary to call-centre roles.

## The three pillars

| Mesa concept | Northline role | Your responsibility |
|--------------|----------------|---------------------|
| `Agent` | Caller or support agent | Per-entity state and (optional) `step` |
| `Model` | The call centre for one run | Global queue, counters, `step()` logic |
| `RandomActivation` | “Who acts this tick?” | Fair random order; calls `agent.step()` |

Mesa 2.x keeps imports shallow:

```python
from mesa import Agent, Model
from mesa.time import RandomActivation
```

## Agent: identity and state

Every entity needs a **unique_id** and a reference to its model:

```python
class SupportAgent(Agent):
  def __init__(self, unique_id: int, model: Model) -> None:
    super().__init__(unique_id, model)


class Caller(Agent):
  def __init__(self, unique_id: int, model: Model, patience: int) -> None:
    super().__init__(unique_id, model)
    self.patience = patience
    self.waited = 0
    self.abandoned = False
    self.served = False
```

Callers in the course lab mostly update through **model-level queue logic** rather than `Caller.step()`. That pattern is acceptable for beginners; later you can move waiting logic onto the caller agent for clarity.

## Model: orchestration

The `Model` subclass owns:

- Parameters (`n_agents`, `arrival_prob`, `service_prob`, …)
- Collections (`waiting` list, counts)
- A **random source** (`random.Random(seed)` for reproducibility)
- The **schedule**

```python
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
    self.waiting: list[Caller] = []
    self.served_count = 0
    self.abandoned_count = 0

    for i in range(n_agents):
      self.schedule.add(SupportAgent(i, self))
    self._next_id = n_agents
```

Note: support agents are on the schedule even if their `step()` is empty—the course model performs matching in `Model.step()`.

## RandomActivation: shuffled activation

`RandomActivation.step()` picks a random permutation of agents and calls `.step()` on each. For Northline:

- Reduces **order bias** when multiple agents could act.
- Does **not** by itself model simultaneous phone calls; the lab uses aggregate queue processing inside `Model.step()`.

```python
# Typical end of Model.step():
self.schedule.step()
```

## Model.step(): one tick of Northline time

Treat one `step()` as **one minute** (or any fixed interval—document your choice). A canonical ordering:

1. **Arrivals** — Bernoulli trial; spawn `Caller`, push to `waiting`, add to schedule.
2. **Service & waiting** — for each caller in queue: try assign + service draw; else increment wait; check patience.
3. **Schedule** — advance Mesa internal clock via `schedule.step()`.

```python
def step(self) -> None:
  if self.random.random() < self.arrival_prob:
    caller = Caller(self._next_id, self, self.default_patience)
    self._next_id += 1
    self.waiting.append(caller)
    self.schedule.add(caller)

  free_agents = self.n_agents
  still_waiting: list[Caller] = []
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
```

## Running the model

```python
model = CallCentreModel(
  n_agents=4,
  arrival_prob=0.35,
  service_prob=0.5,
  default_patience=5,
  seed=42,
)
for _ in range(200):
  model.step()
```

Return metrics from a function (see challenge stub) so pytest can assert stability and edge cases.

## Mesa vs spatial ABM

Many Mesa tutorials place agents on a **grid**. Northline is **non-spatial**: topology is the FIFO `waiting` list plus agent count. Skip `SingleGrid` unless you model a physical floor plan.

## File layout convention

| Path | Purpose |
|------|---------|
| `challenges/call_centre_abm.py` | Student implementation |
| `tests/04_agent_based_modelling/` | Behavioural contracts |
| `shared/models.py` | Shared snapshots (Module 02+) |

Keep Mesa imports inside the challenge or a local module—course tests import student functions, not Mesa directly.

## Key takeaways

- **`Model` orchestrates`; **`Agent` holds state**; **`RandomActivation` orders micro steps**.
- Northline maps cleanly to Mesa without a spatial grid.
- Document **what one tick means** and keep arrivals → queue → schedule order consistent.
- Reuse **seeded RNG** on the model for reproducible ABM experiments.
