# Revision Tasks for Agent-3

## Context

Agent-3 owns `03_sdp_discrimination/`, the SDP channel discrimination folder. Validators found no critical or major mathematical problems: the Watrous SDP form matched the project convention, closed-form Pauli/depolarizing checks passed, and the notebook/tests execute successfully. Revisions are mostly explanatory and integration-oriented.

## CRITICAL Tasks

None.

## MAJOR Tasks

### Task M1: Align Choi helper naming with the unified API
- **What**: Agent-3 uses `apply_choi_to_state(choi, rho, d_in, d_out)` and `kraus_to_choi(kraus_ops: list[np.ndarray])`, while the consistency review recommends `apply_choi_channel(choi, rho, d_in=None, d_out=None)` and `kraus_to_choi(kraus_ops: Sequence[np.ndarray])`.
- **Where**: `03_sdp_discrimination/sdp_tools.py:74`; `03_sdp_discrimination/sdp_tools.py:108`; `92_validation_consistency/CONSISTENCY_REVIEW.md`, Function Signature Mismatches.
- **Why it matters**: The SDP folder will likely be reused by Agent-2 and final integration, so helper naming should not diverge.
- **Suggested fix**: Add a compatibility wrapper named `apply_choi_channel` with the recommended argument order and optional dimensions. If changing the type annotation for `kraus_to_choi` is low-risk, accept `Sequence[np.ndarray]`.
- **Source**: Validator-C Function Signature Mismatches; Validator-C Recommended Standards.

## MINOR Tasks

### Task m1: Clarify that `optimal_input_state` returns a marginal
- **What**: The function returns the optimal input marginal, not the full reference-system input state.
- **Where**: `03_sdp_discrimination/sdp_tools.py:396`; explanatory text in `03_sdp_discrimination/main.ipynb`.
- **Why it matters**: Channel discrimination can require an entangled reference, so confusing the marginal with the full state can mislead readers.
- **Suggested fix**: Add one sentence in the notebook explaining that the full input can be obtained by purifying this marginal, as implemented in the POVM helper path.
- **Source**: Validator-A Agent-3 Minor #1.

### Task m2: Document solver-dependent numerical variation
- **What**: The code prefers MOSEK, then CLARABEL, then SCS, but the README does not clearly state that small numerical differences can depend on the solver.
- **Where**: `03_sdp_discrimination/sdp_tools.py:301`; `03_sdp_discrimination/README.md`.
- **Why it matters**: SDP results can differ slightly by solver and tolerance.
- **Suggested fix**: Add a short README note naming the solver priority and expected small tolerance-level variation.
- **Source**: Validator-B Agent-3 Quality Issue #1.

### Task m3: Log solver names in notebook SDP outputs
- **What**: The notebook reports SDP values but does not consistently show which solver produced them.
- **Where**: `03_sdp_discrimination/main.ipynb`, SDP example cells.
- **Why it matters**: Solver names make numerical results easier to reproduce and debug.
- **Suggested fix**: Where practical, call the result-returning solver function and print `result.solver` alongside the numerical value.
- **Source**: Validator-B Agent-3 Suggestion #2.

### Task m4: Pin CVXPY and solver-related dependencies
- **What**: `requirements.txt` uses lower bounds only.
- **Where**: `03_sdp_discrimination/requirements.txt:1`-`8`.
- **Why it matters**: CVXPY and conic solver behavior can shift across releases.
- **Suggested fix**: Pin versions known to pass validation, or add a tested environment export for final reproducibility.
- **Source**: Validator-B Agent-3 Quality Issue #2; Validator-C Recommended Standards.

### Task m5: Mark future slow SDP tests if the suite grows
- **What**: Validator-B suggested a slow-test marker if more expensive SDP examples are added later.
- **Where**: `03_sdp_discrimination/test_sdp_tools.py`.
- **Why it matters**: It keeps routine validation fast while allowing deeper numerical checks.
- **Suggested fix**: No immediate code change is required unless new slow tests are added; if they are, mark them clearly and document how to run them.
- **Source**: Validator-B Agent-3 Suggestion #1.

### Task m6: Apply unified notation and visual standards during cleanup
- **What**: Agent-3 is mostly consistent, but the project-wide glossary recommends exact terminology for `C_\Phi`, `\Phi`, dimension names, and Choi heatmap styles.
- **Where**: `03_sdp_discrimination/main.ipynb`; `03_sdp_discrimination/README.md`; any revised plots.
- **Why it matters**: Agent-3 supplies the diamond-norm standard used by other folders.
- **Suggested fix**: Use `C_\Phi` for Choi matrices of channel differences and reserve "diamond norm" for exact SDP or analytic values. Use shared heatmap and palette conventions in any revised figures.
- **Source**: Validator-C Notation Inconsistencies; Validator-C Visual Style Issues; Validator-C Unified Glossary.

## Cross-cutting Notes

There are no critical mathematical changes for Agent-3. Prioritize API compatibility and solver reproducibility notes so other agents can rely on this folder as the reference SDP implementation.
