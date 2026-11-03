from shared.testing import load_challenge

mod = load_challenge("06_comparing_paradigms", "compare_paradigms.py")
normalize_simulation_metrics = mod.normalize_simulation_metrics


def test_normalize_des():
    out = normalize_simulation_metrics(
        "des",
        {"calls_served": 20, "mean_wait": 1.2, "max_queue": 3},
    )
    assert out == {"throughput": 20.0, "mean_delay": 1.2, "peak_queue": 3.0}


def test_normalize_abm():
    out = normalize_simulation_metrics(
        "abm",
        {"served": 31, "abandon_rate": 0.1, "waiting": 2},
    )
    assert out == {"throughput": 31.0, "mean_delay": 0.1, "peak_queue": 2.0}


def test_normalize_sd():
    out = normalize_simulation_metrics(
        "sd",
        {"answered_today": 100.0, "final_backlog": 5.0, "backlog_history": [1, 5, 3]},
    )
    assert out == {"throughput": 100.0, "mean_delay": 5.0, "peak_queue": 5.0}
