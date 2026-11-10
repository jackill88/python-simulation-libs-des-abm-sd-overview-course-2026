# Portfolio & Peer Review Checklist

Use this checklist before submitting your **Northline Support** capstone or peer review packet. It mirrors what instructors look for in Module 06–07 submissions.

## Repository hygiene

| Item | Done? |
|------|-------|
| All challenge tests pass locally (`pytest tests/ -v`) | ☐ |
| Seeds and run parameters recorded in README or brief | ☐ |
| No debug `print` in challenge entry points | ☐ |
| `shared/models.py` types used where applicable | ☐ |

```bash
pytest tests/03_discrete_event_simulation/test_call_centre_des.py -v
pytest tests/04_agent_based_modelling/test_call_centre_abm.py -v
pytest tests/05_system_dynamics/test_call_centre_sd.py -v
```

## Comparison brief (required artefact)

| Section present | Done? |
|-----------------|-------|
| Decision statement (one Northline choice) | ☐ |
| Scenario card (λ, μ, agents, horizons, seeds) | ☐ |
| Paradigm roles (lead + support) | ☐ |
| KPI table with **per-paradigm definitions** | ☐ |
| V&V paragraph (verification + validation) | ☐ |
| Limits & assumptions ledger | ☐ |
| Actionable recommendation with uncertainty | ☐ |

## Model-specific verification

### DES (Module 03)

| Check | Done? |
|-------|-------|
| Stable traffic when \(A < 1\) | ☐ |
| `mean_wait` sensible with zero queue edge case | ☐ |
| Warm-up / run length addressed in prose | ☐ |

### ABM (Module 04)

| Check | Done? |
|-------|-------|
| `arrival_prob=0` → no activity | ☐ |
| Patience rule documented (strict vs non-strict) | ☐ |
| `abandon_rate` denominator matches lab definition | ☐ |
| Reproducible with fixed `seed` | ☐ |

### SD (Module 05)

| Check | Done? |
|-------|-------|
| Stocks stay non-negative | ☐ |
| `dt` stated; optional refinement note | ☐ |
| `backlog_history` length = `steps + 1` | ☐ |
| Hiring/attrition tied to diagram narrative | ☐ |

## Normalization (Module 06)

| Check | Done? |
|-------|-------|
| Called `normalize_simulation_metrics` for each paradigm | ☐ |
| Explained proxy fields (`mean_delay` semantics) | ☐ |
| Did not claim numeric equality across proxies | ☐ |

```python
# Example audit row in your brief
# des mean_delay = mean wait (minutes)
# abm mean_delay slot = abandon_rate (course mapping)
# sd mean_delay = final_backlog (calls)
```

## Experiment design

| Check | Done? |
|-------|-------|
| Named factors and levels | ☐ |
| OFAT or small factorial described | ☐ |
| At least 3 seeds for stochastic runs OR justified single seed | ☐ |
| Primary response identified | ☐ |

## Visuals & communication

| Check | Done? |
|-------|-------|
| Axes labelled with units | ☐ |
| One figure supports the recommendation | ☐ |
| Jargon decoded for ops reader | ☐ |

## Peer review etiquette

When reviewing a classmate’s packet:

| Question | Notes |
|----------|-------|
| Can I reproduce from their scenario card? | |
| Is the lead paradigm justified? | |
| Are limits honest? | |
| Is the recommendation overstated? | |

Give **specific** feedback (“define abandon denominator”) not only scores.

## Optional stretch items (portfolio plus)

| Stretch | Points to self |
|---------|----------------|
| Hybrid SD → DES script | ☐ |
| ABM segment mix + calibration table | ☐ |
| SD attrition linked to backlog stress | ☐ |
| Sensitivity chart across seeds | ☐ |

## Submission bundle suggestion

```
northline_portfolio/
  comparison_brief.md
  scenario_cards/
    baseline.yaml
  figures/
    backlog_sd.png
  README.md          # how to run pytest
```

## Key takeaways

- Passing tests is **verification**; the brief proves **communication and validation thinking**.
- Never submit normalized KPIs without a **glossary**.
- Peer review is a simulation stakeholder rehearsal—be kind and precise.
- Use this checklist as a **gate** before git tag or LMS upload.
