"""Blind shot-noise draws scored against frozen, preparation-specific predictions."""
import hashlib
import json
from statistics import NormalDist

import numpy as np

from predict import HERE, prepare, v


def check_freeze():
    for row in (HERE / "freeze.sha256").read_text().splitlines():
        expected, name = row.split()
        content = (HERE/name).read_text(encoding="utf-8-sig").encode()
        if hashlib.sha256(content).hexdigest() != expected:
            raise ValueError(f"Frozen input differs: {name}")


def evolution(free, tau):
    if tau is None:
        return [free(t) for t in v.TIMES]
    after = v.trajectory(v.H_CUT, free(tau))
    return [free(t) if t <= tau else after(t-tau) for t in v.TIMES]


def wilson(k, n):
    z = NormalDist().inv_cdf(1 - 0.05/(2*8))
    p = k/n
    c = p + z*z/(2*n)
    h = z*np.sqrt(p*(1-p)/n + z*z/(4*n*n))
    return [(c-h)/(1+z*z/n), (c+h)/(1+z*z/n)]


def evaluate(free, taus, calibration, rng):
    eigenvalues, vectors = np.linalg.eigh(v.CURRENT)
    outcomes = np.arange(-3, 4)
    labels = np.rint(eigenvalues).astype(int)
    np.testing.assert_allclose(labels, eigenvalues, atol=1e-12)
    probabilities = []
    pref = np.array([v.mean(free(t), v.CURRENT) for t in v.TIMES])
    for tau in taus:
        arm = []
        for state in evolution(free, tau):
            weights = np.abs(vectors.conj().T @ state)**2
            p = np.bincount(labels+3, weights, minlength=7)
            np.testing.assert_allclose(p.sum(), 1, atol=2e-13, rtol=0)
            p /= p.sum()
            np.testing.assert_allclose(p @ outcomes, v.mean(state, v.CURRENT), atol=1e-12)
            arm.append(p)
        probabilities.append(arm)
    probs = np.asarray(probabilities)
    means = probs @ outcomes
    templates = means - pref
    gap = templates[0] - templates[1]
    result = dict(means_relative_to_open=templates.tolist(), threshold_minus_clock=gap.tolist())
    if calibration:
        np.testing.assert_allclose(probs[0], probs[1], atol=1e-12, rtol=0)
        result["identical_law_balanced_accuracy"] = 0.5
        return result
    variances = probs @ (outcomes**2) - means**2
    w = 1 / np.maximum(variances.mean(axis=0), 1e-12)
    n = 2000
    stats = {}
    for arm, label in enumerate(("threshold", "timer")):
        readings = np.column_stack([
            rng.multinomial(2000, p, size=n) @ outcomes / 2000 for p in probs[arm]
        ]) - pref
        dsq = ((readings[:, None, :] - templates)**2 * w).sum(axis=2)
        choice = np.argmin(dsq, axis=1)
        ties = dsq[:,0] == dsq[:,1]
        choice[ties] = rng.integers(2, size=ties.sum())
        k = int(np.sum(choice == arm))
        stats[label] = dict(correct=k, decisions=n, accuracy=k/n, ci=wilson(k,n))
    result.update(arms=stats, balanced_accuracy=sum(a["accuracy"] for a in stats.values())/2,
                  passed=all(a["ci"][0] > 0.70 for a in stats.values()))
    return result


if __name__ == "__main__":
    check_freeze()
    frozen = json.loads((HERE/"predictions.json").read_text(encoding="utf-8-sig"))
    rng = np.random.default_rng(20261119)
    results = {}
    for fidelity, settings in frozen.items():
        results[fidelity] = {}
        for prep, tau in settings["threshold_times"].items():
            free = v.trajectory(v.H_OPEN, prepare(prep))
            results[fidelity][prep] = evaluate(free, (tau, settings["timer"]), prep=="300000", rng)
    print(json.dumps(results, indent=2, allow_nan=False))
