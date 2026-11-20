"""Fourier readout on known number inputs, with hopping active during the write."""
import json
import numpy as np
from scipy.special import rel_entr
from model import CAPS, F, HERE, NR, unitaries


def capacity(channel):
    prior = np.full(len(channel), 1/len(channel))
    for _ in range(5000):
        div = rel_entr(channel, prior @ channel).sum(axis=1)
        lower = prior @ div
        if max(div)-lower < 1e-12:
            return float(lower)
        prior *= np.exp(div-max(div))
        prior /= prior.sum()
    raise RuntimeError('Capacity bounds did not converge')


def main():
    # Each computational basis vector is a different prepared Fock input.
    u = np.array(unitaries(False,'region',.05,.05,True))
    gram = np.einsum('jba,kba->ajk',u,u.conj())
    out = []
    for f,static_cap in zip(F,CAPS):
        coherence = (3*f-1)/2
        damping = coherence + (1-coherence)*np.eye(3)
        probabilities = []
        for y in range(3):
            v = np.exp(2j*np.pi*y*np.arange(3)/3)
            kernel = np.outer(v,v.conj())*damping
            probabilities.append(np.einsum('ajk,jk->a',gram,kernel).real/9)
        p = np.array(probabilities).T
        np.testing.assert_allclose(p.sum(axis=1),1,atol=1e-12)
        assert p.min()>-1e-12
        by_number = np.array([p[NR==x].mean(axis=0) for x in range(4)])
        channel = np.array([.5*(by_number[0]+by_number[3]),*by_number[1:3]])
        out.append(dict(f=f,static_cap=static_cap,finite_write_cap=capacity(channel),
                        calibration_inputs=by_number.tolist(),
                        p_correct_range=[float(p[np.arange(len(NR)),NR%3].min()),
                                         float(p[np.arange(len(NR)),NR%3].max())]))
    (HERE/'calibration.json').write_text(json.dumps(out,indent=2)+'\n')
    print(out)


if __name__ == '__main__':
    main()
