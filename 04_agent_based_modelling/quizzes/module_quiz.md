# Quiz: Agent-Based Modelling (Mesa)

---

**1.** In Mesa, an `Agent` typically represents:

- A) A Python virtual environment
- B) An individual entity with state and rules
- C) A pytest fixture only
- D) A SimPy Environment

**2.** A `Model` in Mesa orchestrates:

- A) Only SQL migrations
- B) Agents, scheduling, and global model state
- C) Git branches
- D) Euler integration exclusively

**3.** `RandomActivation.step()` in Mesa 2.x:

- A) Activates agents in random order each tick
- B) Deletes all agents
- C) Runs continuous SD equations
- D) Builds APK files

**4.** Northline ABM callers with **patience** illustrate:

- A) Why heterogeneous rules can change abandon rates without changing mean service time
- B) That all callers must behave identically
- C) That DES is impossible
- D) That queues never form

**5.** Discrete **time steps** in ABM differ from DES because:

- A) ABM never uses randomness
- B) All updates happen on a fixed tick; events are not necessarily instantaneous
- C) ABM cannot count served calls
- D) Time runs backward

**6.** Emergence in ABM means:

- A) Macro patterns arise from micro rules without being hard-coded globally
- B) The model must import SimPy
- C) Every agent reads a global SQL table each nanosecond
- D) pytest creates agents automatically

**7.** Mesa is a strong fit when you want to:

- A) Model individual caller patience, agent skill tiers, or shift rules explicitly
- B) Avoid any object-oriented code
- C) Replace all stocks and flows
- D) Compute Erlang C by hand only

**8.** In the course ABM lab, `abandon_rate` is:

- A) abandoned / (served + abandoned) when at least one caller finished or left
- B) Always 1.0
- C) The SimPy resource capacity
- D) Hiring rate minus attrition

**9.** ABM validation often includes:

- A) Checking extreme cases (no arrivals, infinite patience) and distribution of outcomes
- B) Ignoring seed sensitivity
- C) Only visual inspection
- D) Deleting unit tests

**10.** Compared to DES for Northline, ABM trades:

- A) Some temporal precision for richer individual behaviour rules
- B) All randomness for determinism
- C) Python for spreadsheets
- D) Queues for stocks only

---

## Answers

1. **B** — Agents are micro-level entities.
2. **B** — Models host agents and stepping logic.
3. **A** — Random activation shuffles agent order per tick.
4. **A** — Patience rules drive abandonment dynamics.
5. **B** — Fixed ticks vs continuous/event time.
6. **A** — Macro from micro.
7. **A** — Individual rules are the ABM strength.
8. **A** — Definition used in the lab metrics.
9. **A** — Edge cases and distributions build trust.
10. **A** — Behaviour richness vs event-level timing.
