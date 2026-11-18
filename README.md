# ITHKOR — Feedback-off Bose–Hubbard experiment

In a six-site ring with three bosons, the proposed identification of local entropy threshold with the capacity of a nearby three-symbol register predicts **0.40 → 0.55** in inverse hopping units. For the nominal 92% and 99% symmetric readout settings, the simulated probabilities of at least one boson leaving at the respective times are 6.1134% and 5.4484%. The article describes the simulation, the proposed hardware test and reanalyses of other teams' measurements. [Slovenský článok](https://ithz.dev/sk/blog/od-troch-telies-ku-kvantovemu-testu/) · [English article](https://ithz.dev/blog/from-three-bodies-to-a-quantum-test/)

[Laboratórny protokol (SK)](2026-11-18-bhm-feedback-off-power/PROTOCOL.sk.md) · [Exact prediction JSON](2026-11-18-bhm-apparatus-capacity/predictions.json) · [Model assumptions (EN)](2026-11-18-bhm-apparatus-capacity/PROTOCOL.md) · [Original hashes and internal calculation dates](2026-11-18-bhm-apparatus-capacity/freeze.txt)

The ring experiment awaits hardware data. With 280 preparations per setting, the statistical power is 91.9663% under the specified signal and detector model (80% efficiency and 0.5% false-click probability per window). Calibration runs are additional. A physical change in the register can still disturb the atoms through heating or crosstalk with electronic feedback disconnected. The public GitHub release timestamp records publication of these files. It makes no claim of legal priority.

## Reproduce

Use Python 3.12 from the root of the release. The power calculation and evaluator use the Python standard library. The evaluator tests generate synthetic trials and exercise both CLI phases, including rejection of tampered files. See the Slovak protocol for the hardware input schema and freeze/report commands.

```sh
sha256sum -c SHA256SUMS
python -B 2026-11-18-bhm-feedback-off-power/power.py
python -B 2026-11-18-bhm-feedback-off-power/test_evaluate.py
python -m pip install -r requirements.txt
python -B 2026-11-18-bhm-apparatus-capacity/run.py > prediction-replay.json
```

The power calculation should print 157 preparations per setting for an ideal detector and 267 for the model detector at 90% power. For the proposed sample of 280 per setting, the model detector should give `power(280)=0.91966333` approximately. In the simulator replay, compare `cases.baseline.settings` with the published JSON. The replay has a new `prediction_time` and floating-point values can differ slightly across platforms. The shared solver files are included solely as dependencies of that simulation.

| Study | Code and inputs |
| --- | --- |
| Arnold et al., optical and microwave receivers and pulse repetition rate | [Report](2026-11-18-capacity-fixed-probe/RESULTS.md) · [analyze.py](2026-11-18-capacity-fixed-probe/analyze.py) · [Zenodo 14033026](https://zenodo.org/records/14033026) |
| van Thiel et al., optical readout and coherence controls | [Workbook sources](https://zenodo.org/records/14293253) · [Report](2026-11-18-capacity-fixed-probe/RESULTS.md). The Arnold script processes only the Arnold ZIP. |
| Hassani et al., two successive readouts | [Report](2026-11-18-zenodo-readout/REPORT.sk.md) · [analyze.py](2026-11-18-zenodo-readout/analyze.py) · [Zenodo 8004359](https://zenodo.org/records/8004359) |
| TU Delft, same final verifier after different first pulses | [Report](2026-11-18-fixed-verification/REPORT.sk.md) · [raw_check.py](2026-11-18-fixed-verification/raw_check.py) · [4TU data v2](https://data.4tu.nl/datasets/22122209-2f78-4a66-8d04-fe18ac8b244e/2) |

```sh
python -B 2026-11-18-capacity-fixed-probe/analyze.py AllopticalSCQreadout_data.zip
python -B 2026-11-18-zenodo-readout/analyze.py "Source Data _ full_version.zip" > hassani-replay.json
python -B 2026-11-18-fixed-verification/raw_check.py > delft-replay.json
```

Get the first two ZIPs from the authors' Zenodo records above. Each analyzer verifies the archive's published MD5. The Delft runner reads seven byte ranges from the authors' large ZIP and verifies the ZIP member CRC32. If the host cannot serve the ranges, extract the seven HDF5 members of the same ZIP version, name them by the keys in `raw_check.py` (for example `w1.h5`), and pass their directory as `--cache`. The authors' datasets stay at their original archives. Only scripts, aggregate outputs and a synthetic example are included here.

The [four-time readout simulation scores](2026-11-18-bhm-signed-fine/validation.json) are supplied as a numerical reference. At 8,000 simulated shots per trajectory, four measurements of signed, reference-subtracted current reached 73.22% balanced accuracy on 2,048 held-out pairs. A final-time-only observation gave 52.17% at the same shot budget. This separate classifier study's simulation pipeline is outside this release.
