import hashlib
import json
from statistics import NormalDist

import numpy as np

from late import CAP, HERE, PULSE, path, v


def template(sign, tau):
    trajectory = path(sign, tau)
    states = np.stack([trajectory(t) for t in v.TIMES])
    return np.einsum("ij,ij->i", states.conj(), states @ v.CURRENT.T).real


def law(sign, tau):
    trajectory = path(sign, tau)
    eig, vec = np.linalg.eigh(v.CURRENT)
    outcomes = np.rint(eig).astype(int)
    np.testing.assert_allclose(outcomes, eig, atol=1e-12)
    rows = []
    for t in v.TIMES:
        s = trajectory(t)
        weights = np.abs(vec.conj().T @ s)**2
        p = np.bincount(outcomes+3, weights, minlength=7)
        assert abs(p.sum()-1) < 2e-13
        rows.append(p/p.sum())
    return np.array(rows)


def bounds(k,n):
    z = NormalDist().inv_cdf(1 - 0.05/8)
    p = k/n
    mid = p + z*z/(2*n)
    width = z*np.sqrt(p*(1-p)/n + z*z/(4*n*n))
    return [(mid-width)/(1+z*z/n), (mid+width)/(1+z*z/n)]


def score(target, timer, ref, rng):
    laws = np.stack((target,timer))
    outcomes = np.arange(-3,4)
    means = laws @ outcomes
    deltas = means - ref
    var = laws @ outcomes**2 - means**2
    w = 1/np.maximum(var.mean(axis=0),1e-12)
    counts = []
    n = 2000
    for arm, branch in enumerate(laws):
        draws = np.column_stack([rng.multinomial(1000, p, size=n) @ outcomes / 1000 for p in branch]) - ref
        loss = (((draws[:,None,:] - deltas)**2)*w).sum(axis=2)
        choice = loss.argmin(axis=1)
        ties = loss[:,0] == loss[:,1]
        choice[ties] = rng.integers(2,size=ties.sum())
        counts.append(int((choice==arm).sum()))
    intervals = [bounds(k,n) for k in counts]
    return dict(correct=counts, n_per_arm=n, balanced_accuracy=sum(counts)/(2*n),
                simultaneous_intervals=intervals, passed=all(ci[0]>.7 for ci in intervals),
                current_gap=(means[0]-means[1]).reshape(2,4).tolist(),
                threshold_delta_J=deltas[0].reshape(2,4).tolist(),
                timer_delta_J=deltas[1].reshape(2,4).tolist())


def run():
    for row in (HERE/'freeze.sha256').read_text().splitlines():
        digest, name = row.split()
        assert hashlib.sha256((HERE/name).read_text(encoding='utf-8-sig').encode()).hexdigest()==digest
    taus = json.loads((HERE/'predictions.json').read_text(encoding='utf-8-sig'))
    signs = (1,-1)
    timer = taus['0']
    old_file = HERE.parent/'2026-11-19-bhm-preparation-clock'/'predictions.json'
    calibrated = json.loads(old_file.read_text(encoding='utf-8-sig'))['0.99']['threshold_times']['210000']
    np.testing.assert_allclose(law(0,timer),law(0,calibrated),rtol=0,atol=1e-12)
    for s in signs:
        np.testing.assert_allclose(v.S(path(s,None)(PULSE)),v.S(path(0,None)(PULSE)),atol=1e-12)
        for t in v.TIMES:
            if t >= taus[str(s)]:
                np.testing.assert_allclose(v.S(path(s,taus[str(s)])(t)), CAP, atol=1e-12)
    ref = np.concatenate([template(s,None) for s in signs])
    target = np.vstack([law(s,taus[str(s)]) for s in signs])
    outcomes = np.arange(-3,4)
    target_mean = target @ outcomes
    w = 1/np.maximum(target @ outcomes**2 - target_mean**2,1e-12)
    grid = np.arange(2501)/1000
    objective = []
    for t in grid:
        shared = np.concatenate([template(s,t) for s in signs])
        objective.append(np.sum(w*(shared-target_mean)**2))
    best = float(grid[np.argmin(objective)])
    result = {}
    rng = np.random.default_rng(20261120)
    for label,t in [('calibrated',timer),('best_shared_grid',best)]:
        candidate = np.vstack([law(s,t) for s in signs])
        result[label] = dict(timer=t,**score(target,candidate,ref,rng))
    return result


if __name__=='__main__':
    print(json.dumps(run(),indent=2,allow_nan=False))
