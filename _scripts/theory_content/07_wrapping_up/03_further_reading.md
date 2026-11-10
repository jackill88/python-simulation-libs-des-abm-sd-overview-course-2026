# Further Reading & Next Models

You have a working **Northline** stack in Python. This lesson points to **deeper references** for discrete-event, agent-based, and system dynamics work—plus sensible **next models** when you outgrow the course scope.

## Discrete-event simulation (SimPy)

| Resource | Focus |
|----------|-------|
| [SimPy documentation](https://simpy.readthedocs.io/) | Processes, resources, monitors |
| Gross & Harris, *Fundamentals of Queueing Theory* | M/M/c, stability, performance measures |
| Law, *Simulation Modeling and Analysis* | DES methodology, output analysis |
| Course Module 03 theory | Event calendar, warm-up, run length |

**Next Northline extensions**

- Add **abandonment** as timeout while waiting on `resource.request()`.
- Log **time-series** queue length for comparison to SD backlog.
- Use `simpy.PriorityResource` for VIP callers.

```python
# Sketch: abandon after patience seconds in DES
with resource.request() as req:
  res = yield req | env.timeout(patience)
  if res != req:
    # abandoned
    ...
```

## Agent-based modelling (Mesa)

| Resource | Focus |
|----------|-------|
| [Mesa documentation](https://mesa.readthedocs.io/) | Agents, schedulers, DataCollector |
| Railsback & Grimm, *Agent-Based and Individual-Based Modeling* | ODD protocol, design patterns |
| Bonabeau, “Agent-Based Modeling” (PNAS overview) | When ABM wins |
| Course Module 04 theory | Patience, emergence, observability |

**Next Northline extensions**

- Implement **skill tiers** (`service_prob` per agent class).
- Add **supervisor** agents that toggle routing when `len(waiting) > k`.
- Export Mesa DataCollector to CSV for Module 06 figures.

```python
from mesa.datacollection import DataCollector
# model_reporters={"AbandonRate": lambda m: m.abandon_rate}
```

## System dynamics

| Resource | Focus |
|----------|-------|
| Sterman, *Business Dynamics* | Stocks, flows, loop dominance |
| Rahmandad, *System Dynamics* (MIT OpenCourseWare notes) | Policy design |
| Course Module 05 theory | Euler steps, HR loops |
| [PySD](https://pysd.readthedocs.io/) (optional) | Read classic SD models in Python |

**Next Northline extensions**

- Add **in-service** stock and **abandonment** flow from backlog.
- Replace constant `hiring_rate` with **threshold policy** on backlog.
- Couple attrition to backlog stress multiplier.

```python
# Stress-linked attrition (portfolio idea)
attrition = base_attrition * (1.0 + 0.02 * backlog) * staffed * dt
```

## Operations research breadth

| Topic | Why after Northline |
|-------|---------------------|
| Erlang C / workforce scheduling | Connect DES outputs to staffing calculators |
| Discrete optimization | Agent rostering given SIM outputs |
| Sensitivity / metamodels | Surrogate λ–c–SLA surfaces |

## Reproducibility & software practice

| Practice | Reference habit |
|----------|-----------------|
| `random.Random(seed)` per subsystem | Course Modules 03–04 |
| Versioned scenario YAML | Module 06 brief |
| pytest as living verification | All challenge folders |

## Communities & models (explore, don’t cram)

- **COSSA / OpenABM** model library patterns for agent models.
- **NetLogo models** (conceptual); translate ideas to Mesa/Python.
- **Vensim/Stella** example models for SD pedagogy—re-implement key loops in course Euler style.

## Suggested learning path (after this course)

```text
Week A — DES depth: SimPy + one abandonment variant + confidence intervals on mean wait
Week B — ABM depth: segment mix + calibration table + DataCollector plots
Week C — SD depth: hiring delay stock + dt sensitivity report
Week D — Multi-method brief for a NEW domain (clinic, warehouse, helpdesk)
```

Repeat the **comparison brief** format each week.

## Staying grounded in Northline

When reading advanced texts, ask:

1. What is the **time grain**?
2. What entity is **smallest**?
3. What **feedback** is explicit?

If you can map answers to DES, ABM, or SD, you are reading actively—not collecting bibliography.

## Key takeaways

- **SimPy**, **Mesa**, and **SD textbooks** deepen what the course introduced in miniature.
- Next models should add **one physical effect at a time** (abandon in DES, segments in ABM, delays in SD).
- Keep **pytest + scenario cards** as habits when scaling complexity.
- Reuse the Module 06 **brief template** on every new domain—you already know how to compare paradigms.
