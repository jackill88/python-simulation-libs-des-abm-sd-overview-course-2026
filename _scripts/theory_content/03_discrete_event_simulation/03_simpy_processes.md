# SimPy Processes & Resources

[SimPy](https://simpy.readthedocs.io/) implements DES with **Python generators**: a process `yield`s requests and timeouts; the `Environment` resumes it when conditions are met. This lesson is the **standard Northline pattern**—exponential arrivals, `Resource` with capacity c, service timeout, and isolated `random.Random` seeds.

## Environment and clock

```python
import simpy

env = simpy.Environment()
# env.now starts at 0; advances only when env.run() executes events
```

| Method | Purpose |
|--------|---------|
| `env.process(gen())` | Register a process |
| `env.run(until=T)` | Run until time T |
| `env.now` | Current simulation time |

## Processes: `yield` is mandatory

A SimPy process is a generator function. **`yield env.timeout(d)`** schedules the next resumption at `env.now + d`.

```python
def service_call(env, agents, rng, mu: float):
    with agents.request() as req:
        yield req  # wait for one of c agents
        yield env.timeout(rng.expovariate(mu))  # busy time
```

Without `yield`, the function is not a SimPy process.

## Resource: Northline agent pool

```python
agents = simpy.Resource(env, capacity=4)  # c = 4
```

| Pattern | Meaning |
|---------|---------|
| `with agents.request() as req: yield req` | Join FIFO queue; block until granted |
| Context exit | Release agent automatically |

**PriorityResource** (mention only): VIP calls jump queue via priority integer—use if outage module adds tiers.

```python
# Optional pattern — not baseline Northline
# agents = simpy.PriorityResource(env, capacity=4)
# with agents.request(priority=0) as req:
#     yield req
```

Lower priority number = higher precedence in SimPy.

## Arrival process as infinite loop

```python
import random
import simpy

LAMBDA = 10.0
MU = 3.0
C = 4


def arrival_generator(env, agents, rng, handle_call):
    while True:
        yield env.timeout(rng.expovariate(LAMBDA))
        env.process(handle_call(env, agents, rng))


def handle_call(env, agents, rng, metrics):
    arrive = env.now
    with agents.request() as req:
        yield req
        wait = env.now - arrive
        metrics.record_wait(wait)
        yield env.timeout(rng.expovariate(MU))
    metrics.served += 1
```

`handle_call` is spawned **per call**; the generator keeps producing arrivals.

## Wiring a replication

```python
class Metrics:
    def __init__(self):
        self.wait_min: list[float] = []
        self.served = 0

    def record_wait(self, w: float) -> None:
        self.wait_min.append(w)


def run_once(seed: int = 42, horizon_min: float = 60.0):
    rng = random.Random(seed)
    env = simpy.Environment()
    agents = simpy.Resource(env, capacity=C)
    metrics = Metrics()

    def hc(env, agents, rng):
        return handle_call(env, agents, rng, metrics)

    def ag(env, agents, rng):
        return arrival_generator(env, agents, rng, hc)

    env.process(ag(env, agents, rng))
    env.run(until=horizon_min)
    return metrics
```

## Timeout vs `request`

| Construct | Models |
|-----------|--------|
| `env.timeout(x)` | Service duration, patience timer |
| `agents.request()` | Competition for capacity |

Patience (extended lab): wrap `request` in a race with `timeout(patience)` using `simpy.events.AnyOf` or separate process—see challenge hints.

## Observability hooks

| Hook | KPI |
|------|-----|
| `len(agents.queue)` after events | Max queue |
| `agents.count` / `capacity` | Utilisation proxy |
| `env.now - arrival` at `yield req` return | Wait |

Log `max_queue` only at **change points** if performance matters on long runs.

## Testing SimPy fragments

```python
def test_resource_capacity():
    env = simpy.Environment()
    res = simpy.Resource(env, capacity=2)
    assert res.capacity == 2
```

Integration tests cap horizon or arrival count for speed.

## Design checklist

- [ ] One `Random` per replication
- [ ] Units: minutes for Northline
- [ ] `env.run(until=...)` matches charter horizon
- [ ] Metrics object passed in, not global

## Key takeaway

SimPy **processes** are call stories; **Resources** are the agent pool; **timeouts** are service and arrival delays. Northline’s DES challenge is this pattern plus disciplined metrics—everything else is parameter and validation work.
