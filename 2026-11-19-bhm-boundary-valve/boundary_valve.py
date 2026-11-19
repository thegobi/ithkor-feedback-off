"""Closed three-boson ring: hard boundary cut and continuous boundary taper."""

import json
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "2026-11-19-bhm-two-sites"))
from run import entropy, ring, subsystem_indices


TIMES = (0.75, 1.0, 1.5, 2.5)
REGION, LOCAL = subsystem_indices([x[:2] for x in ring.BASIS])
REST, OUTSIDE = subsystem_indices([x[2:] for x in ring.BASIS])
H_OPEN = ring.hamiltonian(0.35, 0.65)
H_CUT = ring.hamiltonian(0.35, 0)
BOUNDARY = H_OPEN - H_CUT
MOVE = ring.hopping(1, 0)
CURRENT = 1j * (MOVE - MOVE.T)
INITIAL = np.eye(len(ring.BASIS))[ring.INDEX[(3, 0, 0, 0, 0, 0)]]


def spectrum(state):
    amplitudes = np.zeros((len(LOCAL), len(OUTSIDE)), complex)
    amplitudes[REGION, REST] = state
    return np.linalg.eigvalsh(amplitudes @ amplitudes.conj().T)


def S(state):
    return entropy(spectrum(state))


def mean(state, operator):
    return float(np.vdot(state, operator @ state).real)


def trajectory(h, initial):
    energies, modes = np.linalg.eigh(h)
    weights = modes.T @ initial
    return lambda t: modes @ (weights * np.exp(-1j * energies * t))


def first_crossing(free, cap, step):
    for k in range(1, round(TIMES[-1] / step) + 1):
        if S(free(k * step)) >= cap:
            lo, hi = (k-1) * step, k * step
            break
    else:
        raise ValueError("No crossing in the observation window")
    for _ in range(45):
        mid = (lo + hi) / 2
        if S(free(mid)) < cap:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


def hard(free, cap):
    tau = first_crossing(free, cap, 0.01)
    assert abs(tau - first_crossing(free, cap, 0.005)) < 1e-11
    at_cap = free(tau)
    after = trajectory(H_CUT, at_cap)
    trace = [after(t - tau) if t > tau else free(t) for t in TIMES]
    eigenvalues = spectrum(at_cap)
    for elapsed in np.linspace(0, TIMES[-1] - tau, 101):
        state = after(elapsed)
        np.testing.assert_allclose(spectrum(state), eigenvalues, atol=2e-13, rtol=0)
        assert abs(mean(state, H_CUT) - mean(at_cap, H_CUT)) < 1e-12
    return {
        "first_crossing": tau,
        "open_entropy_slope_at_crossing": (S(free(tau+1e-5)) - S(free(tau-1e-5))) / 2e-5,
        "switch_energy_change": mean(at_cap, H_CUT) - mean(at_cap, H_OPEN),
        "entropy_at_times": [S(s) for s in trace],
        "delta_J": [mean(s, CURRENT) - mean(free(t), CURRENT) for t, s in zip(TIMES, trace)],
    }


def smooth(free, cap, step):
    def derivative(s):
        factor = max(0.0, 1 - S(s)/cap)
        return -1j * (H_CUT @ s + factor * (BOUNDARY @ s))

    state = INITIAL.astype(complex)
    readouts = {round(t/step): t for t in TIMES}
    currents, entropies = [], []
    maximum = 0.
    for k in range(1, round(TIMES[-1]/step) + 1):
        a = derivative(state)
        b = derivative(state + step*a/2)
        c = derivative(state + step*b/2)
        d = derivative(state + step*c)
        state += step/6 * (a + 2*b + 2*c + d)
        value = S(state)
        maximum = max(maximum, value)
        assert abs(np.vdot(state, state) - 1) < 1e-9
        if k in readouts:
            currents.append(mean(state, CURRENT) - mean(free(readouts[k]), CURRENT))
            entropies.append(value)
    assert maximum <= cap + 1e-10
    return {"max_sampled_entropy": maximum, "entropy_at_times": entropies, "delta_J": currents}


def main():
    assert len(ring.BASIS) == 56 and all(sum(config) == 3 for config in ring.BASIS)
    free = trajectory(H_OPEN, INITIAL)
    result = {"times": TIMES, "reference_entropy": [S(free(t)) for t in TIMES],
              "reference_J": [mean(free(t), CURRENT) for t in TIMES], "settings": {}}
    for f in (0.92, 0.99):
        cap = float(np.log(3) + f*np.log(f) + (1-f)*np.log((1-f)/2))
        coarse = smooth(free, cap, 0.005)
        fine = smooth(free, cap, 0.0025)
        error = float(np.max(np.abs(np.array(coarse["delta_J"]) - fine["delta_J"])))
        assert error < 1e-7
        result["settings"][str(f)] = {"cap": cap, "hard": hard(free, cap), "smooth": fine,
                                      "step_halving_max_delta_J_error": error}
    print(json.dumps(result, indent=2, allow_nan=False))


if __name__ == "__main__":
    main()
