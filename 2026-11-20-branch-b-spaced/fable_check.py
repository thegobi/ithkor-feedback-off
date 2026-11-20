import numpy as np, itertools
from scipy.linalg import expm
L, N, U, Jb, tf, tw = 6, 3, 0.35, 0.65, 0.40, 0.05
B = [s for s in itertools.product(range(N+1), repeat=L) if sum(s) == N]
ix = {s: i for i, s in enumerate(B)}; D = len(B)
def hop(i, j):
    M = np.zeros((D, D))
    for s, a in ix.items():
        if s[j]:
            t = list(s); t[j] -= 1; t[i] += 1
            M[ix[tuple(t)], a] += np.sqrt(s[j]*(s[i]+1))
    return M + M.T
def Ham(closed):
    H = np.diag([U/2*sum(n*(n-1) for n in s) for s in B]).astype(complex)
    for i in range(L):
        b = (i, (i+1) % L)
        J = (0.0 if closed else Jb) if b in [(1, 2), (5, 0)] else 1.0
        H -= J*hop(*b)
    return H
nop = lambda k: np.array([s[k] for s in B], float)
XS = {"n1": nop(1), "n0+n1": nop(0)+nop(1)}
NR = (nop(0)+nop(1)).astype(int)
ka = sorted({s[:2] for s in B}); ia = {k: i for i, k in enumerate(ka)}
grp = {}
for s, a in ix.items(): grp.setdefault(s[2:], []).append(a)
def SR(rho):
    r = np.zeros((len(ka),)*2, complex)
    for g in grp.values():
        q = [ia[B[a][:2]] for a in g]
        r[np.ix_(q, q)] += rho[np.ix_(g, g)]
    p = np.linalg.eigvalsh(r); p = p[p > 1e-14]
    return float(-(p*np.log(p)).sum())
def run(X, cap=None, labels=(0, 1, 2), strobe=False, gain=1.0):
    x = XS[X]; cache = {}
    def props(c):
        if c not in cache:
            H = Ham(c); W = []
            for j in labels:
                if strobe:
                    W.append(np.diag(np.exp(-2j*np.pi*j*gain*x/3)) @ expm(-1j*H*tw))
                else:
                    W.append(expm(-1j*(H + gain*j*2*np.pi/(3*tw)*np.diag(x))*tw))
            cache[c] = (expm(-1j*H*tf), W)
        return cache[c]
    psi = np.zeros(D, complex); psi[ix[(3, 0, 0, 0, 0, 0)]] = 1
    rho = np.outer(psi, psi.conj()); closed = False; first = None; S = []
    for c in (1, 2, 3):
        Uf, W = props(closed)
        rho = Uf @ rho @ Uf.conj().T
        rho = sum(w @ rho @ w.conj().T for w in W)/len(W)
        S.append(SR(rho))
        if cap is not None and not closed and S[-1] > cap:
            closed = True; first = c
    d = rho.diagonal().real
    P = np.array([d[NR == k].sum() for k in range(N+1)])
    return first, S, float(P @ np.arange(N+1)), P
caps = {"open": None, "L": 0.764391142, "H": 1.035679283}
np.set_printoptions(precision=6, suppress=True)
for X in XS:
    for m, cap in caps.items():
        f, S, mu, P = run(X, cap)
        fc = "none" if f is None else f"cycle {f} (t={f*(tf+tw):.2f})"
        print(f"X={X:6s} {m:4s} first close: {fc}; S_R(nats) at .45/.90/1.35 =",
              np.array(S), f"; <N_R>={mu:.6f}; P(N_R=0..3) =", P)
    for tag, kw in [("strobe", dict(strobe=True)), ("single-image j=1", dict(labels=(1,))),
                    ("gain 0.95", dict(gain=0.95))]:
        f, S, mu, P = run(X, None, **kw)
        print(f"X={X:6s} open control [{tag}]: S_R =", np.array(S), f"; <N_R>={mu:.6f}; P =", P)
