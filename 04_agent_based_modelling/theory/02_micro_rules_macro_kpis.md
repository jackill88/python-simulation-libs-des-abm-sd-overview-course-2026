# Micro Rules, Macro KPIs

Operations at **Northline Support** read dashboards: mean wait, abandon rate, service level. None of those numbers is typed into the model as a magic dial. They **emerge** when thousands of micro decisions—wait one more tick, attempt service, hang up—accumulate.

This lesson separates **what each agent does** from **what leadership measures**.

## Emergence in one sentence

> Macro patterns appear at the population level without being hard-coded as global equations.

If every caller uses the same patience rule but arrivals are random, you still get a **distribution** of waits and abandons—not a single deterministic outcome.

## Heterogeneity: same macro name, different micro stories

Two models can report **abandon_rate = 0.12** with different mechanisms:

| Model | Micro story | Same macro KPI? |
|-------|-------------|-----------------|
| A | All callers patience = 3 ticks | 12% abandon |
| B | 50% patience = 1, 50% patience = 8 | 12% abandon |

Leadership sees one KPI; modellers must know **which callers left**. ABM preserves that split in agent state and in post-run aggregates.

## Mapping Northline micro rules to KPIs

| Micro rule (caller) | Micro rule (agent) | Likely macro effect |
|---------------------|--------------------|---------------------|
| `waited += 1` each tick in queue | Idle until assigned | Queue builds → higher mean wait |
| `waited > patience` → abandon | — | Raises **abandon_rate**, lowers served count |
| — | `service_prob` per tick when free | Throughput ceiling; stochastic completions |
| Arrival Bernoulli trial each tick | Fixed `n_agents` | Utilization and congestion |

The course lab collapses service into a probability per tick per free agent—didactic, not literal telephony—but the **pattern** matches richer models: local rules → global counts.

## Worked intuition: patience shock

Baseline: `default_patience = 4`, `arrival_prob = 0.35`, four agents, 200 steps.

**Experiment:** drop patience to 2 for half of new callers.

```python
def patience_for_new_caller(rng: random.Random, default: int) -> int:
  if rng.random() < 0.5:
    return default // 2
  return default
```

You may see **abandon_rate rise** while **mean service time per agent** is unchanged—because callers leave the queue, not because agents slowed down. That confound is common in real A/B tests; ABM makes it visible.

## Decomposition checklist

When a KPI moves, ask:

1. **Arrivals** — more entities or higher per-tick probability?
2. **Capacity** — fewer free agents or lower service success?
3. **Patience / routing** — who leaves early or takes a different path?
4. **Measurement** — warm-up ticks included? Denominator for rates?

```python
total_finished = served + abandoned
abandon_rate = abandoned / total_finished if total_finished else 0.0
```

Align this definition with Module 06 normalization so DES, ABM, and SD sit on one scorecard.

## Macro KPIs as observables, not objectives (yet)

In exploration, treat KPIs as **observables**:

```python
class CallCentreModel(Model):
  def __init__(self, ...):
    ...
    self.served_count = 0
    self.abandoned_count = 0

  @property
  def abandon_rate(self) -> float:
    done = self.served_count + self.abandoned_count
    return self.abandoned_count / done if done else 0.0
```

Optimization (staffing, patience messaging) comes **after** you trust the micro rules—a topic for Module 06 experiment design.

## Stylized facts to reproduce (validation hints)

Before trusting emergent KPIs, check micro rules produce sensible edge cases:

| Scenario | Expected macro behaviour |
|----------|--------------------------|
| `arrival_prob = 0` | Served → 0; abandon → 0 |
| Huge patience | Abandon → 0 if capacity > 0 |
| `n_agents = 0` | Queue grows; abandons dominate |

If edge cases fail, fixing macro dashboards is pointless.

## Connection to queueing theory

M/M/c mean wait formulas assume homogeneous exponential patience (often **no abandonment**). Northline ABM **relaxes** those assumptions. Compare qualitatively to DES (Module 03): when heterogeneity is off, ABM and DES should trend toward similar utilization; when patience rules turn on, they diverge—by design.

## Key takeaways

- **Emergence** links individual rules to leadership KPIs; never infer micro rules from one macro number alone.
- **Heterogeneity** means two models can match a KPI but imply different interventions.
- Track **who** contributes to abandons and serves before recommending staffing or IVR changes.
- Define rates with explicit denominators and match them across paradigms in Module 06.
