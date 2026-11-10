# Queueing Basics

Call centres are **queueing systems**: work (calls) arrives, waits if servers (agents) are busy, then receives service. Before you simulate Northline in SimPy, you need stable **intuition** for M/M/c queueing: Markovian arrivals, Markovian service, **c** parallel servers.

## Kendall notation (what M/M/c means)

| Symbol | Northline meaning |
|--------|-------------------|
| M (1st) | Inter-arrival times exponential → Poisson arrivals |
| M (2nd) | Service times exponential per call |
| c | Parallel identical agents |

Variants you may hear: M/M/1 (one agent), M/M/c, M/M/c/K (finite waiting room). The baseline Northline model is **unbounded FIFO** with **c = 4**.

## Traffic intensity and stability

**Offered load** (in Erlangs):

\[
A = \frac{\lambda}{c \mu}
\]

| Condition | System behaviour |
|-----------|------------------|
| \(A < 1\) | **Stable** — queue does not grow without bound on average |
| \(A \ge 1\) | **Unstable** — backlog grows; SL metrics break |

Northline baseline: λ = 10/min, μ = 3/min per agent, c = 4:

\[
A = \frac{10}{4 \times 3} = 0.833
\]

```python
def traffic_intensity(lam: float, c: int, mu: float) -> float:
    return lam / (c * mu)

def is_stable(lam: float, c: int, mu: float) -> bool:
    return traffic_intensity(lam, c, mu) < 1.0

assert is_stable(10, 4, 3)
assert not is_stable(40, 4, 3)  # A = 3.33 — fictional meltdown hour
```

## Why exponential times?

Exponential distributions are **memoryless**: the expected time until the next arrival does not depend on how long you have already waited. That assumption yields clean formulas and matches Poisson call arrivals in many planning models.

In code:

```python
import random

rng = random.Random(42)
inter_arrival = rng.expovariate(10.0)   # mean 1/10 min if rate is 10/min
service = rng.expovariate(3.0)          # mean 1/3 min per call at one agent
```

**Rate parameterisation:** `random.expovariate(lambd)` uses **rate** λ, not mean. Mean inter-arrival \(= 1/\lambda\).

## M/M/1 intuition (c = 1)

With one agent, utilisation \(\rho = \lambda/\mu\) must be **< 1**.

| Metric | M/M/1 formula (steady state) |
|--------|------------------------------|
| Lq — mean in queue | \(\rho^2 / (1 - \rho)\) |
| Wq — mean wait | \(Lq / \lambda\) |

Northline **training** example with **one** agent (not operations plan): λ = 2/min, μ = 3/min → ρ = 2/3.

```python
rho = 2.0 / 3.0
Lq = (rho ** 2) / (1 - rho)
Wq = Lq / 2.0  # Wq in minutes if lambda is per minute
print(f"M/M/1 mean wait Wq = {Wq * 60:.1f} seconds")
```

Real centres rarely run M/M/1 at peak; the exercise shows how \(\rho\) close to 1 **inflates** waits.

## M/M/c intuition (multiple agents)

Exact steady-state wait formulas use **Erlang C** (probability wait > 0). You implement helpers in Module 02’s challenge; for now remember the shape:

| Raise c, fixed λ | Effect |
|------------------|--------|
| A decreases | Mean wait usually drops sharply |
| | Occupancy may fall — staffing trade-off |

**Worked numeric anchor (qualitative):** at λ = 10, μ = 3, c = 4, \(A \approx 0.83\). Expect **non-zero** waits whenever all four agents are simultaneously busy—common during bursts even when average load is safe.

| c | A (λ=10, μ=3) | Stability |
|---|---------------|-----------|
| 3 | 1.11 | Unstable |
| 4 | 0.83 | Stable |
| 5 | 0.67 | More headroom |

## Little’s Law (relates averages)

In steady state:

\[
L = \lambda W
\]

**Mean calls in system** = arrival rate × **mean time in system** (wait + service). Useful to cross-check simulation output.

```python
# If simulation reports W = 0.75 min system time and lambda = 10/min:
L = 10.0 * 0.75  # 7.5 calls in system on average
```

## Relationship to simulation

| Approach | Pros | Cons |
|----------|------|------|
| Formulas (M/M/c) | Fast, analytic SL targets | Abandonment, time-varying λ, heterogeneous μ |
| DES | Flexible dynamics | Requires run length + validation |

Northline DES should **approximate** Erlang predictions in the no-abandon, stationary case—your validation checklist (Module 03) will exploit that.

## Key takeaway

**Stability first:** compute \(A = \lambda/(c\mu)\) before trusting ASA plots. Northline’s baseline is stable with moderate utilisation; M/M/c theory explains why waits still happen, and why simulation adds abandonment, patience, and time-of-day realism that formulas alone cannot carry.
