# Delft fluxonium measurement-strength comparison

At the published readout flux, the fixed final verifier assigned the prepared state correctly on 70.15% of trials after the 50 mV drive and 61.56% after the 350 mV drive, with equal weight for each preparation. A stochastic relabeling of the 350 mV first-readout calibration reproduces the entire binary first-readout channel at 50 mV. Applying that relabeling offline leaves the strong drive's final-verifier marginal at 61.56%.

| Measured probability | 50 mV | 350 mV |
|---|---:|---:|
| First readout reports 0 given preparation 0 | 0.604507 | 0.859055 |
| First readout reports 1 given preparation 1 | 0.611847 | 0.851501 |
| Final verifier reports 0 given preparation 0, swept drive present | 0.855560 | 0.667969 |
| Final verifier reports 1 given preparation 1, swept drive present | 0.547348 | 0.563141 |
| Balanced final success, swept drive omitted | 0.739594 | 0.734337 |

## Selection and calculation

Before examining the verification outcomes we selected the authors' marked flux setting (140 mV flux control) and operating drive (350 mV), the lowest sampled drive (50 mV), and a 2 µs swept pulse to match the independent calibration across flux and amplitude. The published final readout uses a fixed 1 µs pulse at 5.18 MHz drive strength. We used the identity condition, which leaves the verifier in the preparation basis. The repository also has interleaved preparations and conditions with an extra X operation. All 12 drive levels for the chosen flux are in the JSON.

Let the rows of C index preparation and its columns index assigned label. Solving C(strong) K = C(weak) gives rows of K equal to (0.647423, 0.352577) and (0.342937, 0.657063). All entries are probabilities, and each row sums to one. This fits the two empirical first-readout conditionals in calibration. The held-separate verifier measurements give the observed weak-minus-strong difference of +8.590 percentage points. The corresponding sample differences for preparations 0 and 1 are +18.759 and −1.579 percentage points. Subtracting the weak-minus-strong difference in the drive-omitted control gives +8.064 points.

Both acquisition series used qubit Q1 and the same nominal control settings. First-readout calibration took place on April 25, 2026. Verification took place on May 1. The experiment recorded only the final IQ outcome during the verification sequence. Separate calibration permits the marginal comparison and leaves the joint outcome distribution unmeasured. The reported first-readout match uses the same calibration data used to estimate K. Authors optimized calibration integration weights at each power and flux. The fixed verifier has assignment errors and the measured effect includes drive-induced state transitions. The net result depends on the preparation mixture.

## Verification and uncertainty

Four raw instrument snapshots independently confirm the Q1 measure_flux settings. The two first-readout calibrations had 0.05 and 0.35 V pulse amplitude, both with 2 µs pulse duration, 2 µs integration time and 0.14 V flux control. Both final verification acquisitions had the same 0.35 V pulse amplitude, 1 µs pulse duration, 2 µs integration time and 0.14 V flux control. The swept drive in those sequences belongs to the notebook section labeled “Dataset 3, 2 us RO pulse duration”. The file snapshot.json is adjacent to each raw dataset.hdf5. Approximate confidence intervals below use only shot noise.

Each of the six selected raw HDF5 files contains 131,072 IQ records with two alternating preparations and 65,536 shots per preparation. The respective weak/strong TUIDs were verified using the authors' chronological indexing.

| Run | Weak TUID | Strong TUID |
|---|---|---|
| First-readout calibration | 20260425-230239-817-d4caa5 | 20260425-231021-250-cc447e |
| Identity, drive present | 20260501-164210-632-5dc4a0 | 20260501-164910-564-558adc |
| Identity, drive omitted | 20260501-164223-687-148cb1 | 20260501-164923-589-268c61 |

For independent Bernoulli trials, the nominal 95% normal interval is +8.239 to +8.941 points for the direct difference and +7.586 to +8.543 points for the control-adjusted difference. These intervals quantify counting noise. Calibration uncertainty, temporal dependence, slow drift, and systematic measurement error require additional checks. The numerical replay reads three small published processed arrays from the ZIP64 archive using byte ranges and checks each member name and CRC32. The authors' classifier counts accepted shot indices with NumPy's count_nonzero on where indices, which can omit index zero in a subset. Its maximum size per individual probability is one shot out of 65,536.

Run `python delft_replay.py` with NumPy and requests installed to regenerate `delft_results.json`.

[Author dataset, version 2](https://data.4tu.nl/datasets/22122209-2f78-4a66-8d04-fe18ac8b244e/2) · [Pulse sequences and assignment calibration](https://arxiv.org/html/2606.17866v1) · [Author analysis notebook, pinned revision](https://github.com/AndersenQubitLab/fluxonium-mist/blob/7f9b58215572e99e05a74e45d53e96b482f30ec6/data_processing.ipynb)
