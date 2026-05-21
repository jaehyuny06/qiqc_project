# Agent-1 Revision Log

Date of revision-log backfill: 2026-05-22

## Tasks Completed

- Administrative follow-up: Added this missing `REVISION_LOG.md` artifact so Validator-B can verify that Agent-1's notebook and tests still execute after Phase 3.

## Tasks Skipped

- M1: Not executed in this follow-up. The current folder does not show a new explicit six-direction conversion demonstration beyond the existing representation-conversion material.
- M2: Not executed in this follow-up. The current folder does not define the shared `apply_choi_channel(choi, rho, d_in=None, d_out=None)` helper.
- m1: Not executed in this follow-up. Dimension-inference limitations were not newly documented here.
- m2: Not executed in this follow-up. `requirements.txt` still uses development lower bounds.
- m3: Not executed in this follow-up. Existing notation was not changed here.
- m4: No new changes made in this follow-up. The current notebook already uses `RdBu_r` for its signed Choi heatmap.
- m5: Not executed in this follow-up. No local formatting/style note was added.

## New Issues Discovered During Revision

- The original Agent-1 Phase 3 revision log was missing. This file is a backfilled artifact and does not claim that the pending Agent-1 revision tasks were completed.

## Verification

- `pytest -q` from `01_theory/`: 16 passed.
- `jupyter nbconvert --to notebook --execute main.ipynb --output-dir <temp> --output executed_main.ipynb` completed successfully on a fresh kernel. The run emitted the same non-fatal Windows ZMQ runtime warning seen elsewhere in validation.
