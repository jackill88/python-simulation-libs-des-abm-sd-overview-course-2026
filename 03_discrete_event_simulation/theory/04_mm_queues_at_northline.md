# M/M/1 and M/M/c at Northline

Before trusting a SimPy run, connect Northline Support to **classical queueing results**. You do not need heavy derivations—just stable formulas for **utilisation**, **stability**, and **qualitative wait behaviour** so DES output can be validated.

## Stationary assumptions

M/M/c steady-state formulas assume:

| Assumption | Northline busy hour |
|------------|---------------------|
| Poisson arrivals (rate λ) | Marketing plateaus OK short term |
| Exponential service (rate μ) per agent | Blended AHT |
| c identical servers | 4 parallel agents |
| Infinite queue (baseline) | No hard cap |
| No abandonment (classical) | Add in extended DES |

When abandonment matters, treat Erlang results as an **upper bound** on service quality.

## Utilisation and stability

Per-server utilisation in busy system:

\[
\rho = \frac{\lambda}{c\mu} = A \quad (\text{offered load in Erlangs})
\]

| Northline baseline | Value |
|--------------------|-------|
| λ | 10 / min |
| μ | 3 / min |
| c | 4 |
| \(A\) | 10 / 12 ≈ **0.833** |

Stable because \(A < 1\). If you drop to **c = 3**, \(A = 1.11\) → **unstable** (queue grows without bound in theory).

```python
def offered_load(lam: float, c: int, mu: float) -> float:
    return lam / (c * mu)

baseline = offered_load(10, 4, 3)
scenario_c3 = offered_load(10, 3, 3)
```

## M/M/1 warm-up (one agent)

Use **c = 1** only for pedagogy—Northline does not run peak with one agent—but the algebra is memorable:

\[
\rho = \frac{\lambda}{\mu}, \quad \rho < 1
\]

Mean number in queue:

\[
L_q = \frac{\rho^2}{1 - \rho}
\]

Mean wait in queue (Little):

\[
W_q = \frac{L_q}{\lambda}
\]

**Numeric:** λ = 2/min, μ = 3/min → ρ = 2/3, \(L_q = 0.67\), \(W_q \approx 0.33\) min ≈ **20 s**.

## M/M/c — what changes with parallel agents

With **c > 1**, the probability an arriving call **waits** (Erlang C) drops relative to one fast server at the same aggregate capacity—**pooling** helps.

| Idea | Intuition |
|------|-----------|
| Pooling c agents | One short call frees any agent |
| Same total μ | c small servers beat one megaserver at same sum μ |
| \(A\) near 1 | Waits explode even if stable |

Exact \(W_q\) needs Erlang C; Module 02 challenge implements helpers. For validation, compare **order of magnitude**: λ = 10, c = 4, μ = 3 should yield **tens of seconds** ASA in many stationary runs—not minutes—unless abandonment is off and unlucky draws dominate short runs.

## DES ↔ theory cross-check protocol

| Step | Action |
|------|--------|
| 1 | Disable abandon; stationary λ, μ, c |
| 2 | Long run + warm-up + replications |
| 3 | Estimate mean wait at answer |
| 4 | Compare to Erlang / `queueing_metrics` functions |
| 5 | Tolerance: few % if run length adequate |

```python
# Qualitative check after simulation
asa_seconds = 38.0
if 15 < asa_seconds < 90:
    print("ASA plausible for Northline M/M/c ballpark")
```

Tight agreement requires many replications; syllabus emphasizes **directional** validation.

## Effect of +1 agent (Northline what-if)

| c | A (λ=10, μ=3) | Planner expectation |
|---|---------------|---------------------|
| 4 | 0.83 | Baseline SL stress |
| 5 | 0.67 | Lower waits; lower occupancy |

Run DES with **common random numbers** (same seeds) to compare scenarios fairly.

## When M/M/c misleads for Northline

| Reality | M/M/c gap |
|---------|-----------|
| Caller patience | Overstates answered volume |
| Time-varying λ | Single (λ, μ) pair lies |
| Breaks / ACW | Effective c drops |

Document deviations in your validation checklist.

## Python: mean service vs rate

```python
MU = 3.0  # per minute rate
mean_service_min = 1.0 / MU
print(f"Mean service {mean_service_min * 60:.0f} s")  # 20 s
```

SimPy: `rng.expovariate(MU)` with MU as **rate** per minute.

## Key takeaway

M/M/c is Northline’s **sanity anchor**: compute \(A = \lambda/(c\mu)\) first, use M/M/1 for algebraic intuition, and use Erlang-level expectations to judge whether SimPy ASA is in a believable band before you tune abandonment or intraday schedules.
