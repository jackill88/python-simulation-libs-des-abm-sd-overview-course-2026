# Mesa Agents and Steps

Course pattern (Mesa 2.x API):

```python
from mesa import Agent, Model
from mesa.time import RandomActivation

class Caller(Agent):
    def __init__(self, unique_id, model, patience):
        super().__init__(unique_id, model)
        self.patience = patience
        self.waited = 0

class CallCentreModel(Model):
    def __init__(self, n_agents, seed):
        super().__init__()
        self.schedule = RandomActivation(self)
        self.random = __import__("random").Random(seed)
        # add agents, waiting list, counters ...

    def step(self):
        # arrivals, service attempts, abandon checks
        self.schedule.step()
```

Your challenge wraps a full model in `run_call_centre_abm(...)`.
