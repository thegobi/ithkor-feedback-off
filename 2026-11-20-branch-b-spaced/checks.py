"""Timing sweep, continuous first hits, number-readout and phase controls."""
import itertools
import json
from functools import cache

import numpy as np
from scipy.optimize import brentq
from model import (HERE, CAPS, NR, INITIAL, advance, snapshot, entropy, trajectory,
                   fixture)
from power import measured


@cache
def open_state(path):
    if not path:
        return INITIAL
    gap,width=path[-1]
    rho=advance(open_state(path[:-1]),False,'region',width,gap,False)
    return advance(rho,False,'region',width,width,True)


def timing():
    stages=list(itertools.product((.39,.4,.41),(.045,.05,.055)))
    stats={}
    @cache
    def info(path):
        return snapshot(open_state(path))
    diffs=[]
    for path in itertools.product(stages,repeat=3):
        rows=[info(path[:n]) for n in (1,2,3)]
        hits=[next((i+1 for i,r in enumerate(rows) if r['S']>c),0) for c in CAPS]
        key=str(tuple(hits))
        stats[key]=stats.get(key,0)+1
        # Once closed, the number distribution stays exactly fixed.
        means=[rows[(h or 3)-1]['mean'] for h in hits]
        diffs.append(means[0]-means[1])
    return dict(paths=len(diffs),cycles=stats,contrast_range=[min(diffs),max(diffs)])


def continuous(cap,gap,width,spacings):
    # Only the pre-hit trajectory is needed: N_R is conserved after cutoff.
    rho=INITIAL
    start=0.
    for _ in range(3):
        for duration,write in ((gap,False),(width,True)):
            def state(t):
                return advance(rho,False,'region',width,float(t),write)
            def difference(t):
                return entropy(state(t))-cap
            prev=0.
            for t in np.linspace(0,duration,spacings+1)[1:]:
                if difference(t)>=0:
                    hit=brentq(difference,prev,t)
                    return dict(time=start+hit,phase='write' if write else 'free',
                                **snapshot(state(hit)))
                prev=t
            rho=state(duration)
            start+=duration
    return None


def main():
    cases={x:{arm:trajectory(x,c,((.40,.05),)*4) for arm,c in [('open',None),('L',CAPS[0]),('H',CAPS[1])]}
           for x in ('region','site0','site1')}
    assert np.allclose(np.diag(NR)@fixture.hamiltonian(.35,0),
                       fixture.hamiltonian(.35,0)@np.diag(NR))
    for case in cases['region'].values():
        if case['hit'] is not None:
            closed=[r for r in case['rows'] if r['closed']]
            for r in closed:
                np.testing.assert_allclose(r['p'],closed[0]['p'],atol=1e-12)
                assert abs(r['S']-closed[0]['S'])<1e-12
    cont=[continuous(c,.40,.05,24) for c in CAPS]
    for c,r in zip(CAPS,cont):
        assert abs(r['time']-continuous(c,.40,.05,80)['time'])<1e-9
    # Baseline with no register; disambiguate site versus total parity readout.
    free=snapshot(advance(INITIAL,False,'region',.05,1.35,False))
    low,high=[cases['region'][arm]['rows'][2] for arm in ('L','H')]
    eta=high['mean']/low['mean']
    controls=dict(sham_cycle4_p=np.mean([low['p'],high['p']],axis=0).tolist(),
                  loss_only=dict(prob=1-eta,total_deficit=3*(1-eta),
                                 high_p=measured(low['p'],eta).tolist()))
    report=dict(cases=cases,controls=controls,continuous=cont,continuous_contrast=cont[0]['mean']-cont[1]['mean'],
                timing=timing(),free_no_register=free)
    (HERE/'results.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    for x in cases:
        for arm,r in cases[x].items():
            print(x,arm,r['hit'],r['rows'][-1])
    print('continuous',cont)
    print('timing',report['timing'],'free',free)


if __name__=='__main__':
    main()
