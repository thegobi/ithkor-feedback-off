# Branch A laboratory handoff

ITHKOR-A-SPACED-1.0.0, 20 November 2026. The enclosed Slovak protocol governs the experiment. The primary prediction concerns the first detected atomic loss in two absolute timing windows. The physical register acts during the write. The proposed threshold responds at the end of a write. Program execution uses Python 3 and its standard library.

Use three bosons on six sites, initial state |300000⟩, and monitor site 1, indexed from zero. In both arms apply two free intervals of 0.40, each followed by a 0.05 write into a fresh qutrit. Match the physical pulse areas and shapes between arms. Target gτ = 2π/3 and use pure register dephasing to calibrate the two ternary channels. The model predicts a 10.4434% loss at 0.45 in L and a 7.6961% loss at 0.90 in H. The ordinary ring dynamics gives equal loss statistics between arms under matched conditions. Keep actuator feedback physically disconnected.

Before the first primary shot, finalize the apparatus qualification and record its SHA-256, including calibration of each complete channel, waveform-to-coupling mapping, both pulse areas, latency, jitter and detector performance. Verify timing order and statistical power over the validated uncertainty range. Commit the approved calibration file, randomized key and package manifest hashes to an independent custodian before collection. Log both measured pulses for every assigned trial, retain the raw waveforms and detector timestamps, and blind the analyst to arm assignment. Use 280 independent trials per arm. The analysis takes the first click in [0.425, 0.475) or [0.865, 0.935). Both one-sided Fisher tests must pass at 0.05, early L > H and late H > L.

## Files

- `calibration.json` has `latency_ticks` (a nonnegative integer), `validated_area_rad` (the two hardware-qualified bounds enclosing 2π/3), and `qualification_sha256` (64 lowercase hex digits). The custodian verifies the underlying qualification file against that hash. The analyst verifies the qualification decision independently of the click results.
- `key.jsonl` holds one object per trial with fields `id` and `arm` (L or H). Keep it separate until after the blinded lock. Use opaque IDs and commit the hash of the original file bytes.
- `trials.jsonl` holds `id`, `symbol` (first-write register symbol 0, 1, 2 or null), `click_ticks` (all raw timestamps as integers), and `recorded_until_tick`. Archive both register writes separately. Retain a complete recording even for an empty click list. One model time unit is 1,000,000 ticks; tick zero is the end of preparation.
- `pulses.jsonl` holds `id` and a list `writes` with exactly two entries in chronological order. Each has `gap_ticks` (from preparation or previous write end), `width_ticks`, and `area_rad` (measured integral of g). A missing pulse record is an explicit null entry. Supply all 560 IDs in each trial file; all remain in the denominator. Preserve actual times and areas without clipping or substituting nominal values.

## Blinded analysis

Freeze the raw data, calibrated latency and pulse log before releasing the assignment key. Replace the uppercase placeholders below with the independently recorded hashes. Use fresh output filenames.

```text
python evaluate.py freeze --kind hardware --raw trials.jsonl --pulses pulses.jsonl --calibration calibration.json --calibration-sha256 CALIBRATION_SHA256 --key-sha256 KEY_SHA256 --out lock.json
python evaluate.py report --raw trials.jsonl --pulses pulses.jsonl --calibration calibration.json --key key.jsonl --lock lock.json --lock-sha256 LOCK_SHA256 --out report.json
```

Between commands, record the SHA-256 of lock.json with the custodian. Inspect all deviations in `lock.pulse_deviation_ids`, the instrument traces and the signed qualification. Report primary counts and differences from `primary_first_in_windows`, including negative findings. The field `both_directions_pass` addresses the statistical criterion. Physical qualification and instrument integrity require separate sign-off. Run `python test_protocol.py` for a synthetic end-to-end check.
