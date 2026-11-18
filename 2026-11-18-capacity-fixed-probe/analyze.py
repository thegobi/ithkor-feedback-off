"""Reanalyse Arnold et al., Zenodo 14033026. Pass the downloaded ZIP path."""

import hashlib
import io
import sys
from zipfile import ZipFile

import numpy as np
from scipy.io import loadmat
from scipy.optimize import minimize_scalar
from scipy.special import xlogy


def capacity(channel):
    def negative_information(p):
        prior = np.array([p, 1 - p])
        terms = xlogy(channel, channel) - xlogy(channel, prior @ channel)
        return -prior @ terms.sum(axis=1)

    return -minimize_scalar(negative_information, bounds=(0, 1), method="bounded").fun


def histogram_channel(hist):
    centers = np.unique(hist[:, 0].ravel())
    thresholds = (centers[:-1] + centers[1:]) / 2
    prob = np.array([
        (counts * (x < thresholds[:, None])).sum(axis=1) / counts.sum()
        for x, counts in hist
    ])
    p = prob[:, np.argmax(np.abs(prob[0] - prob[1]))]
    return np.column_stack([p, 1 - p])


def samples(mat, suffix):
    return np.stack([np.column_stack([mat[f"I_{s}{suffix}"], mat[f"Q_{s}{suffix}"]])
                     for s in ("g", "e")])


def fit(x):
    train = x[:, ::2]
    direction = train[1].mean(axis=0) - train[0].mean(axis=0)
    scores = (train @ direction).ravel()
    order = np.argsort(scores, kind="stable")
    scores = scores[order]
    labels = np.repeat([1, -1], train.shape[1])[order]
    valid = np.flatnonzero(np.diff(scores) > 0)
    i = valid[np.argmax(np.cumsum(labels)[valid])]
    return direction, (scores[i] + scores[i + 1]) / 2


def evaluate(x, model):
    direction, threshold = model
    p = (x[:, 1::2] @ direction > threshold).mean(axis=1)
    return np.column_stack([1 - p, p])


def main(path):
    with open(path, "rb") as f:
        if hashlib.file_digest(f, "md5").hexdigest() != "d2c73dc589981208cd4444be6adffd26":
            raise ValueError("Input differs from the archived Zenodo ZIP")
    with ZipFile(path) as z:
        prefix = "AllopticalSCQreadout_data/"
        for name in ["hist_MW2MW.npy", "hist_MW2Opt.npy"]:
            w = histogram_channel(np.load(io.BytesIO(z.read(prefix + name))))
            f = (1 + abs(w[0, 0] - w[1, 0])) / 2
            print(f"{name} F={f:.5f} C={capacity(w):.6f} nat")
        models = None
        for hz in [10, 50, 250, 500, 1000]:
            data = z.read(f"{prefix}Fig_4a/IQblobs_{hz}Hz.mat")
            mat = loadmat(io.BytesIO(data), simplify_cells=True)
            first, second = (samples(mat, s) for s in ("", "2"))
            if models is None:
                models = fit(first), fit(second)
            w1, w2 = evaluate(first, models[0]), evaluate(second, models[1])
            print(f"{hz:4} Hz F1={w1.trace()/2:.5f} C1={capacity(w1):.6f} "
                  f"F2={w2.trace()/2:.5f}")


if __name__ == "__main__":
    main(sys.argv[1])
