# Quiz: The Call Centre Story

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
