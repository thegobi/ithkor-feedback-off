"""Two-site entropy and current in the six-site, fixed-three-boson ring."""

import json
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "2026-11-18-ithkor-evidence-search"))
import physics_phase_pair as ring


def entropy(weights):
    positive = weights[weights > 1e-14]
    return float(-positive @ np.log(positive))


def subsystem_indices(configs):
    labels = sorted(set(configs))
    return np.array([labels.index(c) for c in configs]), labels


def run():
    ham = ring.hamiltonian(0.35, 0.65)
    energies, modes = np.linalg.eigh(ham)
    initial = ring.INDEX[(3, 0, 0, 0, 0, 0)]
    region, labels = subsystem_indices([x[:2] for x in ring.BASIS])
    rest, rest_labels = subsystem_indices([x[2:] for x in ring.BASIS])
    move = ring.hopping(1, 0)
    current = 1j * (move - move.T)
    assert all(sum(x) == 3 for x in ring.BASIS)
    np.testing.assert_allclose(np.linalg.norm(current, 2), 3, atol=1e-12)

    def state(t):
        return modes @ (np.exp(-1j * t * energies) * modes[initial])

    def local(psi):
        a = np.zeros((len(labels), len(rest_labels)), dtype=complex)
        a[region, rest] = psi
        return a @ a.conj().T

    def local_entropy(t):
        return entropy(np.linalg.eigvalsh(local(state(t))))

    def flux(psi):
        return float(np.vdot(psi, current @ psi).real)

    def trial(fidelity, step):
        cap = np.log(3) + fidelity * np.log(fidelity) + (1-fidelity) * np.log((1-fidelity)/2)
        t = next(k*step for k in range(1,round(2.5/step)+1) if local_entropy(k*step) > cap)
        s = state(t)
        rho = local(s)
        s_before = local_entropy(t)
        prob = rho.diagonal().real
        number_entropy = entropy(np.bincount([sum(x) for x in labels], weights=prob))
        phased = s * np.exp(1j * np.pi * np.array([x[0] for x in ring.BASIS]))
        np.testing.assert_allclose(np.linalg.eigvalsh(local(phased)), np.linalg.eigvalsh(rho), atol=1e-12)
        np.testing.assert_allclose(flux(phased), -flux(s), atol=1e-12)
        # Full local occupation dephasing kills all matrix elements of J on 0--1.
        pure_dm = np.outer(s, s.conj())
        dm = pure_dm * (region[:, None] == region[None, :])
        j_dephased = np.trace(dm @ current).real
        dephase_d = float(np.abs(np.linalg.eigvalsh(dm - pure_dm)).sum()/2)
        energy_change = float(np.trace((dm - pure_dm) @ ham).real)
        np.testing.assert_allclose(j_dephased, 0, atol=1e-12)
        assert entropy(prob) >= s_before - 1e-12
        lo, hi = t-step, t
        for _ in range(50):
            mid = (lo+hi)/2
            if local_entropy(mid) > cap:
                hi = mid
            else:
                lo = mid
        crossing = (lo+hi)/2
        # A one-time inverse evolution of the whole ring is an ordinary unitary
        # comparator, not an autonomous local entropy-reduction law.
        back = modes @ (np.exp(1j * (t-crossing) * energies) * (modes.T @ s))
        np.testing.assert_allclose(back, state(crossing), atol=1e-12)
        np.testing.assert_allclose(local_entropy(crossing), cap, atol=1e-12)
        np.testing.assert_allclose(np.vdot(back, ham @ back), np.vdot(s, ham @ s), atol=1e-12)
        d = np.sqrt(max(0, 1-abs(np.vdot(s, back))**2))
        delta = [flux(state(crossing+h))-flux(state(t+h)) for h in (0, 0.25, 0.5, 1)]
        assert max(map(abs, delta)) <= 6*d + 1e-10
        return dict(cap_nats=cap, sample=t, crossing=crossing, S_before=s_before,
                    S_number_floor=number_entropy, S_full_dephasing=entropy(prob),
                    J_before=flux(s), J_dephased=j_dephased, dephasing_d=dephase_d,
                    dephasing_energy_change=energy_change,
                    rewind_d=d, rewind_delta_J=delta)

    return {str(f): {str(step): trial(f, step) for step in (0.05, 0.025, 0.005)}
            for f in (0.92,0.99)}


if __name__ == "__main__":
    print(json.dumps(run(), indent=2, allow_nan=False))
