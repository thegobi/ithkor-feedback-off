"""Exact three-boson ensemble maps, in units hbar=J_in=1."""
from functools import cache
from pathlib import Path

import numpy as np
from scipy.linalg import eigh
from scipy.special import entr

HERE = Path(__file__).resolve().parent
import physics_phase_pair as fixture

BASIS = np.array(fixture.BASIS)
NR = BASIS[:,:2].sum(axis=1)
F = (.92,.99)
CAPS = [np.log(3)+f*np.log(f)+(1-f)*np.log((1-f)/2) for f in F]
D = len(BASIS)
INITIAL = np.zeros((D,D), complex)
INITIAL[fixture.INDEX[(3,0,0,0,0,0)],fixture.INDEX[(3,0,0,0,0,0)]] = 1
LOCAL, LOCAL_ID = np.unique(BASIS[:,:2],axis=0,return_inverse=True)
_, EXTERIOR = np.unique(BASIS[:,2:],axis=0,return_inverse=True)
BOUNDARY = fixture.hamiltonian(.35,.65)-fixture.hamiltonian(.35,0)


@cache
def spectrum(closed, x, label, width):
    h = fixture.hamiltonian(.35, 0 if closed else .65)
    diag = {'region': NR, 'site0': BASIS[:,0], 'site1': BASIS[:,1]}[x]
    return eigh(h + (label * 2*np.pi/(3*width))*np.diag(diag))


@cache
def unitaries(closed,x,width,duration,write):
    result=[]
    for j in (range(3) if write else [0]):
        energies,vectors=spectrum(closed,x,j,width)
        result.append((vectors*np.exp(-1j*energies*duration))@vectors.T)
    return result


def advance(rho, closed, x, width, duration, write):
    us=unitaries(closed,x,width,duration,write)
    return sum(u @ rho @ u.conj().T for u in us)/len(us)


def entropy(rho):
    inside=np.zeros((len(LOCAL),len(LOCAL)),complex)
    for k in np.unique(EXTERIOR):
        ix=np.flatnonzero(EXTERIOR==k)
        inside[np.ix_(LOCAL_ID[ix],LOCAL_ID[ix])] += rho[np.ix_(ix,ix)]
    w=np.linalg.eigvalsh(inside)
    assert w.min()>-1e-10 and abs(w.sum()-1)<1e-10
    return float(entr(w.clip(0)).sum())


def snapshot(rho):
    p=np.bincount(NR,rho.diagonal().real,minlength=4)
    return dict(S=entropy(rho),p=p.tolist(),mean=float(p@np.arange(4)))


def trajectory(x, cap, schedule=((.40,.05),)*3):
    rho=INITIAL
    closed=False
    hit=None
    time=0.
    rows=[]
    for gap,width in schedule:
        rho=advance(rho,closed,x,width,gap,False)
        rho=advance(rho,closed,x,width,width,True)
        time=round(time+gap+width,12)
        measurement=snapshot(rho)
        work=0.
        if not closed and cap is not None and measurement['S']>cap:
            hit=time
            closed=True
            work=-float(np.trace(rho@BOUNDARY).real)
        rows.append(dict(time=time,closed=closed,switch_work=work,**measurement))
    return dict(hit=hit,rows=rows)


if __name__=='__main__':
    import json
    cases={x:{arm:trajectory(x,cap) for arm,cap in
              [('open',None),('L',CAPS[0]),('H',CAPS[1])]} for x in ('region','site1')}
    print(json.dumps(cases,indent=2))
