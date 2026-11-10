# Three Lenses, Same Call Centre

**Northline Support** is one operational system. **DES**, **ABM**, and **SD** are three faithful simplifications—not three competing realities. Module 06 teaches you to hold all three in view without flattening differences.

## One scenario, three encodings

| Shared story element | DES (SimPy) | ABM (Mesa) | SD (Euler) |
|---------------------|-------------|------------|------------|
| Calls arrive | `arrival_process` timeouts | Bernoulli `arrival_prob` / tick | Flow `λ · dt` |
| Agents serve | `Resource(c)` | `n_agents` + `service_prob` | `staffed × μ · dt` |
| Congestion KPI | `mean_wait`, `max_queue` | `waiting`, `abandon_rate` | `backlog`, peak history |
| Time | Event `env.now` | Integer steps | `steps × dt` |

Parameters λ, μ, and c from Module 02 anchor **names** across models even when units differ slightly.

## Strengths and blind spots

| Lens | Strength on Northline | Blind spot |
|------|----------------------|------------|
| DES | Precise waits, queue depth events | Slow HR feedback without extra stocks |
| ABM | Patience segments, local rules | Tick time ≠ exact telephony |
| SD | Hiring/attrition loops, backlog arcs | No per-call abandonment by default |

None replaces the others—they **answer different questions** on the same floor.

## Conceptual alignment diagram

```
           ┌──────────── Northline KPIs ────────────┐
           │ mean wait · abandon · throughput · Q   │
           └─────────────────┬────────────────────┘
                             │
        ┌────────────────────┼────────────────────┐
        ▼                    ▼                    ▼
    ┌───────┐           ┌─────────┐         ┌──────────┐
    │  DES  │           │   ABM   │         │    SD    │
    │ events│           │ agents  │         │  stocks  │
    └───────┘           └─────────┘         └──────────┘
        │                    │                    │
   minute SLAs          behaviour tests      workforce quarters
```

## Running the “same” experiment (method)

1. Write a **scenario card** (λ, μ, c/agents, horizon, seed policy).
2. Implement each paradigm without retro-tuning to match outputs.
3. Map outputs through **`normalize_simulation_metrics`**.
4. Compare **directions** and **orders of magnitude**, not bitwise equality.

```python
from challenges.compare_paradigms import normalize_simulation_metrics  # capstone path

des_kpi = normalize_simulation_metrics("des", des_raw)
abm_kpi = normalize_simulation_metrics("abm", abm_raw)
sd_kpi = normalize_simulation_metrics("sd", sd_raw)
```

Read field names as **proxies**—see lesson 02 comparison brief.

## When stories agree

Expect qualitative agreement when:

- Abandonment is **off** or patience is huge (ABM ≈ DES utilization).
- SD staffing is **fixed**, λ and μ imply stable \(A < 1\), and you compare congestion trends.
- Horizons are short and backlog in SD starts near DES queue snapshot.

## When stories diverge (on purpose)

| Feature enabled | Expected divergence |
|-----------------|---------------------|
| ABM patience | Higher effective loss vs DES without abandon |
| SD hiring delay ignored | Staff differs from constant c in DES |
| Coarse ABM ticks | Mean wait differs from DES exponential draws |

Divergence is **information**, not failure—document the cause.

## Decision routing table

| If the decision is… | Lead lens | Supporting lenses |
|---------------------|-----------|-------------------|
| Intraday SLA staffing | DES | ABM for abandon segments |
| IVR patience messaging | ABM | DES for timing check |
| Quarterly hiring plan | SD | DES peak validation |

## Anti-patterns

| Anti-pattern | Why it hurts |
|--------------|--------------|
| Picking the model that gave the “best” number | Confirmation bias |
| Averaging DES and SD outputs as “truth” | Mixes semantics |
| Ignoring units on `mean_delay` after normalize | Misleading tables |

## Northline narrative example

**Question:** “Can we reduce abandons 20% without new hires?”

- **ABM** — test patience messaging (longer effective patience distribution).
- **DES** — verify wait distribution improves for SLA.
- **SD** — check backlog side-effects if abandon drops (more answered → longer handles? optional extension).

Lead with ABM; use DES as timing referee; mention SD only if backlog feedback to hiring matters.

## Key takeaways

- One call centre, **three purposeful simplifications**.
- Align **inputs** and **KPI definitions**; expect **output** differences when grains differ.
- Use normalization helpers with a **glossary** of what each field means per paradigm.
- Choose a **lead lens** from the decision horizon, not from favourite tooling.
