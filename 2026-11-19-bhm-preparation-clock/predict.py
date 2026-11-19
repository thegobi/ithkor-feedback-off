"""Predict event times using just the open ring, without current readout."""
import json
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
VALVE = HERE.parent / "2026-11-19-bhm-boundary-valve"
sys.path.insert(0, str(VALVE))
import boundary_valve as v


def prepare(digits):
    state = np.zeros(len(v.ring.BASIS))
    state[v.ring.INDEX[tuple(map(int, digits))]] = 1
    return state


def event(free, cap, step):
    try:
        return v.first_crossing(free, cap, step)
    except ValueError as e:
        if str(e) != "No crossing in the observation window":
            raise
        return None


if __name__ == "__main__":
    baseline = json.loads((VALVE / "results.json").read_text(encoding="utf-8-sig"))
    settings = {}
    for name, row in baseline["settings"].items():
        cap = row["cap"]
        timer = row["hard"]["first_crossing"]
        times = {}
        for prep in ("300000", "210000", "111000"):
            free = v.trajectory(v.H_OPEN, prepare(prep))
            tau = event(free, cap, 0.005)
            other = event(free, cap, 0.001)
            assert tau == other or (tau is not None and other is not None and abs(tau-other) < 1e-11)
            times[prep] = tau
        assert abs(times["300000"] - timer) < 1e-12
        settings[name] = dict(cap=cap, timer=timer, threshold_times=times)
    print(json.dumps(settings, indent=2, allow_nan=False))
