"""Freeze onset predictions, then validate categorical first-click distributions."""

import argparse
import hashlib
import json
from math import ceil, log
from pathlib import Path
import sys

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "2026-11-18-bhm-entropy-clamp"))
import run as clamp

fixture = clamp.fixture
CAP = log(3)
DT = 0.05
SAMPLES = 50
AGE_STEPS = 4
GAMMA = 0.10
FIXED_SAMPLE = 15
FIXED_Q = 0.10
PREPS = ("A_fock", "B_preaged_fock", "phase_plus", "phase_minus")


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def state_setup():
    hamiltonian = fixture.hamiltonian(clamp.U, clamp.BARRIER)
    spectrum = np.linalg.eigh(hamiltonian)
    occupation = np.asarray(fixture.BASIS)[:, clamp.SITE]
    fock = np.zeros(len(occupation), dtype=complex)
    fock[fixture.INDEX[(3, 0, 0, 0, 0, 0)]] = 1
    states = {
        "A_fock": fock,
        "B_preaged_fock": clamp.unitary(spectrum, AGE_STEPS * DT) @ fock,
        "phase_plus": fixture.condensate(),
        "phase_minus": fixture.condensate().conj(),
    }
    return hamiltonian, spectrum, occupation, states


def probabilities(state, occupation):
    return np.bincount(occupation, abs(state)**2, minlength=fixture.PARTICLES + 1)


def polynomial_interval(polynomials, low, high):
    bounds = []
    for polynomial in polynomials:
        points = [low, high]
        points.extend(root.real for root in polynomial.deriv().roots()
                      if abs(root.imag) < 1e-12 and low < root.real < high)
        values = polynomial(np.array(points))
        bounds.append((min(values) - 1e-12, max(values) + 1e-12))
    lower_bound = 0
    for j, ((p_min, _), (next_min, next_max)) in enumerate(zip(bounds, bounds[1:]), 1):
        ratio_log = log(p_min / next_max)
        lower_bound += j * min(next_min * ratio_log, next_max * ratio_log)
    return lower_bound


def strength(p):
    polynomials = clamp.thinning_polynomials(p)
    def excess(eta):
        return clamp.entropy(np.array([polynomial(eta) for polynomial in polynomials])) - CAP

    high = 1.0
    slope_bounds = []
    for grid_index in range(99, 0, -1):
        low = grid_index / 100
        slope_bounds.append(polynomial_interval(polynomials, low, high))
        assert slope_bounds[-1] > 0, "Cannot certify first monotone attenuation crossing."
        if excess(low) < 0:
            eta = clamp.bisect(excess, low, high)
            assert abs(excess(eta)) < 1e-12
            return 1 - eta, min(slope_bounds)
        high = low
    raise AssertionError("No entropy-target root bracket located.")


def first_trigger(trajectory, occupation, cap=CAP):
    previous = None
    for k, vector in enumerate(trajectory):
        p = probabilities(vector, occupation)
        entropy = clamp.entropy(p)
        if entropy > cap:
            q, bound = strength(p)
            return {"sample": k, "time": k * DT, "previous_S_R": previous,
                    "S_R": entropy, "p": p.tolist(), "q": q,
                    "min_eta_times_S_slope_lower_bound": bound}
        previous = entropy
    return None


def exact_trajectory(spectrum, state, samples):
    return [clamp.unitary(spectrum, k * DT) @ state for k in range(samples + 1)]


def predict():
    _, spectrum, occupation, states = state_setup()
    base = exact_trajectory(spectrum, states["A_fock"], SAMPLES + AGE_STEPS)
    trajectories = {
        "A_fock": base[:SAMPLES + 1],
        "B_preaged_fock": base[AGE_STEPS:],
        **{name: exact_trajectory(spectrum, states[name], SAMPLES) for name in PREPS[2:]},
    }
    events = {name: first_trigger(vectors, occupation) for name, vectors in trajectories.items()}
    a, b = (events[name] for name in PREPS[:2])
    if a is not None and a["sample"] >= AGE_STEPS:
        assert b["sample"] == a["sample"] - AGE_STEPS
        assert abs(b["q"] - a["q"]) < 1e-12
    return {
        "protocol_sha256": sha256(HERE / "PROTOCOL.md"),
        "runner_sha256": sha256(Path(__file__)),
        "inputs": {"cap_nats": CAP, "native_site_ceiling_nats": log(4), "cadence": DT,
                   "horizon": SAMPLES * DT, "preage_time": AGE_STEPS * DT, "gamma": GAMMA,
                   "fixed_pulse_time": FIXED_SAMPLE * DT, "fixed_q": FIXED_Q},
        "initial_occupation_probabilities": {
            name: probabilities(state, occupation).tolist() for name, state in states.items()},
        "predicted_events": events,
        "native_cap_triggers": {
            name: first_trigger(vectors, occupation, cap=log(4)) for name, vectors in trajectories.items()},
    }


def pulse_distribution(sample, no_loss_probability):
    outcome = np.zeros(SAMPLES + 2)
    outcome[-1] = no_loss_probability
    if sample is not None:
        outcome[sample] = 1 - no_loss_probability
    return outcome


def clamp_distribution(event, trajectory, occupation):
    if event is None:
        return pulse_distribution(None, 1.0)
    k = event["sample"]
    branches = clamp.loss_branches(trajectory[k], 1 - event["q"], occupation)
    weights = [np.vdot(vector, vector).real for vector in branches]
    post = sum(np.bincount(np.asarray(list(fixture.occupations(3 - lost, 6)))[:, clamp.SITE],
                           abs(vector)**2, minlength=4)
               for lost, vector in enumerate(branches))
    np.testing.assert_allclose(clamp.entropy(post), CAP, atol=1e-12, rtol=0)
    np.testing.assert_allclose(sum(weights), 1, atol=1e-12, rtol=0)
    return pulse_distribution(k, weights[0])


def markov_propagator(hamiltonian, occupation):
    effective = hamiltonian - 0.5j * GAMMA * np.diag(occupation)
    values, vectors = np.linalg.eig(effective)
    inverse = np.linalg.inv(vectors)
    np.testing.assert_allclose((vectors * values) @ inverse, effective,
                               atol=1e-11, rtol=0)
    return (vectors * np.exp(-1j * values * DT)) @ inverse


def markov_distribution(initial, step):
    outcome = np.zeros(SAMPLES + 2)
    survival = 1.0
    state = initial
    for k in range(1, SAMPLES + 1):
        state = step @ state
        next_survival = np.vdot(state, state).real
        outcome[k] = survival - next_survival
        survival = next_survival
    outcome[-1] = survival
    return outcome


def comparison(left, right):
    tv = float(abs(left - right).sum() / 2)
    if tv < 1e-12:
        return {"total_variation": 0, "hellinger_squared": 0,
                "sufficient_shots_for_error_at_most_0_05": None}
    bc = min(1.0, float(np.sqrt(left * right).sum()))
    return {"total_variation": tv, "hellinger_squared": 1 - bc,
            "sufficient_shots_for_error_at_most_0_05": ceil(log(.1) / log(bc)) if bc > 0 else 1}


def validate(prediction):
    assert prediction["protocol_sha256"] == sha256(HERE / "PROTOCOL.md")
    assert prediction["runner_sha256"] == sha256(Path(__file__))
    hamiltonian, spectrum, occupation, states = state_setup()
    step = clamp.unitary(spectrum, DT)
    markov_step = markov_propagator(hamiltonian, occupation)
    outcomes = {}
    events = {}
    for name, initial in states.items():
        trajectory = [initial]
        for _ in range(SAMPLES):
            trajectory.append(step @ trajectory[-1])
        event = first_trigger(trajectory, occupation)
        expected = prediction["predicted_events"][name]
        if expected is None:
            assert event is None
        else:
            assert event["sample"] == expected["sample"]
            assert abs(event["q"] - expected["q"]) < 1e-12
            np.testing.assert_allclose(event["p"], expected["p"], atol=1e-12, rtol=0)
        events[name] = event
        fixed_p = probabilities(trajectory[FIXED_SAMPLE], occupation)
        distributions = {
            "clamp": clamp_distribution(event, trajectory, occupation),
            "constant_markov": markov_distribution(initial, markov_step),
            "common_fixed_pulse": pulse_distribution(
                FIXED_SAMPLE, float(fixed_p @ (1 - FIXED_Q)**np.arange(4))),
            "same_ordinary_feedback": clamp_distribution(expected, trajectory, occupation),
        }
        for distribution in distributions.values():
            assert min(distribution) >= 0
            assert abs(sum(distribution) - 1) < 1e-12
        outcomes[name] = distributions

    return {
        "prediction_sha256": sha256(HERE / "predictions.json"),
        "versions": {"python": sys.version.split()[0], "numpy": np.__version__},
        "outcome_bins": ["t=0"] + [round(k * DT, 10) for k in range(1, SAMPLES + 1)] + ["no click"],
        "validated_events": events,
        "outcomes": {name: {key: values.tolist() for key, values in models.items()}
                     for name, models in outcomes.items()},
        "clamp_versus_controls": {
            name: {model: comparison(models["clamp"], distribution)
                   for model, distribution in models.items() if model != "clamp"}
            for name, models in outcomes.items()},
        "A_versus_B": {
            model: comparison(outcomes["A_fock"][model], outcomes["B_preaged_fock"][model])
            for model in outcomes["A_fock"]},
        "phase_plus_versus_minus_clamp": comparison(outcomes["phase_plus"]["clamp"],
                                                    outcomes["phase_minus"]["clamp"]),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", choices=("predict", "validate"))
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    if args.mode == "predict":
        result = predict()
    else:
        result = validate(json.loads((HERE / "predictions.json").read_text(encoding="utf-8")))
    payload = json.dumps(result, indent=2, allow_nan=False) + "\n"
    if args.output:
        args.output.write_text(payload, encoding="utf-8")
    else:
        print(payload, end="")


if __name__ == "__main__":
    main()
