"""Synthetic, standard-library tests for the locked Branch A revision."""
import json
from pathlib import Path
import subprocess
import sys
from tempfile import TemporaryDirectory
import unittest

import evaluate as ev


class ProtocolTests(unittest.TestCase):
    def test_negative_control(self):
        self.assertEqual(ev.contrast(7,7)["difference"],0)
        self.assertFalse(ev.contrast(7,7)["reject_at_0.05"])
        outcomes = {str(i): ((450000,450000) if i<10 else (None,None)) for i in range(560)}
        arms = {str(i): ("H" if i%2 else "L") for i in range(560)}
        self.assertFalse(ev.summarize(outcomes,arms,0)["both_directions_pass"])

    def test_half_open_boundaries(self):
        for t, label in [(424999,"outside"), (425000,"early"), (474999,"early"),
                         (475000,"outside"), (864999,"outside"), (865000,"late"),
                         (934999,"late"), (935000,"outside")]:
            self.assertEqual(ev.gate(t), label)
        row = dict(id="sample", recorded_until_tick=2500007,
                   click_ticks=[400007, 935006, 865007])
        self.assertEqual(ev.endpoint(row, 7), (865000, 400000))
        with self.assertRaises(ValueError):
            ev.endpoint(dict(row, recorded_until_tick=2500000), 7)

    def test_blinded_pipeline(self):
        with TemporaryDirectory() as folder:
            base = Path(folder)
            def cli(*args):
                return subprocess.run([sys.executable,"-B",ev.__file__,*args],cwd=base,
                                      capture_output=True,text=True)
            raw, pulses, keys = [], [], []
            write = dict(gap_ticks=400000,width_ticks=50000,area_rad=2.0944)
            for i in range(560):
                name = f't{i}'
                arm = "L" if i%2==0 else "H"
                clicks = ([450007] if arm=="L" else [900007]) if i<40 else []
                raw.append(dict(id=name,symbol=i%3,click_ticks=clicks,recorded_until_tick=2500007))
                pulses.append(dict(id=name,writes=[write,write] if i else [None,write]))
                keys.append(dict(id=name,arm=arm))
            for name, records in [('raw',raw),('pulse',pulses),('key',keys)]:
                (base/name).write_bytes(b'\n'.join(ev.json_bytes(r) for r in records))
            calibration=ev.json_bytes(dict(latency_ticks=7,validated_area_rad=[2.09,2.10],
                                           qualification_sha256='a'*64))
            (base/'cal').write_bytes(calibration)
            common=['--raw','raw','--calibration','cal','--pulses','pulse']
            freeze=['freeze',*common,'--kind','synthetic','--key-sha256',ev.digest((base/'key').read_bytes()),
                    '--calibration-sha256',ev.digest(calibration),'--out','lock']
            completed=cli(*freeze)
            self.assertEqual(completed.returncode,0,completed.stderr)
            lock_hash=ev.digest((base/'lock').read_bytes())
            report=['report',*common,'--key','key','--lock','lock','--lock-sha256',lock_hash,'--out','result']
            completed=cli(*report)
            self.assertEqual(completed.returncode,0,completed.stderr)
            result=json.loads((base/'result').read_bytes())
            self.assertTrue(result['primary_first_in_windows']['both_directions_pass'])
            self.assertEqual(result['lock']['pulse_deviation_ids'],['t0'])
            self.assertEqual(result['primary_first_in_windows']['counts']['L']['early'],20)
            self.assertEqual(result['paired_H_sham']['matched_atomic_endpoints'],280)
            self.assertTrue(result['paired_H_sham']['perturbation_exercised'])
            for counts in result['primary_first_in_windows']['counts'].values():
                self.assertEqual(sum(counts.values()),280)
            for name in ('cal','pulse','key','raw','lock'):
                path=base/name
                original=path.read_bytes()
                path.write_bytes(original+b'\n')
                self.assertNotEqual(cli(*report[:-1],'other').returncode,0)
                path.write_bytes(original)
            (base/'cal').write_bytes(calibration+b' ')
            self.assertNotEqual(cli(*freeze[:-1],'otherlock').returncode,0)
            self.assertFalse((base/'otherlock').exists())


if __name__=='__main__':
    unittest.main()
