# Proposed `choi_common` Library Structure

The proposed code lives under `94_integration/proposed_library/choi_common/` for review only. It is not the real root-level package yet.

## Package Layout

```text
choi_common/
├── __init__.py
├── representations.py
├── channels.py
├── validation.py
├── visualization.py
├── metrics.py
└── utils.py
```

## `representations.py`

Shared conversions and channel-application helpers.

| Function | Signature | Source folders | Base notes |
| --- | --- | --- | --- |
| `kraus_to_choi` | `kraus_to_choi(kraus_ops: Sequence[np.ndarray]) -> Array` | 01, 02, 03, 04, 05 | Base on Agent 1 vectorized implementation plus Agent 3/5 validation. |
| `choi_to_kraus` | `choi_to_kraus(choi: np.ndarray, tol: float = 1e-10, d_in: int \| None = None, d_out: int \| None = None) -> list[Array]` | 01, 02, 05 | Base on Agent 1, but add explicit dimensions. |
| `kraus_to_stinespring` | `kraus_to_stinespring(kraus_ops: Sequence[np.ndarray]) -> Array` | 01 | Not duplicated but belongs with representations. |
| `stinespring_to_kraus` | `stinespring_to_kraus(isometry: np.ndarray, env_dim: int) -> list[Array]` | 01 | Not duplicated but belongs with representations. |
| `choi_to_natural` | `choi_to_natural(choi: np.ndarray, d_in: int \| None = None, d_out: int \| None = None) -> Array` | 01, 04 | Use Agent 1 tensor method with Agent 4 signature. |
| `natural_to_choi` | `natural_to_choi(natural: np.ndarray, d_in: int \| None = None, d_out: int \| None = None) -> Array` | 01, 04 | Same convention as `choi_to_natural`; column stacking. |
| `apply_kraus_channel` | `apply_kraus_channel(rho: np.ndarray, kraus_ops: Sequence[np.ndarray]) -> Array` | 01, 05 | Rename `apply_channel` to avoid ambiguity with Choi form. |
| `apply_choi_channel` | `apply_choi_channel(choi: np.ndarray, rho: np.ndarray, d_in: int \| None = None, d_out: int \| None = None) -> Array` | 02, 03, 04, 05 | Use project-standard name and argument order. |
| `compose_choi_channels` | `compose_choi_channels(choi_after: np.ndarray, choi_before: np.ndarray, d_mid: int \| None = None) -> Array` | 01, 02 | Standardize order as `after o before`. |

Docstring standard:

- State unnormalized Choi convention and input-first tensor order.
- State Kraus shape `(d_out, d_in)`.
- State natural representation uses column-stacking vectorization.

## `channels.py`

Standard channels and Choi convenience constructors.

| Function | Signature | Source folders | Base notes |
| --- | --- | --- | --- |
| `pauli_matrices` | `pauli_matrices() -> dict[str, Array]` | 03, 05 | Use Agent 3 labels `I`, `X`, `Y`, `Z`; Agent 5 constants can disappear. |
| `identity_channel` | `identity_channel(d: int = 2) -> list[Array]` | 01, 05 | Base on Agent 1; `identity_kraus` becomes compatibility alias if needed. |
| `identity_channel_choi` | `identity_channel_choi(d: int = 2) -> Array` | 03 | Convenience wrapper over `kraus_to_choi`. |
| `unitary_channel_choi` | `unitary_channel_choi(unitary: np.ndarray, check_unitary: bool = True) -> Array` | 02, 03 | Agent 3 validates unitarity; Agent 2 name was `choi_from_unitary`. |
| `pauli_channel` | `pauli_channel(px: float, py: float, pz: float) -> list[Array]` | 01, 05 | Base on Agent 1 naming, support Agent 5 probability validation. |
| `pauli_channel_choi` | `pauli_channel_choi(probabilities: Mapping[str, float]) -> Array` | 03 | Base on Agent 3. |
| `bit_flip_channel` | `bit_flip_channel(p: float) -> list[Array]` | 01, 05 | Same semantics across producers. |
| `bit_flip_channel_choi` | `bit_flip_channel_choi(p: float) -> Array` | 03 | Wrapper over `bit_flip_channel`. |
| `phase_flip_channel` | `phase_flip_channel(p: float) -> list[Array]` | 01, 05 | Same semantics across producers. |
| `phase_flip_channel_choi` | `phase_flip_channel_choi(p: float) -> Array` | 03 | Wrapper over `phase_flip_channel`. |
| `depolarizing_channel` | `depolarizing_channel(p: float, d: int = 2, convention: Literal["replacement", "pauli_error"] = "replacement") -> list[Array]` | 01, 05 | Must document `p` convention. Default matches Agents 1/3. |
| `depolarizing_channel_choi` | `depolarizing_channel_choi(p: float, d: int = 2, convention: Literal["replacement", "pauli_error"] = "replacement") -> Array` | 03 | Base on Agent 3; support Agent 2/5 convention explicitly. |
| `amplitude_damping_channel` | `amplitude_damping_channel(gamma: float) -> list[Array]` | 01, 05 | Same semantics across producers. |
| `amplitude_damping_channel_choi` | `amplitude_damping_channel_choi(gamma: float) -> Array` | 03 | Wrapper over Kraus constructor. |
| `phase_damping_channel` | `phase_damping_channel(gamma: float) -> list[Array]` | 01, 05 | Same semantics across producers. |
| `phase_damping_channel_choi` | `phase_damping_channel_choi(gamma: float) -> Array` | 03 | Wrapper over Kraus constructor. |
| `z_rotation_channel_choi` | `z_rotation_channel_choi(theta: float) -> Array` | 03 | Useful for Agent 3 examples. |
| `unital_qubit_channel_choi` | `unital_qubit_channel_choi(lambda_x: float, lambda_y: float, lambda_z: float) -> Array` | 05 | Keep non-CP-capable behavior documented for visualization. |
| `mixed_choi` | `mixed_choi(choi_a: np.ndarray, choi_b: np.ndarray, alpha: float) -> Array` | 05 | Generic convex mixture helper. |
| `depolarizing_after_unitary` | `depolarizing_after_unitary(unitary: np.ndarray, p: float, convention: Literal["pauli_error", "replacement"] = "pauli_error") -> Array` | 02 | Keep Agent 2 default to preserve current QPT examples. |
| `amplitude_damping_after_unitary` | `amplitude_damping_after_unitary(unitary: np.ndarray, gamma: float) -> Array` | 02 | Useful QPT fixture helper. |
| `two_qubit_depolarizing_after_unitary` | `two_qubit_depolarizing_after_unitary(unitary: np.ndarray, p: float, convention: Literal["pauli_error"] = "pauli_error") -> Array` | 02 | Keep as explicit two-qubit fixture helper. |

Docstring standard:

- Constructors returning Kraus operators should say so clearly.
- Constructors returning Choi matrices should end in `_choi`.
- Depolarizing functions must name the parameter convention.

## `validation.py`

Physicality checks and tensor traces.

| Function | Signature | Source folders | Base notes |
| --- | --- | --- | --- |
| `partial_trace` | `partial_trace(operator: np.ndarray, dims: Sequence[int], trace_out: Sequence[int]) -> Array` | 04 | Base on Agent 4 generic tensor trace. |
| `partial_trace_output` | `partial_trace_output(choi: np.ndarray, d_in: int, d_out: int) -> Array` | 01, 02, 03, 05 | Wrapper over generic trace for Choi output system. |
| `partial_trace_input` | `partial_trace_input(choi: np.ndarray, d_in: int, d_out: int) -> Array` | 01 | Useful for unitality. |
| `is_cp` | `is_cp(choi: np.ndarray, tol: float = 1e-9, require_hermitian: bool = True) -> bool` | 01, 02, 03, 05 | Default should preserve Agent 1 strictness. |
| `is_tp` | `is_tp(choi: np.ndarray, d_in: int, d_out: int \| None = None, tol: float = 1e-9) -> bool` | 01, 02, 03, 05 | Matches glossary. |
| `is_unital` | `is_unital(choi: np.ndarray, d_in: int, d_out: int \| None = None, tol: float = 1e-9) -> bool` | 01 | Generalize Agent 1. |
| `choi_rank` | `choi_rank(choi: np.ndarray, tol: float = 1e-10) -> int` | 01, 05 indicators | Shared rank diagnostic. |
| `tp_residual` | `tp_residual(choi: np.ndarray, d_in: int, d_out: int \| None = None) -> float` | 02, 05 indicators | Common scalar diagnostic. |

Docstring standard:

- `is_tp` checks `Tr_B(C_E) = I_A`.
- `partial_trace_output` traces the output tensor factor, not the second matrix axis.

## `visualization.py`

Matplotlib visualization helpers. These should remain optional-use helpers; importing non-plotting modules should not require Matplotlib.

| Function | Signature | Source folders | Base notes |
| --- | --- | --- | --- |
| `plot_choi_heatmap` | `plot_choi_heatmap(choi: np.ndarray, *, title: str \| None = None, axes: Sequence[Any] \| None = None, include_abs: bool = True) -> Any` | 02, 05 | Axes-first Agent 5 style plus Agent 2 magnitude panel. |
| `bloch_affine_map` | `bloch_affine_map(choi: np.ndarray) -> tuple[np.ndarray, np.ndarray]` | 05, 02 diagnostics | Base on Agent 5. |
| `choi_to_pauli_transfer` | `choi_to_pauli_transfer(choi: np.ndarray) -> Array` | 02 | Useful for Bloch/noise diagnostics. |
| `plot_bloch_deformation` | `plot_bloch_deformation(choi: np.ndarray, ax: Any \| None = None) -> Any` | 02, 05 | Combine scatter and ellipsoid modes later. |
| `plot_eigenspectrum` | `plot_eigenspectrum(choi: np.ndarray, ax: Any \| None = None, tol: float = 1e-9) -> Any` | 05 | Base on Agent 5. |
| `extract_kraus_display` | `extract_kraus_display(choi: np.ndarray, tol: float = 1e-10) -> list[tuple[float, Array]]` | 05 | Diagnostic display only; not `choi_to_kraus`. |

Docstring standard:

- Mark Bloch functions as qubit-only.
- Use `RdBu_r` for real/imaginary Choi panels and `viridis` for magnitude.

## `metrics.py`

Distances, fidelities, and discrimination metrics.

| Function/Class | Signature | Source folders | Base notes |
| --- | --- | --- | --- |
| `DiamondNormResult` | dataclass with `value`, `rho`, `witness`, `solver`, `status` | 03 | Use Agent 3 result shape. |
| `raw_process_fidelity` | `raw_process_fidelity(choi_actual: np.ndarray, choi_ideal: np.ndarray) -> float` | 02, 05 indicators | Base on Agent 2. |
| `process_fidelity` | `process_fidelity(choi_actual: np.ndarray, choi_ideal: np.ndarray, clip: bool = True) -> float` | 02, 05 indicators | Base on Agent 2, expose clip behavior. |
| `average_gate_fidelity` | `average_gate_fidelity(choi_actual: np.ndarray, choi_ideal: np.ndarray, d: int) -> float` | 02 | Base on Agent 2. |
| `trace_distance` | `trace_distance(rho: np.ndarray, sigma: np.ndarray) -> float` | 04 | Base on Agent 4. |
| `solve_diamond_norm_sdp` | `solve_diamond_norm_sdp(choi_diff: np.ndarray, d_in: int, d_out: int, solver: str \| None = None, eps: float = 1e-6, max_iters: int = 50_000) -> DiamondNormResult` | 03, 02 | Base on Agent 3. |
| `diamond_norm_sdp` | `diamond_norm_sdp(choi_diff: np.ndarray, d_in: int, d_out: int, solver: str \| None = None, eps: float = 1e-6, max_iters: int = 50_000) -> float` | 02, 03 | Float wrapper. |
| `diamond_norm_distance` | `diamond_norm_distance(choi_actual: np.ndarray, choi_ideal: np.ndarray, d_in: int \| None = None, d_out: int \| None = None) -> float` | 02 | Half-diamond distance wrapper. |
| `diamond_distance_proxy` | `diamond_distance_proxy(choi_actual: np.ndarray, choi_ideal: np.ndarray, d: int \| None = None) -> float` | 02 | Explicitly heuristic Choi nuclear-norm proxy. |
| `analytical_pauli_diamond_norm` | `analytical_pauli_diamond_norm(probabilities_0: Mapping[str, float], probabilities_1: Mapping[str, float]) -> float` | 03 | Base on Agent 3. |
| `analytical_depolarizing_diamond_norm` | `analytical_depolarizing_diamond_norm(p0: float, p1: float, d: int = 2) -> float` | 03 | Applies to replacement-probability depolarizing convention. |
| `discrimination_probability` | `discrimination_probability(choi_0: np.ndarray, choi_1: np.ndarray, d_in: int \| None = None, d_out: int \| None = None) -> float` | 03 | Useful shared channel-discrimination metric. |

Docstring standard:

- Use "diamond norm" only for SDP or analytical exact results.
- Use "diamond-distance proxy" for the Choi nuclear-norm heuristic.

## `utils.py`

Low-level helpers with no domain-specific side effects.

| Function | Signature | Source folders | Base notes |
| --- | --- | --- | --- |
| `as_complex_matrix` | `as_complex_matrix(matrix: Any, name: str = "matrix", square: bool = False) -> Array` | 01, 03 | Generalize matrix validation. |
| `dagger` | `dagger(matrix: np.ndarray) -> Array` | 02, 04 | Shared conjugate transpose. |
| `hermitian_part` | `hermitian_part(matrix: np.ndarray) -> Array` | 02, 03 | Shared Hermitian projection. |
| `validate_probability` | `validate_probability(value: float, name: str = "p") -> float` | 01, 05 | Return validated float. |
| `infer_choi_dims` | `infer_choi_dims(choi: np.ndarray, d_in: int \| None = None, d_out: int \| None = None, tol: float = 1e-8) -> tuple[int, int]` | 01, 03, 05 | Prefer explicit dimensions; infer square as fallback. |
| `infer_natural_dims` | `infer_natural_dims(natural: np.ndarray, d_in: int \| None = None, d_out: int \| None = None) -> tuple[int, int]` | 01, 04 | Shared natural-dimension inference. |

Docstring standard:

- Inference helpers should document limitations for rectangular and non-TP maps.
