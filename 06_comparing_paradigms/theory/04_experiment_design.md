# Experiment Design & Factor Swaps

Once three Northline models run, the temptation is to tweak until KPIs look good. **Experiment design** structures changes so you learn **which factor moved the needle**—staffing, patience, arrival rate, or integration step.

## Factors and scenarios

| Factor | Levels (example) | Paradigms affected |
|--------|------------------|-------------------|
| Agents `c` | 3, 4, 5 | DES, ABM, SD initial staff |
| Arrival λ | 0.25, 0.35, 0.45 | All |
| Patience | 3, 5, 8 ticks | ABM primarily |
| `dt` | 0.5, 1.0 | SD |
| Seed | 42, 43, 44 | DES, ABM |

A **scenario** is a full assignment of levels (scenario card from lesson 02).

## Response variables (Northline)

| Response | Source |
|----------|--------|
| Throughput | Normalized `throughput` |
| Congestion | DES mean wait; SD peak backlog; ABM `waiting` |
| Loss | ABM abandon_rate; optional DES extensions |
| Staff path | SD `final_staffed` |

## OFAT vs factorial (light touch)

**One-factor-at-a-time (OFAT):** change `c` while holding λ, μ, patience fixed.

| Pros | Cons |
|------|------|
| Easy to explain | Misses interactions (λ high + low patience) |
| Few runs | Can mis-rank factors |

**Factorial (small):** all combinations of two factors at two levels—\(2^2 = 4\) runs.

Example: λ ∈ {0.3, 0.4} × patience ∈ {3, 6}

```python
def run_grid(lambdas, patiences, seed: int) -> list[dict]:
  rows = []
  for lam in lambdas:
    for pat in patiences:
      rows.append(
        run_call_centre_abm(
          n_agents=4,
          steps=200,
          arrival_prob=lam,
          service_prob=0.5,
          default_patience=pat,
          seed=seed,
        )
      )
  return rows
```

For course scope, a **partial factorial** on ABM plus **one** DES confirmation run per corner is enough.

## Blocking and common random numbers

Use the **same seed list** across scenarios when comparing paradigms to reduce variance:

```python
seeds = [42, 43, 44]
des_means = [run_des(seed=s)["mean_wait"] for s in seeds]
abm_means = [run_abm(seed=s)["abandon_rate"] for s in seeds]
```

**Block** on time-of-day if using real data later; here scenarios are synthetic.

## Treatments table template

| Run ID | c | λ | patience | Paradigm | Notes |
|--------|---|---|----------|----------|-------|
| R01 | 4 | 0.35 | 5 | ABM | baseline |
| R02 | 5 | 0.35 | 5 | ABM | OFAT +staff |
| R03 | 4 | 0.45 | 5 | ABM | OFAT +load |
| R04 | 4 | 0.35 | 3 | ABM | OFAT impatient |

Mirror **R01–R02** in DES with `n_agents` matching `c` when testing capacity.

## Interactions to watch at Northline

| Interaction | Signal |
|-------------|--------|
| High λ × low patience | Abandon spike, throughput collapse |
| High staff × low μ | Diminishing returns on waits |
| Small SD `dt` × fast hiring | Numerical overshoot in staff |

Plot interaction only when factorial data exists—avoid dramatizing noise.

## Guardrails

- **Pre-register** scenario card before runs (even a markdown file).
- **Limit** primary factors to 2–3 per report.
- **Stop** when additional runs shrink confidence intervals negligibly (rule-of-thumb for course: 3–5 seeds).

## Analysis without heavy stats

| Tool | Use |
|------|-----|
| Mean / range across seeds | Basic uncertainty |
| Percent change vs baseline | OFAT interpretation |
| Ranking | Which factor moved abandon most? |

```python
def pct_change(base: float, new: float) -> float:
  return (new - base) / base * 100 if base else float("nan")
```

## Reporting experiments in the brief

Include:

1. Factors and levels
2. Design type (OFAT or 2×2)
3. Primary response
4. Main finding in one bullet

## Key takeaways

- Define **factors**, **scenarios**, and **responses** before touching parameters.
- OFAT is fine for teaching; use **small factorials** when interactions matter (load × patience).
- Reuse **seeds** for fair cross-paradigm comparisons.
- Tie each run to a **run ID** in your comparison brief and portfolio.
