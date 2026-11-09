# Module 04: Agent-Based Modelling (Mesa)

Model callers and agents as **individuals** on a discrete time grid.

## Learning Objectives

- Separate micro-rules from macro KPIs (emergence)
- Structure a Mesa 2.x model: agents, schedule, model step
- Encode patience, service success, and abandonment
- Observe and debug agent populations

## Lessons

| # | Topic | Theory |
|---|-------|--------|
| 1 | Why ABM for Call Centres | [theory/01_why_abm.md](theory/01_why_abm.md) |
| 2 | Micro Rules, Macro KPIs | [theory/02_micro_rules_macro_kpis.md](theory/02_micro_rules_macro_kpis.md) |
| 3 | Mesa Model Structure (2.x) | [theory/03_mesa_structure.md](theory/03_mesa_structure.md) |
| 4 | Schedulers & Discrete Time | [theory/04_schedulers_and_time_steps.md](theory/04_schedulers_and_time_steps.md) |
| 5 | Patience, Abandonment & Calibration | [theory/05_patience_abandonment_calibration.md](theory/05_patience_abandonment_calibration.md) |
| 6 | Observability & Debugging ABMs | [theory/06_abm_observability.md](theory/06_abm_observability.md) |

## Quiz

[quizzes/module_quiz.md](quizzes/module_quiz.md)

## Challenge

[challenges/call_centre_abm.py](challenges/call_centre_abm.py)

```bash
pytest tests/04_agent_based_modelling/test_call_centre_abm.py -v
```
