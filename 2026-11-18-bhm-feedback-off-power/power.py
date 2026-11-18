"""Joint power for two directional, one-sided Fisher tests on two first-click gates."""

from functools import cache
from math import comb, fsum
from pathlib import Path
import json


HERE = Path(__file__).resolve().parent
SOURCE = HERE.parent / "2026-11-18-bhm-apparatus-capacity" / "predictions.json"


@cache
def critical_count(n, wrong):
    """Smallest count in the predicted arm giving a one-sided p-value <= 1/20."""
    for correct in range(wrong + 1, n + 1):
        total = correct + wrong
        tail = sum(comb(n, k) * comb(n, total - k)
                   for k in range(correct, min(n, total) + 1))
        if 20 * tail <= comb(2 * n, total):
            return correct
    return n + 1


def binomial_prefix(n, p, tolerance=1e-14):
    """Omit a tail only after bounding its mass by a geometric series."""
    term = (1 - p) ** n
    for k in range(n + 1):
        yield k, term
        ratio = (n - k) * p / ((k + 1) * (1 - p))
        if ratio < 1 and term * ratio / (1 - ratio) < tolerance:
            break
        term *= ratio


def gate_probabilities(signal, efficiency, false_click, early):
    at_signal = 1 - (1 - efficiency * signal) * (1 - false_click)
    early_gate, late_gate = (at_signal, false_click) if early else (false_click, at_signal)
    return early_gate, (1 - early_gate) * late_gate


def joint_power(n, low, high):
    """Condition on low/late and high/early counts to preserve gate dependence."""
    low_correct, low_wrong = low
    high_wrong, high_correct = high

    @cache
    def passes(remaining, threshold, probability):
        if remaining < threshold:
            return 0.0
        return 1 - fsum(comb(remaining, k) * probability**k * (1 - probability)**(remaining - k)
                        for k in range(threshold))

    terms = []
    for lw, pl in binomial_prefix(n, low_wrong):
        for hw, ph in binomial_prefix(n, high_wrong):
            a = passes(n - lw, critical_count(n, hw), low_correct / (1 - low_wrong))
            b = passes(n - hw, critical_count(n, lw), high_correct / (1 - high_wrong))
            terms.append(pl * ph * a * b)
    return fsum(terms)


def main():
    settings = json.loads(SOURCE.read_text(encoding="utf-8-sig"))["cases"]["baseline"]["settings"]
    signal = [1 - settings[key]["loss_multiplicity"][0] for key in ("L", "H")]
    for efficiency, false_click in [(1.0, 0.0), (0.8, 0.005)]:
        low = gate_probabilities(signal[0], efficiency, false_click, early=True)
        high = gate_probabilities(signal[1], efficiency, false_click, early=False)
        previous = 0.0
        for n in range(1, 501):
            power = joint_power(n, low, high)
            if power >= 0.90:
                print(f"eta={efficiency} b={false_click}  n/arm={n}  total={2*n}  "
                      f"power(n-1)={previous:.8f}  power(n)={power:.8f}  "
                      f"power(280)={joint_power(280, low, high):.8f}")
                break
            previous = power
        else:
            raise RuntimeError("90 percent power not reached in the search range")


if __name__ == "__main__":
    main()
