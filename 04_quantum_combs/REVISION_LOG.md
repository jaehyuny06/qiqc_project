# Revision Log

Date of revision: 2026-05-22

## Tasks Completed

- M1: Added `deterministic_comb_causality_check` for the recursive deterministic-comb causality hierarchy in unnormalized Choi convention, kept a separate `comb_global_trace_preservation_check` for the weaker global TP condition, updated tests, and revised notebook text/output to distinguish the two checks.
- M2: Clarified in `main.ipynb` and `README.md` that the RHP-style quantity is a grid-based CP-divisibility witness using pseudo-inverse reconstructed adjacent intermediate maps, not the full continuous RHP integral.
- M3: Migrated `apply_choi_channel` to the unified API order `apply_choi_channel(choi, rho, d_in=None, d_out=None)`, updated all local callers, added a deprecated legacy wrapper for the old order, and added a regression test.
- M4: Added dense-scaling warnings to `embed_operator`, `main.ipynb`, and `README.md`.
- m1: Added notebook text stating the BLP calculation is a finite-grid approximation over sampled antipodal pure-state pairs.
- m2: Pinned `requirements.txt` to the versions used for this validation run.
- m3: Standardized terminology around quantum comb `T`, process tensor, and `C_\mathcal{E}` within the revised files.
- m4: Updated marginal heatmaps to use `viridis` for magnitude plots, matching the shared plotting convention.

## Tasks Skipped

- None.

## New Issues Discovered

- The user prompt used the placeholder path `04_subtask_name/`, while `AGENT_4_TASKS.md` identifies Agent-4's actual folder as `04_quantum_combs/`. All edits were limited to `04_quantum_combs/`.

## Verification

- `python -m pytest -q` from `04_quantum_combs/`: 7 passed.
- `jupyter nbconvert --to notebook --execute main.ipynb --output executed_main.ipynb` from `04_quantum_combs/`: completed successfully on a fresh kernel. The temporary executed output file was removed after verification.
