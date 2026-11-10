"""Theory lesson titles keyed by module (filename → display title)."""

from __future__ import annotations

THEORY_LESSONS: dict[str, list[tuple[str, str]]] = {
    "01_get_started": [
        ("01_course_overview.md", "Course Overview"),
        ("02_simulation_workflow.md", "The Simulation Workflow"),
        ("03_python_stack_and_conventions.md", "Python Stack & Conventions"),
    ],
    "02_the_call_centre": [
        ("01_meet_northline.md", "Meet Northline Support"),
        ("02_queueing_basics.md", "Queueing Basics"),
        ("03_choosing_a_lens.md", "Choosing a Simulation Lens"),
        ("04_kpis_and_service_levels.md", "KPIs & Service Levels"),
        ("05_randomness_and_seeds.md", "Randomness & Reproducibility"),
        ("06_mapping_parameters.md", "Mapping Parameters Across Paradigms"),
    ],
    "03_discrete_event_simulation": [
        ("01_why_des.md", "Why DES for Call Centres"),
        ("02_des_concepts.md", "DES Concepts & Event Calendar"),
        ("03_simpy_processes.md", "SimPy Processes & Resources"),
        ("04_mm_queues_at_northline.md", "M/M/1 and M/M/c at Northline"),
        ("05_statistics_warmup_run_length.md", "Statistics, Warm-up & Run Length"),
        ("06_des_validation_checklist.md", "DES Validation Checklist"),
    ],
    "04_agent_based_modelling": [
        ("01_why_abm.md", "Why ABM for Call Centres"),
        ("02_micro_rules_macro_kpis.md", "Micro Rules, Macro KPIs"),
        ("03_mesa_structure.md", "Mesa Model Structure (2.x)"),
        ("04_schedulers_and_time_steps.md", "Schedulers & Discrete Time"),
        ("05_patience_abandonment_calibration.md", "Patience, Abandonment & Calibration"),
        ("06_abm_observability.md", "Observability & Debugging ABMs"),
    ],
    "05_system_dynamics": [
        ("01_why_sd.md", "Why SD for Workforce Loops"),
        ("02_stocks_flows_notation.md", "Stocks, Flows & Notation"),
        ("03_stock_flow_diagram_northline.md", "Northline Stock–Flow Diagram"),
        ("04_euler_and_time_step.md", "Euler Integration & Time Step"),
        ("05_feedback_loops_hr.md", "Feedback Loops (Hiring & Attrition)"),
        ("06_sd_limits_and_pairing.md", "SD Limits & Pairing with DES/ABM"),
    ],
    "06_comparing_paradigms": [
        ("01_three_lenses_same_call_centre.md", "Three Lenses, Same Call Centre"),
        ("02_comparison_brief.md", "Building a Comparison Brief"),
        ("03_verification_vs_validation.md", "Verification vs Validation"),
        ("04_experiment_design.md", "Experiment Design & Factor Swaps"),
        ("05_hybrid_and_multimethod.md", "Hybrid & Multi-Method Models"),
    ],
    "07_wrapping_up": [
        ("01_conclusion.md", "Conclusion"),
        ("02_portfolio_checklist.md", "Portfolio & Peer Review Checklist"),
        ("03_further_reading.md", "Further Reading & Next Models"),
    ],
}
