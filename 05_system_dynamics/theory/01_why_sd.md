# Why SD for Workforce Loops

**Northline Support** does not live in a single peak hour. Hiring pipelines, attrition, training backlogs, and morale feedback unfold over **weeks and quarters**. Discrete-event and agent models can simulate those stories, but **system dynamics (SD)** is built for aggregate stocks connected by flows and **feedback loops**.

## Questions SD answers well

| Horizon | Example Northline question | Why SD |
|---------|---------------------------|--------|
| Multi-month | Will backlog spiral if attrition rises 2%? | Stocks accumulate; loops explicit |
| Policy | What if we cap hiring when backlog > 50? | Flows switch with stock levels |
| Capacity planning | Agents vs backlog over a fiscal year | Staffing is a stock, not only c |

SD is weaker when leadership needs **“who waited how long at 10:07 Tuesday”**—that is DES (Module 03).

## Aggregate lens, same organisation

You still model Northline, but entities are **counts and rates**:

- **Backlog** — calls waiting (stock)
- **Staffed agents** — logged-in agents (stock)
- **Arrival rate** — calls per minute (flow into backlog)
- **Service completion** — limited by agents × productivity (flow out of backlog)
- **Hiring / attrition** — HR flows on the staffing stock

Individual caller transcripts never appear; the paradigm trades detail for **strategic clarity**.

## Feedback: the SD mindset

```text
backlog ↑ → executives approve hiring → staffed_agents ↑
    → service capacity ↑ → backlog ↓ → hiring pressure ↓
```

Delays (time to recruit, time to train) can be added as **pipeline stocks** in advanced models. The course starts with immediate hiring and attrition flows for transparency.

## Complementarity with DES and ABM

| Paradigm | Northline strength | Typical time grain |
|----------|-------------------|-------------------|
| DES | Wait distributions, SLAs | Minutes |
| ABM | Patience segments, rules | Minutes (ticks) |
| SD | Staffing–backlog loops | Days or abstract periods |

Module 06 puts KPIs on one scorecard **qualitatively**—SD backlog peaks align with congestion stories from DES, not with exact mean wait.

## When SD is the wrong first tool

Avoid starting with SD if the decision is:

- Intraday agent schedule to hit 80/30 service level.
- Routing rule A/B with per-caller outcomes.
- Calibration to Erlang C for a single peak hour.

Use SD when the **state variables** leadership debates are already aggregate (headcount, backlog, hiring rate).

## Course implementation choice

The Module 05 challenge uses **Euler integration** in plain Python—no SD GUI—so you see the equations:

```python
def run_call_centre_sd(initial, params, *, steps: int, dt: float):
  ...
```

That matches how many engineers embed SD inside larger digital twins.

## Units discipline

SD models fail in meetings when **units drift**. Northline lab conventions:

| Variable | Unit |
|----------|------|
| `backlog` | calls |
| `staffed_agents` | agents |
| `arrival_rate` | calls per minute |
| `service_rate_per_agent` | calls per agent per minute |
| `hiring_rate` | agents per minute (stylized) |
| `attrition_rate` | 1/minute (per-agent hazard stylized) |
| `dt` | minutes |

Always label axes when plotting `backlog_history`.

## Stylized vs literal HR

`hiring_rate` as a constant flow is **didactic**. Real HR is lumpy (cohorts, approvals). The point is loop **structure**, not payroll precision.

## Key takeaways

- SD targets **policy and feedback** over long horizons at Northline.
- Stocks are **accumulations**; flows are **rates**—mind your units.
- Pair SD with DES/ABM: timing detail vs strategic staffing dynamics.
- The course SD lab is **code-first Euler**, preparing you to read stock–flow diagrams and implement them.
