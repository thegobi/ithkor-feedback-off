# A single image of the proposed quantum valve

**ITHKOR-B-SPACED-1.0.0, 20 November 2026.** This research proposal fixes predictions for a future experiment. It includes the simulation used to choose the observable, an independent solver and a readout protocol. The [Slovak protocol](PROTOCOL.sk.md) specifies the assumptions, controls and interpretation.

A six-site Bose–Hubbard ring starts in |300000⟩. Let R contain sites 0 and 1. Both boundary hops have strength 0.65, the remaining hops 1, and U = 0.35. One physical qutrit couples equally to both sites through the total number in R. Each 0.40 free interval precedes a 0.05 write into a fresh ancilla. The coupling area is 2π/3. Only pure dephasing of the register changes between the nominal 92% (L) and 99% (H) settings. No register readout controls any actuator. The standard model predicts identical unconditional ring states in both arms. A finite-duration write already changes atomic motion in that common reference.

The candidate assigns the static ternary channel capacity to R and closes both boundary links permanently at the first write end where the ensemble entropy of R exceeds that capacity. The predicted closure times are 0.90 and 1.35 in units of ℏ/J. The mean particle numbers at the third write end are 2.59195 (L) and 2.41511 (H). A site-1-only register instead closes both arms at 0.45, as does the site-0-only control. With the original continuously active threshold and the same collective register the predicted times are 0.79037 and 1.27775. These are distinct trigger assumptions.

The primary comparison uses 480 randomized L/H blocks, two independent preparations per block and one number-resolved terminal image per preparation, taken at the actual end of the third write. Count all particles in R including double/triple occupancy, record the total in the same image, and retain every outcome. Freeze readout calibration, count extraction and image IDs before unblinding. Use a one-sided exact paired randomization test of mean L−H at 0.05. With identical independent 90% per-atom detection efficiency, zero false positives and nominal timing, prospective power is about 93%. Detector calibration and controls require additional preparations.

For the fourth-cycle diagnostic use new preparations. The predicted mean is 2.41511 for H and 2.25323 for an open boundary. An arm-blind random timer gives equal arm histograms. An arm-aware ordinary actuator can imitate the proposed effect. An extra 6.82% per-particle loss in H after a common cycle-two lock also reproduces the regional mean difference. Check the global count, differential detection, residual hopping, heating, pulse area and which-site sensitivity before attributing a difference to the threshold. Ancilla output symbols for occupancies 0 and 3 coincide in the static calibration. The independent final camera must resolve those occupancies.

## Reproduce

Use Python 3.10+ with NumPy and SciPy. Run from the extracted directory. The timing grid covers 729 timing sequences with matched arm schedules and compensated pulse areas.

```sh
python -m pip install -r requirements.txt
python checks.py
python calibration.py
python power.py
python validate.py
```

`results.json` contains closure times, work, entropies and all number histograms, including the fourth-cycle sham and the ordinary loss counterexample. `calibration.json` contains the finite-write readout calculation. `power.json` reports prospective power at three budgets and two efficiencies. `fable_check.py` is the independent Fable 5.2 solver. The validation compares all six nominal cases and enumerates small exact permutation tests. The independent check covers these six cases. Calibration, statistical power and timing sensitivity are calculations from the main implementation.

After unblinding, prepare a CSV with columns `pair,L,H`, one row per randomized block, with integer counts in [0,3]. Run `python score.py trials.csv 480`. Missing images make the primary comparison incomplete. Archive the raw six-site counts, blinded assignments, register settings and pulse traces separately. No experimental observations are included in this release.
