"""Deterministic synthetic trial log and end-to-end regression checks."""

import json
from pathlib import Path
from random import Random
import subprocess
import sys
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch

import evaluate as ev
from power import critical_count


def synthetic_inputs(null=False):
    assignments = ["L", "H"] * ev.N
    Random(819).shuffle(assignments)
    raw, key = [], []
    seen = {"L": 0, "H": 0}
    for i, arm in enumerate(assignments):
        trial = f"x{i:03}"
        j = seen[arm]
        seen[arm] += 1
        if j < 16:
            ticks = [120000, 400000] if null or arm == "L" else [120000, 550000]
        elif j == 16:
            ticks = [550000] if null or arm == "L" else [400000]
        else:
            ticks = []
        raw.append({"id": trial, "symbol": None if j == 30 else j % 3,
                    "click_ticks": ticks, "recorded_until_tick": ev.END_TICK})
        key.append({"id": trial, "arm": arm})
    return tuple(b"".join(ev.json_bytes(row) + b"\n" for row in rows) for rows in (raw, key))


class TestEvaluator(unittest.TestCase):
    def test_edges_latency_and_missing_acquisition(self):
        def read(*ticks):
            return ev.endpoint({"id":"x","click_ticks":list(ticks),"recorded_until_tick":2500010}, 10)
        self.assertEqual(read(9, 2500010), (None, ev.END_TICK))
        self.assertEqual(read(100, 375010, 525010), (375000, 90))
        self.assertEqual(read(425010, 525010), (525000, 425000))
        self.assertEqual(read(575010), (None, 575000))
        self.assertEqual(read(), (None, None))
        with self.assertRaises(ValueError):
            ev.endpoint({"id":"x","click_ticks":[],"recorded_until_tick":100}, 0)

    def test_exact_fisher(self):
        self.assertEqual(ev.contrast(0, 0)["p_one_sided"], 1.0)
        self.assertAlmostEqual(ev.contrast(1, 0)["p_one_sided"], 0.5)
        for wrong in range(10):
            threshold = critical_count(ev.N, wrong)
            self.assertTrue(ev.contrast(threshold, wrong)["reject_at_0.05"])
            self.assertFalse(ev.contrast(threshold-1, wrong)["reject_at_0.05"])

    def test_equal_arms_and_validation(self):
        raw, key = synthetic_inputs(null=True)
        lock, _, _ = ev.blind(raw, ev.digest(key), 0, "synthetic")
        report = ev.evaluate(raw, key, lock)
        primary = report["primary_first_in_windows"]
        self.assertFalse(primary["both_directions_pass"])
        self.assertEqual(primary["counts"]["L"], primary["counts"]["H"])
        invalid = [raw.replace(b'"id":"x001"', b'"id":"x000"'),
                   raw.replace(b'"id":"x001"', b'"id":"x001","arm":"L"'),
                   raw.replace(b'"id":"x001"', b'"id":"x001","id":"x001"'),
                   raw.split(b"\n",1)[1]]
        for data in invalid:
            with self.assertRaises(ValueError):
                ev.blind(data, ev.digest(key), 0, "synthetic")
        for bad_key in [key.replace(b'"H"', b'"L"'), key.replace(b'x001', b'x999')]:
            committed, _, _ = ev.blind(raw, ev.digest(bad_key), 0, "synthetic")
            with self.assertRaises(ValueError):
                ev.evaluate(raw, bad_key, committed)

    def test_sham_detects_a_symbol_dependent_endpoint(self):
        raw, key = synthetic_inputs()
        with patch.object(ev, "endpoint", side_effect=lambda row, latency: (row["symbol"], None)):
            with self.assertRaisesRegex(ValueError, "sham changed atomic timing"):
                ev.blind(raw, ev.digest(key), 0, "synthetic")

    def test_cli_and_tampering(self):
        def cli(*args):
            return subprocess.run([sys.executable, "-B", ev.__file__, *args], cwd=folder,
                                  capture_output=True, text=True)

        with TemporaryDirectory() as temp:
            folder = Path(temp)
            raw, key = synthetic_inputs()
            (folder/"raw").write_bytes(raw)
            frozen = cli("freeze","--raw","raw","--key-sha256",ev.digest(key),"--latency-ticks",
                         "0","--kind","synthetic","--out","lock")
            self.assertEqual(frozen.returncode, 0, frozen.stderr)
            (folder/"key").write_bytes(key)
            lock_bytes = (folder/"lock").read_bytes()
            args = ["report","--raw","raw","--key","key","--lock","lock","--lock-sha256",
                    ev.digest(lock_bytes),"--out","report"]
            completed = cli(*args)
            self.assertEqual(completed.returncode, 0, completed.stderr)
            report = json.loads((folder/"report").read_text())
            self.assertTrue(report["primary_first_in_windows"]["both_directions_pass"])
            self.assertFalse(report["sensitivity_first_from_start"]["both_directions_pass"])
            self.assertEqual(report["paired_H_sham"]["matched_atomic_endpoints"], ev.N)
            self.assertTrue(report["paired_H_sham"]["perturbation_exercised"])
            self.assertNotEqual(cli(*args).returncode, 0)
            args[-1] = "other"
            for file, original in [("raw",raw), ("key",key), ("lock",lock_bytes)]:
                (folder/file).write_bytes(original + b" ")
                self.assertNotEqual(cli(*args).returncode, 0)
                self.assertFalse((folder/"other").exists())
                (folder/file).write_bytes(original)


if __name__ == "__main__":
    unittest.main()
