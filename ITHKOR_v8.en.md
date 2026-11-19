# ITHKOR v8 — Local information capacity and entropy growth

19 November 2026 · Technical proposal and evidence

**Hypothesis.** A region $R$ has a physical capacity $C(R)$ that limits growth of its von Neumann entropy $S(\rho_R)=-\mathrm{Tr}(\rho_R\ln\rho_R)$. The proposal yields two distinct observables: the time window for particle loss in an open ring and a change in transfers across a two-site boundary in a ring with fixed particle number. Both await laboratory tests. The hardware data below test the readout-control method.

**Relation to v7.** The previous version closed an earlier model after a negative test of its minimal variant on Q109. Version 8 introduces new assumptions for a Bose–Hubbard ring. The earlier negative result still applies to the tested variant.

The six digits in a preparation denote occupations of sites 0 through 5. Times run from preparation in units of $\hbar/J_{\rm in}$, where $J_{\rm in}$ is the reference internal hopping amplitude. Calculations set $\hbar=J_{\rm in}=1$. Natural logarithms give entropy in nats and channel capacity in nats per use.

## 1. Derived limits on local interventions

In the three-boson sector of a six-site ring, the reduced state is block diagonal in the particle number $n$ in $R$. For sector probabilities $p_n$ and normalized blocks $\rho_n$,

$$S(\rho_R)=H(p_n)+\sum_{n:p_n>0}p_n S(\rho_n)\ \geq\ H(p_n).$$

For one site every block is one dimensional. An unconditional local operation preserving each occupation therefore cannot lower the entropy. A decrease requires a change in $p_n$, for example a particle leaving the site. Transfer across the site boundary is compatible with fixed particle number in the full ring. [Single-site derivation](2026-11-18-bhm-entropy-clamp/DERIVATION.sk.md)

On the pair $R=\{0,1\}$ every local unitary preserves the spectrum of $\rho_R$. A phase of $\pi$ at site 0 thus reverses the internal current at unchanged entropy. Complete dephasing in the occupation basis is a mixture of phase unitaries, so concavity gives $S_{\rm after}\ge S_{\rm before}$. In the simulated example at $t=0.60$, current fell from 2.39133 to zero and entropy rose from 0.80295 to 1.88715 nats. At fixed $p_n$ its lower bound was 0.80244 nats. [Two-site calculation](2026-11-19-bhm-two-sites/results.json)

## 2. Branch A — open ring and external register

**Postulate.** A three-state register adjoins site 1 of a ring prepared in $|300000\rangle$. Its calibrated channel $W$ has capacity $C_{\rm op}=\max_p I(X;Y)$. Identifying $C(R)=C_{\rm op}$ for one use and triggering a loss pulse at the first above-threshold sample are additional physical assumptions. The register-to-actuator feedback line is physically disconnected. Residual register coupling, classical crosstalk, heating and changes in tunnelling require independent controls.

**Prediction.** In the symmetric channel with reliability $F$, the two wrong responses are equally probable. Sampling at steps of 0.05 gives the following first interventions. The probability of loss uses all runs, including those without an event. [Frozen v1.0.0 predictions](https://github.com/thegobi/ithkor-feedback-off/blob/334da54a6d8f9a98c17efb182d545f05683bf7f6/2026-11-18-bhm-apparatus-capacity/predictions.json)

| Setting | $F$ | Capacity (nats/use) | Intervention time | Probability of at least one loss |
|---|---:|---:|---:|---:|
| L | 92% | 0.76439 | 0.40 | 6.1134% |
| H | 99% | 1.03568 | 0.55 | 5.4484% |

**Proposed measurement.** Use 560 independent preparations (280 L + 280 H), with separate calibration runs. Count the first click in the union of $[0.375,0.425)$ and $[0.525,0.575)$ over all assigned trials. Both one-sided Fisher tests must give $p\le0.05$, with L > H early and H > L late. With 80% detector efficiency and independent background of 0.5% per window, the joint criterion has calculated power of 91.97% under the specified timing and detection model.

In the blinded phase, `evaluate.py freeze` processes the records and produces a lock referencing the assignment key’s SHA-256 digest. Its custodian records the digest of the lock before releasing the key. The `report` phase verifies digests, trial identities and counts. The paired software control degrades H symbols after acquisition to match L readability. Each atomic outcome and time must match across the two copies. [Protocol](2026-11-18-bhm-feedback-off-power/PROTOCOL.sk.md) · [Evaluator](2026-11-18-bhm-feedback-off-power/evaluate.py)

## 3. Branch B — boundary valve on a pair in a closed ring

**Derivation.** Write $H=H_R+H_Q+fV$, where $Q$ is the rest of the ring, $V$ contains links 1–2 and 5–0 (each 0.65), the internal link 0–1 has strength 1 and the interaction is $U=0.35$. Every term conserves total particle number $N=3$. At a given instantaneous state,

$$\dot S=f\,g(\rho),\qquad g(\rho)=i\,\mathrm{Tr}\!\left([V,\rho](\ln\rho_R\otimes I_Q)\right).$$

The partial trace removes the $H_Q$ contribution, and $H_R$ only rotates the local basis. The logarithm is taken on the support, with a limiting interpretation at zero eigenvalues. If $g>0$ at the ceiling, the common nonnegative multiplier must vanish at that instant to prevent further growth. The calculation leaves both the closure duration and the value of $C$ undetermined.

**Two postulated rules.** The closed model imports the numerical L and H ceilings from branch A. Under sharp closure, $f=1$ until first contact at $S=C$, then $f=0$ permanently. The subsequent propagator factors as $U_R\otimes U_Q$, so the entire local spectrum and entropy remain constant. Under smooth closure, $f=\max(0,1-S/C)$ weakens the boundary from the start. For $S(0)<C$, the gap $C-S(t)=[C-S(0)]\exp[-\int_0^t g(\rho(s))\,ds/C]$ stays positive at finite times for bounded $g$.

**Simulated signatures.** For $|300000\rangle$, sharp closure first reaches the lower and higher ceilings at 0.57024 and 0.81947. Let $\Delta J$ denote the difference in mean internal current $i(a_1^\dagger a_0-a_0^\dagger a_1)$ from the unmodified ring at the same time. At the higher ceiling and $t=0.75$, sharp closure gives $\Delta J=0$ and smooth closure gives $+0.306$. At the lower ceiling and $t=2.50$, smooth closure gives $-1.636$. These are differences in model means before measurement noise. [Valve results](2026-11-19-bhm-boundary-valve/results.json)

### Threshold or shared timer?

**Changed preparation.** At each ceiling the timer retained its $|300000\rangle$ calibration. After changing the preparation to $|210000\rangle$ or $|111000\rangle$, current was measured at 0.75, 1.00, 1.50 and 2.50, using 2,000 fresh copies per time. Scoring against frozen model templates without training gave balanced accuracies of 91.33% and 99.20% at the lower ceiling, and 99.18% and 99.95% at the higher ceiling, in the stated preparation order. Balanced accuracy averages the two class-specific success rates. The model assumes known instrument calibration. [Checksums](2026-11-19-bhm-preparation-clock/freeze.sha256) · [Results](2026-11-19-bhm-preparation-clock/results.json)

**Delayed choice.** At the higher ceiling, preparation $|210000\rangle$ received a $+\pi/2$ or $-\pi/2$ pulse on site 0 at $t=0.30$. The sharp threshold predicted closure at 0.71634 and 0.76344, respectively. With 8,000 current measurements per decision, balanced accuracy fell from 80.28% against the original timer at 0.60430 to 53.93% against a shared timer at 0.758 selected to match eight model means. The predictions were saved and hashed locally before synthetic sampling. The predefined criterion required the lower confidence bound on accuracy to exceed 70% in each class. Internal current failed this criterion against the retuned timer. [Checksums](2026-11-19-bhm-delayed-choice/freeze.sha256) · [Results](2026-11-19-bhm-delayed-choice/results.json)

**Direct boundary probe.** Around $t=0.74$ the threshold leaves only the negative-pulse branch open. Passive counting estimates the change in mean $N_R=n_0+n_1$ between 0.72 and 0.76 on independent copies. With 8,000 copies per decision, balanced accuracy reached 86.1% against the 0.758 timer and 77.4% against the 0.7381 timer retuned to particle number. This is one specific setting. Worst-case passive accuracy remains undetermined.

The ideal paired quantum nondemolition (QND) probe reads $N_R$ twice on the same copy. The calculation includes projection after the first reading. A changed count signals net transfer, so an outward hop followed by a return can go undetected. The threshold decision requires zero changes after positive pulses and at least five after negative pulses. With 3,170 copies per sign (6,340 total, 12,680 readings), sensitivity is 90.0%. The target was at least 90% sensitivity and at most 5% false alarms. This budget was calculated after the primary test. The false-alarm upper bound is 0.87% for every time in the continuous family of shared fixed timers, assuming independent preparations, known parameters and error-free readout. Each such timer uses one fixed time across all copies and both signs. Per-copy randomised timers fall outside this bound. A timer with access to the sign can mimic both closures. [Probe protocol](2026-11-19-bhm-boundary-probe/PROTOCOL.sk.md) · [Results](2026-11-19-bhm-boundary-probe/results.json)

## 4. Hardware results — testing the readout method

**Hassani et al.** In held-out pairs from a superconducting qubit, disagreement fell from 17.20% to 11.00% when power increased from −21 to −15 dBm. Degrading only the first high-power readout in software produced expected disagreement of 15.71% with descriptive matching on the held-out data and 17.36% with independent calibration. Each copy retained its original second outcome. Both physical pulses changed with power. Disagreement alone therefore cannot identify the probability of a physical transition. [Zenodo 8004359](https://zenodo.org/records/8004359) · [Results](2026-11-18-zenodo-readout/results.json)

**TU Delft fluxonium chip.** Fixed second-readout balanced fidelity was 70.14% after the physically weak first pulse (50 mV) and 61.53% after the strong pulse (350 mV). After software degradation, first-readout fidelity on held-out calibration data was 60.92% for the strong pulse versus 60.74% for the weak pulse. The second-readout difference was 8.61 percentage points (within-series 95% interval 8.23–9.00). Subtracting the difference between controls omitting the first pulse gave 8.09 points (7.52–8.67). First-readout calibration and verifier outcomes came from separate acquisitions. The comparison assumes calibration transfer and identifies a physical pulse-setting effect while leaving its microscopic cause unresolved. [Public data v2](https://data.4tu.nl/datasets/22122209-2f78-4a66-8d04-fe18ac8b244e/2) · [Raw-data analysis results](2026-11-18-fixed-verification/raw_results.json)

## 5. Open postulates and limitations

**Switching energy.** Sharp closure changes the mean energy of the instantaneous Hamiltonian by $-\langle V\rangle$, giving −0.18080 and −0.24264 in units of $J_{\rm in}$ at the lower and higher ceilings. Smooth closure gives $d\langle H\rangle/dt=\dot f\langle V\rangle$. The source or recipient of this work remains unidentified. Conservation of three particles alone leaves the energy balance open.

**Origin of the threshold.** Reduced-state entropy describes the statistics of an ensemble of identically prepared copies. A microscopic derivation of the capacity and of a regulator that senses this entropy and changes $f$ in an individual closed run remains open.

**Physical QND probe.** With closure independently verified, measure the false-transfer probability $p_{\rm err}$ and establish its maximum tolerable value for the target sensitivity and false-alarm rate. Even a single false transfer can defeat the zero-change rule on the positive branch. A laboratory budget must also account for preparation errors, probe backaction and timing jitter. The second reading at 0.76 precedes the modelled negative-branch closure by just 0.00344 time units.

**Empirical status on 19 November 2026.** The public datasets identified to date include neither a measurement of the 0.40 → 0.55 shift with physically disconnected feedback nor a direct probe of the boundary valve. A positive result would require comparison with ordinary apparatus backaction and a precisely specified class of timers. Sufficiently precise data incompatible with the predicted transfers would challenge the sharp rule at the chosen ceiling and known ring parameters. Failure to reach significance alone would be inconclusive. [Apparatus controls](2026-11-18-capacity-fixed-probe/RESULTS.md)

## What is proved, what is postulated and what awaits laboratory testing

| Status | Claim and scope |
|---|---|
| Derived | Sector lower bound, local-unitary invariance, removal of occupation-basis coherences under complete dephasing and the corresponding entropy inequality. For the specified Hamiltonian, $\dot S=f g(\rho)$ and cutting the boundary preserves the local spectrum. |
| Postulated | Physical ceiling $S\le C(R)$, identification with register capacity, loss pulse and both valve rules. |
| Simulated | Intervention times, currents, test power, timer discrimination and ideal probe performance under the specified models. |
| Measured on hardware | Qubit data show classification-sensitive disagreement and a difference in fixed verifier output following physically different pulses. |
| Awaiting laboratory tests | Feedback-disconnected loss shift, direct boundary probe with calibrated noise and the regulator’s energy balance. |
