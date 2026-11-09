# Randomness & Reproducibility

Northline Support is **stochastic**: arrivals bunch, service varies, and wait times are random even when \(A = \lambda/(c\mu)\) is stable. Simulation turns that randomness into **decisions** only when you control **seeds**, document **sampling**, and run enough **replications** to see signal through noise.

## Why stochastic at all?

| Deterministic model | Stochastic model |
|---------------------|------------------|
| Same output every run | Distribution of outcomes |
| Hides burst risk | Shows queue spikes |
| Easy spreadsheet | Matches call centre reality |

If λ = 10/min is interpreted as **exactly** one call every 6 seconds, you will **underestimate** concurrent arrivals and ASA.

```python
import random

rng = random.Random(42)
arrivals_in_5_min = [rng.expovariate(10.0) for _ in range(50)]
# Inter-arrival times vary; sum ≈ expected offered load only on average
```

## Random variables in baseline Northline

| Process | Common model | Code draw |
|---------|--------------|-----------|
| Inter-arrival | Exponential, rate λ | `rng.expovariate(lam)` |
| Service time | Exponential, rate μ | `rng.expovariate(mu)` |
| Patience (ABM) | Exponential / fixed | Challenge-specific |

**Poisson arrivals** over an interval are equivalent to exponential inter-arrivals in a stationary DES.

## RNG streams: one object per replication

| Practice | Reason |
|----------|--------|
| `rng = random.Random(seed)` | Isolated state |
| Pass `rng` into all draws | No hidden global state |
| Change seed per replication | Independent sample paths |

```python
def run_northline_rep(rep: int, *, base_seed: int = 1000):
    seed = base_seed + rep
    rng = random.Random(seed)
    # env, agents, arrival process all use this rng
    return seed, rng
```

## Pytest reproducibility

Autograders fix seeds so your implementation is judged on **logic**, not lucky draws.

| Test layer | Typical seed pattern |
|------------|----------------------|
| Unit tests (formulas) | No RNG |
| Short DES smoke test | `seed=0`, few events |
| Golden KPI bands | Tight tolerances with fixed seed |

When a test fails only on CI, suspect **global `random`** usage or time-dependent bugs—not “unlucky” randomness.

```python
# Avoid in course code:
import random
random.seed(1)  # mutates global state, affects other tests

# Prefer:
rng = random.Random(1)
t = rng.expovariate(3.0)
```

## Replications vs one long run

| Approach | Estimates | Pitfall |
|----------|-----------|---------|
| Many **replications**, same horizon | Mean KPI + variation | Must discard warm-up each rep |
| One very long run | Time-average with autocorrelation | Warm-up; batch means |

For Northline ASA reporting, **30+ replications** of one busy hour (after warm-up) is a teaching default; production studies may need more.

## Common random numbers (preview)

When comparing **c = 4** vs **c = 5**, reusing the same arrival stream (same seed) **reduces variance** in scenario difference estimates—useful in Module 06 experiments.

## Seeds and nondeterminism elsewhere

| Source | Course guidance |
|--------|-----------------|
| NumPy in SD | `numpy.random.default_rng(seed)` |
| Parallel DES | Not required; single-threaded SimPy |
| Floating point | Rare KPI ties; use tolerances in pytest |

## Documentation discipline

Every results table should include:

| Field | Example |
|-------|---------|
| Base seed | 1000 |
| Replications | 50 |
| Horizon | 60 min after 15 min warm-up |
| RNG | `random.Random` |

## Key takeaway

Randomness is a **feature** that exposes congestion risk at Northline. Seeds turn it into a **reproducible laboratory**: pytest stays stable, you can diff code changes fairly, and stakeholders see confidence intervals instead of one arbitrary timeline.
