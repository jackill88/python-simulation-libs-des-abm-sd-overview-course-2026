# Building a Comparison Brief

Stakeholders do not read your pytest logs. They read a **comparison brief**: a short document that states the Northline question, the three models, assumptions, and findings—with enough traceability to reproduce your work.

## Brief template (recommended sections)

| Section | Content |
|---------|---------|
| 1. Decision | One sentence Northline choice |
| 2. Scenario card | λ, μ, agents, horizon, seeds |
| 3. Paradigm roles | Why DES / ABM / SD each appear |
| 4. KPI mapping | Normalized fields + caveats |
| 5. Results | Table or small chart |
| 6. Limits | What we did not model |
| 7. Recommendation | Action + uncertainty |

Keep to **2–4 pages** for course peer review; append run cards to the portfolio.

## Scenario card example

```yaml
name: northline_peak_q3_baseline
arrival_rate_per_min: 0.35
service_rate_per_agent_per_min: 0.12
agents: 4
des:
  mean_inter_arrival: 2.857  # 1/0.35
  mean_service_time: 8.333   # 1/0.12 stylized
  max_calls: 500
  seed: 42
abm:
  arrival_prob: 0.35
  service_prob: 0.5
  default_patience: 5
  steps: 200
  seed: 42
sd:
  dt: 1.0
  steps: 200
  hiring_rate: 0.0
  attrition_rate: 0.0
  initial_backlog: 0.0
```

Frozen card **before** runs prevents post-hoc tuning.

## KPI table with semantics

| Normalized field | DES meaning | ABM meaning | SD meaning |
|------------------|-------------|-------------|------------|
| `throughput` | Calls served | `served` count | `answered_today` |
| `mean_delay` | Mean wait time | **Proxy:** `abandon_rate`* | **Proxy:** `final_backlog` |
| `peak_queue` | Max DES queue | Current `waiting` / peak tick | `max(backlog_history)` |

\*Course mapping uses `abandon_rate` as ABM `mean_delay` slot—**document this quirk** in your brief or remap for presentations.

```python
# Illustration — clarify in prose when publishing
abm_kpi = normalize_simulation_metrics("abm", abm_raw)
# abm_kpi["mean_delay"] is abandon_rate in the course helper
```

## Writing defensible claims

| Weak claim | Stronger claim |
|------------|----------------|
| “SD says waits are 12 minutes.” | “SD final backlog of 12 calls suggests sustained congestion under fixed staff.” |
| “ABM and DES match.” | “Throughput within 8% with abandonment disabled; ABM higher abandon with patience=5.” |

Use **intervals** when stochastic (multiple seeds):

```python
def run_seeds(fn, seeds: list[int]) -> tuple[float, float]:
  vals = [fn(seed=s) for s in seeds]
  return sum(vals) / len(vals), max(vals) - min(vals)
```

## Visuals that work

- **Overlay** DES queue sample path (if logged) vs SD `backlog_history`—label axes.
- **Bar chart** of normalized `throughput` only—clearest cross-paradigm numeric.
- Avoid single-number **mean_delay** panels unless definitions are footnoted.

## Assumptions ledger

| ID | Assumption | Risk if wrong |
|----|------------|---------------|
| A1 | 1 ABM tick = 1 minute | SLA sub-minute wrong |
| A2 | SD no abandonment | Overstates served in crisis |
| A3 | Exponential service in DES | Tail waits mis-estimated |

Reviewers grade transparency, not omniscience.

## Peer review questions (Module 07 checklist preview)

- Can I reproduce from the scenario card?
- Is the lead lens obvious?
- Are KPI names decoded?
- Is uncertainty stated?

## Example executive summary (two sentences)

> Under λ = 0.35 and four agents, DES and ABM agree throughput is capacity-limited within Monte Carlo noise. ABM with patience=5 raises abandon to 14%, which DES without abandonment cannot see—recommend IVR test before hiring.

## Key takeaways

- A comparison brief is **scenario card + roles + KPI glossary + limits**.
- Never ship normalized metrics without **per-paradigm definitions**.
- Freeze parameters before runs; report **seeds and spread** for stochastic lenses.
- Recommend actions tied to the **lead paradigm**, with others as support.
