"""One-shot entropy-cap toy and ordinary-channel controls on the existing BHM fixture."""

import argparse
import hashlib
import json
from math import comb, log
from pathlib import Path
import sys

import numpy as np
from numpy.polynomial import Polynomial

FIXTURE_DIR = Path(__file__).resolve().parent.parent / "2026-11-18-ithkor-evidence-search"
sys.path.insert(0, str(FIXTURE_DIR))
import physics_phase_pair as fixture


SITE = 1  # Zero-based.
U = 0.35
BARRIER = 0.65
CAP = 1.195
CADENCE = 0.05
TIMES = (0.75, 1.0, 1.5, 2.5)
N = fixture.PARTICLES


def entropy(probabilities):
    positive = probabilities[probabilities > 0]
    return float(-positive @ np.log(positive))


def unitary(spectrum, time):
    values, vectors = spectrum
    return (vectors * np.exp(-1j * values * time)) @ vectors.T


def density(state):
    return np.outer(state, state.conj())


def bisect(function, low, high):
    assert function(low) < 0 < function(high)
    for _ in range(45):
        middle = (low + high) / 2
        if function(middle) > 0:
            high = middle
        else:
            low = middle
    return (low + high) / 2


def thinning_polynomials(probabilities):
    eta = Polynomial([0, 1])
    return [
        sum(probabilities[n] * comb(n, kept) * eta**kept * (1 - eta)**(n - kept)
            for n in range(kept, N + 1))
        for kept in range(N + 1)
    ]


def entropy_derivative_lower_bound(polynomials, low):
    # Over [low,1], enclose each probability via endpoints and stationary points.
    bounds = []
    for polynomial in polynomials:
        points = [low, 1.0]
        points.extend(root.real for root in polynomial.deriv().roots()
                      if abs(root.imag) < 1e-12 and low < root.real < 1)
        values = polynomial(np.array(points))
        bounds.append((min(values) - 1e-12, max(values) + 1e-12))
    lower_bound = 0.0
    for j, ((p_min, _), (next_min, next_max)) in enumerate(zip(bounds, bounds[1:]), 1):
        ratio_log = log(p_min / next_max)
        lower_bound += j * min(next_min * ratio_log, next_max * ratio_log)
    # This positive lower bound also bounds H' because it bounds eta * H'.
    return lower_bound


def current_operator():
    forward = fixture.hopping(1, 0)
    return 1j * (forward - forward.T)


def check_state(rho):
    assert abs(np.trace(rho) - 1) < 1e-10
    np.testing.assert_allclose(rho, rho.conj().T, atol=1e-10, rtol=0)
    assert np.linalg.eigvalsh(rho)[0] > -1e-10


def trace_distance(first, second):
    return float(np.abs(np.linalg.eigvalsh(first - second)).sum() / 2)


def current(rho, operator):
    return float(np.einsum("ij,ji->", rho, operator).real)


def loss_branches(state, eta, occupations):
    # Select the isometry column associated with a vacuum environment, then
    # resolve it in the environment number basis and trace out that basis.
    branches = []
    for lost in range(N + 1):
        target_basis = list(fixture.occupations(N - lost, fixture.SITES))
        target_index = {config: i for i, config in enumerate(target_basis)}
        vector = np.zeros(len(target_basis), dtype=complex)
        for config, n, amplitude in zip(fixture.BASIS, occupations, state):
            if n >= lost:
                target = list(config)
                target[SITE] -= lost
                vector[target_index[tuple(target)]] = (
                    amplitude * np.sqrt(comb(int(n), lost) * eta**(n - lost) * (1 - eta)**lost)
                )
        branches.append(vector)
    return branches


def sector_operators():
    # Reuse the original Hamiltonian and ladder matrices for each surviving
    # sector with its own Fock basis. Restore the fixture even on failure.
    original_basis, original_index = fixture.BASIS, fixture.INDEX
    sectors = []
    try:
        for surviving in range(N, -1, -1):
            fixture.BASIS = list(fixture.occupations(surviving, fixture.SITES))
            fixture.INDEX = {config: i for i, config in enumerate(fixture.BASIS)}
            sectors.append((np.linalg.eigh(fixture.hamiltonian(U, BARRIER)),
                            current_operator(), np.asarray(fixture.BASIS)[:, SITE]))
    finally:
        fixture.BASIS, fixture.INDEX = original_basis, original_index
    return sectors


def markov_control(initial, spectrum, decay, operator, steps_per_unit):
    rho = initial
    step = 1 / steps_per_unit
    half_step = unitary(spectrum, step / 2)
    reverse = half_step.conj().T
    damping = np.exp(-decay * step)
    checkpoints = {round(time / step) for time in TIMES}
    readouts = []
    for i in range(1, max(checkpoints) + 1):
        rho = half_step @ ((half_step @ rho @ reverse) * damping) @ reverse
        if i in checkpoints:
            check_state(rho)
            readouts.append(current(rho, operator))
    return readouts

def run():
    sectors = sector_operators()
    spectrum, operator, occupations = sectors[0]
    hamiltonian = fixture.hamiltonian(U, BARRIER)
    initial = fixture.condensate()
    def reference_state(time):
        return unitary(spectrum, time) @ initial

    def probabilities(state):
        return np.bincount(occupations, abs(state)**2, minlength=N + 1)

    def excess(time):
        return entropy(probabilities(reference_state(time))) - CAP

    samples = []
    for index in range(round(TIMES[-1] / CADENCE) + 1):
        time = round(index * CADENCE, 12)
        samples.append({"t": time, "S_R": excess(time) + CAP})
        if excess(time) > 0:
            break
    else:
        return {"verdict": "no_sampled_trigger", "cap": CAP, "sampling": samples}

    trigger = samples[-1]["t"]
    time_bracket = (samples[-2]["t"], trigger)
    crossing = bisect(excess, *time_bracket)
    # Differentiate the pre-pulse Fock probabilities analytically. This grid
    # checks for a rising crossing numerically, not a proof on all real times.
    rising_slopes = []
    for time in np.linspace(0, trigger, 301):
        state = reference_state(time)
        dp = np.bincount(occupations, 2 * (state.conj() * (-1j * hamiltonian @ state)).real,
                         minlength=N + 1)
        rising_slopes.append(float(-dp @ np.log(probabilities(state))))
    assert min(rising_slopes) > 0

    event = reference_state(trigger)
    before = density(event)
    polynomial = thinning_polynomials(probabilities(event))
    def thinned(eta):
        return np.array([p(eta) for p in polynomial])

    eta_bracket = (0.95, 1.0)
    derivative_bound = entropy_derivative_lower_bound(polynomial, eta_bracket[0])
    assert derivative_bound > 0
    eta = bisect(lambda value: entropy(thinned(value)) - CAP, *eta_bracket)
    branches = loss_branches(event, eta, occupations)
    phase_branches = [vector * np.exp(1j * np.pi * counts)
                      for vector, (_, _, counts) in zip(branches, sectors)]
    weights = np.array([np.vdot(vector, vector).real for vector in branches])
    marginal = sum(np.bincount(counts, abs(vector)**2, minlength=N + 1)
                   for vector, (_, _, counts) in zip(branches, sectors))
    phase_marginal = sum(np.bincount(counts, abs(vector)**2, minlength=N + 1)
                         for vector, (_, _, counts) in zip(phase_branches, sectors))
    np.testing.assert_allclose([marginal, phase_marginal], [thinned(eta), thinned(eta)],
                               atol=1e-12, rtol=0)
    np.testing.assert_allclose(weights.sum(), 1, atol=1e-12, rtol=0)
    expected_lost = weights @ np.arange(N + 1)
    np.testing.assert_allclose(expected_lost, (1 - eta) * (probabilities(event) @ np.arange(N + 1)),
                               atol=1e-12, rtol=0)

    pulse_strength = -log(eta)
    coherence_gap_squared = (occupations[:, None] - occupations[None, :])**2
    pulse = before * np.exp(-pulse_strength * coherence_gap_squared / 2)
    dephase_marginal = np.bincount(occupations, pulse.diagonal().real, minlength=N + 1)
    np.testing.assert_allclose(dephase_marginal, probabilities(event), atol=1e-12, rtol=0)
    check_state(pulse)

    def measure_branches(vectors, time_since_pulse):
        return sum(current(density(unitary(spectrum, time_since_pulse) @ vector), bond)
                   for vector, (spectrum, bond, _) in zip(vectors, sectors))

    def distance_branches(vectors):
        return trace_distance(density(vectors[0]), before) + (1 - weights[0]) / 2

    def readouts(time, baseline, markov=None):
        delay = time - trigger
        step = unitary(spectrum, delay)
        row = {"t": time, "baseline": baseline}
        channels = {
            "loss_clamp": measure_branches(branches, delay),
            "loss_plus_phase_clamp": measure_branches(phase_branches, delay),
            "coherence_matched_number_dephasing_pulse": current(step @ pulse @ step.conj().T, operator),
            "ordinary_loss_replay": measure_branches(loss_branches(event, eta, occupations), delay),
        }
        if markov is not None:
            channels["coherence_matched_constant_number_dephasing"] = markov
        for channel, value in channels.items():
            row[channel] = {"J": value, "delta_J": value - baseline}
        assert row["loss_clamp"] == row["ordinary_loss_replay"]
        return row

    decay_rate = pulse_strength / TIMES[-1]
    decay = decay_rate * coherence_gap_squared / 2
    coarse = markov_control(density(initial), spectrum, decay, operator, 200)
    fine = markov_control(density(initial), spectrum, decay, operator, 400)
    convergence = float(np.max(np.abs(np.subtract(coarse, fine))))
    assert convergence < 1e-7
    assert abs(entropy(marginal) - CAP) < 1e-12

    return {
        "verdict": "illustrative_one_shot_clamp_with_ordinary_channel_replay",
        "versions": {"python": sys.version.split()[0], "numpy": np.__version__},
        "sha256": {path.name: hashlib.sha256(path.read_bytes()).hexdigest()
                   for path in (Path(__file__), Path(fixture.__file__))},
        "fixture": {"U": U, "barrier_J": BARRIER, "initial": "phase-plus condensate",
                    "region_site_zero_based": SITE, "basis_dimensions_N3_to_N0": [len(v) for v in branches]},
        "controller": {
            "cap_nats": CAP, "kinematic_ceiling_nats": log(N + 1), "cadence": CADENCE,
            "latency": 0.0, "sampling": samples, "tau_sampled": trigger,
            "continuous_equality_bracket": time_bracket, "continuous_equality_time": crossing,
            "minimum_S_slope_on_301_point_grid_through_event": min(rising_slopes),
            "positive_sampled_overshoot_nats": excess(trigger),
        },
        "pulse": {
            "eta_root_bracket": eta_bracket, "eta_times_entropy_derivative_lower_bound": derivative_bound,
            "eta": eta, "q_loss": 1 - eta, "phase_radians_in_second_clamp": np.pi,
            "number_dephasing_pulse_strength": pulse_strength,
            "number_dephasing_gamma": decay_rate, "gamma_match_time": TIMES[-1],
            "strang_max_J_delta_steps_0p005_vs_0p0025": convergence,
            "S_before": entropy(probabilities(event)), "S_after_loss": entropy(marginal),
            "S_after_loss_plus_phase": entropy(phase_marginal),
            "S_after_dephasing": entropy(dephase_marginal), "p_before": probabilities(event).tolist(),
            "p_after_loss": marginal.tolist(), "environment_loss_distribution": weights.tolist(),
            "expected_particles_lost": expected_lost,
            "global_trace_distance_loss": distance_branches(branches),
            "global_trace_distance_loss_plus_phase": distance_branches(phase_branches),
            "global_trace_distance_dephasing": trace_distance(before, pulse),
        },
        "immediately_after_pulse": readouts(trigger, current(before, operator)),
        "observations": [readouts(time, current(density(reference_state(time)), operator), markov)
                         for time, markov in zip(TIMES, fine)],
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    payload = json.dumps(run(), indent=2, allow_nan=False) + "\n"
    if args.output:
        args.output.write_text(payload, encoding="utf-8")
    else:
        print(payload, end="")


if __name__ == "__main__":
    main()

