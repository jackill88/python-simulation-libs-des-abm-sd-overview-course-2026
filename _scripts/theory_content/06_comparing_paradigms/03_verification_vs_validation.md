# Verification vs Validation

Simulation quality rests on two questions modellers often conflate:

- **Verification** — Did we build the model **right** (logic, units, code)?
- **Validation** — Did we build the **right model** for the Northline decision?

Module 06 expects proportional V&V across DES, ABM, and SD—not paperwork for its own sake.

## Verification toolkit

| Technique | DES example | ABM example | SD example |
|-----------|-------------|-------------|------------|
| Unit tests | Zero arrivals → no waits | `arrival_prob=0` → no served | `arrival_rate=0` → flat backlog |
| Analytical limits | M/M/c stable \(A < 1\) | Infinite patience → abandons → 0 | Capacity ≥ λ → backlog bounded |
| Conservation | Calls served ≤ arrivals | `served+abandoned ≤ arrivals` | `answered` increments = sum served |
| Regression | Fixed seed metrics | Same seed, same KPI | Deterministic Euler path |

```python
# SD verification snippet
state = {"backlog": 0.0, "staffed_agents": 4.0, "answered_today": 0.0}
params = {"arrival_rate": 0.0, "service_rate_per_agent": 0.1, "hiring_rate": 0.0, "attrition_rate": 0.0}
state2 = sd_euler_step(state, params, dt=1.0)
assert state2["backlog"] == 0.0
```

Verification is **necessary**; it does not prove operational usefulness.

## Validation toolkit

| Evidence type | Northline use |
|---------------|---------------|
| Face validity | SME agrees patience rules resemble billing callers |
| Historical fit | SD backlog trend qualitatively matches last quarter |
| Cross-paradigm | DES wait band aligns with ABM when heterogeneity off |
| Extreme cases | Model not absurd when λ → 0 or staff → 0 |

Validation is **contextual**—a model validated for hiring planning may fail for sub-minute SLAs.

## V&V proportionality matrix

| Model complexity | Minimum verification | Minimum validation |
|------------------|---------------------|------------------|
| Course DES lab | pytest + stability check | Compare mean wait order to intuition |
| Course ABM | Edge cases + seed repeat | Patience sweep vs narrated abandon |
| Course SD | Non-neg stocks + mass balance | Traffic intensity + plot shape |

## DES-specific checks

- **Warm-up** — exclude initial transient before KPI means.
- **Run length** — enough calls for stable mean wait estimates.
- **Replication** — multiple seeds, report confidence spread.

## ABM-specific checks

- **Emergent sanity** — queue length responds to `arrival_prob`.
- **Micro macro link** — lowering patience raises abandons with fixed capacity.
- **Schedule integrity** — unique ids, no duplicate queue entries.

## SD-specific checks

- **dt refinement** — halve `dt`, compare backlog peak.
- **Units audit** — every rate × `dt` matches stock units.
- **Policy coherence** — hiring/attrition stories match diagram.

## Common failure modes

| Symptom | Likely verification gap | Likely validation gap |
|---------|-------------------------|------------------------|
| Perfect abandon 0 always | Wrong patience inequality | Real callers do abandon |
| DES mean wait < 0 | Code bug | — |
| SD explodes | Missing `max(0,·)` | Unrealistic λ for staff |
| KPIs “match” DES/SD numerically | Overfitted parameters | Different questions answered |

## Documentation snippet for briefs

```markdown
## V&V summary
- Verification: pytest modules 03–05 green; SD dt halving changes peak backlog < 5%.
- Validation: ABM abandon band 10–16% vs ops report 12% (face valid); DES not fit to historical waits (scope: exploration only).
```

## Verification ≠ calibration

Calibration tunes parameters to data (Module 04 patience lesson). Verification ensures the **equations** implement your intent **given** those parameters.

## Key takeaways

- **Verify** logic with tests, invariants, and analytical limits.
- **Validate** usefulness with SMEs, history, and cross-paradigm coherence.
- Match V&V depth to the **decision stakes** and model role in the brief.
- Report both in the comparison brief so peers can trust or challenge findings.
