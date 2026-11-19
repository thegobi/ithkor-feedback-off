# Who closed the doors in the quantum ring?

At 0.74, look at the doors. Wait a little longer and they will be shut in both cases. By then, watching what moves inside will tell you surprisingly little about what closed them. We arrived at that peculiar time by asking a question at the heart of ITHKOR: what would we see if a small region had a physical limit on the quantum information it could hold?

## How to fool our favourite explanation

We arranged six wells in a circle on a computer and put three particles in them. The particles can hop between neighbouring wells. We watch two wells side by side. One variant of the v8 hypothesis says that when the pair’s entanglement with the rest of the ring reaches a specified ceiling, both exits from the pair close. A particle can still move from one well to the other inside the pair.

That result is remarkably easy to imitate. Put a timer on the exits. If we know how the experiment starts, we can set it for the instant when the hypothesis says the exits should close.

So we kept the start identical. Only after the run was under way did we shift the phase of the quantum wave by a quarter turn, in one direction or the other. For sharp closure at a ceiling of 1.036 nats, we predicted closure at **0.7163** for one choice and **0.7634** for the other. A timer that never learns of the late choice still has only one setting for both. These times are measured in the ring’s own units, set by how quickly a particle can hop.

## The timer nearly got away with it

First we sampled the current *between the two wells* at four times. A timer set to 0.758 imitated the threshold so well that even with 8,000 simulated measurements per decision we picked the right explanation only **53.9%** of the time. The exits closed at different moments, but motion inside the pair barely gave that away.

Then we looked where the explanations disagree. At **0.74**, the exits should already be closed after one phase shift and still open after the other. On separate copies, we counted how many particles were in the pair just before and just after that instant. The simulation included random quantum outcomes and assumed error-free readout. With the same budget, accuracy against the same timer rose to **86.1%**. When we let the timer choose a new setting in advance to suit this measurement too, accuracy was **77.4%**. Another setting could do worse. [Calculation and results (Slovak)](https://github.com/thegobi/ithkor-feedback-off/blob/v8.0.0/2026-11-19-bhm-boundary-probe/REPORT.sk.md)

## What a lab can do

Version 8 also gives experimenters a second route. Put a register with three distinguishable states next to the ring and physically disconnect its feedback. If the capacity of that register sets the ceiling, improving its readout fidelity from 92% to 99% should shift the onset of possible particle loss from 0.40 to 0.55. Only a small fraction of runs should actually lose a particle. We have published a plan for 560 main trials and a procedure for scoring them blind. [Laboratory protocol (Slovak)](https://github.com/thegobi/ithkor-feedback-off/blob/v1.0.0/2026-11-18-bhm-feedback-off-power/PROTOCOL.sk.md)

On a real chip, even identifying what disturbed the system takes care. In data from TU Delft, we degraded the stronger first readout in software until its recorded result was about as reliable as the weaker one. With the second readout held fixed, a gap of 8.61 percentage points remained. This result shows why we must also control for the physical effect of the pulse. The Delft chip tested a different setup and the ceiling in the ring remains an open question. [TU Delft data analysis (Slovak)](https://github.com/thegobi/ithkor-feedback-off/blob/v1.0.0/2026-11-18-fixed-verification/REPORT.sk.md)

We now have a time, a place and a way to look, together with numbers that tell us when our test has failed. For internal current, for instance, we required the lower confidence bound on accuracy to clear 70% for each of the two explanations. The test failed against the retuned timer. We still do not know what in a single ring could sense the ceiling, or where the switching energy would go. Both questions remain open in v8. For the boundary probe there is a concrete first step: count how often the detector reports a particle crossing when the experimenter knows both exits stayed shut. [Read ITHKOR v8](https://ithz.dev/downloads/ithkor-v8/en.html) · [Reproducible release](https://github.com/thegobi/ithkor-feedback-off/releases/tag/v8.0.0)
