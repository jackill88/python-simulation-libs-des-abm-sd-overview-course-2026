# Schedulers & Discrete Time

Time is not neutral. **Northline Support** in Module 03 (DES) jumps from event to event; Module 04 (ABM) advances a **clock in equal ticks**. This lesson explains schedulers, tick semantics, and when discretization distorts queue KPIs.

## Two clocks for one call centre

| | DES (SimPy) | ABM (Mesa lab) |
|---|-------------|----------------|
| Clock | Continuous `env.now` | Integer step index |
| Advance | Next scheduled event | `model.step()` every tick |
| Arrival | Process at exact time t | Probability per tick |
| Service | Timeout for exact duration | Bernoulli success per tick |

Both can estimate waits and abandons; they **do not share the same time axis** without careful harmonization.

## What is a tick?

Pick a **tick duration** Δt and stick to it. Example: **1 tick = 1 minute**.

Then:

- `arrival_prob` ≈ probability of ≥1 call in that minute (Bernoulli simplification).
- `service_prob` ≈ chance a free agent **completes** a call within the minute—not the same as exponential service rate μ unless you calibrate.

```python
# Illustrative calibration (not exact Poisson equivalence):
# If λ = 0.35 calls/min, a coarse Bernoulli p ≈ λ·Δt when Δt = 1 and λ small
arrival_prob = 0.35
```

Document approximations in your comparison brief (Module 06).

## Schedulers in Mesa

Mesa ships multiple schedulers; the course uses **`RandomActivation`**:

```python
from mesa.time import RandomActivation

self.schedule = RandomActivation(self)
# ...
self.schedule.step()  # random permutation of agent.step()
```

Others you may meet in the wild:

| Scheduler | Behaviour | Call-centre use |
|-----------|-----------|-----------------|
| `RandomActivation` | Shuffled agents each tick | Default lab choice |
| `SimultaneousActivation` | All agents step, then model | Synchronous “everyone decides at once” |
| `StagedActivation` | Groups in sequence | Shift handovers: supervisors then agents |

For queue FIFO logic, **model-level** processing (as in the challenge) often runs **before** `schedule.step()` so agent order does not reorder the queue incorrectly.

## ABM time vs DES event time — diagram

```
DES:  |----arrival----wait----service----complete---->
      ^              ^ events only exist at instants

ABM:  |--tick--|--tick--|--tick--|--tick--|
      all callers wait +1; maybe serve; maybe arrive
```

DES gives **exact** wait = start_service − arrival. ABM gives **wait in ticks** × Δt unless you track sub-tick arrivals—typically absent in the lab.

## Harmonizing with Northline DES parameters

Module 02 defines λ, μ, c. Translating to ABM ticks:

| DES quantity | ABM proxy (didactic) |
|--------------|----------------------|
| λ (calls/min) | `arrival_prob` per 1-min tick |
| μ (per agent) | `service_prob` when agent is free |
| c | `n_agents` |
| Patience | Max ticks in queue (not exponential) |

Run both models with the **same seed policy** (separate RNG streams per paradigm) and compare **trends**, not digit-identical waits.

## Step count vs simulation horizon

```python
steps = 200  # 200 minutes if Δt = 1 min
```

Longer runs reduce Monte Carlo noise but increase compute. For ABM:

- Discard **warm-up** ticks (e.g. first 20) before logging KPIs if the queue starts empty artificially.
- Report **both** `steps` and physical duration in your write-up.

## Parallelism illusion

`RandomActivation` does **not** mean wall-clock parallel execution—it is still a single-threaded Python loop. Do not confuse “agents act in random order” with “calls happen in parallel on separate CPUs.”

## When finer ticks help

If mean wait is sensitive to tick size, **halve Δt** and halve per-tick probabilities (roughly) to refine accuracy:

| Δt (min) | arrival_prob (example) |
|--------|-------------------------|
| 1.0 | 0.35 |
| 0.5 | ~0.18 per half-minute |

This mirrors Euler refinement in SD (Module 05): smaller steps, better fidelity, more iterations.

## Choosing ABM tick for Northline questions

| Question | Tick guidance |
|----------|----------------|
| Patience thresholds in whole minutes | 1-min ticks align with rules |
| Sub-minute service level (80% in 30s) | Prefer DES; ABM ticks too coarse |
| Segment mix / coaching rules | ABM ticks usually fine |

## Key takeaways

- ABM uses **fixed ticks**; DES uses **uneven events**—always state which clock you mean.
- **`RandomActivation`** shuffles agent `step()` calls; queue logic may still live on the model.
- Calibrate `arrival_prob` and `service_prob` to λ and μ **approximately**, then validate qualitatively against DES.
- Shorter Δt improves timing fidelity at the cost of more `step()` iterations.
