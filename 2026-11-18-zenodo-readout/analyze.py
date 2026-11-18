"""Reanalyze the original Zenodo 8004359 ZIP. Run with Python, NumPy and SciPy."""

import argparse
import hashlib
import io
import json
import re
from pathlib import Path
from zipfile import ZipFile

import numpy as np
from scipy.io import loadmat
from scipy.special import xlogy


LOW, HIGH = -21, -15


def load_series(archive, paired):
    folder = "fig7b" if paired else "fig7a"
    groups = {}
    for name in sorted(archive.namelist()):
        match = re.search(r"_([ge])_neg([\d,.]+)_\d+_data_", name)
        if f"/{folder}/" not in name or not match or not name.endswith(".mat"):
            continue
        label, power = match.groups()
        data = loadmat(io.BytesIO(archive.read(name)), simplify_cells=True)
        if paired:
            signal = np.stack((data["I_4"], data["Q_6"]), axis=-1)
            pulses = [signal[:, start:stop].mean(axis=1) for start, stop in [(21, 32), (40, 51)]]
        else:
            pulses = [np.column_stack((data["I_data_4"], data["Q_data_6"]))]
        power = -float(power.replace(",", "."))
        group = groups.setdefault(power, {})
        assert label not in group and np.isfinite(pulses).all()
        group[label] = np.stack(pulses, axis=1)
    return groups


def confusion(joint):
    first = joint.sum(axis=2)
    return first / first.sum(axis=1, keepdims=True)


def capacity(w):
    prior = np.array([0.5, 0.5])
    for _ in range(10000):
        output = prior @ w
        divergence = (xlogy(w, w) - xlogy(w, output)).sum(axis=1)
        information = prior @ divergence
        if divergence.max() - information < 1e-11:
            return float(information)
        prior *= np.exp(divergence)
        prior /= prior.sum()
    raise RuntimeError("Channel capacity did not converge")


def decode(groups):
    tables = {}
    for power, classes in groups.items():
        x = np.stack([classes["g"], classes["e"]])
        partition = np.arange(x.shape[1]) % 4
        centers = x[:, partition == 0, 0].mean(axis=1)
        assigned = (x - centers.mean(axis=0)) @ (centers[1] - centers[0]) > 0
        index = 2 * assigned[:, :, 0] + assigned[:, :, -1]
        subsets = {}
        for name, mask in (("cal", partition == 1), ("test", partition >= 2)):
            subsets[name] = np.stack([np.bincount(row[mask], minlength=4).reshape(2, 2)
                                      for row in index])
        tables[power] = subsets
    return tables


def normalized(counts):
    return counts / counts.sum(axis=(-2, -1), keepdims=True)


def metrics(joint):
    """Last dimensions are preparation, first readout, second readout."""
    e_given_g = joint[..., 0, :, 1].sum(axis=-1)
    e_given_e = joint[..., 1, :, 1].sum(axis=-1)
    return {
        "F1": (joint[..., 0, 0, :].sum(axis=-1) + joint[..., 1, 1, :].sum(axis=-1)) / 2,
        "F2": (1 - e_given_g + e_given_e) / 2,
        "R2_e_given_g": e_given_g, "R2_e_given_e": e_given_e,
        "disagreement": (joint[..., :, 0, 1] + joint[..., :, 1, 0]).mean(axis=-1),
    }


def degrade(joint, kernel):
    return np.einsum("...pij,ik->...pkj", joint, kernel)


def match(tables):
    wl, wh = [confusion(tables[p]["cal"]) for p in (LOW, HIGH)]
    kernel = np.linalg.solve(wh, wl)
    method = "full calibration matrix"
    if kernel.min() < 0 or kernel.max() > 1:
        fl, fh = [np.trace(w) / 2 for w in (wl, wh)]
        r = (fh - fl) / (2 * fh - 1)
        assert 0 <= r <= 1
        kernel = np.array([[1-r, r], [r, 1-r]])
        method = "balanced fidelity only"
    low, high = [tables[p]["test"] for p in (LOW, HIGH)]
    low_j, high_j = normalized(low), normalized(high)
    sham = degrade(high_j, kernel)
    np.testing.assert_allclose(sham.sum(axis=1), high_j.sum(axis=1), atol=1e-14)
    rng = np.random.default_rng(8004359)

    def resample(counts):
        groups = [rng.multinomial(int(row.sum()), row.ravel()/row.sum(), size=20000)
                  for row in counts]
        return normalized(np.stack(groups, axis=1).reshape(-1, 2, 2, 2))

    ml, mh = metrics(resample(low)), metrics(degrade(resample(high), kernel))
    ci = {k: np.quantile(mh[k] - ml[k], [.025, .975]).tolist() for k in ml}
    return {"method": method, "K": kernel.tolist(), "cal_W_low": wl.tolist(),
            "cal_W_high": wh.tolist(), "test_W_sham": sham.sum(axis=2).tolist(),
            "low": metrics(low_j), "high": metrics(high_j), "sham": metrics(sham),
            "sham_minus_low_ci95_conditional": ci}


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("archive", type=Path)
    args = ap.parse_args()
    with args.archive.open("rb") as file:
        if hashlib.file_digest(file, "md5").hexdigest() != "ced1ed4af893ad064045900903e19a17":
            raise ValueError("ZIP does not match the published MD5")
    result = {}
    with ZipFile(args.archive) as archive:
        for paired in (False, True):
            tables = decode(load_series(archive, paired))
            curve = {}
            for power, split in sorted(tables.items()):
                counts = split["test"]
                w = confusion(counts)
                point = {"test_n_per_prep": counts.sum(axis=(1, 2)).tolist(),
                         "W": w.tolist(), "F1": np.trace(w)/2, "C_nats": capacity(w)}
                if paired:
                    point.update(metrics(normalized(counts)))
                    point["joint_counts"] = counts.tolist()
                curve[power] = point
            matched = match(tables)
            if paired:
                # Descriptive standardization on the observed first-read marginals.
                # No second-read labels enter K. This is not a holdout calibration.
                lo, hi = [tables[p]["test"] for p in (LOW, HIGH)]
                same_set_kernel = np.linalg.solve(confusion(hi), confusion(lo))
                assert np.all((0 <= same_set_kernel) & (same_set_kernel <= 1))
                standardized = degrade(normalized(hi), same_set_kernel)
                np.testing.assert_allclose(standardized.sum(axis=2), confusion(lo))
                np.testing.assert_allclose(standardized.sum(axis=1), normalized(hi).sum(axis=1))
                matched["descriptive_same_set_match"] = {
                    "K": same_set_kernel.tolist(), **metrics(standardized)}
            else:
                # Single-pulse rows have no independent second measurement.
                for field in ("low", "high", "sham", "sham_minus_low_ci95_conditional"):
                    matched[field] = {"F1": matched[field]["F1"]}
            result["paired" if paired else "single"] = {"curve": curve, "comparison": matched}
    print(json.dumps(result, indent=2, allow_nan=False))


if __name__ == "__main__":
    main()
