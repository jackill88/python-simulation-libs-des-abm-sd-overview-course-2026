# Observability & Debugging ABMs

Agent models fail quietly: the run finishes, KPIs look plausible, but **half the callers never entered the schedule**. This lesson builds **observability** for Northline ABM—logging, counters, checkpoints, and test hooks—without drowning in print output.

## What to observe

| Layer | Northline examples | Mechanism |
|-------|-------------------|-----------|
| Micro | One caller’s `waited` vs `patience` | Agent state dump |
| Meso | Queue length each tick | Time series list |
| Macro | `served`, `abandoned`, `abandon_rate` | Model counters |
| Integrity | `unique_id`, schedule size | Assertions |

Start with **macro** for pytest; add **meso** when debugging; drill to **micro** only for single-ticket bugs.

## Model-level time series

```python
class CallCentreModel(Model):
  def __init__(self, ...):
    ...
    self.history: dict[str, list[float | int]] = {
      "waiting": [],
      "served_cum": [],
      "abandoned_cum": [],
    }

  def step(self) -> None:
    # ... existing logic ...
    self.history["waiting"].append(len(self.waiting))
    self.history["served_cum"].append(self.served_count)
    self.history["abandoned_cum"].append(self.abandoned_count)
    self.schedule.step()
```

Plot `waiting` to see stability vs drift—useful in notebooks, optional in the graded challenge.

## DataCollector (Mesa optional pattern)

Mesa offers `DataCollector` for agent- and model-level reporting. Minimal example:

```python
from mesa.datacollection import DataCollector

self.datacollector = DataCollector(
  model_reporters={
    "Queue": lambda m: len(m.waiting),
    "Served": "served_count",
    "Abandoned": "abandoned_count",
  },
)
# inside step(), after updates:
self.datacollector.collect(self)
```

The course challenge does not require it; prefer simple lists if imports stay lean.

## Structured logging vs prints

For local debugging, gate verbose traces behind a flag:

```python
def step(self) -> None:
  ...
  if self.debug and self.schedule.steps % 50 == 0:
    print(f"t={self.schedule.steps} q={len(self.waiting)} served={self.served_count}")
```

Never leave `print` in submitted code paths used by CI.

## Invariants (assert while developing)

| Invariant | Check |
|-----------|--------|
| Non-negative counts | `served_count >= 0` |
| Waiting callers in sync | `len(waiting) <= arrivals - served - abandoned` (custom accounting) |
| IDs unique | set of ids length equals count |
| Bounded patience | `0 <= waited <= patience + 1` while in queue |

```python
assert all(c.waited <= c.patience + 1 for c in self.waiting)
```

Convert stable invariants to **pytest** cases (no arrivals → empty queue at end).

## Observability for abandonment bugs

Symptoms and traces:

| Symptom | Trace |
|---------|--------|
| abandon_rate = 0 always | Log first caller with `waited > patience` branch hit |
| abandon_rate = 1.0 | Check `service_prob`, `n_agents`, patience too low |
| `waiting` grows unbounded | Plot queue; check capacity |

```python
def debug_first_abandon(model: CallCentreModel) -> None:
  for c in model.waiting:
    if c.waited > c.patience:
      raise AssertionError(f"id={c.unique_id} waited={c.waited} patience={c.patience}")
```

## Reproducibility hooks

Always thread **`seed`** into `random.Random(seed)` on the model. For experiments, log:

```python
RUN_CARD = {
  "seed": 42,
  "n_agents": 4,
  "arrival_prob": 0.35,
  "service_prob": 0.5,
  "default_patience": 5,
  "steps": 200,
}
```

Store `RUN_CARD` alongside outputs in Module 06 comparison work.

## Testing observability without Mesa in tests

Student tests call `run_call_centre_abm(...)` and assert dict keys:

```python
result = run_call_centre_abm(n_agents=2, steps=10, arrival_prob=0.0, ...)
assert result["served"] == 0
assert result["abandoned"] == 0
assert result["waiting"] == 0
```

Expose enough **macro** structure for tests; keep Mesa classes private inside the challenge file.

## Dashboard mapping (operations language)

| ABM observable | Ops dashboard name |
|----------------|-------------------|
| `len(waiting)` | Calls waiting |
| `served_count / steps` | Rough throughput per tick |
| `abandon_rate` | Abandon % among resolved |
| Queue time series peak | Intraday max queue |

Translate ticks to minutes when presenting to stakeholders.

## Key takeaways

- Layer **micro / meso / macro** observability; match depth to the bug.
- Prefer **counters and time series** over ad-hoc prints in shared code.
- Encode **invariants** as assertions during development, then as **pytest** edge cases.
- Log **seeds and run cards** so ABM results are replayable in Module 06.
