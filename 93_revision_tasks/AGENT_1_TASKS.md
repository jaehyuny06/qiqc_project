# Revision Tasks for Agent-1

## Context

Agent-1 owns `01_theory/`, the theoretical foundations folder. Validators found no critical failures: tests and notebook execution passed, the core Choi convention is correct, and the main numerical round trips are sound. Revisions are mainly about matching the promised coverage, documenting edge cases, and aligning integration-facing notation/API/style with the unified glossary.

## CRITICAL Tasks

None.

## MAJOR Tasks

### Task M1: Complete the promised six representation-conversion directions
- **What**: The notebook says it covers all six directions among Kraus, Choi, Stinespring, and natural forms, but it only demonstrates direct conversions and says the rest can be composed.
- **Where**: `01_theory/main.ipynb`, Section 4; related helpers in `01_theory/channel_reps.py`.
- **Why it matters**: The Agent-1 notebook is the project foundation, so its stated conversion coverage should match the specification.
- **Suggested fix**: Explicitly list the six representation pairings and show at least one composed route, such as Natural -> Choi -> Kraus. Keep the current direct helpers if they are correct; the revision can be mostly notebook narrative plus one or two compact sanity checks.
- **Source**: Validator-A Agent-1 Major #1.

### Task M2: Align Choi-channel application API with the project glossary
- **What**: Agent-1 exposes `apply_channel(rho, kraus_ops)` for Kraus form, while the consistency review recommends a shared Choi API named `apply_choi_channel(choi, rho, d_in=None, d_out=None)`.
- **Where**: `01_theory/channel_reps.py`, `apply_channel`; `92_validation_consistency/CONSISTENCY_REVIEW.md`, Function Signature Mismatches.
- **Why it matters**: This mismatch will create friction when integrating examples from multiple producer folders.
- **Suggested fix**: Add or document a Choi-form application helper with the recommended name and argument order, while preserving the existing Kraus helper if notebook code already depends on it. Update notebook references only where useful for integration clarity.
- **Source**: Validator-C Function Signature Mismatches.

## MINOR Tasks

### Task m1: Document dimension-inference limitations for inverse Choi routines
- **What**: Choi dimension inference currently relies on TP constraints or square input/output shape, which is not enough for some non-TP rectangular CP maps.
- **Where**: `01_theory/channel_reps.py:68`; `choi_to_kraus`; `choi_to_natural`.
- **Why it matters**: Users may overgeneralize the helper behavior beyond the examples.
- **Suggested fix**: Add docstring notes explaining when dimension inference is valid and when explicit dimensions would be needed. If time permits, add a dimension-aware optional helper, but a clear limitation note is sufficient.
- **Source**: Validator-A Agent-1 Minor #1; Validator-B Agent-1 Suggestion #2.

### Task m2: Pin or otherwise freeze dependencies for reproducibility
- **What**: `requirements.txt` uses lower bounds only.
- **Where**: `01_theory/requirements.txt:1`-`6`.
- **Why it matters**: Lower bounds are convenient during development but weaker for archival reruns.
- **Suggested fix**: Pin versions known to pass validation, or add a comment explaining that these are development lower bounds and provide a lockfile or environment export for final submission.
- **Source**: Validator-B Agent-1 Quality Issue #1; Validator-C Recommended Standards.

### Task m3: Apply the unified notation standard in prose
- **What**: Agent-1 uses `C_E`, `C`, `E1`, and `E2`; the glossary recommends `C_\mathcal{E}` for channels, `\mathcal{E}` for channels, `A` for input, and `B` for output.
- **Where**: `01_theory/main.ipynb`; `01_theory/README.md`; `01_theory/channel_reps.py` docstrings.
- **Why it matters**: The theory chapter sets notation for the rest of the project.
- **Suggested fix**: Update explanatory prose and markdown equations to match `92_validation_consistency/UNIFIED_GLOSSARY.md`. Code variable names can remain pragmatic where changing them would add churn.
- **Source**: Validator-C Notation Inconsistencies; Validator-C Recommended Standards.

### Task m4: Standardize heatmap styling for final integration
- **What**: Agent-1 uses its own palette and heatmap settings; the consistency review recommends `RdBu_r` centered at zero for signed Choi heatmaps and `viridis` for magnitudes.
- **Where**: `01_theory/main.ipynb`, Choi heatmap cells.
- **Why it matters**: Consistent figures will make the final report easier to read.
- **Suggested fix**: Keep the local palette if desired, but adjust Choi real/imaginary heatmaps to the shared colormap/orientation convention.
- **Source**: Validator-C Visual Style Issues; Validator-C Recommended Standards.

### Task m5: Add a lightweight style or formatting note
- **What**: Validator-B suggested adding a small `pyproject.toml` or formatting note if final integration will enforce style.
- **Where**: `01_theory/README.md` or a local project-style note.
- **Why it matters**: It reduces ambiguity for final cleanup and future contributors.
- **Suggested fix**: Add a short note saying which formatter/style was assumed, or defer to the final repo-level style file once integration begins.
- **Source**: Validator-B Agent-1 Suggestion #1.

## Cross-cutting Notes

Follow `92_validation_consistency/UNIFIED_GLOSSARY.md`: unnormalized Choi matrices, input-first tensor order `A \otimes B`, TP condition `Tr_B(C_\mathcal{E})=I_A`, and code dimensions `d_in`, `d_out`.
