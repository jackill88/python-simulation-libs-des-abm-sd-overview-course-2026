# Quiz: Discrete-Event Simulation (SimPy)

---

**1.** In SimPy, `simpy.Environment` is responsible for:

- A) Training neural networks
- B) Advancing simulation time and scheduling events
- C) Compiling Python to C
- D) Rendering Mesa agents

**2.** A `simpy.Resource(capacity=c)` models:

- A) c identical servers (agents) with a wait queue
- B) c independent Poisson processes only
- C) A system dynamics stock
- D) A matplotlib axis

**3.** `yield env.timeout(x)` in a SimPy process means:

- A) Stop the program for x wall-clock seconds always
- B) Suspend the process for x **simulated** time units
- C) Delete the environment
- D) Reset random seeds

**4.** M/M/c queue notation implies:

- A) Markovian arrivals, Markovian service, c servers
- B) Monthly/monthly/calendar queues
- C) Manual/manual/coffee breaks
- D) Mesa/Mesa/c agents

**5.** Why set a **random seed** in DES labs?

- A) To hide bugs
- B) To make stochastic runs reproducible for debugging and pytest
- C) Because SimPy forbids randomness otherwise
- D) To speed up GPU rendering

**6.** Which metric is natural from a DES event log?

- A) Individual agent morale stock
- B) Per-call waiting times and queue length samples
- C) Only annual hiring budgets
- D) Syntax tree depth

**7.** Inter-arrival times with `random.expovariate(1/mean)` implement:

- A) Uniform arrivals every mean seconds exactly
- B) Exponential inter-arrivals (Poisson process)
- C) Fixed deterministic arrivals
- D) SD Euler steps

**8.** DES is often the best first choice when:

- A) You need aggregate feedback over years with no detail
- B) You care about precise timing of congestion, queues, and resource contention
- C) Every agent must have a GUI tile
- D) Closed-form formulas always exist

**9.** In the Northline DES lab, `max_queue` tracks:

- A) The deepest wait line observed while calls waited for agents
- B) Total payroll
- C) Number of Python files
- D) Mesa grid size

**10.** After implementing DES, comparing results to M/M/c intuition helps you:

- A) Avoid testing
- B) Sanity-check whether stochastic output is in a plausible range
- C) Eliminate all randomness
- D) Replace SimPy with Excel

---

## Answers

1. **B** — The environment owns simulated time.
2. **A** — Resource capacity models parallel servers.
3. **B** — Timeout advances simulated time only.
4. **A** — Standard queueing shorthand.
5. **B** — Reproducibility for tests and debugging.
6. **B** — DES excels at wait and queue trajectories.
7. **B** — Exponential inter-arrivals are standard.
8. **B** — Event timing is the DES sweet spot.
9. **A** — Queue depth while waiting for service.
10. **B** — Cross-check stochastic models.
