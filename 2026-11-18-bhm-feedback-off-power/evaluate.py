"""Blinded fixed-sample analysis of the two BHM timing windows. Standard library only."""

import argparse
from collections import Counter
from fractions import Fraction
from hashlib import sha256
import json
from math import comb, hypot, sqrt
import os
from pathlib import Path
from random import Random
import re
import sys
from tempfile import NamedTemporaryFile


N = 280
END_TICK = 2500000
GATES = {"early": (375000, 425000), "late": (525000, 575000)}
SEED = "ithkor-feedback-off-sham-v1"
HERE = Path(__file__).resolve().parent


def require(condition, message):
    if not condition:
        raise ValueError(message)


def unique_fields(pairs):
    result = {}
    for field, value in pairs:
        require(field not in result, f"duplicate JSON field: {field}")
        result[field] = value
    return result


def digest(data):
    return sha256(data).hexdigest()


def json_bytes(obj):
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), allow_nan=False).encode("utf-8")


def read_trials(data, fields):
    rows = {}
    for number, line in enumerate(data.decode("utf-8-sig").splitlines(), 1):
        row = json.loads(line, object_pairs_hook=unique_fields)
        require(isinstance(row, dict) and set(row) == fields, f"unexpected fields in row {number}")
        trial = row["id"]
        require(isinstance(trial, str) and re.fullmatch(r"[a-zA-Z0-9_-]{1,100}", trial),
                f"invalid id in row {number}")
        require(trial not in rows, f"duplicate id: {trial}")
        rows[trial] = row
    require(len(rows) == 2 * N, f"expected exactly {2*N} unique trials")
    return rows


def gate(tick):
    for name, (start, stop) in GATES.items():
        if start <= tick < stop:
            return name
    return "outside"


def endpoint(row, latency):
    ticks = row["click_ticks"]
    end = row["recorded_until_tick"]
    require(type(end) is int and end >= END_TICK + latency, f"incomplete recording: {row['id']}")
    require(isinstance(ticks, list) and all(type(t) is int and 0 <= t <= end for t in ticks),
            f"invalid raw click times: {row['id']}")
    times = sorted(t - latency for t in ticks if latency <= t <= END_TICK + latency)
    first = next((t for t in times if gate(t) != "outside"), None)
    return (first, times[0] if times else None)


def sham_symbol(trial, symbol):
    require(symbol is None or (type(symbol) is int and 0 <= symbol <= 2),
            f"invalid register symbol: {trial}")
    rng = Random(f"{SEED}/{trial}")
    if symbol is not None and rng.randrange(197) < 14:
        return (symbol + rng.randrange(1, 3)) % 3
    return symbol


def blind(raw, key_hash, latency, kind):
    require(re.fullmatch("[0-9a-f]{64}", key_hash), "invalid key SHA-256")
    require(type(latency) is int and latency >= 0, "invalid latency")
    require(kind in ("synthetic", "hardware"), "invalid data kind")
    rows = read_trials(raw, {"id", "symbol", "click_ticks", "recorded_until_tick"})
    outcomes = {}
    symbols = {}
    for trial, row in rows.items():
        changed = sham_symbol(trial, row["symbol"])
        outcomes[trial] = endpoint(row, latency)
        require(endpoint({**row, "symbol": changed}, latency) == outcomes[trial],
                f"sham changed atomic timing: {trial}")
        symbols[trial] = (row["symbol"], changed)
    lock = {
        "schema": "ithkor-feedback-off-first-in-gates-v1", "data_kind": kind,
        "raw_sha256": digest(raw), "key_sha256": key_hash,
        "evaluator_sha256": digest(Path(__file__).read_bytes()),
        "protocol_sha256": digest((HERE / "PROTOCOL.sk.md").read_bytes()),
        "latency_ticks": latency, "gates_half_open_ticks": GATES,
        "ticks_per_time_unit": 1000000, "sham_seed": SEED,
        "trials": len(rows), "outcomes_sha256": digest(json_bytes(outcomes)),
        "symbol_pairs_sha256": digest(json_bytes(symbols)),
    }
    return lock, outcomes, symbols


def contrast(a, b):
    total = a + b
    numerator = sum(comb(N, k) * comb(N, total-k) for k in range(a, min(N, total) + 1))
    p = Fraction(numerator, comb(2*N, total))
    x, y = a/N, b/N
    z = 1.959963984540054

    def wilson(v):
        center = v + z*z / (2*N)
        radius = z * sqrt(v*(1-v)/N + z*z/(4*N*N))
        return [(center-radius)/(1+z*z/N), (center+radius)/(1+z*z/N)]

    xl, xu = wilson(x)
    yl, yu = wilson(y)
    return {"counts": [a, b], "fractions": [x, y], "difference": x-y,
            "difference_ci95_newcombe": [x-y-hypot(x-xl, yu-y), x-y+hypot(xu-x, y-yl)],
            "p_one_sided": float(p), "reject_at_0.05": p <= Fraction(1, 20)}


def summarize(outcomes, arms, index):
    outside = "outside_only" if index == 0 else "first_outside"
    counts = {arm: dict.fromkeys(("early", "late", outside, "no_click"), 0)
              for arm in ("L", "H")}
    times = {arm: Counter() for arm in counts}
    for trial, (selected, first) in outcomes.items():
        tick = (selected, first)[index]
        category = "no_click" if first is None else outside
        if tick is not None:
            category = gate(tick)
            if category == "outside":
                category = outside
        arm = arms[trial]
        counts[arm][category] += 1
        if tick is not None:
            times[arm][tick] += 1
    tests = {"early_L_minus_H": contrast(counts["L"]["early"], counts["H"]["early"]),
             "late_H_minus_L": contrast(counts["H"]["late"], counts["L"]["late"])}
    return {"counts": counts, "first_tick_histograms": times, "directional_tests": tests,
            "both_directions_pass": all(t["reject_at_0.05"] for t in tests.values())}


def evaluate(raw, key, frozen):
    key_hash = digest(key)
    require(key_hash == frozen["key_sha256"], "assignment key differs from commitment")
    lock, outcomes, symbols = blind(raw, key_hash, frozen["latency_ticks"], frozen["data_kind"])
    require(json_bytes(lock) == json_bytes(frozen), "blinded lock mismatch")
    rows = read_trials(key, {"id", "arm"})
    arms = {trial: row["arm"] for trial, row in rows.items()}
    require(arms.keys() == outcomes.keys(), "trial IDs differ between input and key")
    require(Counter(arms.values()) == {"L": N, "H": N}, "expected 280 L and 280 H trials")
    transitions = Counter(symbols[t] for t in arms if arms[t] == "H")
    changed = sum(n for (a, b), n in transitions.items() if a != b)
    return {"lock": lock, "n_per_arm": N, "primary_first_in_windows": summarize(outcomes, arms, 0),
            "sensitivity_first_from_start": summarize(outcomes, arms, 1),
            "paired_H_sham": {"matched_atomic_endpoints": N, "flip_probability": "14/197",
                              "changed": changed, "perturbation_exercised": changed > 0,
                              "symbol_order": [0, 1, 2, None],
                              "transitions": [[transitions[a,b] for b in (0,1,2,None)]
                                              for a in (0,1,2,None)]}}


def save_new(path, result):
    with NamedTemporaryFile(dir=path.parent, delete=False) as tmp:
        temporary = Path(tmp.name)
    try:
        temporary.write_text(json.dumps(result, sort_keys=True, indent=2, allow_nan=False) + "\n",
                             encoding="utf8")
        os.link(temporary, path)
    finally:
        temporary.unlink(missing_ok=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    freeze = commands.add_parser("freeze")
    freeze.add_argument("--key-sha256", required=True)
    freeze.add_argument("--latency-ticks", required=True, type=int)
    freeze.add_argument("--kind", required=True, choices=["synthetic", "hardware"])
    report = commands.add_parser("report")
    report.add_argument("--key", type=Path, required=True)
    report.add_argument("--lock", type=Path, required=True)
    report.add_argument("--lock-sha256", required=True)
    for command in (freeze, report):
        command.add_argument("--raw", type=Path, required=True)
        command.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    raw = args.raw.read_bytes()
    if args.command == "freeze":
        result, _, _ = blind(raw, args.key_sha256, args.latency_ticks, args.kind)
    else:
        lock_bytes = args.lock.read_bytes()
        require(digest(lock_bytes) == args.lock_sha256, "lock differs from recorded commitment")
        frozen = json.loads(lock_bytes.decode("utf8"), object_pairs_hook=unique_fields)
        result = evaluate(raw, args.key.read_bytes(), frozen)
        result["lock_sha256"] = args.lock_sha256
    save_new(args.out, result)


if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError, KeyError, TypeError) as error:
        sys.exit(f"Evaluation stopped: {error}")
