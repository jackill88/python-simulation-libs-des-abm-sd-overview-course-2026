# Module 05: System Dynamics

Track backlog and staffing as **stocks** connected by **flows**.

## Learning Objectives

- Draw and read stock–flow diagrams for Northline
- Choose time step and interpret Euler integration error
- Model hiring, attrition, and backlog feedback
- Connect SD curves to DES/ABM KPIs qualitatively

## Lessons

| # | Topic | Theory |
|---|-------|--------|
| 1 | Why SD for Workforce Loops | [theory/01_why_sd.md](theory/01_why_sd.md) |
| 2 | Stocks, Flows & Notation | [theory/02_stocks_flows_notation.md](theory/02_stocks_flows_notation.md) |
| 3 | Northline Stock–Flow Diagram | [theory/03_stock_flow_diagram_northline.md](theory/03_stock_flow_diagram_northline.md) |
| 4 | Euler Integration & Time Step | [theory/04_euler_and_time_step.md](theory/04_euler_and_time_step.md) |
| 5 | Feedback Loops (Hiring & Attrition) | [theory/05_feedback_loops_hr.md](theory/05_feedback_loops_hr.md) |
| 6 | SD Limits & Pairing with DES/ABM | [theory/06_sd_limits_and_pairing.md](theory/06_sd_limits_and_pairing.md) |

## Quiz

[quizzes/module_quiz.md](quizzes/module_quiz.md)

## Challenge

[challenges/call_centre_sd.py](challenges/call_centre_sd.py)

```bash
pytest tests/05_system_dynamics/test_call_centre_sd.py -v
```
