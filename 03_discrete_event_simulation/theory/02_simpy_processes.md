# SimPy Processes & Resources

Minimal pattern for Northline:

```python
import random
import simpy

def run_once(seed: int = 42):
    rng = random.Random(seed)
    env = simpy.Environment()
    agents = simpy.Resource(env, capacity=2)

    def handle_call():
        with agents.request() as req:
            yield req
            yield env.timeout(rng.expovariate(1 / 3.0))  # mean service 3 min

    def arrivals():
        for _ in range(5):
            yield env.timeout(rng.expovariate(1 / 4.0))  # mean inter-arrival 4 min
            env.process(handle_call())

    env.process(arrivals())
    env.run()
```

Your project generalizes this with metrics: `calls_served`, `mean_wait`, `max_queue`.
