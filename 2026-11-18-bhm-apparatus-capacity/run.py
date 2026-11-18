"""Predict first loss for independently specified register readout channels."""

from datetime import datetime
from math import log
from pathlib import Path
from importlib.util import module_from_spec, spec_from_file_location
import json

import numpy as np

HERE = Path(__file__).resolve().parent
previous_path = HERE.parent / "2026-11-18-bhm-capacity-prediction" / "run.py"
spec = spec_from_file_location("capacity_prediction", previous_path)
previous = module_from_spec(spec)
spec.loader.exec_module(previous)

clamp = previous.clamp
fixture = clamp.fixture
ERRORS = {"L": 0.08, "H": 0.01}
TIMES = np.arange(previous.SAMPLES + 1) * previous.DT


def channel_capacity(error):
    return log(3) + (1 - error) * log(1 - error) + error * log(error / 2)


def first_event(distributions, entropies, cap):
    crossings = np.flatnonzero(entropies > cap)
    if not len(crossings):
        return None
    k = int(crossings[0])
    probabilities = distributions[k]
    polynomials = clamp.thinning_polynomials(probabilities)

    def overshoot(eta):
        return clamp.entropy(np.array([poly(eta) for poly in polynomials])) - cap

    high = 1.0
    slope_bounds = []
    for endpoint in range(99, 0, -1):
        low = endpoint / 100
        slope_bounds.append(previous.polynomial_interval(polynomials, low, high))
        assert slope_bounds[-1] > 0
        if overshoot(low) < 0:
            eta = clamp.bisect(overshoot, low, high)
            break
        high = low
    else:
        raise AssertionError("No certified first root bracket.")

    assert abs(overshoot(eta)) < 1e-12
    calibration_min = float(max(entropies[:k])) if k else None
    calibration_max = float(entropies[k])
    return {
        "sample": k,
        "time": float(TIMES[k]),
        "previous_time": float(TIMES[k - 1]) if k else None,
        "previous_entropy": float(entropies[k - 1]) if k else None,
        "entropy": calibration_max,
        "site_probabilities": probabilities.tolist(),
        "capacity_interval_for_same_bin_inclusive_lower": [calibration_min, calibration_max],
        "strength_q": 1 - eta,
        "min_eta_times_entropy_slope_bound": min(slope_bounds),
    }


def predict_case(interaction, barrier):
    hamiltonian = fixture.hamiltonian(interaction, barrier)
    spectrum = np.linalg.eigh(hamiltonian)
    occupations = np.asarray(fixture.BASIS)[:, clamp.SITE]
    fock = np.zeros(len(occupations), dtype=complex)
    fock[fixture.INDEX[(3, 0, 0, 0, 0, 0)]] = 1
    states = previous.exact_trajectory(spectrum, fock, previous.SAMPLES)
    distributions = [previous.probabilities(state, occupations) for state in states]
    entropies = np.array([clamp.entropy(probabilities) for probabilities in distributions])
    capacities = {name: channel_capacity(error) for name, error in ERRORS.items()}
    capacities["native_ceiling"] = log(4)
    settings = {}
    for name, cap in capacities.items():
        event = first_event(distributions, entropies, cap)
        if event is None:
            loss_weights = [1.0, 0.0, 0.0, 0.0]
        else:
            branches = clamp.loss_branches(states[event["sample"]], 1 - event["strength_q"], occupations)
            loss_weights = [float(np.vdot(vector, vector).real) for vector in branches]
            post = sum(np.bincount(np.asarray(list(fixture.occupations(3 - lost, 6)))[:, clamp.SITE],
                                   abs(vector)**2, minlength=4)
                       for lost, vector in enumerate(branches))
            np.testing.assert_allclose(clamp.entropy(post), cap, atol=1e-12, rtol=0)

        outcomes = previous.pulse_distribution(event["sample"] if event else None, loss_weights[0])
        settings[name] = {
            "capacity_nats": cap,
            "event": event,
            "loss_multiplicity": loss_weights,
            "first_click_distribution": outcomes.tolist(),
        }
    markov = previous.markov_distribution(fock, previous.markov_propagator(hamiltonian, occupations))
    for series in [markov] + [setting["first_click_distribution"] for setting in settings.values()]:
        assert min(series) >= 0
        np.testing.assert_allclose(sum(series), 1, atol=1e-12, rtol=0)

    pair = [np.asarray(settings[name]["first_click_distribution"]) for name in ERRORS]
    return {
        "interaction": interaction,
        "barrier": barrier,
        "maximum_sampled_entropy": float(max(entropies)),
        "maximum_entropy_sample_time": float(TIMES[np.argmax(entropies)]),
        "settings": settings,
        "markov_first_click_both_settings": markov.tolist(),
        "ordinary_matched_feedback": "Same vectors as the clamp, including the no-click probabilities.",
        "L_vs_H": previous.comparison(*pair),
        "markov_L_vs_H": previous.comparison(markov, markov),
        "clamp_vs_markov": {name: previous.comparison(vec, markov) for name, vec in zip(ERRORS, pair)},
    }


def main():
    cases = {
        "baseline": (0.35, 0.65),
        "interaction_low": (0.34, 0.65),
        "interaction_high": (0.36, 0.65),
        "barrier_low": (0.35, 0.64),
        "barrier_high": (0.35, 0.66),
    }
    result = {
        "prediction_time": datetime.now().astimezone().isoformat(),
        "source_sha256": {path.name: previous.sha256(path) for path in (HERE / "PROTOCOL.md", Path(__file__))},
        "confusion_matrix_by_setting": {
            label: (np.eye(3) * (1 - 1.5 * error) + error / 2).tolist() for label, error in ERRORS.items()
        },
        "right_endpoints_of_click_bins_then_no_click": [round(t, 10) for t in TIMES] + ["no click"],
        "cases": {name: predict_case(*params) for name, params in cases.items()},
    }
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
