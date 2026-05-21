# Agent-5 Revision Log

Date of revision: 2026-05-22

## Tasks Completed

- M1: Added `apply_choi_channel(choi, rho, d_in=None, d_out=None)` as the integration-facing helper and documented that Agent-5 supports qubit Choi matrices only. Kept `apply_choi_to_state` as a backward-compatible alias and added a regression test.
- m1: Updated indicator formatting so non-CP or non-TP maps display raw Choi overlap indicators with a warning instead of process fidelity labels.
- m2: Added README and notebook notes that the widget is qubit-only and currently re-renders the full Matplotlib dashboard on every control update, with a debounce/split-update plan for future heavier plots.
- m3: Pinned `requirements.txt` to the versions used for this validated revision.
- m4: Updated README, notebook text, helper documentation, and display labels to follow the shared unnormalized Choi convention, including `C_\mathcal{E}`, `Tr_B(C_\mathcal{E}) = I_A`, and `Tr(C_\mathcal{E}) = d_in`.
- m5: Kept `RdBu_r` for signed real/imaginary Choi heatmaps and regenerated `figures/widget_preview.png` after label changes.

## Tasks Skipped

- None.

## New Issues Discovered

- None. During notebook execution on Windows, `nbconvert` emitted a `zmq` event-loop runtime warning, but the notebook still executed and saved successfully.

## Verification

- `pytest -q` passed.
- `main.ipynb` was executed top-to-bottom with `jupyter nbconvert --to notebook --execute --inplace main.ipynb` and completed successfully.
