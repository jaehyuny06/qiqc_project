# Mathematical and Physical Correctness Review

Validator-A reviewed the five producer folders against the shared Choi convention

```text
C_E = sum_ij |i><j| tensor E(|i><j|)
```

with the input system as the first tensor factor. Producer code was not modified. Independent numerical checks are in `scratch/verify_math_claims.py` and `scratch/verify_math_claims.log`.

## Findings for Agent-1

### Critical (must fix)
- [ ] None found.

### Major (should fix)
- [ ] The notebook advertises "All 6 directions" between Kraus, Choi, Stinespring, and natural forms, but `01_theory/main.ipynb` only demonstrates the direct conversions and says the remaining pairings are obtained by composition. This is mathematically acceptable, but the section should explicitly list the six pairings and show at least one composed route such as Natural -> Choi -> Kraus to match the spec.

### Minor (nice to fix)
- [ ] `01_theory/channel_reps.py:68` infers Choi dimensions from TP constraints or square shape. This is fine for the examples, but the inverse Choi routines should state that non-TP rectangular CP maps need explicit dimensions, which the current public API does not expose.

## Findings for Agent-2

### Critical (must fix)
- [ ] None found.

### Major (should fix)
- [ ] `02_ibm_experiment/qpt_tools.py:586` implements `diamond_distance_proxy` as a scaled nuclear norm of Choi differences. The Agent-2 spec asks for diamond norm distance using an independent reimplementation of Agent-3's SDP formulation. The label "proxy" is honest, but it does not satisfy the mathematical deliverable. Suggested fix: add a small CVXPY diamond-norm SDP for reconstructed-vs-ideal Choi matrices, and keep the nuclear norm only as a fast optional diagnostic.
- [ ] `02_ibm_experiment/main.ipynb:200` says exact simulated one-qubit data are already physical; this is true for the deterministic fixtures, but the notebook should show at least one finite-shot or deliberately perturbed linear inversion example with a negative Choi eigenvalue to support the claim that MLE is needed.

### Minor (nice to fix)
- [ ] `02_ibm_experiment/qpt_tools.py:457` clips process fidelity into `[0, 1]`. For presentation this is convenient, but diagnostics should also expose the unclipped value so numerical/modeling issues are not hidden.

## Findings for Agent-3

### Critical (must fix)
- [ ] None found.

### Major (should fix)
- [ ] None found. The SDP in `03_sdp_discrimination/sdp_tools.py:345`-`355` matches the Watrous primal form for the project tensor convention, and the independent check reproduced the Pauli closed form.

### Minor (nice to fix)
- [ ] `03_sdp_discrimination/sdp_tools.py:396` returns an optimal input marginal, but the notebook could more clearly distinguish this marginal from a full reference-system input state. The purification step is implemented later, but the explanatory text would benefit from that caveat.

## Findings for Agent-4

### Critical (must fix)
- [ ] None found.

### Major (should fix)
- [ ] `04_quantum_combs/combs_tools.py:393`-`407` checks only the global trace-preservation condition `Tr_{B0...BN}(T)=I_{A0...AN}`. The validator checklist asks for the quantum-comb causality hierarchy. A deterministic comb requires recursive constraints, not only the global channel TP condition. Suggested fix: add a function and notebook statement for the hierarchy, e.g. for two slots `Tr_{B1}(T_2)=I_{A1} tensor T_1` and `Tr_{B0}(T_1)=I_{A0}` with the correct normalization under the unnormalized Choi convention.
- [ ] `04_quantum_combs/combs_tools.py:461` calls the RHP quantity an "RHP-style" witness. That is acceptable, but the notebook should avoid presenting it as the full continuous RHP measure. It is a grid-based sum of intermediate-map Choi negativity and depends on the pseudo-inverse in `combs_tools.py:481`.

### Minor (nice to fix)
- [ ] `04_quantum_combs/combs_tools.py:438` uses a finite grid of antipodal pure-state pairs for BLP. The README notes this, but the notebook should explicitly state that the true BLP measure involves an optimization over all state pairs.

## Findings for Agent-5

### Critical (must fix)
- [ ] None found.

### Major (should fix)
- [ ] None found. The independent check confirmed the expected Bloch behavior: depolarizing maps to a centered isotropic contraction and amplitude damping maps to an off-center ellipsoid.

### Minor (nice to fix)
- [ ] `05_interactive_widget/widget_core.py:264`-`267` clips process fidelity indicators into `[-1, 1]`. For physical CP/TP channels these values should lie in `[0, 1]`; if the widget intentionally allows non-CP maps, the label should say "overlap indicator" or display unclipped raw values when outside the physical range.

## Summary

- Total critical issues: 0
- Total major issues: 4
- Total minor issues: 4
- Overall mathematical soundness: B+

The core Choi convention, CP/TP checks, Agent-1 round trips, Agent-3 SDP examples, Agent-4 Markovianity witnesses, and Agent-5 Bloch geometry all passed representative numerical checks. The main revision needs are Agent-2's missing true diamond-norm SDP and Agent-4's incomplete comb causality hierarchy.
