# Conclusion

You began with **Northline Support** as a queueing story—λ, μ, c, mean wait, abandon rate. You leave with **three executable lenses** and a discipline for comparing them without pretending they are the same equation in different fonts.

## What you built

| Module | Paradigm | Core skill |
|--------|----------|------------|
| 03 | Discrete-event simulation | Event calendars, SimPy resources, wait distributions |
| 04 | Agent-based modelling | Mesa structure, patience rules, emergent KPIs |
| 05 | System dynamics | Stocks, flows, Euler integration, HR feedback |
| 06 | Comparison | Briefs, V&V, experiments, normalization |

The challenges are modest in line count; the **method** is not—scenario cards, units, seeds, and honest limits.

## The through-line

Every paradigm answers: *“If we assume the world works like this simplified mechanism, what happens to congestion, throughput, and staffing?”*

- **DES** privileges **when** things happen.
- **ABM** privileges **who** follows which rule.
- **SD** privileges **how much** has accumulated and how policies push back.

Northline stays constant so you practice **translation**, not memorizing three unrelated demos.

## What “done” looks like

You are in strong shape when you can:

1. Pick a **lead lens** from the decision horizon in under a minute.
2. Run pytest for each challenge and explain **one** verification test per paradigm.
3. Produce a **comparison brief** with a KPI glossary, not only a table of numbers.
4. State **what you did not model** (abandonment in SD, sub-minute SLAs in ABM ticks).

## From classroom to workplace

Operational research and data science teams rarely ship a single SimPy file. They ship **traceable studies**:

- Frozen assumptions
- Sensitivity on 2–3 factors
- Visuals aligned to stakeholder language (waits vs backlog vs abandon)

Carry the **comparison brief** format into internships and capstones—it scales better than raw notebooks alone.

## Python as integration layer

You implemented SD without a GUI, ABM without a grid, DES without a commercial simulator. That mirrors industry practice: **orchestration in code**, diagrams in markdown, tests as verification anchors.

```python
# The course’s unifying idea — names differ, structure repeats
def run_model(params: dict, *, seed: int) -> dict:
  ...
```

## Encouragement on ambiguity

Models will disagree. Your job is not to eliminate disagreement—it is to **attribute** it to time grain, abandonment physics, or staffing feedback. That attribution is professional judgement.

## Where Module 07 continues

- **Portfolio checklist** — package artefacts for reviewers.
- **Further reading** — deepen SimPy, Mesa, and SD without losing Northline context.

## A final Northline rehearsal

Pick one real question—“Do we add a fifth agent for Q4?”—and say out loud:

1. Which paradigm leads and why.
2. Which KPI decides yes/no.
3. What evidence would falsify your recommendation.

If you can answer without opening the repo, the course did its job; the repo remains your **reproducible backup**.

## Key takeaways

- Three paradigms, one call centre: **timing**, **behaviour**, **policy loops**.
- Credibility comes from **V&V, scenario cards, and documented KPI meanings**.
- Disagreement across models is expected; **explain** it, don’t hide it.
- Treat this repo as a **template** for the next operational system you model.
