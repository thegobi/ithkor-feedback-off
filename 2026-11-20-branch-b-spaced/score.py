"""Exact one-sided paired randomization test for randomized L/H order."""
import csv
import sys
from functools import lru_cache

import numpy as np
from scipy.stats import binom


@lru_cache(maxsize=2048)
def weighted_binomial(count, weight):
    prob = np.zeros(count * weight + 1)
    prob[::weight] = binom.pmf(np.arange(count + 1), count, .5)
    return prob


def p_value(difference_counts):
    """Input counts are for observed L-H differences -3 through +3."""
    magnitudes = difference_counts[2::-1] + difference_counts[4:]
    distribution = np.array([1.])
    for weight, count in enumerate(magnitudes, 1):
        distribution = np.convolve(distribution, weighted_binomial(int(count), weight))
    observed = int(difference_counts[4:] @ np.arange(1, 4))
    return min(1., float(distribution[observed:].sum()))


def score(path, expected_pairs):
    with open(path, encoding='utf-8-sig', newline='') as f:
        rows = list(csv.DictReader(f))
    ids = [r['pair'] for r in rows]
    if expected_pairs < 1 or len(rows) != expected_pairs or len(set(ids)) != len(ids) or not all(ids):
        raise ValueError('Expected complete unique randomized blocks.')
    values = [(int(r['L']), int(r['H'])) for r in rows]
    if any(not 0 <= v <= 3 for pair in values for v in pair):
        raise ValueError('A snapshot must give a count from 0 to 3.')
    diff = np.array([l-h for l,h in values])
    return dict(pairs=len(rows), contrast=diff.mean(),
                p_one_sided=p_value(np.bincount(diff+3, minlength=7)))


if __name__ == '__main__':
    print(score(sys.argv[1], int(sys.argv[2])))
