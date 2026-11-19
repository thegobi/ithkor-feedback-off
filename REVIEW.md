# ITHKOR v8 release review

Claude Fable 5.2 reviewed the Slovak and English technical documents and lay articles in two passes on 19 November 2026. It received the drafts and excerpts from the simulation and hardware reports. This was an AI review of the text. It did not inspect the repository or perform a hardware experiment. An earlier review of the delayed-choice study used the same model.

The first pass identified three issues that affected interpretation. The second pass marked all three resolved.

- The 0.87% false-alarm bound assumes error-free readout and a single deterministic, sign-blind timer setting across all copies. Per-copy randomisation and sign-aware timers lie outside the calculation.
- The internal-current benchmark required a lower confidence bound above 70% for each class. It failed against the 0.758 timer. A sufficiently precise incompatible boundary result would challenge the specified sharp rule at the adopted ceiling. A nonsignificant result alone is inconclusive.
- Both language versions now give the same scope for local entropy change, detector calibration and probe backaction. The Delft comparison concerns a physical pulse-setting effect on another device.

Final copy edits identified the retuned timer correctly in the probe report, clarified timing jitter, labelled AI checks, added the current criterion to the lay articles, and aligned the translations.

Separately, the seven simulation programs listed in the README ran in an isolated release copy. All seven complete JSON outputs matched the archived values within relative tolerance 1e-6 and absolute tolerance 1e-7. Both prediction manifests verified all three SHA-256 entries. The local hashes document the frozen inputs used for the simulations. The public release date records when the package became available.

The published hardware analyses use the original authors’ archived data. The open-ring loss shift and the closed-ring boundary-valve prediction both await laboratory tests.
