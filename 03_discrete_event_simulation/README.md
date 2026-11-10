# Module 03: Discrete-Event Simulation (SimPy)

Model Northline as arriving calls, a FIFO wait line, and **c** parallel agents.

## Learning Objectives

- Explain events, processes, resources, and monitors in SimPy
- Build an M/M/c-style DES with reproducible seeds
- Collect queue statistics and interpret warm-up / run length
- Relate simulation output to queueing intuition from Module 02

## Lessons

| # | Topic | Theory |
|---|-------|--------|
| 1 | Why DES for Call Centres | [theory/01_why_des.md](theory/01_why_des.md) |
| 2 | DES Concepts & Event Calendar | [theory/02_des_concepts.md](theory/02_des_concepts.md) |
| 3 | SimPy Processes & Resources | [theory/03_simpy_processes.md](theory/03_simpy_processes.md) |
| 4 | M/M/1 and M/M/c at Northline | [theory/04_mm_queues_at_northline.md](theory/04_mm_queues_at_northline.md) |
| 5 | Statistics, Warm-up & Run Length | [theory/05_statistics_warmup_run_length.md](theory/05_statistics_warmup_run_length.md) |
| 6 | DES Validation Checklist | [theory/06_des_validation_checklist.md](theory/06_des_validation_checklist.md) |

## Quiz

[quizzes/module_quiz.md](quizzes/module_quiz.md)

## Challenge

[challenges/call_centre_des.py](challenges/call_centre_des.py)

```bash
pytest tests/03_discrete_event_simulation/test_call_centre_des.py -v
```
