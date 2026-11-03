# Python Simulation Libraries: DES, ABM & System Dynamics

A self-paced, test-driven course on **three simulation paradigms in Python**, using one shared scenario: the imaginary **Northline Support** call centre.

## Learning Objectives

After finishing this course, you will be able to:

- Frame operational questions (KPIs, stability, time grain) before choosing a library
- Build a **discrete-event** call-centre model with **SimPy**
- Build an **agent-based** model with **Mesa** (callers, agents, patience)
- Build a **system dynamics** backlog/staffing model with Euler integration
- Compare outputs across paradigms on a normalized scorecard

## Libraries

| Paradigm | Library | Role in course |
|----------|---------|----------------|
| Discrete-Event Simulation (DES) | [SimPy](https://simpy.readthedocs.io/) | Event calendar, queues, agents as resources |
| Agent-Based Modelling (ABM) | [Mesa](https://mesa.readthedocs.io/) | Individual callers & agents, discrete ticks |
| System Dynamics (SD) | NumPy-style equations (pure Python) | Stocks, flows, hiring/attrition feedback |

Supporting tools: **pytest** (verify labs), **Pydantic** (typed snapshots), **Streamlit/Flet** (course navigator apps — same layout as the AI backend course).

## Course Structure

| Module | Topic | Challenges |
|--------|-------|------------|
| [01_get_started](01_get_started/README.md) | Get Started | — |
| [02_the_call_centre](02_the_call_centre/README.md) | The Call Centre Story | 1 lab |
| [03_discrete_event_simulation](03_discrete_event_simulation/README.md) | Discrete-Event Simulation (SimPy) | 1 project |
| [04_agent_based_modelling](04_agent_based_modelling/README.md) | Agent-Based Modelling (Mesa) | 1 project |
| [05_system_dynamics](05_system_dynamics/README.md) | System Dynamics | 1 lab |
| [06_comparing_paradigms](06_comparing_paradigms/README.md) | Comparing Paradigms | 1 capstone |
| [07_wrapping_up](07_wrapping_up/README.md) | Wrapping Up | — |

Each module contains:

- **`theory/`** — Markdown lessons with explanations and Python examples
- **`quizzes/`** — Self-check multiple-choice quizzes
- **`challenges/`** — Python files with function stubs (where applicable)

Tests live in **`tests/`**, organized by module.

## Getting Started

```bash
pip install -r requirements.txt
pytest -v
```

When **all tests pass**, you have completed the hands-on parts of the course.

Maintainers can sanity-check content:

```bash
python3 _scripts/verify_course.py
python3 _scripts/verify_tests.py
```

## Course Navigator App

### Streamlit (desktop / browser)

```bash
pip install -r requirements-app.txt
streamlit run app/main.py
```

### Flet (Android APK)

```bash
pip install -r requirements-flet.txt
python flet_app/prepare_assets.py   # copies markdown to flet_app/bundled_course + course_nav
flet run flet_app/main.py

# Build offline APK (run prepare_assets immediately before build)
python flet_app/prepare_assets.py
flet build apk
```

The APK reads course files from `flet_app/bundled_course/` (plain app files). Markdown under `assets/` alone is not reliably readable on Android via Python `Path.read_text`.
