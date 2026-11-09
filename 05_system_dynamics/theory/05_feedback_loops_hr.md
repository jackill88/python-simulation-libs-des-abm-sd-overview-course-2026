# Feedback Loops (Hiring & Attrition)

Workforce dynamics at **Northline Support** rarely settle instantly. **Hiring** responds to backlog pain; **attrition** erodes capacity when load and morale strain agents. System dynamics makes those **loops** visible on the stock–flow canvas and in code.

## Balancing loop: hire until pain eases

Narrative:

1. **Backlog** rises (demand spike or attrition dip).
2. Leadership raises **hiring_rate** or approves contractors.
3. **Staffed agents** stock grows (with delay in reality).
4. Service capacity rises → **backlog** falls.
5. Hiring pressure eases.

Label: **B1** (balancing toward acceptable backlog).

In the minimal lab, hiring may be a **constant parameter**—you still explain the loop you are approximating:

```python
hiring = params.get("hiring_rate", 0.0) * dt
new_staffed = max(0.0, staffed + hiring - attrition)
```

## Reinforcing loop: burnout spiral

Narrative alternative when HR is slow:

1. High **backlog** → overtime and stress.
2. **Attrition_rate** effective rises (model as function of backlog in extensions).
3. **Staffed agents** falls.
4. Service capacity drops → **backlog** rises further.

Label: **R1** (reinforcing congestion spiral).

Course baseline uses **linear attrition on staff**:

```python
attrition = params.get("attrition_rate", 0.0) * staffed * dt
```

Extension sketch tying attrition to backlog:

```python
stress_multiplier = 1.0 + 0.01 * backlog
attrition = params["attrition_rate"] * stress_multiplier * staffed * dt
```

Document if you add such coupling in portfolio work.

## Table: HR flows in the Northline lab

| Flow | Parameter | Effect on stock |
|------|-----------|-----------------|
| Hiring | `hiring_rate` (agents/min) | ↑ `staffed_agents` |
| Attrition | `attrition_rate` × staff | ↓ `staffed_agents` |
| Service | `service_rate_per_agent` × staff | ↓ `backlog` (via capacity) |

## Delays matter (conceptual)

Real hiring loops include **delays**:

| Delay | Modeling pattern |
|-------|------------------|
| Approval time | Hiring flow gated by backlog > threshold for N days |
| Training | New hires enter a `trainees` stock before `staffed_agents` |
| Recruiting pipeline | Third stock “offers accepted” |

The course omits pipeline stocks to keep `sd_euler_step` readable—call that out when advising executives.

## Scenario: attrition shock

Initial: 4 agents, stable λ, hiring matches attrition.

**Shock:** double `attrition_rate` for a quarter (simulate with higher rate param).

| Time | Expectation |
|------|-------------|
| Early | Staff falls unless hiring jumps |
| Mid | Backlog accumulates if λ > capacity |
| Late | Higher hiring restores balance (if policy allows) |

```python
params_shock = {
  **params,
  "attrition_rate": params["attrition_rate"] * 2,
  "hiring_rate": params["hiring_rate"] * 1.5,  # partial response
}
```

Plot `backlog_history` for narrative slides.

## Coupling backlog and staffing decisions

Policy table (stylized):

| Backlog level | HR policy |
|---------------|-----------|
| < 5 | Maintain hiring at baseline |
| 5–15 | Increase `hiring_rate` 50% |
| > 15 | Emergency contractor flow |

Implementation requires **conditional flows**—beyond the base lab but excellent portfolio extensions.

## Contrasting SD HR with ABM shift rules

| Aspect | SD HR loop | ABM shift rules |
|--------|-----------|-----------------|
| Unit | Headcount stock | Individual agents |
| Attrition | Aggregate rate | Per-agent churn rules |
| Best question | “Do we oscillate?” | “Which team burns out first?” |

Use both lenses in hybrid designs (Module 06).

## Stability check using traffic intensity

From Module 02:

```python
A = arrival_rate / (staffed_agents * service_rate_per_agent)
# A < 1 suggests capacity can balance average inflow (steady-state intuition)
```

SD can show **temporary** backlog even when long-run \(A < 1\) due to initial conditions—do not confuse transient with instability.

## Key takeaways

- **Hiring** and **attrition** move the **staffed_agents** stock; service capacity feeds back on **backlog**.
- Name **balancing** vs **reinforcing** loops when telling Northline workforce stories.
- Lab uses constant rates; real credibility requires **delays** and conditional policies in extensions.
- Cross-check capacity vs λ using traffic-intuition; plot backlog after HR shocks.
