# Duplication Analysis

This analysis follows `92_validation_consistency/UNIFIED_GLOSSARY.md`: unnormalized Choi matrices, input system first, output system second, and `Tr_B(C_E) = I_A` for trace preservation.

## Summary

The strongest duplication is in channel representation math: `kraus_to_choi`, Choi application, CP/TP checks, standard qubit channel constructors, and Choi/Bloch visualizations. The cleanest common base is a hybrid:

- Use Agent 1 (`01_theory/channel_reps.py`) as the base for general representation conversions.
- Use Agent 4 (`04_quantum_combs/combs_tools.py`) for generic tensor partial trace and explicit `d_in`, `d_out` natural-representation signatures.
- Use Agent 3 (`03_sdp_discrimination/sdp_tools.py`) as the base for diamond-norm SDP and Choi-returning standard channels.
- Use Agent 5 (`05_interactive_widget/widget_core.py`) as the base for Bloch affine maps and widget-friendly visualization surfaces.
- Use Agent 2 (`02_ibm_experiment/qpt_tools.py`) as the base for process-fidelity metrics, QPT-specific projections, and hardware/tomography wrappers that should mostly remain local.

## Duplicate Groups

### `kraus_to_choi`

Found in:

- `01_theory/channel_reps.py:kraus_to_choi(kraus_ops: list[Array])`
- `02_ibm_experiment/qpt_tools.py:kraus_to_choi(kraus_ops: list[np.ndarray])`
- `03_sdp_discrimination/sdp_tools.py:kraus_to_choi(kraus_ops: Sequence[np.ndarray])`
- `04_quantum_combs/combs_tools.py:kraus_to_choi(kraus_ops: Sequence[Array])`
- `05_interactive_widget/channel_utils.py:kraus_to_choi(kraus_ops: Sequence[Array])`

Differences:

- All use the same unnormalized input-first Choi convention.
- Agents 1 and 5 validate all Kraus shapes up front; Agents 2 and 3 validate during conversion; Agent 4 assumes compatible shapes after reading the first operator.
- Agents 1, 2, 3, and 5 explicitly Hermitize the result; Agent 4 returns the direct block result without Hermitization.
- Agent 1 uses vectorization (`op.T.reshape`) and is compact/general; Agents 2, 3, 4, and 5 use explicit block loops.
- Dtype handling varies between `complex`, `np.complex128`, and untyped `np.asarray`.

Cleanest base:

- Agent 1 is the cleanest implementation shape and supports rectangular `(d_out, d_in)` Kraus operators naturally.
- Agent 3/5 validation style is worth preserving via a shared `_validate_kraus_ops` helper.

Semantic mismatches:

- No convention mismatch was found for Choi ordering or normalization.
- Agent 4 should stop being the only version that does not Hermitize, or the common function should document that exact algebraic output is Hermitian up to numerical noise and return the Hermitian part consistently.

### `choi_to_kraus` and Choi Eigenoperators

Found in:

- `01_theory/channel_reps.py:choi_to_kraus(choi, tol=1e-10)`
- `02_ibm_experiment/qpt_tools.py:choi_to_kraus(choi, tol=1e-10)`
- `05_interactive_widget/channel_utils.py:choi_to_kraus(choi, tol=1e-10)`
- Near-duplicate display helper: `05_interactive_widget/widget_core.py:extract_kraus_display(choi)`

Differences:

- Agent 1 infers `(d_in, d_out)` by checking TP-compatible factor pairs, then falls back to square channels.
- Agents 2 and 5 infer square input/output dimensions from `sqrt(choi.shape[0])`.
- Agents 2 and 5 sort eigenvalues descending by `argsort`; Agent 1 iterates reversed `np.linalg.eigh` output.
- `extract_kraus_display` intentionally keeps negative Choi eigenweights for non-CP diagnostics, so it is not a true Kraus extraction.

Cleanest base:

- Agent 1 is the most general, but the shared API should add optional `d_in` and `d_out` so rectangular non-TP maps do not rely on inference.

Semantic mismatches:

- `extract_kraus_display` must remain a visualization/diagnostic helper, not a replacement for `choi_to_kraus`.

### Choi/Natural Representation Conversions

Found in:

- `01_theory/channel_reps.py:choi_to_natural(choi)`, `natural_to_choi(natural)`
- `04_quantum_combs/combs_tools.py:choi_to_natural(choi, d_in=None, d_out=None)`, `natural_to_choi(natural, d_in=None, d_out=None)`

Differences:

- Agent 1 infers dimensions internally and exposes no dimension parameters.
- Agent 4 exposes optional dimensions and requires both dimensions if either is supplied.
- Both use column-stacking natural representation and agree on tested qubit examples.

Cleanest base:

- Use Agent 1's compact tensor-transpose implementation, but adopt Agent 4's explicit optional `d_in`, `d_out` signature to match the glossary.

Semantic mismatches:

- No vectorization mismatch was found, but the shared docstring must explicitly state column-stacking.

### Applying Channels

Found in:

- Kraus form: `01_theory/channel_reps.py:apply_channel(rho, kraus_ops)`, `05_interactive_widget/channel_utils.py:apply_channel(rho, kraus_ops)`
- Choi form: `02_ibm_experiment/qpt_tools.py:apply_choi_channel(choi, rho, d_in=None, d_out=None)`
- Choi form: `03_sdp_discrimination/sdp_tools.py:apply_choi_channel(choi, rho, d_in=None, d_out=None)`
- Choi form: `04_quantum_combs/combs_tools.py:apply_choi_channel(choi, rho, d_in=None, d_out=None)`
- Qubit-only Choi form: `05_interactive_widget/widget_core.py:apply_choi_channel(choi, rho, d_in=None, d_out=None)`

Differences:

- The shared standard name and argument order is already `apply_choi_channel(choi, rho, d_in=None, d_out=None)`.
- Agent 2 has a legacy helper `apply_channel_to_state(rho, choi, d_out=None)`.
- Agent 4 keeps `apply_choi_channel_legacy(rho, choi, ...)`.
- Agent 5 only supports qubits and Hermitizes the output.
- Dimension inference differs: Agent 2 infers `d_in` from `rho`; Agent 3 infers equal dimensions if both are omitted; Agent 4 infers `d_in` from `rho`; Agent 5 requires qubit dimensions.

Cleanest base:

- Use the Agent 2/4 API behavior: infer `d_in` from `rho`, infer `d_out` from Choi size, validate shape, and compute by tensor contraction.

Semantic mismatches:

- The legacy `(rho, choi)` helpers should not be in the common API except possibly as producer-local compatibility wrappers.
- Hermitization of output should be optional or omitted in the core helper; applying a non-Hermiticity-preserving linear map should reveal that behavior.

### CP/TP Validation and Partial Traces

Found in:

- `01_theory/channel_reps.py:is_cp`, `is_tp`, `_partial_trace_output`, `_partial_trace_input`, `is_unital`, `choi_rank`
- `02_ibm_experiment/qpt_tools.py:is_cp`, `is_tp`, `partial_trace_output`, `hermitize`
- `03_sdp_discrimination/sdp_tools.py:is_cp`, `is_tp`, `_partial_trace_output`
- `04_quantum_combs/combs_tools.py:partial_trace`, comb causality checks
- `05_interactive_widget/channel_utils.py:is_cp`, `is_tp`, `partial_trace_output`

Differences:

- Agent 1's `is_cp` checks Hermiticity before eigenvalues; Agents 2, 3, and 5 Hermitize first and then check eigenvalues.
- `is_tp` signatures vary:
  - Agent 1: `is_tp(choi, d_in, tol=...)`
  - Agent 2: `is_tp(choi, d_in, d_out=None, tol=...)`
  - Agent 3: `is_tp(choi, d_in, d_out, tol=...)`
  - Agent 5: `is_tp(choi, tol=...)`, infers square dimensions
- Agent 4's `partial_trace(operator, dims, trace_out)` is fully generic and should be shared.
- Agent 5 uses a Frobenius-norm residual for TP; others use `np.allclose`.

Cleanest base:

- Use Agent 4 for generic `partial_trace`.
- Use Agent 2's `is_tp(choi, d_in, d_out=None, tol=...)` signature because it matches the glossary while preserving optional `d_out`.
- Use Agent 1's stricter Hermiticity check in `is_cp`.

Semantic mismatches:

- Agent 5's `is_tp(choi)` callers must supply `d_in=2` or go through a qubit compatibility wrapper.

### Standard Channel Constructors

Found in:

- Kraus-returning: `01_theory/channel_reps.py` (`identity_channel`, `bit_flip_channel`, `phase_flip_channel`, `pauli_channel`, `depolarizing_channel`, `amplitude_damping_channel`, `phase_damping_channel`)
- Kraus-returning qubit helpers: `05_interactive_widget/channel_utils.py` (`identity_kraus`, `bit_flip_kraus`, `phase_flip_kraus`, `pauli_kraus`, `depolarizing_kraus`, `amplitude_damping_kraus`, `phase_damping_kraus`)
- Choi-returning: `03_sdp_discrimination/sdp_tools.py` (`identity_channel_choi`, `unitary_channel_choi`, `pauli_channel_choi`, `bit_flip_channel_choi`, `phase_flip_channel_choi`, `depolarizing_channel_choi`, `amplitude_damping_channel_choi`, `phase_damping_channel_choi`, `z_rotation_channel_choi`)
- Choi-returning after-unitary noise models: `02_ibm_experiment/qpt_tools.py` (`depolarizing_after_unitary`, `amplitude_damping_after_unitary`, `two_qubit_depolarizing_after_unitary`)

Differences:

- Agents 1 and 3 use depolarizing parameter `p` as replacement probability in `E_p(rho) = (1-p)rho + p Tr(rho) I/d`. For qubits this corresponds to Pauli probabilities `I: 1 - 3p/4`, `X/Y/Z: p/4`.
- Agents 2 and 5 use depolarizing parameter `p` as total non-identity Pauli-error probability: `I: 1-p`, `X/Y/Z: p/3`.
- Agents 1 and 5 return Kraus operators; Agent 3 returns Choi matrices.
- Agent 3 supports `d > 2` directly in `depolarizing_channel_choi`; the Kraus-returning versions are qubit-only for depolarizing.
- Agent 5's `unital_choi` intentionally allows non-CP Pauli-diagonal maps for visualization.

Cleanest base:

- Use Agent 1's Kraus-returning constructors for common qubit channels.
- Use Agent 3's Choi-returning convenience constructors and unitary validation.
- Include an explicit depolarizing `convention` parameter or separate names so Agent 2/5 behavior is not silently changed.

Semantic mismatches:

- Depolarizing `p` is the biggest mismatch and must be resolved before implementation. The recommended default is `convention="replacement"` because it matches Agents 1 and 3 and the analytical diamond-norm formula in Agent 3. Agent 2 and Agent 5 migrations should use `convention="pauli_error"`.

### Visualization: Choi Heatmaps, Bloch Sphere, Eigenspectrum

Found in:

- `02_ibm_experiment/qpt_tools.py:plot_choi_heatmap(choi, title)`, `plot_bloch_deformation(choi)`
- `05_interactive_widget/widget_core.py:plot_choi_heatmap(choi, ax_real, ax_imag)`, `plot_bloch_ellipsoid(choi, ax_3d)`, `plot_eigenspectrum`, `bloch_affine_map`, `extract_kraus_display`
- Simple heatmap data helper in `04_quantum_combs/non_markovian_dynamics.py:choi_abs_matrix` is used by the comb notebook but is outside the primary requested input files.

Differences:

- Agent 2 creates full figures internally and includes real, imaginary, and magnitude panels.
- Agent 5 accepts caller-provided axes, plots real and imaginary panels only, and has a richer Bloch affine-map helper.
- Both follow glossary colormap standards: `RdBu_r` for real/imaginary and `viridis` for magnitude where present.

Cleanest base:

- Use Agent 5's axes-first API for composability, with Agent 2's optional magnitude panel and title support.

Semantic mismatches:

- Bloch helpers are qubit-only and should explicitly validate `(4, 4)` Choi inputs.

### Metrics and Diamond Norm

Found in:

- `02_ibm_experiment/qpt_tools.py:raw_process_fidelity`, `process_fidelity`, `average_gate_fidelity`, `diamond_norm_sdp`, `diamond_norm_distance`, `diagnose_noise`
- `03_sdp_discrimination/sdp_tools.py:solve_diamond_norm_sdp`, `diamond_norm_sdp`, `analytical_pauli_diamond_norm`, `analytical_depolarizing_diamond_norm`, discrimination helpers
- `04_quantum_combs/combs_tools.py:trace_distance`

Differences:

- Agent 2's `diamond_norm_sdp` returns only a float and has solver kwargs directly on that function.
- Agent 3 separates `solve_diamond_norm_sdp` returning `DiamondNormResult` from `diamond_norm_sdp` returning a float.
- Agent 2 defines `diamond_norm_distance` as `0.5 * ||E_actual - E_ideal||_diamond`, aligning with glossary terminology.
- Agent 2's `diamond_distance_proxy` in `diagnose_noise` is a Choi nuclear-norm heuristic, correctly labeled as a proxy.

Cleanest base:

- Use Agent 3's `DiamondNormResult` and SDP solver structure.
- Use Agent 2's fidelity and half-diamond-distance wrappers.
- Move `trace_distance` from Agent 4 into metrics.

Semantic mismatches:

- Do not call Choi nuclear-norm quantities "diamond norm"; keep any proxy explicitly named `diamond_distance_proxy`.

### Generic Utilities

Found in:

- `dagger`: Agent 2 and Agent 4
- `hermitize` / `_hermitian_part`: Agent 2 and Agent 3, equivalent to inline Hermitian projections elsewhere
- Probability validation: Agent 1 `_check_probability`, Agent 5 `validate_probability`
- Dimension inference helpers: Agents 1, 3, 5
- JSON complex matrix serialization: Agent 2 only

Cleanest base:

- Put low-level shared math helpers in `choi_common.utils`.
- Keep QPT storage helpers such as `matrix_to_json_dict` and `save_json` local to Agent 2 unless another producer starts using them.

Semantic mismatches:

- Dimension inference should prefer explicit `d_in`, `d_out`; inference should be documented as a convenience, not a guarantee for arbitrary rectangular or non-TP maps.

## Not Recommended for Immediate Extraction

The following are valuable but not duplicated enough to justify moving during the first common-library step:

- IBM/Qiskit execution and result wrappers: `ProcessTomographyResult`, `run_process_tomography`, `linear_inversion_choi`, `mle_choi`, `project_to_cptp`.
- Quantum-comb construction and causality hierarchy: `construct_process_tensor`, `marginal_channel`, `is_markovian`, `deterministic_comb_causality_check`.
- Widget orchestration: `build_widget`, `render_dashboard_figure`, `format_indicator_text`, and UI constants.
- Folder-specific noise diagnosis: `diagnose_noise` can use common metrics and visualization later, but it mixes shared math with Agent-2 narrative heuristics.
