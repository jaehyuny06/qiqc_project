# Revision Tasks for Agent-2

## Context

Agent-2 owns `02_ibm_experiment/`, the IBM Quantum process tomography folder. Validators found no execution blockers: the offline notebook runs without IBM credentials and tests pass. The main revision burden is substantial: replace the diamond-distance proxy with a real SDP-based diamond norm, strengthen the MLE demonstration, and reduce future reproducibility risk around Qiskit dependencies and solver behavior.

## CRITICAL Tasks

None.

## MAJOR Tasks

### Task M1: Replace the diamond-distance proxy with a true SDP diamond norm
- **What**: `diamond_distance_proxy` is a scaled nuclear norm of Choi differences, not the diamond norm SDP required by the Agent-2 specification.
- **Where**: `02_ibm_experiment/qpt_tools.py:586`; diagnostics returned near `02_ibm_experiment/qpt_tools.py:595`; notebook discussion around `02_ibm_experiment/main.ipynb:248`.
- **Why it matters**: Calling a proxy a diamond-distance result would be mathematically misleading and inconsistent with Agent-3's exact SDP treatment.
- **Suggested fix**: Add a small local CVXPY implementation of the diamond-norm SDP for reconstructed-vs-ideal Choi matrices. Keep the nuclear-norm quantity only as an explicitly named fast proxy if useful.
- **Source**: Validator-A Agent-2 Major #1; Validator-B Agent-2 Quality Issue #1; Validator-C Terminology Inconsistencies.

### Task M2: Add a non-physical linear-inversion example to justify MLE
- **What**: The notebook states that finite-shot data can make linear inversion non-physical, but the deterministic examples are already physical.
- **Where**: `02_ibm_experiment/main.ipynb:200`, Section 4.
- **Why it matters**: The MLE section should visibly demonstrate why CP/TP projection is needed.
- **Suggested fix**: Add one finite-shot, bootstrap, or deliberately perturbed one-qubit tomography example whose linear-inversion Choi matrix has a negative eigenvalue. Then show that `mle_choi` projects it back to a CP/TP matrix.
- **Source**: Validator-A Agent-2 Major #2.

### Task M3: Fix solver-option handling in the MLE CVXPY loop
- **What**: SCS-specific options are passed inside a loop that also tries CLARABEL, which can become solver-incompatible if SCS is unavailable.
- **Where**: `02_ibm_experiment/qpt_tools.py:390`-`394`.
- **Why it matters**: The current environment passes, but a slightly different solver installation may fail.
- **Suggested fix**: Pass `eps` and `max_iters` only when solving with SCS. Use CLARABEL-compatible keyword arguments, or no extra solver-specific options, for CLARABEL.
- **Source**: Validator-B Agent-2 Quality Issue #2.

### Task M4: Pin or cap Qiskit-family dependencies
- **What**: The requirements file uses broad lower bounds for packages whose APIs change quickly.
- **Where**: `02_ibm_experiment/requirements.txt:1`-`11`.
- **Why it matters**: Agent-2 is the highest-risk folder for future reproducibility drift because Qiskit, Qiskit Experiments, and IBM Runtime APIs evolve.
- **Suggested fix**: Pin versions known to pass validation, or add upper caps for Qiskit-family packages. If exact pins are too strict, include an environment export or tested-version table in the README.
- **Source**: Validator-B Agent-2 Quality Issue #3; Validator-B Agent-2 Suggestion #1; Validator-C Recommended Standards.

### Task M5: Align Choi helper signatures with the unified API
- **What**: Agent-2 uses `apply_channel_to_state(rho, choi, d_out=None)` while the glossary recommends `apply_choi_channel(choi, rho, d_in=None, d_out=None)`.
- **Where**: `02_ibm_experiment/qpt_tools.py:142`; `92_validation_consistency/CONSISTENCY_REVIEW.md`, Function Signature Mismatches.
- **Why it matters**: Inconsistent argument order is a common source of integration bugs.
- **Suggested fix**: Add a wrapper or rename path with the recommended name and argument order. Preserve backward compatibility for existing notebook cells if desired.
- **Source**: Validator-C Function Signature Mismatches; Validator-C Recommended Standards.

## MINOR Tasks

### Task m1: Expose unclipped process fidelity diagnostics
- **What**: `process_fidelity` clips results into `[0, 1]`, which can hide numerical or modeling issues.
- **Where**: `02_ibm_experiment/qpt_tools.py:457`-`466`.
- **Why it matters**: Diagnostics should reveal when reconstruction produces suspicious values.
- **Suggested fix**: Return or log the raw value alongside the clipped presentation value. Keep clipping only for display if needed.
- **Source**: Validator-A Agent-2 Minor #1.

### Task m2: Keep IBM hardware submission and retrieval separate from offline notebook execution
- **What**: Validator-B suggested making hardware job submission/retrieval separate scripts so notebook execution remains offline by default.
- **Where**: `02_ibm_experiment/README.md`; optional scripts in `02_ibm_experiment/`.
- **Why it matters**: It prevents queue waits or credential issues from breaking reproducible notebook runs.
- **Suggested fix**: Add short scripts or documented commands for submit and retrieve flows, while keeping `main.ipynb` deterministic offline.
- **Source**: Validator-B Agent-2 Suggestion #2.

### Task m3: Normalize notebook cell IDs
- **What**: Agent-2 emitted a notebook missing-id warning during nbconvert.
- **Where**: `02_ibm_experiment/main.ipynb`; `91_validation_code/execution_logs/02_ibm_experiment_nbconvert.log`.
- **Why it matters**: `nbformat` warns that missing cell IDs may become a hard error in future versions.
- **Suggested fix**: Open and save the notebook with a current Jupyter version or run a notebook normalization step that adds cell IDs without changing content.
- **Source**: Validator-B Cross-Cutting Observations.

### Task m4: Tighten terminology around diamond norm versus proxy
- **What**: Agent-2's diagnostics sit next to Agent-3's true diamond norm, so proxy language must be unambiguous.
- **Where**: `02_ibm_experiment/main.ipynb`; `02_ibm_experiment/README.md`; `02_ibm_experiment/qpt_tools.py`.
- **Why it matters**: The integrated report should not conflate a heuristic Choi norm with the diamond norm.
- **Suggested fix**: After implementing Task M1, reserve "diamond norm" for SDP results and label any heuristic norm as "diamond-distance proxy" only.
- **Source**: Validator-C Terminology Inconsistencies; Validator-C Unified Glossary.

## Cross-cutting Notes

Use `C_\mathcal{E}` for Choi matrices, `\mathcal{E}` for channels, and `Tr_B(C_\mathcal{E})=I_A` for trace preservation. For Choi heatmaps, use `RdBu_r` for signed real/imaginary panels and `viridis` for magnitudes where plots are revised.
