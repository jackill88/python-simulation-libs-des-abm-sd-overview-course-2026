"""Quiz markdown keyed by module id."""

QUIZZES = {
    "02_the_call_centre": """# Quiz: The Call Centre Story

Questions about Northline Support, queueing intuition, and when simulation beats spreadsheets.

---

**1.** Northline Support measures **mean wait time** and **abandon rate**. Why are these KPIs natural for a call centre?

- A) They are the only metrics Python can compute
- B) They connect customer experience (waiting, leaving) to staffing decisions
- C) They replace the need for any simulation
- D) They are fixed constants in every DES model

**2.** Offered load in an Erlang sense is often written A = λ / (c · μ). What does **stability** require?

- A) A > 1 so agents stay busy
- B) A < 1 so arrivals do not outrun long-run capacity
- C) λ = μ regardless of c
- D) c = 1 always

**3.** You have λ = 10 calls/min, c = 4 agents, μ = 3 calls/min per agent. What is A?

- A) 0.833
- B) 1.2
- C) 40
- D) 0.075

**4.** Which change **most directly** reduces average wait in a queueing mental model?

- A) Renaming KPIs in the dashboard
- B) Adding agents or reducing mean service time while holding arrivals fixed
- C) Switching from Python to Excel
- D) Increasing random seed values

**5.** Why use an **imaginary** call centre for this course?

- A) Real data is illegal in Python
- B) A shared scenario lets DES, ABM, and SD tell the same story with different lenses
- C) Call centres cannot be simulated
- D) Quizzes require fictional companies by law

**6.** In discrete-event simulation, what is an **event**?

- A) Any line of Python code
- B) An instantaneous change such as a call arrival or service completion
- C) A matplotlib chart
- D) A quiz question

**7.** Agent-based models are especially useful when:

- A) Every entity behaves identically and averages are enough
- B) Heterogeneous behaviour (patience, skill, rules) drives outcomes
- C) You only need closed-form Erlang formulas
- D) Time does not matter

**8.** System dynamics models emphasise:

- A) Individual call transcripts
- B) Stocks, flows, feedback loops, and continuous time integration
- C) Only discrete event calendars
- D) GPU shader programming

**9.** For Northline, **abandonment** feeds back on future demand in many real centres. That hint points toward:

- A) ABM or SD where feedback and aggregates matter
- B) Ignoring customer behaviour
- C) Using only static spreadsheets
- D) Removing KPIs

**10.** Before writing code, the course recommends you:

- A) Pick a library at random
- B) Define the question, KPIs, and time grain (event vs step vs continuous)
- C) Skip theory and run pytest
- D) Deploy to production

---

## Answers

1. **B** — Wait and abandon rate tie operations to customer experience.
2. **B** — Load must stay below capacity for steady-state queues.
3. **A** — 10 / (4 × 3) ≈ 0.833.
4. **B** — More capacity or faster service lowers congestion.
5. **B** — One scenario, three paradigms.
6. **B** — Events change system state at instants in time.
7. **B** — Individual rules create emergent queue behaviour.
8. **B** — SD is stock–flow thinking with feedback.
9. **A** — Feedback loops are native to ABM/SD framing.
10. **B** — Problem framing prevents pretty but wrong models.
""",
    "03_discrete_event_simulation": """# Quiz: Discrete-Event Simulation (SimPy)

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
""",
    "04_agent_based_modelling": """# Quiz: Agent-Based Modelling (Mesa)

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
""",
    "05_system_dynamics": """# Quiz: System Dynamics

---

**1.** A **stock** in system dynamics represents:

- A) A Python package on PyPI
- B) A quantity that accumulates over time (e.g. backlog)
- C) A single DES event
- D) A Mesa agent id

**2.** A **flow** is:

- A) A rate that increases or decreases a stock per unit time
- B) A random seed
- C) A unit test assertion
- D) A Flet widget

**3.** Euler integration approximates:

- A) stock(t + Δt) ≈ stock(t) + net_flow · Δt
- B) Exact closed-form queueing for all models
- C) GPU matrix inversion only
- D) pytest collection order

**4.** In the Northline SD lab, backlog grows when:

- A) Arrivals plus existing backlog exceed what agents can serve in Δt
- B) You rename variables
- C) Random seed is zero
- D) Mesa steps run

**5.** SD models shine for:

- A) Reading each call transcript
- B) Policy feedback (hiring, attrition, morale) over months or quarters
- C) Nanosecond packet tracing
- D) Replacing all stochastic detail always

**6.** `service_rate_per_agent` multiplied by staffed agents gives:

- A) Nominal service capacity per time unit
- B) Abandon rate directly
- C) SimPy environment id
- D) Quiz score

**7.** Time step `dt` should be chosen so that:

- A) Δt is as large as possible regardless of dynamics
- B) Flows do not change too much per step (accuracy vs performance trade-off)
- C) dt must always equal 1 day
- D) dt replaces the need for stocks

**8.** Comparing SD backlog curve to DES wait times:

- A) Is meaningless
- B) Can align qualitatively when both represent congestion, but grains differ
- C) Requires identical random seeds always
- D) Proves ABM is wrong

**9.** Hiring and attrition flows change:

- A) The staffed_agents stock
- B) pytest version
- C) Git branch name
- D) Markdown quiz titles only

**10.** Over long horizons, SD encourages you to ask:

- A) What feedback loops amplify backlog or staffing crises?
- B) Only what colour to use in charts
- C) How to avoid units
- D) Whether Python exists

---

## Answers

1. **B** — Stocks accumulate.
2. **A** — Flows change stocks continuously.
3. **A** — Euler is first-order explicit integration.
4. **A** — Insufficient service capacity increases backlog.
5. **B** — Policy and feedback over longer horizons.
6. **A** — Capacity scales with staffed agents.
7. **B** — Step size affects numerical fidelity.
8. **B** — Compare trends with care about time grain.
9. **A** — Staffing stock moves with HR-like flows.
10. **A** — Feedback is the SD mindset.
""",
    "06_comparing_paradigms": """# Quiz: Comparing DES, ABM, and SD

---

**1.** All three paradigms can model Northline Support because:

- A) They must produce identical numeric outputs always
- B) They are different lenses on the same operational system
- C) Python allows only one paradigm per repo
- D) Quizzes require three answers

**2.** DES is usually the most precise for:

- A) Event-level queue timing with resource contention
- B) decade-long morale narratives only
- C) Rendering UI buttons
- D) Git merges

**3.** ABM adds the most value when:

- A) Individual behaviour rules drive system outcomes
- B) You refuse to use classes
- C) You need no randomness
- D) Closed-form Erlang is enough

**4.** SD is strongest when:

- A) Aggregates and policy feedback dominate the question
- B) You need every call's exact timestamp
- C) You simulate one caller only once
- D) Unit tests are disabled

**5.** Normalizing KPIs (`throughput`, `mean_delay`, `peak_queue`) helps you:

- A) Hide differences between paradigms
- B) Compare runs on a shared scorecard even when raw dict keys differ
- C) Avoid documenting assumptions
- D) Skip pytest

**6.** If DES and ABM disagree materially, you should first:

- A) Publish whichever looks nicer
- B) Check time grain, definitions of delay, and whether abandonment is modeled
- C) Delete both models
- D) Increase temperature

**7.** A hybrid approach in industry often:

- A) Uses DES for intraday staffing and SD for workforce planning
- B) Forbids Mesa
- C) Runs only spreadsheets
- D) Avoids defining KPIs

**8.** For stakeholder communication, SD diagrams are useful because:

- A) Stocks and flows map well to non-technical policy discussions
- B) They replace all data collection
- C) They are identical to SimPy traces
- D) They remove the need for metrics

**9.** pytest in this course ensures:

- A) Your implementation matches reproducible reference behaviour for labs
- B) Real call centres certify your model
- C) SimPy is installed on Android only
- D) Quizzes auto-submit to GitHub

**10.** The capstone `normalize_simulation_metrics` teaches:

- A) Translation layers between engineering artifacts
- B) That only one paradigm may exist
- C) How to avoid documentation
- D) Random number generation only

---

## Answers

1. **B** — Same system, different abstractions.
2. **A** — Event-level timing is DES strength.
3. **A** — Micro rules are ABM strength.
4. **A** — Aggregates/feedback for SD.
5. **B** — Shared KPIs enable comparison.
6. **B** — Alignment of definitions comes first.
7. **A** — Hybrid time horizons are common.
8. **A** — SD visuals communicate policy structure.
9. **A** — Tests verify lab implementations.
10. **A** — Adapter pattern for multi-paradigm studies.
""",
}
