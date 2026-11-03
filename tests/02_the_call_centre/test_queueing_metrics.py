from shared.testing import load_challenge

mod = load_challenge("02_the_call_centre", "queueing_metrics.py")
traffic_intensity = mod.traffic_intensity
is_system_stable = mod.is_system_stable
validate_call_centre_params = mod.validate_call_centre_params


def test_traffic_intensity():
    assert traffic_intensity(10, 4, 3) == 0.8333333333333334


def test_stability():
    assert is_system_stable(10, 4, 3) is True
    assert is_system_stable(20, 4, 3) is False


def test_validate_snapshot():
    snap = validate_call_centre_params(10, 4, 3)
    assert snap.staffed_agents == 4
    assert snap.backlog == 0.0
    assert snap.answered_today == 0.0
