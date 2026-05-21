# Revision Tasks for Agent-4

## Context

Agent-4 owns `04_quantum_combs/`, the non-Markovian dynamics and quantum combs folder. Validators found no execution failures and no critical mathematical errors, but they identified important conceptual gaps around comb causality and the exact status of the RHP/BLP witnesses. This folder has the second-highest revision priority after Agent-2.

## CRITICAL Tasks

None.

## MAJOR Tasks

### Task M1: Implement or document the full quantum-comb causality hierarchy
- **What**: `comb_partial_trace_check` checks only the global trace-preservation condition, not the recursive deterministic-comb causality hierarchy.
- **Where**: `04_quantum_combs/combs_tools.py:393`-`407`; `04_quantum_combs/main.ipynb`, quantum comb section.
- **Why it matters**: A valid comb is constrained by recursive partial trace conditions, not just the global channel TP condition.
- **Suggested fix**: Add a hierarchy check for the demonstrated two-slot comb, including the correct unnormalized-Choi normalization. At minimum, revise the function name and notebook text to state clearly that the current check is only a necessary global TP trace check.
- **Source**: Validator-A Agent-4 Major #1; Validator-B Agent-4 Quality Issue #2; Validator-B Agent-4 Suggestion #1.

### Task M2: Clarify that the RHP quantity is a grid-based witness, not the full continuous measure
- **What**: The code calls the quantity "RHP-style", but the notebook should avoid implying it is the full continuous RHP measure.
- **Where**: `04_quantum_combs/combs_tools.py:461`-`486`; `04_quantum_combs/main.ipynb`, Section 2.
- **Why it matters**: The implemented value depends on a time grid and a pseudo-inverse reconstruction of intermediate maps.
- **Suggested fix**: Add notebook text explaining that this is a discrete CP-divisibility witness based on negative Choi eigenvalues of adjacent intermediate maps. Mention the pseudo-inverse dependence and avoid presenting the number as a continuous RHP integral.
- **Source**: Validator-A Agent-4 Major #2.

### Task M3: Align `apply_choi_channel` argument order with the unified API
- **What**: Agent-4 defines `apply_choi_channel(rho, choi, d_in=None, d_out=None)`, while the glossary recommends `apply_choi_channel(choi, rho, d_in=None, d_out=None)`.
- **Where**: `04_quantum_combs/combs_tools.py:92`; notebook calls in `04_quantum_combs/main.ipynb`.
- **Why it matters**: The function name already matches the recommended name, so the reversed argument order is especially easy to misuse during integration.
- **Suggested fix**: Add a new recommended-order wrapper or migrate calls carefully. If preserving backward compatibility, document the old order clearly and prefer the new order in notebook examples.
- **Source**: Validator-C Function Signature Mismatches; Validator-C Recommended Standards.

### Task M4: Make dense scaling limits explicit
- **What**: `embed_operator` uses explicit dense loops and the comb construction is only practical for small demonstrations.
- **Where**: `04_quantum_combs/combs_tools.py:191`; `04_quantum_combs/README.md`; `04_quantum_combs/main.ipynb`.
- **Why it matters**: Without a warning, users may try dimensions where the construction becomes infeasible.
- **Suggested fix**: Add a short docstring or README note that the implementation is intentionally dense and suitable for small qubit examples only. Keep future demonstrations within those limits.
- **Source**: Validator-B Agent-4 Quality Issue #1; Validator-B Agent-4 Suggestion #2.

## MINOR Tasks

### Task m1: State the finite-grid limitation of the BLP calculation in the notebook
- **What**: The BLP helper searches a finite grid of antipodal pure-state pairs, while the true BLP measure optimizes over all state pairs.
- **Where**: `04_quantum_combs/combs_tools.py:438`-`458`; `04_quantum_combs/main.ipynb`, Section 2.
- **Why it matters**: Readers should not confuse a grid estimate with the exact BLP measure.
- **Suggested fix**: Add one sentence in the notebook near the BLP plot explaining the finite-grid approximation.
- **Source**: Validator-A Agent-4 Minor #1.

### Task m2: Pin dependencies for reproducibility
- **What**: `requirements.txt` uses lower bounds only.
- **Where**: `04_quantum_combs/requirements.txt:1`-`6`.
- **Why it matters**: Lower bounds are weaker for archival reruns.
- **Suggested fix**: Pin versions known to pass validation, or provide a tested environment export for final submission.
- **Source**: Validator-B Agent-4 Quality Issue #3; Validator-C Recommended Standards.

### Task m3: Standardize comb terminology
- **What**: Agent-4 alternates among "quantum comb", "process tensor", "multi-use channel", and "memory comb".
- **Where**: `04_quantum_combs/main.ipynb`; `04_quantum_combs/README.md`; `04_quantum_combs/combs_tools.py` docstrings.
- **Why it matters**: The final report needs a stable formal vocabulary.
- **Suggested fix**: Define process tensor/quantum comb once, then use "quantum comb" for the Choi operator object and "process tensor" when emphasizing multi-time dynamics.
- **Source**: Validator-C Terminology Inconsistencies; Validator-C Unified Glossary.

### Task m4: Standardize Choi/comb figure style
- **What**: Agent-4 uses multiple colormaps, including `viridis` and `magma`, while the consistency review recommends `RdBu_r` for signed real/imaginary Choi panels and `viridis` for magnitudes.
- **Where**: `04_quantum_combs/main.ipynb`, comb and marginal heatmap cells.
- **Why it matters**: Consistent visual conventions reduce interpretation overhead in the final report.
- **Suggested fix**: Use `viridis` for magnitude/residue plots and reserve `RdBu_r` for signed matrix components if those are added.
- **Source**: Validator-C Visual Style Issues; Validator-C Recommended Standards.

## Cross-cutting Notes

Use `T` for comb/process tensor Choi operators and `C_\mathcal{E}` for single-time channel Choi matrices. Keep the subsystem order `A0, B0, A1, B1, ...` explicit wherever partial traces are discussed.
