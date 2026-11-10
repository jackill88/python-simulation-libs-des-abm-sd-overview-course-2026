# KPIs & Service Levels

Operations leaders at Northline Support do not buy “a simulation”; they buy **answers about KPIs**. Every paradigm must eventually surface the same family of metrics—**ASA**, **service level**, **abandon rate**, **occupancy**—even if the internal state representation differs.

## KPI glossary

| KPI | Definition | Typical unit |
|-----|------------|--------------|
| **ASA** | Average speed of answer — mean wait until agent picks up | Seconds |
| **SL30** (example) | % of calls answered within 30 seconds | Percent |
| **Abandon rate** | Abandoned / offered calls | Percent |
| **Occupancy** | Fraction of time agents are busy on calls | Percent |
| **AHT** | Average handle time (service duration) | Minutes |

**Offered load** \(A = \lambda/(c\mu)\) is a **input diagnostic**, not a customer-facing KPI—but planners watch it alongside occupancy.

## Service level vs ASA

| Metric | Sensitive to | Blind spots |
|--------|--------------|-------------|
| SL30 | **Distribution tail** of waits | Hides very long waits if ASA looks fine |
| ASA | **Central tendency** | Can miss “slavery to the percentile” targets |

Northline target: **80% within 30 seconds** **and** ASA ≤ **45 s**. A model can hit ASA while failing SL30 if a fraction waits minutes.

```python
def service_level_percent(wait_seconds: list[float], threshold_s: float = 30.0) -> float:
    if not wait_seconds:
        return 100.0
    within = sum(1 for w in wait_seconds if w <= threshold_s)
    return 100.0 * within / len(wait_seconds)

def asa_seconds(wait_seconds: list[float]) -> float:
    return sum(wait_seconds) / len(wait_seconds)
```

## Abandon rate

\[
\text{Abandon \%} = 100 \times \frac{\text{calls abandoned}}{\text{calls offered}}
\]

**Offered** includes those still waiting at end of simulation—define **consistently** in your report. For a finite horizon DES:

| Disposition | Count toward offered? |
|-------------|------------------------|
| Served | Yes |
| Abandoned | Yes |
| Still in queue at stop | Yes (disclose!) |

Patience models (ABM) make abandon **endogenous**; baseline M/M/c does not.

## Occupancy

Per agent, over interval \([0, T]\):

\[
\text{Occupancy} = \frac{\text{busy time}}{\text{available time}}
\]

With **c = 4** parallel agents, centre occupancy is often reported as **average across agents** or **total busy / total agent-minutes**.

```python
def centre_occupancy(busy_agent_minutes: float, c: int, horizon_min: float) -> float:
    available = c * horizon_min
    return busy_agent_minutes / available if available else 0.0
```

Target band **82–88%** balances spare capacity vs burnout. If DES shows 95% occupancy and rising abandons, staffing is structurally tight.

## How to measure in each paradigm

| KPI | DES (SimPy) | ABM (Mesa) | SD |
|-----|-------------|------------|-----|
| ASA | Timestamp deltas at answer event | Per-caller wait, aggregate | Approximate from backlog / λ |
| SL30 | Histogram waits at answer | Same, per call | Needs wait distribution proxy* |
| Abandon rate | Count abandon events | Agent state `abandoned` | Abandon flow / arrivals |
| Occupancy | Track busy flags on `Resource` | Agent busy ticks | Busy stock / capacity |

\*Pure SD without delay distributions often **cannot** recover SL30; pair with DES or use stylised delay stocks—see Module 05.

## DES event-level instrumentation pattern

```python
# Conceptual metrics collector for Northline DES
class Metrics:
    def __init__(self):
        self.wait_at_answer_s: list[float] = []
        self.offered = 0
        self.abandoned = 0
        self.busy_min = 0.0

    def record_answer(self, wait_min: float):
        self.wait_at_answer_s.append(wait_min * 60.0)

    @property
    def abandon_rate_pct(self) -> float:
        return 100.0 * self.abandoned / self.offered if self.offered else 0.0
```

## Reporting template (stakeholder table)

| Run | Seed | Rep | ASA (s) | SL30 (%) | Abandon (%) | Occupancy (%) |
|-----|------|-----|---------|----------|-------------|---------------|
| Baseline | 42 | 1 | … | … | … | … |

Include **warm-up** exclusion (Module 03) for ASA/SL rows.

## Key takeaway

Align every simulation with **named KPIs** before coding. Northline’s SL30 and abandon targets force you to capture **wait distributions**, not only averages—and the right measurement hooks differ by paradigm even when the headline metrics look identical.
