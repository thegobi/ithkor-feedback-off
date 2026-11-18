"""Exact finite Bose–Hubbard phase-conjugate counterexample."""

import argparse
import hashlib
import json
import math
from pathlib import Path

import numpy as np


SITES = 6
PARTICLES = 3
BRIGHT = (0, 1)
U_VALUES = (0.35, 1.2)
BARRIER_VALUES = (0.65, 1.05)
TIMES = (0.0, 0.01, 0.05)
TOLERANCE = 1e-10


def occupations(particles, sites):
    if sites == 1:
        yield (particles,)
        return
    for count in range(particles + 1):
        for rest in occupations(particles - count, sites - 1):
            yield (count, *rest)


BASIS = list(occupations(PARTICLES, SITES))
INDEX = {state: index for index, state in enumerate(BASIS)}
BRIGHT_COUNT = np.array([sum(state[site] for site in BRIGHT) for state in BASIS])
DARK_FRACTION = 1 - BRIGHT_COUNT / PARTICLES


def hopping(destination, source):
    operator = np.zeros((len(BASIS), len(BASIS)))
    for column, state in enumerate(BASIS):
        if state[source]:
            moved = list(state)
            moved[destination] += 1
            moved[source] -= 1
            operator[INDEX[tuple(moved)], column] = math.sqrt(
                state[source] * (state[destination] + 1)
            )
    return operator


def hamiltonian(interaction, barrier):
    matrix = np.diag([
        interaction / 2 * sum(count * (count - 1) for count in state)
        for state in BASIS
    ])
    for source in range(SITES):
        destination = (source + 1) % SITES
        coupling = barrier if (source in BRIGHT) != (destination in BRIGHT) else 1
        move = hopping(destination, source)
        matrix -= coupling * (move + move.T)
    return matrix


def condensate():
    orbital = np.array([1, 1j, -1, 0, 0, 0]) / math.sqrt(3)
    return np.array([
        math.sqrt(math.factorial(PARTICLES) / math.prod(map(math.factorial, state)))
        * np.prod(orbital ** state)
        for state in BASIS
    ])


def expectation(state, operator):
    return np.vdot(state, operator @ state)


def readout(state):
    probabilities = abs(state) ** 2
    sectors = np.bincount(BRIGHT_COUNT, probabilities, minlength=PARTICLES + 1)
    nonzero = sectors[sectors > 0]
    return {
        "D": float(probabilities @ DARK_FRACTION),
        "H_bright": float(-nonzero @ np.log(nonzero) / math.log(PARTICLES + 1)),
        "phase_y": float(0.5 + expectation(state, hopping(0, 1)).imag / PARTICLES),
        "bright_count_distribution": sectors.tolist(),
    }


def run_case(interaction, barrier):
    matrix = hamiltonian(interaction, barrier)
    states = condensate(), condensate().conjugate()
    plus, minus = states
    np.testing.assert_allclose(matrix, matrix.T, atol=TOLERANCE, rtol=0)
    np.testing.assert_allclose(abs(plus) ** 2, abs(minus) ** 2, atol=TOLERANCE, rtol=0)
    energies = [expectation(state, matrix).real for state in states]
    np.testing.assert_allclose(energies, [interaction, interaction], atol=TOLERANCE, rtol=0)
    diagonal = np.diag(DARK_FRACTION)
    derivative = 1j * (matrix @ diagonal - diagonal @ matrix)
    flux = [expectation(state, derivative).real for state in states]
    analytic_flux = 2 * barrier / 3
    np.testing.assert_allclose(flux, [analytic_flux, -analytic_flux], atol=TOLERANCE, rtol=0)

    energies_spectrum, eigenvectors = np.linalg.eigh(matrix)
    rows = []
    for time in TIMES:
        step = eigenvectors * np.exp(-1j * time * energies_spectrum) @ eigenvectors.T
        reverse_step = step.conjugate()
        forward = [step @ state for state in states]
        np.testing.assert_allclose(forward[1], (reverse_step @ plus).conjugate(),
                                   atol=TOLERANCE, rtol=0)
        np.testing.assert_allclose([np.vdot(state, state) for state in forward], 1,
                                   atol=TOLERANCE, rtol=0)
        first, second = map(readout, forward)
        rows.append({"time": time, "plus": first, "minus": second,
                     "D_gap": first["D"] - second["D"]})

    np.testing.assert_allclose([rows[0]["plus"]["D"], rows[0]["minus"]["D"]],
                               1 / 3, atol=TOLERANCE, rtol=0)
    np.testing.assert_allclose([rows[0][label]["phase_y"] for label in ("plus", "minus")],
                               [5 / 6, 1 / 6], atol=TOLERANCE, rtol=0)
    assert abs(rows[0]["plus"]["H_bright"] - rows[0]["minus"]["H_bright"]) < TOLERANCE
    for row in rows[1:]:
        expected_gap = 2 * analytic_flux * row["time"]
        assert abs(row["D_gap"] - expected_gap) < 0.01 * expected_gap

    return {
        "U": interaction,
        "barrier_J": barrier,
        "initial_energy": energies,
        "initial_dD_dt": flux,
        "initial_max_fock_probability_difference": float(np.max(
            abs(abs(plus) ** 2 - abs(minus) ** 2)
        )),
        "trajectory": rows,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = {
        "verdict": "universal_instantaneous_D_plus_H_sufficiency_falsified",
        "basis_dimension": len(BASIS),
        "numpy_version": np.__version__,
        "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "cases": [run_case(u, j) for u in U_VALUES for j in BARRIER_VALUES],
    }
    payload = json.dumps(result, indent=2, allow_nan=False) + "\n"
    if args.output:
        args.output.write_text(payload, encoding="utf-8")
    else:
        print(payload, end="")


if __name__ == "__main__":
    main()
