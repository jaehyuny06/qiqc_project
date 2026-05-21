# Revision Log

Date of revision: 2026-05-22

## Tasks Completed

- **M1: Replace the diamond-distance proxy with a true SDP diamond norm**
  - Added `diamond_norm_sdp` and `diamond_norm_distance` to `qpt_tools.py`.
  - `diagnose_noise` now reports `diamond_distance` as the true SDP-computed half-diamond distance and keeps `diamond_distance_proxy` as an explicitly labeled Choi nuclear-norm proxy.
  - Updated notebook diagnostic text and regenerated `data/raw_results.json` plus `data/sample_simulated_results.json` with the new fields.

- **M2: Add a non-physical linear-inversion example to justify MLE**
  - Added a Section 4 notebook demo that perturbs the X-gate linear-inversion Choi estimate so it has a negative eigenvalue and fails CP/TP.
  - The same cell shows that `mle_choi` projects the estimate back to a CP/TP Choi matrix.

- **M3: Fix solver-option handling in the MLE CVXPY loop**
  - Updated `mle_choi` so SCS-specific `eps` and `max_iters` options are passed only when the selected solver is SCS.
  - CLARABEL is called without SCS-only options.

- **M4: Pin or cap Qiskit-family dependencies**
  - Replaced broad lower bounds in `requirements.txt` with versions from the validated `qiskit_2025_1` environment, including Qiskit, Qiskit Aer, Qiskit Experiments, and Qiskit IBM Runtime.
  - Added a README note that the pins match the validated revision environment.

- **M5: Align Choi helper signatures with the unified API**
  - Added `apply_choi_channel(choi, rho, d_in=None, d_out=None)` with the project-standard argument order.
  - Preserved the original `apply_channel_to_state(rho, choi, d_out=None)` helper for backward compatibility.
  - Added a pytest check confirming the new wrapper matches the legacy helper.

- **m1: Expose unclipped process fidelity diagnostics**
  - Added `raw_process_fidelity`.
  - `diagnose_noise` now includes `process_fidelity_raw` alongside the clipped display-oriented `process_fidelity`.

- **m2: Keep IBM hardware submission and retrieval separate from offline notebook execution**
  - Expanded README wording to state that hardware submission is separate and not executed during the reproducible offline run.

- **m3: Normalize notebook cell IDs**
  - Normalized `main.ipynb`; no cells are missing IDs after revision.

- **m4: Tighten terminology around diamond norm versus proxy**
  - Updated notebook and README wording so "diamond norm/distance" refers to the SDP-computed quantity.
  - The heuristic Choi-norm quantity remains labeled as `diamond_distance_proxy`.

## Tasks Skipped

- None.

## New Issues Discovered

- No new project issues were discovered.
- Notebook execution still emits a non-fatal Windows ZMQ runtime warning from the local Jupyter stack.

## Verification

- `python -B -m pytest -q -p no:cacheprovider`
  - Result: `5 passed in 2.22s`
- `python -m jupyter nbconvert --to notebook --execute main.ipynb --output revision_executed.ipynb --ExecutePreprocessor.timeout=300 --ExecutePreprocessor.kernel_name=python3`
  - Result: completed successfully end-to-end on a fresh kernel.
  - Temporary executed notebook was removed after verification.
