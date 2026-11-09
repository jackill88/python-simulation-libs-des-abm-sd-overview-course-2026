# Euler Integration & Time Step

Module 05 turns the Northline stock–flow diagram into **numbers** with **explicit Euler** steps. This lesson covers the integration rule, choosing `dt`, and errors you should expect when comparing to DES.

## Euler’s rule

For stock \(S\) with net rate \(f(S, t)\):

\[
S_{t+\Delta t} = S_t + f(S_t, t)\,\Delta t
\]

In the lab, one call to `sd_euler_step` advances all stocks synchronously:

```python
def sd_euler_step(state: dict[str, float], params: dict[str, float], dt: float) -> dict[str, float]:
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
```

This is **forward Euler**—simple, first-order accurate.

## Running a horizon

```python
state = dict(initial)
history = [state["backlog"]]
for _ in range(steps):
  state = sd_euler_step(state, params, dt)
  history.append(state["backlog"])
```

`steps` × `dt` = simulated minutes in the lab when rates are per minute.

## Why `min()` changes calculus

Service is not linear flow when capacity binds:

```python
served = min(backlog + arrivals, service_capacity)
```

When backlog is huge, backlog change per step is **capped** by capacity—not by `arrival_rate` alone. That matches operational intuition: extra arrivals queue if agents are saturated.

## Choosing `dt`

| Consideration | Guidance |
|---------------|----------|
| Accuracy | Smaller `dt` → smaller integration error |
| Performance | More steps → slower runs |
| Flow variability | Fast-changing flows need smaller `dt` |
| Policy review | Weekly SD may use `dt = 1 day`; intraday sketch `dt = 1 min` |

**Rule of thumb:** choose `dt` so no stock changes more than ~10–20% of its value in one step *under nominal flows*. If one step empties the entire backlog incorrectly, shrink `dt`.

## Convergence experiment

```python
def final_backlog(dt: float, steps: int) -> float:
  state = {"backlog": 0.0, "staffed_agents": 4.0, "answered_today": 0.0}
  params = {"arrival_rate": 0.4, "service_rate_per_agent": 0.12, "hiring_rate": 0.0, "attrition_rate": 0.0}
  for _ in range(steps):
    state = sd_euler_step(state, params, dt)
  return state["backlog"]

# Compare dt=1.0 vs dt=0.25 with steps scaled so horizon matches
```

If results diverge materially, report the coarser `dt` as approximate.

## Stability vs stiffness

Rapid attrition plus aggressive hiring can oscillate under Euler:

| Phenomenon | Mitigation |
|------------|------------|
| Negative staff without clamp | `max(0, staffed + net)` |
| Overshoot | Reduce `dt` or use better integrator (outside course scope) |
| Oscillating backlog | Check λ versus `staffed × μ` |

Northline didactic params are mild; still clamp stocks.

## Time step vs DES event spacing

DES advances to the **next call**; SD advances a **fixed Δt** regardless of whether a call arrived. Coarse `dt` can **miss** burstiness that DES captures—another reason Module 06 comparisons are **qualitative**.

## Recording `backlog_history`

Tests expect a list including initial backlog:

```python
backlog_history: list[float] = [state["backlog"]]
for _ in range(steps):
  state = sd_euler_step(state, params, dt)
  backlog_history.append(state["backlog"])
```

Peak backlog drives `normalize_simulation_metrics` in Module 06.

## Units sanity script pattern

```python
def assert_units(params: dict[str, float], dt: float) -> None:
  assert params["arrival_rate"] >= 0
  assert params["service_rate_per_agent"] >= 0
  assert dt > 0
```

Document assumptions in markdown when presenting to peers.

## Euler limitations (honest scope)

Euler **drifts** on nonlinear loops with large `dt`. For capstone portfolio work:

- State `dt` used and show a refinement check.
- Do not claim SD matches DES wait percentiles.

## Key takeaways

- **`sd_euler_step`** is forward Euler with Northline-specific `min()` service logic.
- Pick `dt` via accuracy/performance trade-off; verify with a smaller-`dt` check when stakes are high.
- Clamp stocks non-negative; binding capacity changes effective flow shapes.
- SD integration grain differs from DES events—compare paradigms with humility (Module 06).
