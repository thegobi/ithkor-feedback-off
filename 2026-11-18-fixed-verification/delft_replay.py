"""Replay the Delft fixed-verifier comparison from the publisher's ZIP64 archive."""
import io
import json
import struct
import zlib
from pathlib import Path

import numpy as np
import requests


ARCHIVE = ("https://data.4tu.nl/file/22122209-2f78-4a66-8d04-fe18ac8b244e/"
           "5cd67cd0-4a0c-4a4a-bbc2-c4743f8b5f25")
# Member offsets, compressed lengths and CRC32 from the publisher's ZIP64 directory.
MEMBERS = {
    "readout-pulse-amp-flux-amp/results_fidelity0.npy": (35404914478, 2526, 2144811343),
    "readout-pulse-amp-flux-amp/results_fidelity1.npy": (35404917113, 2526, 53224608),
    "QND/2/results_QND.npy": (35404886241, 19730, 1882283686),
}
DRIVES = [50, 75, 100, 125, 150, 200, 250, 300, 350, 400, 450, 500]


def load_member(name):
    start, size, crc = MEMBERS[name]
    end = start + size + 512
    result = requests.get(ARCHIVE, headers={"Range": f"bytes={start}-{end}"}, stream=True, timeout=30)
    with result:
        if result.status_code != 206 or result.headers["Content-Range"] != f"bytes {start}-{end}/35444714301":
            raise ValueError("Archive server did not return the requested range")
        header = result.content
    length, extra = struct.unpack_from("<HH", header, 26)
    filename = header[30:30 + length].decode()
    assert filename == f"Readout Project/Processed data/{name}" and header[:4] == b"PK\x03\x04"
    offset = 30 + length + extra
    data = zlib.decompress(header[offset:offset + size], wbits=-15)
    assert zlib.crc32(data) == crc
    return np.load(io.BytesIO(data), allow_pickle=False)


def main():
    f0, f1, final = (load_member(name) for name in MEMBERS)
    assert f0.shape == f1.shape == (71, 12) and final.size == 71 * 12 * 4 * 2
    flux = 140 // 5
    final = final.reshape(71, 12, 4, 2)[flux]
    calibration = np.stack((f0[flux], f1[flux]), axis=-1)
    channels = np.array([[[p0, 1-p0], [1-p1, p1]] for p0, p1 in calibration])
    weak, strong = DRIVES.index(50), DRIVES.index(350)
    garbling = np.linalg.solve(channels[strong], channels[weak])
    assert np.allclose(garbling.sum(axis=1), 1) and np.all((garbling >= 0) & (garbling <= 1))
    n = 65536  # Verified in all six raw datasets used for the selected comparison.
    delta = final[weak] - final[strong]
    arm_probabilities = final[[weak, strong]]
    arm_variances = arm_probabilities * (1 - arm_probabilities) / n
    balanced_variance = arm_variances.sum(axis=(0, 2)) / 4
    gap = float(delta[2].mean())
    adjusted = float((delta[2] - delta[3]).mean())
    outcome = {
        "flux_mV": 140, "duration_us": 2, "weak_mV": 50, "strong_mV": 350,
        "strong_to_weak_rows": garbling.tolist(),
        "max_first_channel_residual": float(abs(channels[strong] @ garbling - channels[weak]).max()),
        "weak_minus_strong_final_balanced": gap,
        "shots_per_prep_per_selected_run": n,
        "nominal_independent_shot_ci_95": [gap + sign * 1.96 * float(balanced_variance[2]**0.5) for sign in (-1, 1)],
        "omitted_drive_adjusted_gap": adjusted,
        "adjusted_nominal_independent_shot_ci_95": [
            adjusted + sign * 1.96 * float((balanced_variance[2] + balanced_variance[3])**0.5)
            for sign in (-1, 1)
        ],
        "points": [{
            "drive_mV": drive, "first_correct_by_prep": calibration[i].tolist(),
            "final_correct_by_prep": final[i, 2].tolist(), "drive_omitted_final_correct_by_prep": final[i, 3].tolist(),
        } for i, drive in enumerate(DRIVES)]
    }
    dest = Path(__file__).with_name("delft_results.json")
    dest.write_text(json.dumps(outcome, indent=2) + "\n", encoding="utf-8")
    print(dest, outcome["weak_minus_strong_final_balanced"])


if __name__ == "__main__":
    main()
