# Stocks, Flows, and Euler Steps

```python
def step(state, params, dt):
    arrivals = params["arrival_rate"] * dt
    capacity = state["staffed_agents"] * params["service_rate_per_agent"] * dt
    served = min(state["backlog"] + arrivals, capacity)
    backlog = max(0.0, state["backlog"] + arrivals - served)
    return {**state, "backlog": backlog, "answered_today": state["answered_today"] + served}
```

Choose `dt` small enough that flows do not jump wildly per step. Compare SD curves qualitatively to DES/ABM KPIs in Module 06.
