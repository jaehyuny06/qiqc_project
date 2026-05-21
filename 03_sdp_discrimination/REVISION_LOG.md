# Revision Log

Date of revision: 2026-05-22

## Tasks Completed

- **M1: Align Choi helper naming with the unified API**
  - Updated `sdp_tools.py` so `kraus_to_choi` accepts `Sequence[np.ndarray]`.
  - Added `apply_choi_channel(choi, rho, d_in=None, d_out=None)` as the project-standard Choi application wrapper.
  - Allowed the wrapper to infer the missing dimension when either `d_in` or `d_out` is supplied.
  - Added a pytest check confirming the wrapper matches the original explicit-dimension helper.

- **m1: Clarify that `optimal_input_state` returns a marginal**
  - Updated `main.ipynb` Section 6 to state that the SDP variable is the optimal input marginal on system `A`, not the full reference-system input state.

- **m2: Document solver-dependent numerical variation**
  - Updated `README.md` to state the solver preference order: MOSEK, then CLARABEL, then SCS.
  - Added a note that small tolerance-level numerical differences can occur across solvers.

- **m3: Log solver names in notebook SDP outputs**
  - Updated the representative SDP check in `main.ipynb` to call `solve_diamond_norm_sdp` and print the solver name and status.

- **m4: Pin CVXPY and solver-related dependencies**
  - Replaced lower-bound dependencies in `requirements.txt` with versions from the validated `qiskit_2025_1` environment.

- **m6: Apply unified notation and visual standards during cleanup**
  - Updated `README.md` to use `C_\mathcal{E}` for channel Choi matrices and `C_\Phi` for channel differences.
  - The notebook already used `C_\Phi` in the SDP formulation; revised solver/marginal text follows the glossary terminology.

## Tasks Skipped

- **m5: Mark future slow SDP tests if the suite grows**
  - Skipped because no new slow SDP tests were added in this revision. The existing test suite remains small and fast.

## New Issues Discovered

- No new project issues were discovered.
- Notebook execution still emits a non-fatal Windows ZMQ runtime warning from the local Jupyter stack.

## Verification

- `python -B -m pytest -q -p no:cacheprovider`
  - Result: `7 passed in 1.79s`
- `python -m jupyter nbconvert --to notebook --execute main.ipynb --output revision_executed.ipynb --ExecutePreprocessor.timeout=300 --ExecutePreprocessor.kernel_name=python3`
  - Result: completed successfully end-to-end on a fresh kernel.
  - Temporary executed notebook was removed after verification.
