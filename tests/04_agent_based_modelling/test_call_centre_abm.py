from shared.testing import load_challenge

mod = load_challenge("04_agent_based_modelling", "call_centre_abm.py")
run_call_centre_abm = mod.run_call_centre_abm


def test_abm_reproducible_run():
    result = run_call_centre_abm(
        n_agents=3,
        steps=50,
        arrival_prob=0.6,
        service_prob=0.7,
        default_patience=3,
        seed=7,
    )
    assert result["served"] == 31
    assert result["abandoned"] == 0
    assert result["abandon_rate"] == 0.0
    assert result["waiting"] == 0
