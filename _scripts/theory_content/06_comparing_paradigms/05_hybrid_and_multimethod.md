# Hybrid & Multi-Method Models

Real Northline programmes rarely stay inside one paradigm. **Hybrid** and **multi-method** workflows chain DES, ABM, and SD—or embed one inside another—so each engine handles the time scale and entity detail it does best.

## Definitions

| Term | Meaning |
|------|---------|
| **Multi-method** | Separate models, linked by hand via scenario cards and KPI tables |
| **Hybrid** | One workflow invokes another automatically (SD → DES batch) |
| **Nested** | Micro model runs inside macro steps (ABM week inside SD month) |

The course capstone starts **multi-method**; hybrids are optional portfolio enhancements.

## Reference architectures

### Architecture A: SD masters staffing, DES audits SLAs

```
SD (quarterly staff path) ──► sample n_agents(t) ──► DES peak-week SLA runs
```

**Use when** hiring policy is the decision; SLAs are a constraint check.

```python
sd = run_call_centre_sd(initial, params, steps=90, dt=1.0)
n_peak = int(sd["final_staffed"])  # or max from history in full version
sla = run_call_centre_des(n_agents=max(1, n_peak), ...)
```

### Architecture B: DES calibrates ABM ticks

```
DES (event timing) ──► implied wait bands ──► tune arrival_prob / service_prob
```

**Use when** ABM behavioural rules are central but timing felt wrong.

### Architecture C: ABM feeds effective demand into SD

```
ABM abandon scenarios ──► effective λ or loss factor ──► SD backlog projection
```

**Use when** marketing changes patience mix and leadership wants quarterly backlog.

## Coupling contracts

Define **interfaces** between models:

| Contract field | Type | Example |
|----------------|------|---------|
| `staffing_series` | list[float] | Agents per day |
| `effective_arrival_rate` | float | λ after abandon proxy |
| `horizon_minutes` | int | Alignment window |

Version the contract in git when parameters change.

## Syncing time axes

| Paradigm | Horizon in course labs |
|----------|------------------------|
| DES | Until `max_calls` or env idle |
| ABM | `steps` ticks |
| SD | `steps × dt` minutes |

Convert explicitly:

```python
abm_minutes = abm_steps * minutes_per_tick
sd_minutes = sd_steps * dt
assert abs(abm_minutes - sd_minutes) < 1e-6  # when aligning
```

## Failure modes in hybrids

| Pitfall | Prevention |
|---------|------------|
| Double-counting abandons | One model owns loss physics |
| DES stationary staff, SD varying staff | Interpolate `n_agents(t)` |
| KPI apples-to-oranges | Glossary in comparison brief |
| Feedback loop cut | Document open loop vs closed |

## Multi-method credibility without hybrid code

You can deliver value **without** orchestration scripts:

1. SD story for hiring
2. DES table for peak SLA at SD’s staff level
3. ABM table for patience intervention

Peer reviewers check **logical chain**, not microservice elegance.

## Optional orchestration sketch

```python
def multimethod_northline(scenario: dict) -> dict:
  sd_out = run_call_centre_sd(scenario["sd_initial"], scenario["sd_params"], steps=scenario["sd_steps"], dt=scenario["dt"])
  des_out = run_call_centre_des(n_agents=int(sd_out["final_staffed"]), **scenario["des"])
  abm_out = run_call_centre_abm(n_agents=int(sd_out["final_staffed"]), **scenario["abm"])
  return {
    "sd": normalize_simulation_metrics("sd", sd_out),
    "des": normalize_simulation_metrics("des", des_out),
    "abm": normalize_simulation_metrics("abm", abm_out),
  }
```

Add error handling and staff history before production use.

## When to stop adding methods

| Signal | Action |
|--------|--------|
| Third model adds no new KPI insight | Drop it |
| Validation budget exhausted | Freeze scope |
| Stakeholders confused | Simplify to lead lens + one support |

## Governance

- Name **owner** of each sub-model assumptions.
- Log **version** of challenge files when re-running hybrid chains.
- Store **artifacts** (`backlog_history`, seed lists) in portfolio zip.

## Key takeaways

- **Multi-method** linking is the course default; **hybrid** automation is a power-up.
- Publish **coupling contracts** and time-axis conversions between DES, ABM, and SD.
- Let one paradigm **own** each physical effect (loss, staffing, timing).
- Stop when added complexity no longer changes the Northline recommendation.
