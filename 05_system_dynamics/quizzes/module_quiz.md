# Quiz: System Dynamics

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
