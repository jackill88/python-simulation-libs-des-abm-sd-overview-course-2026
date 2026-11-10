"""Module README templates (theory file list lives in theory_manifest)."""

from __future__ import annotations

from theory_manifest import THEORY_LESSONS

_LESSON_ROW = '| {n} | {title} | [theory/{file}](theory/{file}) |'


def theory_table(module_id: str) -> str:
    rows = [
        _LESSON_ROW.format(n=i + 1, title=title, file=filename)
        for i, (filename, title) in enumerate(THEORY_LESSONS[module_id])
    ]
    return "\n".join(
        [
            "| # | Topic | Theory |",
            "|---|-------|--------|",
            *rows,
        ]
    )


MODULE_READMES: dict[str, str] = {
    "01_get_started": f"""# Module 01: Get Started

Welcome to the Northline Support simulation track.

## Learning Objectives

- Understand how theory, quizzes, and pytest challenges fit together
- Follow a repeatable simulation workflow (question → model → verify → communicate)
- Know which Python libraries map to DES, ABM, and SD

## Lessons

{theory_table("01_get_started")}

## Suggested Study Path

1. Read lessons 1–3 in order (about 45–60 minutes)
2. Skim the Python stack reference
3. Continue to Module 02 for the shared call-centre scenario
""",
    "02_the_call_centre": f"""# Module 02: The Call Centre Story

Define **Northline Support** — the scenario every later model shares.

## Learning Objectives

- Describe the imaginary centre, its KPIs, and operational constraints
- Compute traffic intensity, stability, and simple service-level intuition
- Map the same parameters across DES, ABM, and SD representations
- Implement the queueing metrics lab

## Lessons

{theory_table("02_the_call_centre")}

## Quiz

[quizzes/module_quiz.md](quizzes/module_quiz.md)

## Challenge

Implement [challenges/queueing_metrics.py](challenges/queueing_metrics.py):

```bash
pytest tests/02_the_call_centre/test_queueing_metrics.py -v
```

## Suggested Study Path

1. Lessons 1–3 (scenario + queueing)
2. Lesson 4 (KPIs) and lesson 6 (cross-paradigm mapping)
3. Quiz, then lab
""",
    "03_discrete_event_simulation": f"""# Module 03: Discrete-Event Simulation (SimPy)

Model Northline as arriving calls, a FIFO wait line, and **c** parallel agents.

## Learning Objectives

- Explain events, processes, resources, and monitors in SimPy
- Build an M/M/c-style DES with reproducible seeds
- Collect queue statistics and interpret warm-up / run length
- Relate simulation output to queueing intuition from Module 02

## Lessons

{theory_table("03_discrete_event_simulation")}

## Quiz

[quizzes/module_quiz.md](quizzes/module_quiz.md)

## Challenge

[challenges/call_centre_des.py](challenges/call_centre_des.py)

```bash
pytest tests/03_discrete_event_simulation/test_call_centre_des.py -v
```
""",
    "04_agent_based_modelling": f"""# Module 04: Agent-Based Modelling (Mesa)

Model callers and agents as **individuals** on a discrete time grid.

## Learning Objectives

- Separate micro-rules from macro KPIs (emergence)
- Structure a Mesa 2.x model: agents, schedule, model step
- Encode patience, service success, and abandonment
- Observe and debug agent populations

## Lessons

{theory_table("04_agent_based_modelling")}

## Quiz

[quizzes/module_quiz.md](quizzes/module_quiz.md)

## Challenge

[challenges/call_centre_abm.py](challenges/call_centre_abm.py)

```bash
pytest tests/04_agent_based_modelling/test_call_centre_abm.py -v
```
""",
    "05_system_dynamics": f"""# Module 05: System Dynamics

Track backlog and staffing as **stocks** connected by **flows**.

## Learning Objectives

- Draw and read stock–flow diagrams for Northline
- Choose time step and interpret Euler integration error
- Model hiring, attrition, and backlog feedback
- Connect SD curves to DES/ABM KPIs qualitatively

## Lessons

{theory_table("05_system_dynamics")}

## Quiz

[quizzes/module_quiz.md](quizzes/module_quiz.md)

## Challenge

[challenges/call_centre_sd.py](challenges/call_centre_sd.py)

```bash
pytest tests/05_system_dynamics/test_call_centre_sd.py -v
```
""",
    "06_comparing_paradigms": f"""# Module 06: Comparing Paradigms

Place DES, ABM, and SD on one scorecard without pretending they are identical.

## Learning Objectives

- Compare paradigms by decision horizon, granularity, and uncertainty
- Apply verification vs validation (V&V) proportionally
- Design experiments and hybrid model chains
- Implement KPI normalization for the capstone

## Lessons

{theory_table("06_comparing_paradigms")}

## Quiz

[quizzes/module_quiz.md](quizzes/module_quiz.md)

## Challenge

[challenges/compare_paradigms.py](challenges/compare_paradigms.py)

```bash
pytest tests/06_comparing_paradigms/test_compare_paradigms.py -v
```
""",
    "07_wrapping_up": f"""# Module 07: Wrapping Up

Consolidate skills and plan portfolio-quality simulation work.

## Lessons

{theory_table("07_wrapping_up")}

## Optional extensions

- DES: shift schedules, time-varying arrival rates
- ABM: skill tiers and priority queues
- SD: morale stock feeding attrition
""",
}
