"""Check independent Hamiltonian against all six nominal cases and exact score."""
import contextlib
import io
import itertools

import numpy as np
from model import CAPS, trajectory
from score import p_value
with contextlib.redirect_stdout(io.StringIO()):
    import fable_check

for x, ref in [('site1','n1'),('region','n0+n1')]:
    for cap in [None,*CAPS]:
        calc = trajectory(x,cap)
        hit, entropies, mean, p = fable_check.run(ref,cap)
        assert calc['hit'] == (round(hit*.45,2) if hit else None)
        np.testing.assert_allclose([r['S'] for r in calc['rows']],entropies,rtol=0,atol=1e-11)
        np.testing.assert_allclose(calc['rows'][-1]['p'],p,rtol=0,atol=1e-11)
        assert abs(calc['rows'][-1]['mean']-mean)<1e-11

for sample in [(-2,1,3,0),(0,0,0),(3,3,3),(-1,-2,-3),(1,-1)]:
    values = np.array(sample)
    tail = np.mean([np.dot(s,abs(values))>=sum(sample)
                    for s in itertools.product((-1,1),repeat=len(sample))])
    assert abs(tail-p_value(np.bincount(values+3,minlength=7)))<1e-12
print('Six independent simulations and five exact randomization checks passed.')
