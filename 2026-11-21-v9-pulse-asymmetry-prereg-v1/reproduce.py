"""Numerical reproduction of the frozen six-site pulse-asymmetry protocol."""
import os
from functools import lru_cache
from itertools import combinations_with_replacement

# The small matrix operations become much slower with a large BLAS thread pool.
for _variable in ("OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "OMP_NUM_THREADS"):
    os.environ.setdefault(_variable, "1")

import numpy as np
from scipy import sparse
from scipy.integrate import quad, solve_ivp
from scipy.linalg import expm
from scipy.optimize import brentq
from scipy.special import entr


WIDTH = .05
GAP = .4
AREA = 2 * np.pi / 3
SITE = 1
THRESHOLD = .193567742
GAIN = 1.68911
PULSES = {"fast": .1, "slow": .9}
FIDELITIES = (.99, .92)
NUMERICS = {"standard": (.00085, 2e-10), "fine": (.000425, 2e-11)}


def pulse(t, rise, area=AREA, width=WIDTH):
    """Return g and the normalized positive release slope [-g']/g_max."""
    x = np.clip(t / width, 0., 1.)
    if x <= rise:
        return area / width * (1 - np.cos(np.pi * x / rise)), 0.
    angle = np.pi * (x - rise) / (1 - rise)
    return (area / width * (1 + np.cos(angle)),
            np.pi * np.sin(angle) / (2 * width * (1 - rise)))


def history_visibility(fidelity):
    """Fresh pointer, dephased during dummy write T and uncoupled storage 8T."""
    return ((3*fidelity - 1)/2)**9


def cq_entropy(joint):
    """Joint classical site-occupation / quantum pointer conditional entropy."""
    def entropy(matrices):
        return float(entr(np.maximum(np.linalg.eigvalsh(matrices), 0)).sum())
    return entropy(joint) - entropy(joint.sum(axis=0))


def make_sector(particles):
    tuples = [tuple(int(x) for x in np.bincount(sites, minlength=6))
              for sites in combinations_with_replacement(range(6), particles)]
    index = {b: i for i, b in enumerate(tuples)}
    basis = np.array(tuples)
    h = np.diag(.35 / 2 * np.sum(basis * (basis - 1), axis=1))
    for col, state in enumerate(tuples):
        for source, strength in enumerate((1., .65, 1., 1., 1., .65)):
            dest = (source + 1) % 6
            if state[source]:
                moved = list(state)
                moved[source] -= 1
                moved[dest] += 1
                row = index[tuple(moved)]
                element = -strength * np.sqrt(state[source] * (state[dest] + 1))
                h[row, col] += element
                h[col, row] += element
    return basis, index, h


class Ring:
    """Block representation ordered as (N, pointer-j, pointer-k, ring-b, ring-c)."""

    def __init__(self):
        sectors = [make_sector(n) for n in range(4)]
        self.dims = [len(b) for b, _, _ in sectors]
        self.offset = np.cumsum([0] + [9 * d**2 for d in self.dims])
        self.site_groups = []
        free = []
        loss = [[None] * 4 for _ in range(4)]
        drive = []
        dephase = []
        labels = np.arange(3)
        for n, (basis, _, h) in enumerate(sectors):
            d = self.dims[n]
            eye = sparse.eye(d)
            number = basis[:, SITE]
            nhat = sparse.diags(number, dtype=float)
            self.site_groups.append([np.flatnonzero(number == m) * (d + 1) for m in range(4)])
            def replicated(op):
                return sparse.kron(sparse.eye(9), op, format="csr")
            hs = sparse.csr_matrix(h)
            free.append(replicated(-1j * (sparse.kron(hs, eye) - sparse.kron(eye, hs.T))))
            loss[n][n] = replicated(-.5 * (sparse.kron(nhat, eye) + sparse.kron(eye, nhat)))
            if n:
                a = np.zeros((self.dims[n - 1], d))
                for col in np.flatnonzero(number):
                    lower = basis[col].copy()
                    lower[SITE] -= 1
                    a[sectors[n - 1][1][tuple(lower)], col] = np.sqrt(number[col])
                jump = sparse.csr_matrix(a)
                loss[n - 1][n] = replicated(sparse.kron(jump, jump))
            jn = labels[:, None] * number
            drive.append((-1j * (jn[:, None, :, None] - jn[None, :, None, :])).ravel())
            dephase.append(np.repeat((1 - np.eye(3)).ravel(), d*d))
        self.free = sparse.block_diag(free, format="csr")
        self.loss = sparse.bmat(loss, format="csr")
        self.drive = np.concatenate(drive)
        self.dephase = np.concatenate(dephase)
        self.basis, self.index, self.h3 = sectors[-1]

    def blocks(self, flat):
        for n, d in enumerate(self.dims):
            yield flat[self.offset[n]:self.offset[n + 1]].reshape(3, 3, d, d)

    def conditional_entropy(self, flat):
        # Superselection makes the site marginal diagonal in occupation m.
        # Each 3x3 unnormalized pointer block traces over identical ring states.
        joint = np.zeros((4, 3, 3), complex)
        for n, block in enumerate(self.blocks(flat)):
            pairs = block.reshape(3, 3, -1)
            for m, group in enumerate(self.site_groups[n]):
                if len(group):
                    joint[m] += pairs[:, :, group].sum(axis=2)
        return cq_entropy(joint)

    def stats(self, flat):
        traces, min_eigenvalues, defects = [], [], []
        for d, block in zip(self.dims, self.blocks(flat)):
            rho = block.transpose(0, 2, 1, 3).reshape(3*d, 3*d)
            traces.append(rho.trace())
            defects.append(float(np.max(np.abs(rho - rho.conj().T))))
            min_eigenvalues.append(float(np.linalg.eigvalsh(rho)[0]))
        return (np.array(traces).real, float(abs(sum(traces) - 1)),
                max(defects), min(min_eigenvalues))

    @lru_cache(maxsize=32)
    def rise_state(self, rise, control, resolution, area=AREA, width=WIDTH):
        # No loss anywhere on the rising edge. Conditional wavefunctions and
        # analytic pointer dephasing give the full joint state at the peak.
        if control:
            ket = np.eye(len(self.h3))[:, self.index[(0, 3, 0, 0, 0, 0)]]
        else:
            ket = expm(-1j * GAP * self.h3)[:, self.index[(3, 0, 0, 0, 0, 0)]]
        conditional = np.tile(ket, (3, 1)).astype(complex)
        jn = np.arange(3)[:, None] * self.basis[:, SITE]
        def rhs(t, flat):
            psi = flat.reshape(3, -1)
            return (-1j * (psi @ self.h3.T + pulse(t, rise, area, width)[0] * jn * psi)).ravel()
        end = width * rise
        step, tol = NUMERICS[resolution]
        sol = solve_ivp(rhs, (0., end), conditional.ravel(), method="DOP853",
                        t_eval=[end], max_step=step, rtol=tol*.01, atol=tol*.0001)
        if not sol.success:
            raise RuntimeError(sol.message)
        return sol.y[:, -1].reshape(3, -1)

    @lru_cache(maxsize=256)
    def run(self, rise, fidelity, resolution="standard", control=False, label=0, gain=GAIN,
            v0=1., area=AREA, width=WIDTH, threshold=THRESHOLD):
        """fidelity sets contact dephasing at nominal WIDTH for a fresh pointer.

        v0 is its initial off-diagonal visibility at contact, conditional on
        the known classical settings. Width perturbations leave kappa fixed.
        """
        if not 0 <= v0 <= 1 or not 1/3 < fidelity <= 1 or width <= 0 or area <= 0:
            raise ValueError("Invalid pointer visibility, dephasing calibration, width or area")
        step, tol = NUMERICS[resolution]
        eta = (3*fidelity - 1)/2
        kappa = -np.log(eta) / WIDTH
        start = width * rise
        psi = self.rise_state(rise, control, resolution, area, width)
        visibility = v0 * np.exp(-kappa * start)
        phase = np.exp(-2j*np.pi*label*np.arange(3)/3)
        pointer = np.outer(phase, phase.conj()) / 3
        pointer *= visibility + (1 - visibility)*np.eye(3)
        top = np.einsum("jk,jb,kc->jkbc", pointer, psi, psi.conj())
        initial = np.concatenate((np.zeros(self.offset[-2], complex), top.ravel()))
        noise = -kappa * self.dephase
        def rhs(t, flat):
            g, slope = pulse(t, rise, area, width)
            derivative = self.free @ flat + (g * self.drive + noise) * flat
            if gain and slope > 0:
                rate = gain * slope * max(0., self.conditional_entropy(flat) - threshold)
                if rate > 0:
                    derivative += rate * (self.loss @ flat)
            return derivative
        sol = solve_ivp(rhs, (start, width), initial, method="DOP853",
                        rtol=tol, atol=tol*.0003, max_step=step,
                        t_eval=np.linspace(start, width, 5))
        if not sol.success:
            raise RuntimeError(sol.message)
        checks = [self.stats(flat) for flat in sol.y.T]
        sectors = checks[-1][0]
        trace_error = max(s[1] for s in checks)
        hermiticity_error = max(s[2] for s in checks)
        min_eigenvalue = min(s[3] for s in checks)
        if trace_error > 1e-10 or hermiticity_error > 1e-10 or min_eigenvalue < -3e-8:
            raise ValueError("Density-matrix audit failed")
        return dict(p_loss=float(sectors[:3].sum()), mean_N=float(np.arange(4) @ sectors),
                    sectors=sectors.tolist(), max_trace_error=trace_error,
                    max_hermiticity_error=hermiticity_error, min_eigenvalue=min_eigenvalue)


def slow_high_margin(ring, samples=1025):
    """Trace the prospective loss-free fall using three wavefunctions.

    Local reductions contract trace distance. The Audenaert continuity bounds
    below control between-sample variation of the exact trajectory relative to
    its exact samples; the listed sample entropies themselves are numerical.
    """
    rise, f = PULSES["slow"], .99
    start = rise * WIDTH
    kappa = -np.log((3*f-1)/2) / WIDTH
    jn = np.arange(3)[:, None] * ring.basis[:, SITE]
    def rhs(t, flat):
        psi = flat.reshape(3, -1)
        return (-1j * (psi @ ring.h3.T + pulse(t, rise)[0] * jn * psi)).ravel()
    initial = ring.rise_state(rise, False, "fine")
    times = np.linspace(start, WIDTH, samples)
    sol = solve_ivp(rhs, (start, WIDTH), initial.ravel(), method="DOP853",
                    t_eval=times, max_step=.00025, rtol=2e-13, atol=2e-15)
    if not sol.success:
        raise RuntimeError(sol.message)
    values = []
    groups = [ring.basis[:, SITE] == n for n in range(4)]
    for t, flat in zip(times, sol.y.T):
        psi = flat.reshape(3, -1)
        blocks = np.array([psi[:, group] @ psi[:, group].conj().T for group in groups])
        visibility = np.exp(-kappa*t)
        blocks *= (visibility + (1 - visibility)*np.eye(3))/3
        values.append(cq_entropy(blocks))
    peak = int(np.argmax(values))
    # D(rho(t),rho(s)) <= (||H|| + kappa) |t-s| before first activation.
    # ||K n_1||=6. Pinching minus the identity changes D by at most one.
    velocity = float(np.linalg.norm(ring.h3, 2) + 6*(2*AREA/WIDTH) + kappa)
    d = velocity * (WIDTH-start)/(2*(samples-1))
    if not 0 < d < 2/3:
        raise ValueError("Grid too coarse for the entropy-continuity bound")
    variation = float(d*np.log(11*2) + 2*(entr(d)+entr(1-d)))
    return dict(samples=samples, sample_peak_t=float(times[peak]),
                sampled_max_C=values[peak], sampled_margin=THRESHOLD-values[peak],
                between_sample_bound=variation, margin_after_bound=THRESHOLD-values[peak]-variation)


def sensitivity_results(arms):
    """One-at-a-time perturbations for diagnostics; no parameters are estimated."""
    def summary(fidelity, **kwargs):
        rows = arms(fidelity, **kwargs)
        fast, slow = (rows[name]["p_loss"] for name in ("fast", "slow"))
        return dict(fast=fast, slow=slow, delta=fast-slow)

    cases = {}
    for name, value, kwargs in (
        ("F", -.002, {}), ("F", .002, {}),
        ("area_factor", .99, {"area": .99*AREA}), ("area_factor", 1.01, {"area": 1.01*AREA}),
        ("width_factor", .99, {"width": .99*WIDTH}), ("width_factor", 1.01, {"width": 1.01*WIDTH}),
        ("threshold_shift_nat", -.005, {"threshold": THRESHOLD-.005}),
        ("threshold_shift_nat", .005, {"threshold": THRESHOLD+.005}),
        ("initial_visibility_fixed_kappa", .995, {"v0": .995}),
        ("initial_visibility_fixed_end_fidelity", .995, {"v0": .995}),
    ):
        per_arm = {}
        for f in FIDELITIES:
            contact_fidelity = f
            if name == "F":
                contact_fidelity += value
            if name == "initial_visibility_fixed_end_fidelity":
                # Hold v0 exp(-kappa T)=(3 F - 1)/2 constant.
                contact_fidelity = (1 + (3*f-1)/value)/3
            per_arm[str(f)] = summary(contact_fidelity, **kwargs)
        cases.setdefault(name, []).append(dict(value=value, endpoints=per_arm))
    return cases


def physics_results():
    ring = Ring()
    def arms(fidelity, resolution="standard", **kwargs):
        return {name: ring.run(rise, fidelity, resolution, **kwargs)
                for name, rise in PULSES.items()}
    def difference(fidelity, resolution="standard"):
        pair = arms(fidelity, resolution)
        return pair["fast"]["p_loss"] - pair["slow"]["p_loss"]
    results = {str(f): arms(f) for f in FIDELITIES}
    null = {str(f): arms(f, control=True) for f in FIDELITIES}
    history = {str(f): {str(label): arms(f, label=label, v0=history_visibility(f)) for label in (0, 1)}
               for f in FIDELITIES}
    disabled = arms(.92, gain=0.)
    root = brentq(difference, .92, .99, xtol=1e-12)
    root_endpoints = arms(root)
    bracket = [dict(F=root + offset, delta=difference(root + offset, "fine"))
               for offset in (-2e-6, 2e-6)]
    fine_root = brentq(lambda f: difference(f, "fine"), bracket[0]["F"], bracket[1]["F"],
                       xtol=1e-12)
    grid = [dict(F=f, delta=difference(f)) for f in (.92, .93, .94, .95, .96, .97, .98, .99)]
    margin = slow_high_margin(ring)
    if margin["margin_after_bound"] <= 0:
        raise ValueError("High fidelity slow-pulse numerical no-trigger check failed")
    fine = {str(f): arms(f, "fine") for f in FIDELITIES}
    shifts = {key: max(abs(fine[str(f)][p][key] - results[str(f)][p][key])
                       for p in PULSES for f in FIDELITIES) for key in ("p_loss", "mean_N")}
    area = {name: quad(lambda t: pulse(t, rise)[0], 0., WIDTH, points=[rise*WIDTH])[0]
            for name, rise in PULSES.items()}
    if any(abs(value - AREA) > 2e-13 for value in area.values()):
        raise ValueError("Pulse area mismatch")
    # Before first activation only hopping can move |030000> across the
    # n1=3 boundary. With coupling norm ||Q H P|| = sqrt(3*(1**2+.65**2)),
    # |dq/dt| <= 2 ||Q H P|| sqrt(q(1-q)); integration from q(0)=0
    # gives the sine-squared bound through the present short write.
    # The three other occupation values have at most log(3) conditional entropy.
    null_escape = float(np.sin(WIDTH * np.sqrt(3 * (1 + .65**2)))**2)
    null_entropy = float(entr(null_escape) + entr(1-null_escape) + null_escape*np.log(3))
    if null_entropy >= THRESHOLD:
        raise ValueError("Occupation control bound is insufficient")
    if not bracket[0]["delta"] < 0 < bracket[1]["delta"]:
        raise ValueError("Refined solver did not confirm crossing bracket")
    if max(shifts.values()) > 3e-7:
        raise ValueError("Endpoint refinement failed")
    for f in FIDELITIES:
        for p in PULSES:
            if abs(null[str(f)][p]["p_loss"]) > 1e-11:
                raise ValueError("Occupation control fired")
            a, b = [history[str(f)][str(i)][p] for i in (0, 1)]
            if max(abs(a[k] - b[k]) for k in ("p_loss", "mean_N")) > 5e-8:
                raise ValueError("Pointer-symbol control failed")
            if a["p_loss"] <= 1e-5:
                raise ValueError("Pointer-symbol control lacks a loss signal")
    if max(abs(row["p_loss"]) for row in disabled.values()) > 1e-11:
        raise ValueError("Zero-gain control leaked particles")
    return dict(endpoints=results, F_star=root, at_crossing=root_endpoints,
                refined_sign_bracket=bracket, fine_F_star=fine_root, delta_F_grid=grid,
                fine_endpoints=fine, max_refinement_shift=shifts, pulse_integrals=area,
                null_030000=null, null_escape_probability_bound=null_escape,
                null_conditional_entropy_bound=null_entropy,
                prehistory=history, prehistory_v0={str(f): history_visibility(f) for f in FIDELITIES},
                slow_high_entropy_margin=margin, sensitivity=sensitivity_results(arms), zero_gain=disabled)


# Statistical calculations. Each count is the number of detected events.
from math import comb
from operator import index

import numpy as np
from scipy.stats import beta, binom, hypergeom


def _count(value, name):
    if isinstance(value, (bool, np.bool_)):
        raise ValueError(f"{name} must be a nonnegative integer")
    try:
        value = index(value)
    except TypeError as exc:
        raise ValueError(f"{name} must be a nonnegative integer") from exc
    if value < 0:
        raise ValueError(f"{name} must be a nonnegative integer")
    return value


def _observations(events, trials):
    events, trials = _count(events, "events"), _count(trials, "trials")
    if trials < 1 or events > trials:
        raise ValueError("expected 0 <= events <= trials with trials positive")
    return events, trials


def _exact_fisher_tail(x, n_high, y, n_low):
    """Integer hypergeometric sum for tails near the decision boundary."""
    total = x + y
    numerator = sum(comb(n_high, j) * comb(n_low, total - j)
                    for j in range(x, min(n_high, total) + 1))
    return numerator / comb(n_high + n_low, total)


def fisher_greater(x_high, n_high, x_low, n_low, alpha=0.05):
    """One-sided conditional Fisher p-value for p_high > p_low."""
    x_high, n_high = _observations(x_high, n_high)
    x_low, n_low = _observations(x_low, n_low)
    tail = float(hypergeom.sf(x_high - 1, n_high + n_low, x_high + x_low, n_high))
    if abs(tail - alpha) <= 1e-12:
        return _exact_fisher_tail(x_high, n_high, x_low, n_low)
    return tail


def contrast_interval(x_high, n_high, x_low, n_low, confidence=0.95):
    """Conservative two-sided interval for the observed risk difference.

    Subtract simultaneous Clopper-Pearson bounds on the two observed risks;
    their four one-sided noncoverage probabilities sum to 1-confidence.
    Covers a single prespecified contrast without assuming assay calibration.
    """
    x_high, n_high = _observations(x_high, n_high)
    x_low, n_low = _observations(x_low, n_low)
    if not 0 < confidence < 1:
        raise ValueError("confidence must lie inside (0, 1)")
    tail = (1 - confidence) / 4

    def limits(x, n):
        low = 0.0 if x == 0 else float(beta.ppf(tail, x, n - x + 1))
        high = 1.0 if x == n else float(beta.isf(tail, x + 1, n - x))
        return low, high

    lower_high, upper_high = limits(x_high, n_high)
    lower_low, upper_low = limits(x_low, n_low)
    return lower_high - upper_low, upper_high - lower_low


def fisher_power(n, p_high, p_low, alpha=0.05):
    """Unconditional rejection probability of the conditional one-sided test.

    Under independent binomial sampling, condition on each low-arm count y.
    At fixed y the Fisher tail is nonincreasing in x. Locate the smallest
    rejecting x (n+1 if absent), then sum its high-arm binomial upper tail.
    Low-arm counts outside the enumerated window have total mass <= 2e-14.
    """
    n = _count(n, "n")
    if n == 0 or not 0 < alpha < 1 or not (0 <= p_high <= 1 and 0 <= p_low <= 1):
        raise ValueError("expected positive n, alpha in (0, 1), and valid probabilities")
    tail = 1e-14
    y_min = int(binom.ppf(tail, n, p_low))
    y_max = int(binom.isf(tail, n, p_low))
    omitted = binom.cdf(y_min - 1, n, p_low) + binom.sf(y_max, n, p_low)
    if omitted > 2.01 * tail:
        raise ArithmeticError("binomial enumeration failed its omitted-mass bound")
    y = np.arange(y_min, y_max + 1)
    lo = np.zeros_like(y)
    hi = np.full_like(y, n + 1)
    while np.any(lo < hi):
        active = np.flatnonzero(lo < hi)
        mid = (lo[active] + hi[active]) // 2
        tails = hypergeom.sf(mid - 1, 2 * n, mid + y[active], n)
        for i in np.flatnonzero(np.abs(tails - alpha) <= 1e-12):
            tails[i] = _exact_fisher_tail(int(mid[i]), n, int(y[active[i]]), n)
        reject = tails <= alpha
        hi[active[reject]] = mid[reject]
        lo[active[~reject]] = mid[~reject] + 1
    return float(np.dot(binom.pmf(y, n, p_low), binom.sf(lo - 1, n, p_high)))


def design_results(p_H_fast, p_H_slow, p_L_fast, p_L_slow):
    """Evaluate the prespecified allocations at the supplied true risks."""
    if not all(0 <= p <= 1 for p in (p_H_fast, p_H_slow, p_L_fast, p_L_slow)):
        raise ValueError("all four true probabilities must lie in [0, 1]")
    result = {}
    designs = [(0.99, 269, 3545, 571, 3651), (0.98, 371, 3897, 766, 4056)]
    for d, n_h, n_l, n_joint_h, n_joint_l in designs:
        def observed(p):
            return (1 - d) + (2 * d - 1) * p

        h = (observed(p_H_fast), observed(p_H_slow))
        l = (observed(p_L_slow), observed(p_L_fast))

        def allocation(n_high, n_low):
            power_h = fisher_power(n_high, *h)
            power_l = fisher_power(n_low, *l)
            return dict(n_H=n_high, n_L=n_low, total_shots=2 * (n_high + n_low),
                        power_H=power_h, power_L=power_l, joint_power=power_h * power_l)

        component = allocation(n_h, n_l)
        result[f"{d:.2f}"] = {
            "observed_probabilities": dict(H_fast=h[0], H_slow=h[1], L_fast=l[1], L_slow=l[0]),
            "separate": component,
            "joint": allocation(n_joint_h, n_joint_l),
            "balanced_joint": allocation(n_l, n_l),
            "preceding_component_powers": dict(H=fisher_power(n_h - 1, *h), L=fisher_power(n_l - 1, *l)),
        }
    return result


def _simple_null_power_bound(n, high, low, alpha):
    """Bound the power of ANY size-alpha test with n trials in each arm.

    Use the simple common-rate null q, likelihood ratio R, and the bound
    E_alt[test] <= E_null[(R-s)_+] + s*alpha for any positive threshold s.
    A normal quantile only chooses s. The bound uses both binomial laws.
    A test using fewer trials can discard the rest, so the bound applies
    to all allocations with fewer equal-sized arms as well.
    """
    from scipy.special import logit, ndtri

    q = (high + low) / 2
    a, b = logit(high) - logit(q), logit(low) - logit(q)
    base = n * (np.log1p(-high) + np.log1p(-low) - 2 * np.log1p(-q))
    log_s = base + n * q * (a + b) + ndtri(1 - alpha) * np.sqrt(n * q * (1 - q) * (a*a + b*b))
    if log_s > 700:
        return 1.0
    y = np.arange(n + 1)
    threshold = np.floor((log_s - base - b*y) / a).astype(int)

    def exceed(first, second):
        return np.dot(binom.pmf(y, n, second), binom.sf(threshold, n, first))

    return float(exceed(high, low) + np.exp(log_s) * (alpha - exceed(q, q)))


def search_design(p_H_fast, p_H_slow, p_L_fast, p_L_slow, d):
    """Regenerate n at one calibration, independent of the fixed design table.

    Minimize total allocation, then maximize joint power among ties. Do not
    assume nonrandomized Fisher power is monotonic in integer sample size.
    """
    from functools import lru_cache

    target, alpha = 0.80, 0.05
    if not 0.5 < d < 1 or not (0 <= p_H_slow < p_H_fast <= 1 and 0 <= p_L_fast < p_L_slow <= 1):
        raise ValueError("search requires interior calibration and both predicted directions")

    def observed(p):
        return (1 - d) + (2*d - 1) * p

    def component(p_high, p_low):
        high, low = observed(p_high), observed(p_low)

        @lru_cache(maxsize=None)
        def power(n):
            return fisher_power(n, high, low, alpha)

        # Exclude a whole prefix using a more powerful simple-null test.
        # The small numerical cushion protects the comparison at the bound.
        lo, hi = 0, 1
        while _simple_null_power_bound(hi, high, low, alpha) < target - 1e-9:
            lo, hi = hi, 2*hi
        while hi - lo > 1:
            mid = (lo + hi) // 2
            if _simple_null_power_bound(mid, high, low, alpha) < target - 1e-9:
                lo = mid
            else:
                hi = mid
        first = lo + 1
        while power(first) < target:
            first += 1
        return first, power

    min_h, h_power = component(p_H_fast, p_H_slow)
    min_l, l_power = component(p_L_slow, p_L_fast)

    # Find any feasible upper bound on total, then exhaust its entire
    # feasible region. This initial probe only affects search speed.
    probe_h = 2 * min_h
    while h_power(probe_h) <= target:
        probe_h *= 2
    lo, hi = min_l - 1, min_l
    while h_power(probe_h) * l_power(hi) < target:
        lo, hi = hi, 2 * hi
    while hi - lo > 1:
        mid = (lo + hi) // 2
        if h_power(probe_h) * l_power(mid) >= target:
            hi = mid
        else:
            lo = mid
    cap = probe_h + hi
    hs = np.arange(min_h, cap - min_l + 1)
    hp = np.array([h_power(int(n)) for n in hs])
    best_h, best_l = probe_h, hi
    best_key = (cap, -h_power(best_h) * l_power(best_l))
    for nl in range(min_l, cap - min_h + 1):
        nh_count = min(len(hs), best_key[0] - nl - min_h + 1)
        if nh_count <= 0:
            break
        # At a fixed L, the first eligible H has the smallest total.
        eligible = np.flatnonzero(hp[:nh_count] * l_power(nl) >= target)
        if len(eligible):
            i = eligible[0]
            nh = int(hs[i])
            key = (nh + nl, -float(hp[i]) * l_power(nl))
            if key < best_key:
                best_key, best_h, best_l = key, nh, nl
    return dict(separate_n_H=min_h, separate_n_L=min_l, joint_n_H=best_h,
                joint_n_L=best_l, joint_power=-best_key[1])



# These are design acceptance tolerances, not measured calibration intervals.
PHYSICAL_WINDOWS = {"H_fast": (0.0375, 0.0397), "H_slow": (0.0, 0.0011),
                    "L_fast": (0.0991, 0.1014), "L_slow": (0.1188, 0.1211)}
CHANNEL_PROFILES = {
    "A": {"errors": (0.0, 0.011), "n_H": 2100, "n_L": 42000},
    "B": {"errors": (0.009, 0.021), "n_H": 2800, "n_L": 75000},
}
MISSING_LIMIT = 1


def _window(interval):
    if len(interval) != 2 or not 0 <= interval[0] <= interval[1] <= 1:
        raise ValueError("invalid probability interval")
    return tuple(map(float, interval))


def _contains(outer, inner):
    return outer[0] <= inner[0] <= inner[1] <= outer[1]


def channel_window(p, b, f):
    """q=(1-p)b+p(1-f); independent cell-specific envelopes."""
    p, b, f = map(_window, (p, b, f))
    values = [bb * (1 - pp) + (1 - ff) * pp for pp in p for bb in b for ff in f]
    return [min(values), max(values)]


def qualify_calibration(calibration):
    """Return first containing profile and frozen quantitative predictions."""
    if set(calibration) != set(PHYSICAL_WINDOWS):
        raise ValueError("require P,b,f calibration intervals for all four coded cells")
    for cell, values in calibration.items():
        if set(values) != {"P", "b", "f"}:
            raise ValueError("each calibration cell requires exactly P,b,f")
        for interval in values.values():
            _window(interval)
    for label, profile in CHANNEL_PROFILES.items():
        if all(_contains(PHYSICAL_WINDOWS[c], v["P"]) and
               all(_contains(profile["errors"], v[k]) for k in ("b", "f"))
               for c, v in calibration.items()):
            return label, {c: channel_window(v["P"], v["b"], v["f"]) for c, v in calibration.items()}
    return None, {}


def adverse_fisher_power(n, p_high, p_low, m=MISSING_LIMIT, alpha=0.05):
    """Power guaranteed against any pattern of up to m missing per arm.

    Worst adverse completion maps latent X,Y to max(X-m,0), min(Y+m,n).
    The binomial law below is for latent, fully observed detector outcomes.
    """
    from scipy.special import ndtri
    n, m = _count(n, "n"), _count(m, "m")
    if n < 1 or m > n or not 0 < alpha < .5 or not (0 <= p_high <= 1 and 0 <= p_low <= 1):
        raise ValueError("invalid adverse-power arguments")
    ymin, ymax = int(binom.ppf(1e-14, n, p_low)), int(binom.isf(1e-14, n, p_low))
    if binom.cdf(ymin - 1, n, p_low) + binom.sf(ymax, n, p_low) > 2.01e-14:
        raise ArithmeticError("binomial enumeration exceeded omitted-mass bound")
    y = np.arange(ymin, ymax + 1)
    adverse_y = np.minimum(n, y + m)
    # A continuity-corrected normal approximation supplies a starting count
    # only. Exact conditional tails determine and verify every boundary.
    z = ndtri(1 - alpha)
    diff = np.ones_like(y, dtype=float)
    for _ in range(4):
        total = np.minimum(2*n, 2*adverse_y + diff)
        diff = 1 + z * np.sqrt(total * (2*n-total) / (2*n-1))
    critical = np.minimum(n + 1, np.ceil(adverse_y + diff).astype(int))

    def reject(x, yy):
        result = np.zeros(x.shape, dtype=bool)
        result[x > n] = True  # artificial passing sentinel when no x rejects
        ii = np.flatnonzero((x >= 0) & (x <= n))
        tails = hypergeom.sf(x[ii]-1, 2*n, x[ii]+yy[ii], n)
        for j in np.flatnonzero(np.abs(tails - alpha) <= 1e-12):
            k = ii[j]
            tails[j] = _exact_fisher_tail(int(x[k]), n, int(yy[k]), n)
        result[ii] = tails <= alpha
        return result

    while True:
        left = reject(critical-1, adverse_y)
        right = reject(critical, adverse_y)
        if not np.any(left) and np.all(right):
            break
        critical[left] -= 1
        critical[~right] += 1
    latent_threshold = np.where(critical == 0, 0, critical + m)
    return float(np.dot(binom.pmf(y, n, p_low), binom.sf(latent_threshold - 1, n, p_high)))


def robust_designs():
    results = {}
    for label, profile in CHANNEL_PROFILES.items():
        err = profile["errors"]
        windows = {c: channel_window(p, err, err) for c, p in PHYSICAL_WINDOWS.items()}
        # Coordinatewise monotonicity of the adverse rejection event places
        # its minimum at these opposite corners even for unequal channels.
        h = adverse_fisher_power(profile["n_H"], windows["H_fast"][0], windows["H_slow"][1])
        l = adverse_fisher_power(profile["n_L"], windows["L_slow"][0], windows["L_fast"][1])
        joint = h*l
        if joint < 0.82 or h < .80 or l < .80:
            raise ArithmeticError("robust allocation fails its planning margin")
        results[label] = dict(n_H=profile["n_H"], n_L=profile["n_L"],
                              total_shots=2*(profile["n_H"]+profile["n_L"]),
                              errors=list(err), q=windows, power_H=h, power_L=l, joint_power=joint)
    return results


def robust_table(results):
    rows = ["| Profil | H na tvar | L na tvar | H + L spolu | Sila H | Sila L | Spoločná sila |",
            "|---|---:|---:|---:|---:|---:|---:|"]
    for label, r in results.items():
        values = [label, r["n_H"], r["n_L"], r["total_shots"]]
        values += [f"{r[k]:.6f}".replace(".", ",") for k in ("power_H", "power_L", "joint_power")]
        rows.append("| " + " | ".join(map(str, values)) + " |")
    return "\n".join(rows)


def cp_envelope(loss, missing, assigned, confidence=.9875):
    """Pointwise extremes of exact intervals over every possible completion."""
    x, n = _observations(loss, assigned)
    m = _count(missing, "missing")
    if x + m > n or not 0 < confidence < 1:
        raise ValueError("invalid completion or confidence")
    alpha = (1-confidence)/2
    lower = 0.0 if x == 0 else float(beta.ppf(alpha, x, n-x+1))
    upper = 1.0 if x+m == n else float(beta.isf(alpha, x+m+1, n-x-m))
    return [lower, upper]


def score_blinded(plan, h_counts, load_l=None):
    """Score locked H, then open the escrowed L aggregate only after a pass.

    plan contains profile, calibration, codebook, qualified. A stage aggregate
    is indexed by its two opaque codebook values. Each row contains assigned,
    loss and missing. load_l is a callable reading the separate L file.
    """
    profile, predicted = qualify_calibration(plan["calibration"])
    if profile is None or profile != plan["profile"]:
        raise ValueError("preselected profile is not the first eligible calibration profile")
    codes = plan["codebook"]
    if (set(codes) != set(PHYSICAL_WINDOWS) or not all(isinstance(c,str) and c.strip() for c in codes.values())
            or len(set(codes.values())) != 4):
        raise ValueError("codebook must map each cell to its own nonempty blind label")
    gates = plan["qualified"]
    if set(gates) != {"H","L"} or not all(type(v) is bool for v in gates.values()):
        raise ValueError("explicit blinded qualification disposition required for both stages")

    def score(stage, counts):
        high, low = (("H_fast", "H_slow") if stage == "H" else ("L_slow", "L_fast"))
        if set(counts) != {codes[high], codes[low]}:
            raise ValueError(f"expected only the two locked {stage} labels")
        rows, reasons = {}, []
        if not gates[stage]:
            reasons.append("qualification_failed")
        for cell in (high, low):
            row = counts[codes[cell]]
            if set(row) != {"assigned", "loss", "missing"}:
                raise ValueError("stage rows require assigned, loss, missing")
            x, n = _observations(row["loss"], row["assigned"])
            m = _count(row["missing"], "missing")
            ci = cp_envelope(x, m, n)
            bounds = predicted[cell]
            if n != CHANNEL_PROFILES[profile]["n_"+stage]:
                reasons.append(cell + "_wrong_denominator")
            if m > MISSING_LIMIT:
                reasons.append(cell + "_excess_missing")
            rows[cell] = dict(assigned=n, loss=x, missing=m, cp9875=ci, predicted=bounds)
        a,b = rows[high], rows[low]
        x,n,m = a["loss"], a["assigned"], a["missing"]
        y,k,r = b["loss"], b["assigned"], b["missing"]
        pg = fisher_greater(x, n, y+r, k)
        po = fisher_greater(y, k, x+m, n, alpha=.025)
        rd_low = contrast_interval(x,n,y+r,k)[0]
        rd_high = contrast_interval(x+m,n,y,k)[1]
        hi_channel, lo_channel = (plan["calibration"][key] for key in (high, low))
        delta = max(0.0, hi_channel["b"][1] - lo_channel["b"][0],
                    lo_channel["f"][1] - hi_channel["f"][0])
        for row in rows.values():
            lo,hi = row["cp9875"]
            left,right = row["predicted"]
            row["quantitative_contradiction"] = (hi < left or lo > right) if not reasons else None
        return dict(eligible=not reasons, reasons=reasons, cells=rows, high=high, low=low,
                    p_direction=pg, p_opposite=po, risk_difference_range=[x/n-(y+r)/k, (x+m)/n-y/k],
                    risk_difference_ci95=[rd_low, rd_high], directional_pass=not reasons and pg <= .05,
                    channel_bias_upper=delta, exceeds_channel_bias=(rd_low > delta) if not reasons else None,
                    opposite_contradiction=po <= .025 if not reasons else None)

    h = score("H", h_counts)
    out = dict(profile=profile, H=h, L=None, joint_direction=None)
    if not h["directional_pass"]:
        out.update(status="L_NOT_OPENED", joint_direction=False)
    elif load_l is None:
        out.update(status="AWAIT_L")
    else:
        out["L"] = score("L", load_l())
        out.update(status="SCORED", joint_direction=out["L"]["directional_pass"])
    return out


def statistical_self_check():
    # Exhaust all latent tables for small n, including the p=0.05 exact tie.
    for n in (3, 8):
        for m in (0, 1):
            p, q = .73, .15
            expected = 0.0
            for x in range(n+1):
                for y in range(n+1):
                    a, b = max(0,x-m), min(n,y+m)
                    if _exact_fisher_tail(a,n,b,n) <= .05:
                        expected += binom.pmf(x,n,p) * binom.pmf(y,n,q)
            if abs(adverse_fisher_power(n,p,q,m) - expected) > 1e-12:
                raise ArithmeticError("adverse Fisher enumeration vs full tables")
    calibration = {c: dict(P=list(p), b=[.0095,.0105], f=[.0095,.0105])
                   for c,p in PHYSICAL_WINDOWS.items()}
    plan = dict(profile="A", calibration=calibration, codebook={c:f"c{i}" for i,c in enumerate(calibration)},
                qualified=dict(H=True, L=True))
    codes = plan["codebook"]

    def rows(stage, fast, slow, missing=0):
        return {codes[stage+"_"+shape]:dict(assigned=CHANNEL_PROFILES["A"]["n_"+stage],
                                             loss=x, missing=missing)
                for shape,x in (("fast",fast),("slow",slow))}

    def unopened():
        raise AssertionError("L escrow opened after failed H")

    if score_blinded(plan,rows("H",30,50),unopened)["status"] != "L_NOT_OPENED":
        raise ArithmeticError("H direction gate")
    if score_blinded(plan,rows("H",180,0,2),unopened)["H"]["eligible"]:
        raise ArithmeticError("H missingness gate")
    trial = score_blinded(plan,rows("H",100,20,1),lambda:rows("L",4400,5600,1))
    if not trial["joint_direction"] or trial["L"]["p_opposite"] < .025:
        raise ArithmeticError("independent L direction and observed scoring")
    if any(abs(trial[stage]["channel_bias_upper"] - .001) > 1e-12 or
           not trial[stage]["exceeds_channel_bias"] for stage in ("H", "L")):
        raise ArithmeticError("Secondary calibration-bias bound for the scored fixture")
    if not trial["L"]["cells"]["L_slow"]["quantitative_contradiction"]:
        raise ArithmeticError("disjoint simultaneous CP envelope")
    marginal = cp_envelope(0,1,20)
    if marginal != [0.0,cp_envelope(1,0,20)[1]] or cp_envelope(19,1,20)[1] != 1:
        raise ArithmeticError("completion interval endpoints")
    for v in calibration.values():
        v.update(b=[.014,.016], f=[.014,.016])
    if qualify_calibration(calibration)[0] != "B":
        raise ArithmeticError("fallback profile at intermediate calibration")
    calibration["H_fast"]["b"] = [.020,.023]
    if qualify_calibration(calibration)[0] is not None:
        raise ArithmeticError("out-of-profile cell calibration")


"""Blinded qualification of interleaved controls; count events are detected N<3."""
from itertools import combinations
from operator import index

from scipy.stats import beta


def control_gate(rows):
    """Rows: epoch (1/2), family, F (H/L or '-'), shape, n, events, missing."""
    sizes = {"reference": 8192, "null": 8192, "sham": 4096, "pre0": 2048, "pre1": 2048}
    keys = [(e, "reference", "-", "-") for e in (1, 2)]
    keys += [(e, family, f, shape) for e in (1, 2) for family in list(sizes)[1:]
             for f in ("H", "L") for shape in ("fast", "slow")]
    bounds = {}
    tail = 0.05 / (2 * len(keys))
    for row in rows:
        key = (row["epoch"], row["family"], row["F"], row["shape"])
        if key not in keys or key in bounds or isinstance(row["epoch"], bool):
            raise ValueError("unexpected or duplicate control cell")
        vals = [row[field] for field in ("n", "events", "missing")]
        if any(isinstance(v, bool) for v in vals):
            raise ValueError("integer counts required")
        n, events, missing = map(index, vals)
        if n != sizes[key[1]] or min(events, missing) < 0 or events + missing > n:
            raise ValueError("invalid sample size or event/missing count")
        hi = events + missing
        lower = 0.0 if events == 0 else float(beta.ppf(tail, events, n - events + 1))
        upper = 1.0 if hi == n else float(beta.isf(tail, hi + 1, n - hi))
        bounds[key] = (lower, upper)
    if set(keys) != set(bounds):
        raise ValueError("incomplete control panel")

    checks = []

    def compare(left, right, margin):
        low = bounds[left][0] - bounds[right][1]
        high = bounds[left][1] - bounds[right][0]
        checks.append({"left": list(left), "right": list(right), "interval": [low, high],
                       "margin": margin, "pass": low >= -margin and high <= margin})

    for e in (1, 2):
        ref = (e, "reference", "-", "-")
        for family, margin in (("null", 0.018), ("sham", 0.025)):
            cells = [k for k in keys if k[0] == e and k[1] == family]
            for key in cells:
                compare(key, ref, margin)
            for left, right in combinations(cells, 2):
                compare(left, right, margin)
        for f in ("H", "L"):
            for shape in ("fast", "slow"):
                compare((e, "pre0", f, shape), (e, "pre1", f, shape), 0.10)
    for key in keys:
        if key[0] == 1:
            family = key[1]
            margin = 0.10 if family.startswith("pre") else (0.025 if family == "sham" else 0.018)
            compare(key, (2, *key[1:]), margin)

    return {"eligible_controls": all(item["pass"] for item in checks),
            "control_trials": 2 * (8192 + 4 * (8192 + 4096 + 2048 + 2048)),
            "contrasts": checks}


def control_gate_simulation(prehistory, d, trials=20000):
    """Conditional, ideal-control planning scenario, independent from main data."""
    import numpy as np

    rng = np.random.Generator(np.random.PCG64(20261121))
    rows, intervals = [], {}
    for e in (1, 2):
        for family, n in (("reference", 8192), ("null", 8192), ("sham", 4096),
                          ("pre0", 2048), ("pre1", 2048)):
            settings = ([("-", "-")] if family == "reference" else
                        [(f, shape) for f in ("H", "L") for shape in ("fast", "slow")])
            for f, shape in settings:
                p = 0.0
                if family.startswith("pre"):
                    p = prehistory[{"H": "0.99", "L": "0.92"}[f]]["0"][shape]["p_loss"]
                q = (1 - d) + (2*d - 1)*p
                draws = rng.binomial(n, q, trials)
                values, inverse = np.unique(draws, return_inverse=True)
                tail = 0.05/68
                lower = np.where(values == 0, 0, beta.ppf(tail, values, n-values+1))
                upper = np.where(values == n, 1, beta.isf(tail, values+1, n-values))
                intervals[e, family, f, shape] = (lower[inverse], upper[inverse])
                rows.append(dict(epoch=e, family=family, F=f, shape=shape, n=n,
                                 events=round(n*q), missing=0))
    eligible = np.ones(trials, dtype=bool)
    for item in control_gate(rows)["contrasts"]:
        al, au = intervals[tuple(item["left"])]
        bl, bu = intervals[tuple(item["right"])]
        eligible &= (al-bu >= -item["margin"]) & (au-bl <= item["margin"])
    return {"trials": trials, "qualified": int(eligible.sum()), "d": d}


def protocol_tables(physics, designs):
    def fmt(x, digits):
        return f"{x:.{digits}f}".replace(".", ",")

    endpoints = ["| Rameno registra | P(strata) 10/90 | P(strata) 90/10 | Priemer N 10/90 | Priemer N 90/10 |",
                 "|---|---:|---:|---:|---:|"]
    for key, label in [("0.99", "H"), ("0.92", "L")]:
        pair = physics["endpoints"][key]
        cells = [fmt(pair[shape][name], 8 if name == "p_loss" else 7)
                 for name in ("p_loss", "mean_N") for shape in ("fast", "slow")]
        endpoints.append("| " + " | ".join([label] + cells) + " |")
    root = physics["at_crossing"]["fast"]["p_loss"]
    endpoints.extend(["", f"Modelový priesečník je pri F = {fmt(physics['F_star'], 8)}. "
                       f"Spoločná pravdepodobnosť straty je {fmt(root, 8)}."])
    allocations = ["| Presnosť d | H samostatne | L samostatne | H spoločne | L spoločne | Celkom spoločne | Spoločná sila |",
                   "|---|---:|---:|---:|---:|---:|---:|"]
    for key, design in designs.items():
        individual, joint = design["separate"], design["joint"]
        cells = [key.replace(".", ","), individual["n_H"], individual["n_L"], joint["n_H"],
                 joint["n_L"], joint["total_shots"], fmt(joint["joint_power"], 6)]
        allocations.append("| " + " | ".join(map(str, cells)) + " |")
    observed = ["| Presnosť d | H 10/90 | H 90/10 | L 10/90 | L 90/10 |",
                "|---|---:|---:|---:|---:|"]
    for key, design in designs.items():
        rates = design["observed_probabilities"]
        cells = [key.replace(".", ",")] + [fmt(rates[label], 5)
                for label in ("H_fast", "H_slow", "L_fast", "L_slow")]
        observed.append("| " + " | ".join(cells) + " |")
    return {"endpoints": "\n".join(endpoints), "readout": "\n".join(observed),
            "design": "\n".join(allocations)}


def compare_result(value, recorded, path="results"):
    """Compare the independent rerun to the sealed predictions, allowing numerical solver noise."""
    if isinstance(value, dict):
        if not isinstance(recorded, dict) or value.keys() != recorded.keys():
            raise ValueError(f"Schema mismatch at {path}")
        for key, child in value.items():
            compare_result(child, recorded[key], f"{path}.{key}")
    elif isinstance(value, list):
        if not isinstance(recorded, list) or len(value) != len(recorded):
            raise ValueError(f"Array mismatch at {path}")
        for i, child in enumerate(value):
            compare_result(child, recorded[i], f"{path}[{i}]")
    elif isinstance(value, float):
        if not np.isclose(value, recorded, rtol=1e-9, atol=2e-9):
            raise ValueError(f"Numerical mismatch at {path}: {value} vs {recorded}")
    elif value != recorded:
        raise ValueError(f"Mismatch at {path}: {value} vs {recorded}")


def verify_diagnostic_text(document, physics, gate_simulations):
    """Check rounded physics diagnostics and the seeded control-study counts in the protocol."""
    def number(value, places):
        return f"{value:.{places}f}".replace(".", ",").replace("-", "−")

    expected = [number(physics["null_conditional_entropy_bound"], 5)]
    margin = physics["slow_high_entropy_margin"]
    expected.extend(number(margin[key], 8) for key in (
        "sampled_max_C", "sampled_margin", "between_sample_bound", "margin_after_bound"))
    for f in ("0.99", "0.92"):
        expected.append(number(physics["prehistory_v0"][f], 6))
        expected.extend(number(physics["prehistory"][f]["0"][shape]["p_loss"], 8)
                        for shape in ("fast", "slow"))
    for key in ("F", "area_factor", "width_factor", "threshold_shift_nat"):
        for f in ("0.99", "0.92"):
            expected.append(" / ".join(number(case["endpoints"][f]["delta"], 5)
                                       for case in physics["sensitivity"][key]))
    for key in ("initial_visibility_fixed_kappa", "initial_visibility_fixed_end_fidelity"):
        case = physics["sensitivity"][key][0]
        for f in ("0.99", "0.92"):
            expected.append(" / ".join(number(case["endpoints"][f][shape], 5)
                                       for shape in ("fast", "slow")))
    for study in gate_simulations.values():
        expected.append(f"{study['qualified']:,}".replace(",", " "))
    plain = document.replace("{,}", ",")
    for literal in expected:
        if literal not in plain:
            raise ValueError(f"Reported diagnostic does not match calculation: {literal}")


def main():
    import argparse
    import json
    from pathlib import Path

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, help="write computed JSON (stdout by default)")
    parser.add_argument("--verify", type=Path, help="compare fresh calculations with this JSON")
    parser.add_argument("--protocol", type=Path, help="check computed result tables in this protocol")
    parser.add_argument("--controls", type=Path, help="score the unopened main study's interleaved control panel")
    parser.add_argument("--score-plan", type=Path, help="load the precommitted main-study calibration and codebook")
    parser.add_argument("--stage-h", type=Path, help="H counts, kept in a separate file from L")
    parser.add_argument("--stage-l", type=Path, help="escrowed L counts, read only after a passing H decision")
    parser.add_argument("--search-designs", action="store_true",
                        help="also independently regenerate the sample sizes by integer search")
    args = parser.parse_args()
    def load_json(path):
        return json.loads(path.read_text(encoding="utf-8"))

    if any((args.controls, args.score_plan, args.stage_h, args.stage_l)):
        if any((args.output, args.verify, args.protocol, args.search_designs)):
            parser.error("Scoring and theoretical reproduction are separate operations")
        if args.controls is None:
            parser.error("Scoring requires an independent control panel")
        controls = control_gate(load_json(args.controls))
        if args.score_plan is None:
            if args.stage_h or args.stage_l:
                parser.error("Stage files require a locked plan")
            print(json.dumps(controls, indent=2, allow_nan=False))
            return
        if args.stage_h is None:
            parser.error("Scoring a main study requires --stage-h")
        if not controls["eligible_controls"]:
            print(json.dumps({"status": "CONTROL_GATE_FAILED", "controls": controls}, allow_nan=False))
            return
        plan = load_json(args.score_plan)
        if set(plan["qualified"]) != {"H", "L"} or not all(type(v) is bool for v in plan["qualified"].values()):
            raise ValueError("The locked blind qualification must be supplied for H and L")
        if not all(plan["qualified"].values()):
            print(json.dumps({"status": "BLIND_QUALIFICATION_FAILED"}))
            return
        result = score_blinded(plan, load_json(args.stage_h),
                               (lambda: load_json(args.stage_l)) if args.stage_l else None)
        print(json.dumps(result, indent=2, allow_nan=False))
        return
    physics = physics_results()
    risk = physics["endpoints"]
    inputs = [risk[f][p]["p_loss"] for f in ("0.99", "0.92") for p in ("fast", "slow")]
    designs = design_results(*inputs)
    if args.search_designs:
        for key, design in designs.items():
            found = search_design(*inputs, float(key))
            for section in ("separate", "joint"):
                for arm in ("H", "L"):
                    if found[f"{section}_n_{arm}"] != design[section][f"n_{arm}"]:
                        raise ValueError(f"Allocation search disagrees at {key}/{section}/{arm}")
    for d in designs.values():
        if min(d["separate"]["power_H"], d["separate"]["power_L"], d["joint"]["joint_power"]) < .8:
            raise ValueError("A selected design misses its nominal power target")
    robust = robust_designs()
    statistical_self_check()
    result = {"protocol": "ITHKOR-v9-ASYM-1.0.0", "physics": physics, "statistics": designs,
              "operational_design": robust,
              "control_gate_simulation": {str(d): control_gate_simulation(physics["prehistory"], d)
                                          for d in (.99, .98)}}
    if args.verify:
        compare_result(result, json.loads(args.verify.read_text(encoding="utf-8")))
    if args.protocol:
        document = args.protocol.read_text(encoding="utf-8")
        verify_diagnostic_text(document, physics, result["control_gate_simulation"])
        tables = protocol_tables(physics, designs)
        tables["robust"] = robust_table(robust)
        for name, table in tables.items():
            section = f"<!-- generated:{name} -->\n{table}\n<!-- /generated:{name} -->"
            if document.count(section) != 1:
                raise ValueError(f"Protocol table does not match computed numbers: {name}")
    if args.output:
        args.output.write_text(json.dumps(result, indent=2, allow_nan=False) + "\n",
                               encoding="utf-8", newline="\n")
    elif args.verify or args.protocol:
        print("Recomputed physics, controls, statistical design and requested comparisons: PASS")
    else:
        print(json.dumps(result, indent=2, allow_nan=False))


if __name__ == "__main__":
    main()
