# Module 03: Discrete-Event Simulation (SimPy)

Model Northline as arriving calls, a FIFO wait line, and c parallel agents.

## Learning Objectives

- Explain events, processes, and resources in SimPy
- Implement reproducible M/M/c-style DES for the call centre

## Lessons

| # | Topic | Theory |
|---|-------|--------|
| 1 | Why DES for Call Centres | [theory/01_why_des.md](theory/01_why_des.md) |
| 2 | SimPy Processes & Resources | [theory/02_simpy_processes.md](theory/02_simpy_processes.md) |

## Quiz

[quizzes/module_quiz.md](quizzes/module_quiz.md)

## Challenge

[challenges/call_centre_des.py](challenges/call_centre_des.py)

```bash
pytest tests/03_discrete_event_simulation/test_call_centre_des.py -v
```
