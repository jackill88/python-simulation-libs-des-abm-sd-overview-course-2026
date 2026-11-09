# Module 02: The Call Centre Story

Define **Northline Support** — the scenario every later model shares.

## Learning Objectives

- Describe the imaginary centre, its KPIs, and operational constraints
- Compute traffic intensity, stability, and simple service-level intuition
- Map the same parameters across DES, ABM, and SD representations
- Implement the queueing metrics lab

## Lessons

| # | Topic | Theory |
|---|-------|--------|
| 1 | Meet Northline Support | [theory/01_meet_northline.md](theory/01_meet_northline.md) |
| 2 | Queueing Basics | [theory/02_queueing_basics.md](theory/02_queueing_basics.md) |
| 3 | Choosing a Simulation Lens | [theory/03_choosing_a_lens.md](theory/03_choosing_a_lens.md) |
| 4 | KPIs & Service Levels | [theory/04_kpis_and_service_levels.md](theory/04_kpis_and_service_levels.md) |
| 5 | Randomness & Reproducibility | [theory/05_randomness_and_seeds.md](theory/05_randomness_and_seeds.md) |
| 6 | Mapping Parameters Across Paradigms | [theory/06_mapping_parameters.md](theory/06_mapping_parameters.md) |

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
