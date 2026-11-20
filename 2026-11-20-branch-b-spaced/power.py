"""Prospective power of the same exact score used on future images."""
import json
from math import comb
from pathlib import Path

import numpy as np
from scipy.stats import binomtest
from score import p_value

HERE = Path(__file__).resolve().parent


def measured(p, eta):
    return np.array([sum(p[n]*comb(n,k)*eta**k*(1-eta)**(n-k)
                         for n in range(k,4)) for k in range(4)])


def main():
    cases = json.loads((HERE/'results.json').read_text())['cases']['region']
    rng = np.random.default_rng(20261120)
    out = []
    for eta in (1., .90):
        lo, hi = [measured(cases[a]['rows'][2]['p'],eta) for a in ('L','H')]
        prob = np.convolve(lo, hi[::-1])
        for n in (320, 480, 640):
            draws = rng.multinomial(n, prob/prob.sum(), size=4000)
            successes = sum(p_value(row) <= .05 for row in draws)
            ci = binomtest(successes, len(draws)).proportion_ci(method='wilson')
            out.append(dict(eta=eta,pairs=n,contrast=float((lo-hi)@np.arange(4)),
                            power=successes/len(draws),mc95=[ci.low,ci.high]))
    (HERE/'power.json').write_text(json.dumps(out,indent=2)+'\n')
    print(out)


if __name__ == '__main__':
    main()
