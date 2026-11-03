from shared.testing import load_challenge

mod = load_challenge("03_discrete_event_simulation", "call_centre_des.py")
run_call_centre_des = mod.run_call_centre_des


def test_des_reproducible_run():
    result = run_call_centre_des(
        n_agents=2,
        mean_inter_arrival=4.0,
        mean_service_time=3.0,
        max_calls=20,
        seed=42,
    )
    assert result["calls_served"] == 20
    assert result["max_queue"] == 3
    assert abs(result["mean_wait"] - 0.6432097993949829) < 1e-6
