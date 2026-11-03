from shared.testing import load_challenge

mod = load_challenge("05_system_dynamics", "call_centre_sd.py")
sd_euler_step = mod.sd_euler_step
run_call_centre_sd = mod.run_call_centre_sd


def test_single_euler_step():
    state = {"backlog": 10.0, "staffed_agents": 5.0, "answered_today": 0.0}
    params = {
        "arrival_rate": 8.0,
        "service_rate_per_agent": 1.5,
        "hiring_rate": 0.1,
        "attrition_rate": 0.05,
    }
    nxt = sd_euler_step(state, params, dt=1.0)
    assert nxt["backlog"] == 10.5
    assert nxt["answered_today"] == 7.5
    assert abs(nxt["staffed_agents"] - 4.85) < 1e-9


def test_sd_run_history():
    result = run_call_centre_sd(
        {"backlog": 10.0, "staffed_agents": 5.0, "answered_today": 0.0},
        {
            "arrival_rate": 8.0,
            "service_rate_per_agent": 1.5,
            "hiring_rate": 0.1,
            "attrition_rate": 0.05,
        },
        steps=5,
        dt=1.0,
    )
    assert result["backlog_history"] == [
        10,
        10.5,
        11.225000000000001,
        12.163750000000002,
        13.305562500000002,
        14.640284375000004,
    ]
    assert abs(result["final_backlog"] - 14.640284375000004) < 1e-9
