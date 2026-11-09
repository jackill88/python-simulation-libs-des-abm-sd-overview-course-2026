# Stocks, Flows & Notation

System dynamics diagrams are a **shared language** between engineers, operations, and HR. This lesson fixes notation for **Northline Support** before you draw the full stock–flow picture (next lesson) and code Euler steps.

## Stocks

A **stock** \(S\) accumulates:

\[
\frac{dS}{dt} = \text{inflows} - \text{outflows}
\]

In the course Python, stocks are plain dictionary keys updated each step:

```python
state = {
  "backlog": 12.0,
  "staffed_agents": 4.0,
  "answered_today": 0.0,
}
```

| Stock | Meaning at Northline | Non-negativity |
|-------|---------------------|----------------|
| `backlog` | Calls waiting | Yes (`max(0, ...)`) |
| `staffed_agents` | Agents on shift | Yes |
| `answered_today` | Cumulative handled | Yes |

## Flows

A **flow** is a rate (per unit time) that increases or decreases a stock.

| Flow | Affects | Sign |
|------|---------|------|
| Arrivals | `backlog` | + |
| Service completions | `backlog` | − |
| Hiring | `staffed_agents` | + |
| Attrition | `staffed_agents` | − |

```python
arrivals = params["arrival_rate"] * dt
served = min(backlog + arrivals, service_capacity)
```

Flows may depend on **stocks** (e.g. attrition proportional to current staff).

## Auxiliary variables (not stocks)

Quantities computed from stocks and params each step—**not integrated**:

| Auxiliary | Formula (lab) |
|-----------|-----------------|
| `service_capacity` | `staffed_agents * service_rate_per_agent * dt` |
| `served` | `min(backlog + arrivals, service_capacity)` |
| `net_backlog_flow` | `arrivals - served` |

Keeping auxiliaries explicit prevents double-counting in code.

## Notation table (course params)

| Symbol / key | Role | Typical unit |
|--------------|------|--------------|
| `λ` / `arrival_rate` | Call arrival intensity | calls/min |
| `μ_agent` / `service_rate_per_agent` | Agent productivity | calls/agent/min |
| `c` / `staffed_agents` | Staffing stock (instantaneous level) | agents |
| `h` / `hiring_rate` | HR inflow | agents/min |
| `a` / `attrition_rate` | Per-agent loss hazard (stylized) | 1/min |
| `Δt` / `dt` | Integration step | min |

## Conveyor vs stock (conceptual)

Calls **in service** could be a separate stock between “waiting” and “done.” The lab merges waiting backlog and immediate service capacity:

```python
served = min(backlog + arrivals, service_capacity)
new_backlog = max(0.0, backlog + arrivals - served)
```

That is a **minimal** congestion model—enough to couple staffing and backlog.

## Feedback loop annotation

On diagrams, mark loops:

- **R** — reinforcing (growth or collapse spirals)
- **B** — balancing (goal-seeking, e.g. backlog triggers hiring)

Northline hiring when backlog is high is typically **B** (stabilizing), though delays can create **overshoot** (R-like transient).

## Discrete vs continuous

Textbooks use continuous calculus; code uses **finite differences**:

\[
S_{t+\Delta t} = S_t + \dot{S}\,\Delta t
\]

That is **Euler integration** (Module 05 lesson 04).

## Shared snapshot with Module 02

`CallCentreSnapshot` in `shared/models.py` mirrors SD stocks:

```python
from shared.models import CallCentreSnapshot

snap = CallCentreSnapshot(
  backlog=backlog,
  staffed_agents=staffed,
  answered_today=answered,
)
```

Use the same names when exporting results to Module 06.

## Common notation mistakes

| Mistake | Fix |
|---------|-----|
| Treating `arrival_rate` as calls per step without `* dt` | Always scale rates by `dt` |
| Confusing `staffed_agents` stock with `n_agents` from DES | Explain snapshot vs constant c |
| Negative backlog after subtraction | Apply `max(0, ...)` |
| Attrition as flat count not × staff | Use `attrition_rate * staffed * dt` in lab |

## Reading others’ SD models

When reviewing external diagrams:

1. Circle every **stock** (rectangle).
2. Trace **flows** (valves/pipes) into/out of stocks.
3. Mark **delays** (pipeline stocks) if present.
4. Map each element to a **line of code** or intentional omission.

## Key takeaways

- **Stocks accumulate**; **flows are rates** multiplied by `dt` in code.
- Auxiliaries carry algebra; do not integrate them as stocks unless they represent inventory.
- Northline SD uses **backlog** and **staffed_agents** as primary stocks; `answered_today` tracks output.
- Consistent naming with `CallCentreSnapshot` eases cross-paradigm comparison.
