# Conclusion

You modeled **Northline Support** with:

- **SimPy** for event-level queues
- **Mesa** for caller/agent rules
- **System dynamics** for backlog and staffing stocks

The engineering lesson is not “pick the coolest library” — it is **match the paradigm to the decision**, document assumptions, and compare KPIs honestly.

Keep `pytest` green, keep seeds fixed while debugging, and treat simulation output as **evidence**, not prophecy.
