# Patience, Abandonment & Calibration

**Abandon rate** is a headline KPI at Northline Support. In ABM it is the outcome of **patience rules** applied tick after tick—not a parameter you paste from last month’s report without justification.

This lesson covers patience mechanics, calibration workflow, and sanity checks against DES and data.

## Patience as a micro rule

In the course lab each caller stores:

- `patience` — maximum tolerable wait (in ticks)
- `waited` — time spent waiting so far

```python
caller.waited += 1
if caller.waited > caller.patience:
  caller.abandoned = True
  model.abandoned_count += 1
```

Strict inequality means patience = 5 allows ticks 0…5 before abandonment on the next increment—**document your convention** in reports.

## From KPI to micro parameter (inverse problem)

Leadership says: “Abandon runs about **8%** in peak.” You choose a patience model:

| Patience model | Parameters | Flexibility |
|----------------|------------|-------------|
| Fixed integer | `default_patience` | Low |
| Uniform draw | `low`, `high` per caller | Medium |
| Segment-based | billing vs technical | High |

Calibration **searches** micro parameters so simulated abandon_rate ≈ target **under fixed** arrivals and staffing.

```python
def sweep_patience(default_patience: int, seeds: list[int]) -> float:
  rates = []
  for seed in seeds:
    out = run_call_centre_abm(
      n_agents=4,
      steps=500,
      arrival_prob=0.35,
      service_prob=0.5,
      default_patience=default_patience,
      seed=seed,
    )
    rates.append(out["abandon_rate"])
  return sum(rates) / len(rates)
```

Run multiple seeds; ABM is stochastic even with fixed rules.

## Calibration workflow (methodological)

1. **Freeze** macro context — `n_agents`, `arrival_prob`, `service_prob`, `steps`, warm-up.
2. **Pick** a patience distribution family (start with fixed integer).
3. **Grid search** patience values; record mean abandon_rate ± spread across seeds.
4. **Face validity** — do implied wait times before abandon match IVR logs qualitatively?
5. **Document** that other KPIs (served, waiting) come along for the ride—do not tune only one number in isolation.

| Step | Output |
|------|--------|
| Freeze | Scenario card (Module 06) |
| Search | Table patience → abandon_rate |
| Validate | Short narrative + optional DES compare |

## Heterogeneity and identification

With two patience types, **many combinations** yield the same macro abandon rate. Example:

| Type | Share | Patience | Effect |
|------|-------|----------|--------|
| Impatient | 0.3 | 2 | Drives early abandons |
| Patient | 0.7 | 10 | Rarely leaves |

Without segment data you cannot uniquely identify the mix—state **assumptions** explicitly.

## Linking to exponential patience (DES world)

DES extensions sometimes model time-to-abandon as Exp(θ). ABM patience in **ticks** is a **stylized** discrete threshold:

```python
# Optional upgrade: draw continuous patience, convert to ticks
theta = 2.5  # mean minutes
patience_ticks = max(1, int(rng.expovariate(1 / theta)))
```

Smaller θ → shorter draws → higher abandon for the same queue.

## Northline scenario: marketing campaign

A campaign shifts mix toward **billing** (impatient). Micro change: raise share of low patience at spawn.

```python
def patience_new(rng: random.Random) -> int:
  if rng.random() < 0.75:  # campaign mix
    return 2
  return 6
```

Macro expectation: **abandon_rate up**, **served down**, possibly **mean wait down** (queue sheds impatient callers). Misreading the third effect causes bad staffing decisions.

## Metrics denominator (lab contract)

```python
abandon_rate = abandoned / (served + abandoned) if (served + abandoned) else 0.0
```

Callers still waiting at horizon end are **not** in the denominator. For operational SLAs you may also track **abandon among arrivals**—different definition, different number.

## Calibration vs validation

| Activity | Question |
|----------|----------|
| Calibration | Do parameters reproduce reference KPIs? |
| Validation | Does the whole model support the decision under study? |

Fitting abandon alone does not prove patience rules are **causal** for the policy question.

## DES cross-check

Run DES without abandonment (Module 03) for utilization bounds. ABM with patience should:

- **Not** exceed DES served calls when patience is infinite and rules align.
- Show **higher** effective loss when patience is short.

```python
# Qualitative check only:
des = run_call_centre_des(n_agents=4, mean_inter_arrival=1/0.35, ...)
abm = run_call_centre_abm(n_agents=4, arrival_prob=0.35, ...)
```

Compare orders of magnitude on throughput, not exact equality.

## Key takeaways

- **Patience is a micro rule**; abandon rate is an **emergent KPI**.
- Calibrate with **frozen macro scenario**, **multiple seeds**, and documented tick semantics.
- Heterogeneity creates **non-unique** calibrations—record assumptions.
- Align **rate definitions** with Module 06 normalization before comparing paradigms.
