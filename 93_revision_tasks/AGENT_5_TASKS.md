# Revision Tasks for Agent-5

## Context

Agent-5 owns `05_interactive_widget/`, the interactive visualization widget folder. Validators found no critical or major mathematical failures: tests pass, the notebook runs, and Bloch ellipsoid behavior matches expectations for standard channels. Revisions focus on integration-facing API consistency, labeling non-physical indicators clearly, and small reproducibility/responsiveness improvements.

## CRITICAL Tasks

None.

## MAJOR Tasks

### Task M1: Align or clearly document the qubit-only Choi application helper
- **What**: Agent-5 defines `apply_choi_to_state(choi, rho)` for qubits only, while the consistency review recommends a shared `apply_choi_channel(choi, rho, d_in=None, d_out=None)` API.
- **Where**: `05_interactive_widget/widget_core.py:390`; `92_validation_consistency/CONSISTENCY_REVIEW.md`, Function Signature Mismatches.
- **Why it matters**: The widget's helper name and scope differ from the integration standard.
- **Suggested fix**: Add a small wrapper named `apply_choi_channel` with the recommended argument order and document that this widget supports qubit Choi matrices only. Keep the existing helper if other widget code uses it internally.
- **Source**: Validator-C Function Signature Mismatches; Validator-C Recommended Standards.

## MINOR Tasks

### Task m1: Rename non-physical process fidelity indicators as Choi overlaps
- **What**: The widget clips process fidelity indicators into `[-1, 1]` and may display them even for intentionally non-CP maps.
- **Where**: `05_interactive_widget/widget_core.py:264`-`267`; indicator labels in `05_interactive_widget/widget_core.py`.
- **Why it matters**: "Process fidelity" is physically meaningful for CP/TP channels, but the widget can intentionally enter non-physical regions.
- **Suggested fix**: When `is_cp` or `is_tp` is false, label these quantities as "Choi overlap indicators" or show the raw unclipped value with a warning. For physical channels, keep the process fidelity label.
- **Source**: Validator-A Agent-5 Minor #1; Validator-C Terminology Inconsistencies.

### Task m2: Add a responsiveness note or debounce plan for the widget
- **What**: The widget re-renders the full Matplotlib dashboard on every slider update.
- **Where**: `05_interactive_widget/widget_core.py:321`-`345`.
- **Why it matters**: It is responsive for current qubit examples but could become sluggish if larger channels or heavier plots are added.
- **Suggested fix**: Add a README note that the current widget is qubit-only and re-renders full plots. If performance becomes an issue, debounce slider updates or separate scalar indicator updates from heavy plot rendering.
- **Source**: Validator-B Agent-5 Quality Issue #1; Validator-B Agent-5 Suggestion #1; Validator-B Agent-5 Suggestion #2.

### Task m3: Pin dependencies for reproducibility
- **What**: `requirements.txt` uses lower bounds only.
- **Where**: `05_interactive_widget/requirements.txt:1`-`6`.
- **Why it matters**: Widget and Jupyter dependencies can change behavior across releases.
- **Suggested fix**: Pin versions known to pass validation, or provide a tested environment export for final submission.
- **Source**: Validator-B Agent-5 Quality Issue #2; Validator-C Recommended Standards.

### Task m4: Standardize widget notation and labels with the glossary
- **What**: Agent-5 is mostly consistent, but the glossary recommends `C_\mathcal{E}`, `K_k`, unnormalized `Tr(C)=d_in`, and `Tr_B(C_\mathcal{E})=I_A` terminology across all user-facing text.
- **Where**: `05_interactive_widget/main.ipynb`; `05_interactive_widget/README.md`; `05_interactive_widget/widget_core.py` display strings.
- **Why it matters**: The widget will likely be used as a teaching aid alongside the report.
- **Suggested fix**: Update visible markdown and indicator text to match `92_validation_consistency/UNIFIED_GLOSSARY.md`, especially around Choi normalization and Kraus/eigenoperator naming.
- **Source**: Validator-C Notation Inconsistencies; Validator-C Unified Glossary.

### Task m5: Standardize heatmap styling for final report screenshots
- **What**: The widget already uses `RdBu_r` for real/imaginary heatmaps, but final screenshots should follow the shared figure convention.
- **Where**: `05_interactive_widget/widget_core.py:116`-`137`; `05_interactive_widget/figures/widget_preview.png`.
- **Why it matters**: The widget preview should visually match the rest of the integrated project.
- **Suggested fix**: Keep `RdBu_r` for signed real/imaginary panels and use `viridis` for any magnitude panel if one is added. Regenerate the preview if label or style changes affect the screenshot.
- **Source**: Validator-C Visual Style Issues; Validator-C Recommended Standards.

## Cross-cutting Notes

Agent-5 should remain local and IBM-free. Any API-alignment change should preserve the current interactive behavior and qubit-only assumptions.
