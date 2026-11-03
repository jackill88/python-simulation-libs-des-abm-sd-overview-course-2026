# Queueing Basics

Before SimPy or Mesa, check **capacity sanity**.

## Traffic intensity

For c identical agents with exponential service at rate μ and Poisson arrivals at rate λ:

```python
A = lambda_rate / (c * mu_rate)  # offered load per server pool
```

When **A < 1**, the system can keep up on average (stable queue). When **A ≥ 1**, backlog grows without bound in the long run unless you add capacity or shed load.

## Snapshot helper

Your lab returns a `CallCentreSnapshot` — a typed view of staffing and a simple backlog proxy when load exceeds capacity:

```python
from shared.models import CallCentreSnapshot

snap = CallCentreSnapshot(backlog=0.0, staffed_agents=4, answered_today=0.0)
```

Use snapshots to guard impossible parameters before launching heavy simulations.
