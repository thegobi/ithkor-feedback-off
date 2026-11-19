"""Exact pulse, cut and number-conserving propagators; no measurement draws."""
import json
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "2026-11-19-bhm-preparation-clock"))
from predict import prepare, v

CAP = 1.0356792825076628
PULSE = 0.30
START = prepare("210000")
N0 = np.array([x[0] for x in v.ring.BASIS])


def propagator(h):
    eig, vec = np.linalg.eigh(h)

    def advance(s, dt):
        return vec @ (np.exp(-1j*eig*dt) * (vec.T @ s))
    return advance


opened = propagator(v.H_OPEN)
closed = propagator(v.H_CUT)


def path(sign, tau):
    """Both arms receive the pulse, also when a comparison clock closes first."""
    phase = np.exp(1j * sign * np.pi/2 * N0)
    events = [(PULSE, "pulse")]
    if tau is not None:
        events.append((tau, "cut"))
    events.sort()
    segments = [(0., START, opened)]
    for t, action in events:
        prev, state, advance = segments[-1]
        state = advance(state, t-prev)
        if action == "pulse":
            state = phase*state
        else:
            advance = closed
        segments.append((t, state, advance))

    def at(t):
        for prev, state, advance in reversed(segments):
            if prev <= t:
                return advance(state, t-prev)
        raise ValueError("Negative time")
    return at


if __name__ == "__main__":
    results = {}
    for sign in (0, 1, -1):
        free = path(sign, None)
        tau = v.first_crossing(free, CAP, 0.005)
        assert abs(v.first_crossing(free, CAP, 0.001) - tau) < 1e-11
        assert tau > PULSE
        results[str(sign)] = tau
    print(json.dumps(results, indent=2))
