"""Boundary flux, independent number samples and a paired ideal number probe."""
import json
import math
import sys
from pathlib import Path

import numpy as np

PREVIOUS = Path(__file__).resolve().parents[1] / "2026-11-19-bhm-delayed-choice"
sys.path.insert(0, str(PREVIOUS))
from late import CAP, path, v

LEFT, MID, RIGHT = 0.72, 0.74, 0.76
N = np.array(v.ring.BRIGHT_COUNT)
OUT = np.arange(4)
GROUPS = N[:, None] == OUT
N_OP = np.diag(N)
FLUX = 1j * (v.H_OPEN @ N_OP - N_OP @ v.H_OPEN)
EIG, BASIS = np.linalg.eigh(v.H_OPEN)
TRIALS = 2000


def number_law(s):
    return np.bincount(N, weights=abs(s)**2, minlength=4)


def passive(taus):
    p, records = [], []
    for sign, tau in zip((1,-1), taus):
        at = path(sign, tau)
        laws = np.stack([number_law(at(t)) for t in (LEFT,RIGHT)])
        p.append(laws)
        f = int(tau is None or MID < tau)
        current = f*v.mean(at(MID), FLUX)
        derivative = ((number_law(at(MID+1e-6)) - number_law(at(MID-1e-6))) @ OUT) / 2e-6
        np.testing.assert_allclose(current, derivative, atol=1e-8)
        records.append(dict(open=f, inward_current=current, drift=(laws[1]-laws[0]) @ OUT))
    return np.array(p), records


def passive_test(laws,seed=20261121):
    rng = np.random.default_rng(seed)
    means = laws @ OUT
    templates = means[:,:,1] - means[:,:,0]
    variance = (laws @ (OUT**2) - means**2).sum(axis=2).mean(axis=0)
    counts = []
    for arm, pair in enumerate(laws):
        measurements = []
        for start,end in pair:
            a = rng.multinomial(2000,start/start.sum(),size=TRIALS) @ OUT
            b = rng.multinomial(2000,end/end.sum(),size=TRIALS) @ OUT
            measurements.append((b-a)/2000)
        residual = np.stack(measurements,axis=1)[:,None,:]-templates
        decisions = ((residual**2)/variance).sum(axis=2).argmin(axis=1)
        counts.append(int(sum(decisions==arm)))
    return dict(correct=counts, decisions_per_arm=TRIALS, accuracy=sum(counts)/(2*TRIALS))


def number_probe(sign, elapsed, check_threshold=False):
    # Each column is an unnormalized branch following the first number reading.
    initial = path(sign,None)(LEFT)[:,None]*GROUPS
    weights = (abs(initial)**2).sum(axis=0)
    coeff = BASIS.T @ initial
    changes, conditional, ensemble = [], [], []
    for dt in elapsed:
        branches = BASIS @ (np.exp(-1j*dt*EIG)[:,None]*coeff)
        changes.append(float((abs(branches)**2)[~GROUPS].sum()))
        if check_threshold:
            rho = np.zeros((len(v.LOCAL),len(v.LOCAL)),complex)
            for k,w in enumerate(weights):
                if w <= 1e-15:
                    continue
                a = np.zeros((len(v.LOCAL),len(v.OUTSIDE)),complex)
                a[v.REGION,v.REST] = branches[:,k]
                block = a @ a.conj().T
                rho += block
                conditional.append(v.entropy(np.linalg.eigvalsh(block)/w))
            ensemble.append(v.entropy(np.linalg.eigvalsh(rho)))
    return np.array(changes), max(conditional,default=0.), max(ensemble,default=0.)


def alarm(p_plus,p_minus,n=2000):
    # P(no changes for +) times P(at least five changes for -).
    lower = sum(math.comb(n,k)*p_minus**k*(1-p_minus)**(n-k) for k in range(5))
    return (1-p_plus)**n*np.clip(1-lower,0.,1.)


def run():
    prior = json.loads((PREVIOUS/"predictions.json").read_text(encoding="utf-8-sig"))
    ts = (prior["1"],prior["-1"])
    clock = json.loads((PREVIOUS/"results.json").read_text(encoding="utf-8-sig"))["best_shared_grid"]["timer"]
    assert ts[0]<LEFT<MID<clock<RIGHT<ts[1]
    assert not np.any(v.H_CUT @ N_OP - N_OP @ v.H_CUT)
    p_thr, threshold = passive(ts)
    p_clk, timer = passive([clock]*2)
    _, open_baseline = passive([None]*2)
    # Between L and the clock time N_R can change; after the cut it is conserved.
    # If cut before L, the probability of a mismatch is zero for either sign.
    span = np.linspace(0,RIGHT-LEFT,801)
    p_plus, _, _ = number_probe(1,span)
    p_minus, conditional, ensemble = number_probe(-1,span,check_threshold=True)
    assert max(conditional,ensemble) < CAP
    common_alarm = alarm(p_plus,p_minus)
    best = int(np.argmax(common_alarm))
    ic = int(np.argmin(abs(LEFT+span-clock)))
    assert abs(LEFT+span[ic]-clock)<1e-12
    # Supplementary passive clock: regular grid using only the two expected drifts.
    # Once cut, N_R freezes; for all cut times before LEFT the drift is zero.
    drift_target = np.array([r["drift"] for r in threshold])
    paths = [path(s,None) for s in (1,-1)]
    starts = np.array([number_law(f(LEFT)) @ OUT for f in paths])
    drifts = np.array([[number_law(f(LEFT+h)) @ OUT for f in paths] for h in span]) - starts
    threshold_var = (p_thr @ OUT**2 - (p_thr @ OUT)**2).sum(axis=1)
    closest = LEFT+span[np.argmin(np.sum((drifts-drift_target)**2/threshold_var,axis=1))]
    p_adapt,_ = passive([closest]*2)
    # Bound the entire continuous clock family. The change amplitude norm is
    # sqrt(p); its speed is at most ||H_open|| for normalized projected branches.
    eps = np.max(abs(EIG)) * (span[1]-span[0])/2
    lo_plus = np.maximum(0,np.sqrt(p_plus)-eps)**2
    hi_minus = np.minimum(1,np.sqrt(p_minus)+eps)**2
    n90 = 2000
    while alarm(0,p_minus[-1],n90) < 0.9:
        n90 += 1
    return dict(passive_threshold=threshold, passive_clock=timer, passive_open=open_baseline,
                passive_test=passive_test(np.stack([p_thr,p_clk])),
                passive_retuned=dict(timer=closest,**passive_test(np.stack([p_thr,p_adapt]),20261122)),
                ideal_paired=dict(
                    conditional_S_max=conditional, ensemble_S_max=ensemble,
                    threshold_transfer=[0,p_minus[-1]], clock_transfer=[p_plus[ic],p_minus[ic]],
                    threshold_detection=alarm(0,p_minus[-1]),
                    clock_false_alarm=common_alarm[ic],
                    worst_grid_false_alarm=common_alarm[best],worst_grid_clock=LEFT+span[best],
                    coarse_grid_worst=common_alarm[::2].max(),
                    uniform_false_alarm_upper=alarm(lo_plus,hi_minus).max(),
                    n90_per_sign=n90, n90_readouts=4*n90, n90_power=alarm(0,p_minus[-1],n90),
                    n90_uniform_false_alarm_upper=alarm(lo_plus,hi_minus,n90).max()))


if __name__=="__main__":
    print(json.dumps(run(), indent=2,allow_nan=False))
