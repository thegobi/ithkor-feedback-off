"""Held-out IQ calibration and fixed-decoder reanalysis of seven public Delft runs."""

import argparse
from io import BytesIO
import json
from pathlib import Path
import struct
import zlib

import h5py
import numpy as np
import requests

from delft_replay import ARCHIVE


# Byte offsets, compressed sizes and uncompressed CRC32 from the ZIP64 directory.
# In notebook order: Fig. 2(b,c) positions 336 and 344 and the corresponding
# 2 us verification settings with I (no final X), with/without the first pulse.
FILES = {
    "w1": ("20260425-230239-817-d4caa5", 13183644786, 507000, 4278177017),
    "s1": ("20260425-231021-250-cc447e", 13196158366, 619078, 1541808916),
    "w2": ("20260501-164210-632-5dc4a0", 30057848548, 608262, 30299495),
    "s2": ("20260501-164910-564-558adc", 30086852744, 610342, 3625014234),
    "wblank": ("20260501-164223-687-148cb1", 30058754765, 608339, 4267094631),
    "sblank": ("20260501-164923-589-268c61", 30087761040, 608588, 1126957788),
    "verifier": ("20260429-231158-429-cfcf4f", 22514638853, 609046, 2561728717),
}


def read_iq(key, cache):
    uid, pos, size, crc = FILES[key]
    path = cache / (key + ".h5") if cache else None
    if path and path.exists():
        raw = path.read_bytes()
    else:
        end = pos + size + 512
        with requests.get(ARCHIVE, headers={"Range": f"bytes={pos}-{end}"}, stream=True, timeout=45) as r:
            if r.status_code != 206 or r.headers.get("Content-Range") != f"bytes {pos}-{end}/35444714301":
                raise ValueError("Byte range unavailable")
            buf = r.content
        n, extra = struct.unpack_from("<HH", buf, 26)
        assert buf[:4] == b"PK\x03\x04" and uid in buf[30:30+n].decode()
        start = 30 + n + extra
        raw = zlib.decompress(buf[start:start+size], -15)
    if zlib.crc32(raw) != crc:
        raise ValueError(f"ZIP checksum mismatch for {uid}")
    with h5py.File(BytesIO(raw)) as h:
        y = h["x0"][:]
        rep = h["x1"][:]
        iq = np.column_stack((h["y0"][:], h["y1"][:]))
    assert len(y) == 131072 and np.isfinite(iq).all()
    assert np.array_equal(y, np.tile([0, 1], len(y)//2))
    assert np.array_equal(rep, np.arange(len(y))//2)
    return iq, y, rep


def train(x, y):
    direction = x[y == 1].mean(axis=0) - x[y == 0].mean(axis=0)
    score = x @ direction
    order = score.argsort(kind="stable")
    values, labels = score[order], y[order]
    # Predict class 0 to the left of the cut; never split a tie.
    distinct = np.flatnonzero(np.diff(values) > 0)
    gain = np.cumsum(1 - 2 * labels, dtype=int)
    k = distinct[np.argmax(gain[distinct])]
    return direction, (values[k] + values[k+1]) / 2


def predict(x, model):
    direction, cutoff = model
    return (x @ direction > cutoff).astype(int)


def matrix(pred, y):
    return np.stack([np.bincount(pred[y == i], minlength=2) / sum(y == i) for i in (0, 1)])


def main(cache):
    cal, test = {}, {}
    for key in ("w1", "s1"):
        x, y, rep = read_iq(key, cache)
        split = rep % 4
        model = train(x[split == 0], y[split == 0])
        pred = predict(x, model)
        cal[key] = matrix(pred[split == 1], y[split == 1])
        test[key] = matrix(pred[split >= 2], y[split >= 2])
    kernel = np.linalg.solve(cal["s1"], cal["w1"])
    assert np.all((0 <= kernel) & (kernel <= 1))
    np.testing.assert_allclose(kernel.sum(axis=1), 1)
    test["sham"] = test["s1"] @ kernel
    # Same-set descriptive comparison; no final readout enters either kernel.
    descriptive_kernel = np.linalg.solve(test["s1"], test["w1"])
    assert np.all((0 <= descriptive_kernel) & (descriptive_kernel <= 1))
    np.testing.assert_allclose(test["s1"] @ descriptive_kernel, test["w1"])

    x, y, _ = read_iq("verifier", cache)
    final_decoder = train(x, y)
    final, blocks = {}, {}
    for key in ("w2", "s2", "wblank", "sblank"):
        x, y, _ = read_iq(key, cache)
        pred = predict(x, final_decoder)
        final[key] = matrix(pred, y)
        blocks[key] = (pred == y).reshape(-1, 512).mean(axis=1)
    # Resample consecutive blocks of 256 alternating preparation pairs within each file.
    # Inter-file or inter-day systematic error is not estimated from these blocks.
    rng = np.random.default_rng(617866)
    estimates = {k: rng.choice(b, size=(10000, len(b))).mean(axis=1) for k, b in blocks.items()}
    delta = estimates["w2"] - estimates["s2"]
    diff_in_diff = delta - estimates["wblank"] + estimates["sblank"]
    final_balanced = {k: float(v.trace()/2) for k, v in final.items()}
    difference = final_balanced["w2"] - final_balanced["s2"]
    return {"pulse_amplitudes_mV": [50, 350], "first_pulse_us": 2,
            "first_calibration_shots_per_prep_per_setting": 16384,
            "first_test_shots_per_prep_per_setting": 32768, "second_shots_per_prep_per_setting": 65536,
            "software_channel": kernel.tolist(), "first_test": {k:v.tolist() for k,v in test.items()},
            "descriptive_exact_first_channel": descriptive_kernel.tolist(),
            "first_balanced": {k:float(v.trace()/2) for k,v in test.items()},
            "final": {k:v.tolist() for k,v in final.items()},
            "final_balanced": final_balanced, "weak_minus_strong": difference,
            "adjusted_weak_minus_strong": difference - final_balanced["wblank"] + final_balanced["sblank"],
            "weak_minus_strong_CI95_within_acquisitions": np.quantile(delta,[.025,.975]).tolist(),
            "adjusted_CI95_within_acquisitions": np.quantile(diff_in_diff,[.025,.975]).tolist()}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cache", type=Path, help="Optional directory of previously retrieved HDF5 members")
    args = parser.parse_args()
    print(json.dumps(main(args.cache), indent=2, allow_nan=False))
