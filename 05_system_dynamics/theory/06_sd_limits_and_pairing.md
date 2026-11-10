# SD Limits & Pairing with DES/ABM

No paradigm owns **Northline Support**. System dynamics illuminates **staffing–backlog feedback**; it does not replace event-level queue truth. This lesson states SD limits honestly and sketches **pairing patterns** with Modules 03–04.

## What SD does poorly for Northline

| Need | SD limit |
|------|----------|
| 80% answered in 30 seconds | No individual wait events |
| Abandon by segment | No caller agents without ABM coupling |
| Erlang C validation | Aggregate, not M/M/c exact |
| Burst arrivals within a minute | Fixed `dt` smears arrivals |

Use SD when the decision tolerates **aggregate timing error** in exchange for **loop clarity**.

## What SD does well

| Need | SD strength |
|------|-------------|
| Months-long staffing scenarios | Natural stocks |
| Policy tables on backlog | Easy to wire to flows |
| Executive diagrams | Stock–flow is legible |
| Exploring overshoot/oscillation | Plot `backlog_history` |

## Pairing pattern 1: SD → DES capacity check

1. SD explores hiring plan → `staffed_agents` trajectory.
2. Sample peak staffing from SD (`min` or `max` over horizon).
3. DES runs with `n_agents` from that trajectory for SLA metrics.

```python
sd_out = run_call_centre_sd(initial, params, steps=30 * 24 * 60, dt=1.0)
peak_staff = max(
  sd_out["final_staffed"],
  initial["staffed_agents"],
)  # extend with full staff history in portfolio
des = run_call_centre_des(n_agents=int(peak_staff), ...)
```

Narrative: **strategy sets capacity band; DES stress-tests service**.

## Pairing pattern 2: DES → SD calibration

1. DES estimates **mean wait** and **max_queue** for a peak hour.
2. Set SD initial `backlog` or validate that λ and μ implied congestion aligns **directionally**.

| DES output | SD use |
|------------|--------|
| `max_queue` | Initial backlog or peak comparison |
| `mean_wait` | Qualitative only (SD has no wait stock) |
| Utilization | Check `arrival_rate` vs `staffed × μ` |

## Pairing pattern 3: ABM patience + SD staffing

- **SD** sets slow `staffed_agents` path (quarterly).
- **ABM** runs weekly with `n_agents` sampled from SD staffing stock.
- Compare **abandon_rate** distributions conditional on staffing.

Keeps HR loops aggregate while behavioural rules stay micro.

## Normalizing KPIs (Module 06 preview)

Course helper maps paradigms to shared names:

```python
def normalize_simulation_metrics(paradigm: str, raw: dict) -> dict[str, float]:
  ...
```

For SD, `mean_delay` proxy is `final_backlog`; `peak_queue` uses `max(backlog_history)`. **Do not** present those as interchangeable with DES mean wait without a disclaimer.

## Multimethod credibility ladder

| Level | Description |
|-------|-------------|
| 1 | Same λ, μ, c; qualitative story match |
| 2 | Aligned time windows; KPI definitions documented |
| 3 | DES validates ABM timing subset |
| 4 | SD drives staffing scenarios tested in DES |

Aim for **level 2** in the course capstone; level 3+ for portfolio extras.

## When *not* to pair

- Forcing SD backlog to equal DES queue length every minute—**overfitting** linkage.
- Using SD abandons without ABM or DES abandonment logic—**missing physics**.

## Tool boundaries

| Tool | Module | Role in pair |
|------|--------|--------------|
| SimPy | 03 | Timing anchor |
| Mesa | 04 | Behavioural heterogeneity |
| Euler SD | 05 | Workforce/policy horizon |

Optional external SD GUIs (Stella, Vensim) still export equations—you already implement the core in Python.

## Documentation template

When submitting paired models:

```markdown
## Paradigm roles
- SD: staffing + backlog over 90 days, dt=1 day
- DES: SLA check for month 2 peak, n_agents from SD

## Known mismatches
- SD ignores abandonment
- DES ignores hiring delay
```

## Key takeaways

- SD is **strategic**; DES is **operational timing**; ABM is **behavioural**—compose, don’t merge blindly.
- Pair models via **capacity paths**, **shared λ/μ**, and **documented KPI proxies**.
- Use `normalize_simulation_metrics` with explicit **semantic caveats**.
- State SD limits in every comparison brief stakeholders will read.
