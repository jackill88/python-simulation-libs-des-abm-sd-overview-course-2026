# Why ABM for Call Centres

**Northline Support** already has a discrete-event model (Module 03) that records exact arrival and service times. That lens is ideal when the question is *“What is the wait-time distribution with four agents at λ = 10?”*

Agent-based modelling (ABM) answers a sibling question: *“What happens when callers and agents are not interchangeable?”*

## When aggregates hide the story

Classic queueing assumes homogeneous callers and identical servers. Real centres violate both assumptions:

| Real behaviour | Why spreadsheets struggle | Why ABM fits |
|----------------|---------------------------|--------------|
| Callers abandon at different thresholds | Abandon rate is not a single constant | Each caller carries `patience` |
| Agents differ in handle time | Mean μ hides a distribution | Each agent can hold skill state |
| Supervisors change routing mid-shift | Rules are conditional | Rules live on agents or the model |

ABM makes **micro-rules** explicit. Macro KPIs—mean wait, abandon rate, queue length—**emerge** from many local interactions rather than from a single closed-form equation.

## Methodological stance

Think of ABM as a **synthetic population**:

1. **Entities** — callers, agents, supervisors (optional).
2. **State** — patience remaining, busy/idle, queue position.
3. **Rules** — what each entity does when activated (arrive, wait, serve, abandon).
4. **Schedule** — who moves on this tick and in what order.

You are not solving for equilibrium; you are **running a policy in silico** and measuring outcomes.

## Northline example: two patience types

Suppose Northline segments callers:

- **Billing** (60%): hang up if wait exceeds 2 minutes.
- **Technical** (40%): tolerate 5 minutes but retry later if abandoned.

A single `abandon_rate` parameter in DES cannot express that split without extensions. In ABM you spawn callers with drawn patience:

```python
import random

def spawn_caller(rng: random.Random) -> dict[str, int | str]:
  segment = "billing" if rng.random() < 0.6 else "technical"
  patience = 2 if segment == "billing" else 5  # ticks in the lab model
  return {"segment": segment, "patience": patience, "waited": 0}
```

Run the model for a peak hour; compare abandon rate **by segment**. Operations can see whether staffing fixes billing waits without over-serving technical queues.

## ABM vs DES for Northline (same KPIs, different grain)

| Aspect | DES (SimPy) | ABM (Mesa) |
|--------|-------------|------------|
| Time | Continuous; jumps to next event | Fixed ticks (e.g. one per minute) |
| Individuals | Implicit in event logic | First-class `Agent` objects |
| Wait times | Exact from event clock | Approximate unless you sub-tick |
| Rule richness | Add processes per type | Natural on agent classes |

Neither is “more correct.” DES wins on **temporal fidelity** for queueing; ABM wins on **behavioural heterogeneity** and **adaptive rules**.

## When to reach for ABM on this course

Use ABM in the Northline track when at least one of these holds:

- You care **who** abandons, not only **how many**.
- Rules are **local** (“if queue > 5, supervisor frees an agent”).
- You want to **experiment with learning** or shift protocols without rewriting event calendars.

Stay with DES when the study is narrowly queueing-theoretic and closed-form benchmarks (M/M/c) are your validation anchor.

## Python stack reminder

Module 04 uses **Mesa 2.x** (`mesa.Model`, `mesa.Agent`, `mesa.time.RandomActivation`). The challenge keeps logic minimal—no spatial grid—so you focus on call-centre dynamics, not geography.

```python
from mesa import Agent, Model

class Caller(Agent):
  def __init__(self, unique_id, model, patience: int):
    super().__init__(unique_id, model)
    self.patience = patience
    self.waited = 0
```

## Key takeaways

- ABM is the right lens when **individual rules and heterogeneity** drive the decision.
- Northline KPIs still matter; they are **outputs** of micro behaviour, not inputs alone.
- Pair ABM with DES later (Module 06): DES calibrates timing; ABM explores behavioural scenarios.
- Start simple—homogeneous patience, fixed ticks—then add segments and skills only when the question requires them.
