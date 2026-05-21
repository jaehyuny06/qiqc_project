# `choi_common` 라이브러리 구조 제안 한글판

이 문서는 실제 root package를 만들기 전 검토용입니다. 현재 skeleton 코드는 다음 위치에만 있습니다.

```text
94_integration/proposed_library/choi_common/
```

## 제안 구조

```text
choi_common/
├── __init__.py
├── representations.py   # Kraus/Choi/Stinespring/Natural 변환
├── channels.py          # 표준 채널 생성자
├── validation.py        # CP/TP 검사, partial trace
├── visualization.py     # Choi heatmap, Bloch sphere
├── metrics.py           # fidelity, trace distance, diamond norm
└── utils.py             # 공통 low-level helper
```

## 1. `representations.py`

역할:

- Kraus, Choi, Stinespring, Natural representation 사이의 변환
- Choi 또는 Kraus representation으로 채널 적용
- Choi channel composition

제안 함수:

```python
kraus_to_choi(kraus_ops: Sequence[np.ndarray]) -> Array
choi_to_kraus(
    choi: np.ndarray,
    tol: float = 1e-10,
    d_in: int | None = None,
    d_out: int | None = None,
) -> list[Array]
kraus_to_stinespring(kraus_ops: Sequence[np.ndarray]) -> Array
stinespring_to_kraus(isometry: np.ndarray, env_dim: int) -> list[Array]
choi_to_natural(
    choi: np.ndarray,
    d_in: int | None = None,
    d_out: int | None = None,
) -> Array
natural_to_choi(
    natural: np.ndarray,
    d_in: int | None = None,
    d_out: int | None = None,
) -> Array
apply_kraus_channel(rho: np.ndarray, kraus_ops: Sequence[np.ndarray]) -> Array
apply_choi_channel(
    choi: np.ndarray,
    rho: np.ndarray,
    d_in: int | None = None,
    d_out: int | None = None,
) -> Array
compose_choi_channels(
    choi_after: np.ndarray,
    choi_before: np.ndarray,
    d_mid: int | None = None,
) -> Array
```

기반 구현:

- `kraus_to_choi`: Agent 1 기반
- `choi_to_kraus`: Agent 1 기반, 차원 인자 추가
- `choi_to_natural`, `natural_to_choi`: Agent 1 구현 + Agent 4 signature
- `apply_choi_channel`: Agent 2/4 방식 기반
- `compose_choi_channels`: Agent 1/2를 통합하되 인자 순서를 명확히 함

중요 naming:

- `apply_channel`은 모호하므로 공용에서는 `apply_kraus_channel`로 바꿉니다.
- Choi 적용은 항상 `apply_choi_channel(choi, rho, ...)` 순서입니다.

## 2. `channels.py`

역할:

- 표준 quantum channel 생성자
- Kraus를 반환하는 함수와 Choi를 반환하는 함수를 분리
- depolarizing convention 차이를 명시

제안 함수:

```python
pauli_matrices() -> dict[str, Array]
identity_channel(d: int = 2) -> list[Array]
identity_channel_choi(d: int = 2) -> Array
unitary_channel_choi(unitary: np.ndarray, check_unitary: bool = True) -> Array
pauli_channel(px: float, py: float, pz: float) -> list[Array]
pauli_channel_choi(probabilities: Mapping[str, float]) -> Array
bit_flip_channel(p: float) -> list[Array]
bit_flip_channel_choi(p: float) -> Array
phase_flip_channel(p: float) -> list[Array]
phase_flip_channel_choi(p: float) -> Array
depolarizing_channel(
    p: float,
    d: int = 2,
    convention: Literal["replacement", "pauli_error"] = "replacement",
) -> list[Array]
depolarizing_channel_choi(
    p: float,
    d: int = 2,
    convention: Literal["replacement", "pauli_error"] = "replacement",
) -> Array
amplitude_damping_channel(gamma: float) -> list[Array]
amplitude_damping_channel_choi(gamma: float) -> Array
phase_damping_channel(gamma: float) -> list[Array]
phase_damping_channel_choi(gamma: float) -> Array
z_rotation_channel_choi(theta: float) -> Array
unital_qubit_channel_choi(lambda_x: float, lambda_y: float, lambda_z: float) -> Array
mixed_choi(choi_a: np.ndarray, choi_b: np.ndarray, alpha: float) -> Array
depolarizing_after_unitary(
    unitary: np.ndarray,
    p: float,
    convention: Literal["pauli_error", "replacement"] = "pauli_error",
) -> Array
amplitude_damping_after_unitary(unitary: np.ndarray, gamma: float) -> Array
two_qubit_depolarizing_after_unitary(
    unitary: np.ndarray,
    p: float,
    convention: Literal["pauli_error"] = "pauli_error",
) -> Array
```

기반 구현:

- Kraus 반환 함수: Agent 1과 Agent 5
- Choi 반환 함수: Agent 3
- unitary 뒤 noise helper: Agent 2
- `unital_qubit_channel_choi`, `mixed_choi`: Agent 5

가장 중요한 설계 결정:

`depolarizing_channel`은 `convention` 인자를 가져야 합니다. 그렇지 않으면 Agent 1/3과 Agent 2/5의 `p` 의미가 충돌합니다.

권장 기본값:

```python
convention="replacement"
```

이 기본값은 Agent 1/3과 수학 설명에 맞습니다. Agent 2/5는 migration할 때 `convention="pauli_error"`를 명시하면 됩니다.

## 3. `validation.py`

역할:

- partial trace
- CP 검사
- TP 검사
- unital 검사
- Choi rank와 TP residual

제안 함수:

```python
partial_trace(operator: np.ndarray, dims: Sequence[int], trace_out: Sequence[int]) -> Array
partial_trace_output(choi: np.ndarray, d_in: int, d_out: int) -> Array
partial_trace_input(choi: np.ndarray, d_in: int, d_out: int) -> Array
is_cp(choi: np.ndarray, tol: float = 1e-9, require_hermitian: bool = True) -> bool
is_tp(
    choi: np.ndarray,
    d_in: int,
    d_out: int | None = None,
    tol: float = 1e-9,
) -> bool
is_unital(
    choi: np.ndarray,
    d_in: int,
    d_out: int | None = None,
    tol: float = 1e-9,
) -> bool
choi_rank(choi: np.ndarray, tol: float = 1e-10) -> int
tp_residual(choi: np.ndarray, d_in: int, d_out: int | None = None) -> float
```

기반 구현:

- `partial_trace`: Agent 4
- `is_cp`: Agent 1의 strict check
- `is_tp`: Agent 2 signature
- `is_unital`, `choi_rank`: Agent 1
- `tp_residual`: Agent 2/5 indicator logic

중요한 변화:

Agent 5의 `is_tp(choi)`는 공용화 후 아래처럼 바뀌어야 합니다.

```python
is_tp(choi, d_in=2, d_out=2)
```

## 4. `visualization.py`

역할:

- Choi 행렬 heatmap
- qubit Bloch deformation
- Choi eigenspectrum
- 표시용 eigenoperator 추출

제안 함수:

```python
plot_choi_heatmap(
    choi: np.ndarray,
    *,
    title: str | None = None,
    axes: Sequence[Any] | None = None,
    include_abs: bool = True,
) -> Any
bloch_affine_map(choi: np.ndarray) -> tuple[np.ndarray, np.ndarray]
choi_to_pauli_transfer(choi: np.ndarray) -> Array
plot_bloch_deformation(choi: np.ndarray, ax: Any | None = None) -> Any
plot_eigenspectrum(choi: np.ndarray, ax: Any | None = None, tol: float = 1e-9) -> Any
extract_kraus_display(choi: np.ndarray, tol: float = 1e-10) -> list[tuple[float, Array]]
```

기반 구현:

- Agent 5의 axes-first plotting 구조
- Agent 2의 real/imag/abs heatmap 구성
- Agent 5의 `bloch_affine_map`
- Agent 2의 `choi_to_pauli_transfer`

주의:

- Bloch 관련 함수는 qubit 전용입니다.
- `plot_choi_heatmap`은 real/imag에는 `RdBu_r`, magnitude에는 `viridis`를 사용해야 합니다.

## 5. `metrics.py`

역할:

- process fidelity
- average gate fidelity
- trace distance
- diamond norm SDP
- channel discrimination probability

제안 class/function:

```python
@dataclass(frozen=True)
class DiamondNormResult:
    value: float
    rho: Array
    witness: Array
    solver: str
    status: str

raw_process_fidelity(choi_actual: np.ndarray, choi_ideal: np.ndarray) -> float
process_fidelity(
    choi_actual: np.ndarray,
    choi_ideal: np.ndarray,
    clip: bool = True,
) -> float
average_gate_fidelity(choi_actual: np.ndarray, choi_ideal: np.ndarray, d: int) -> float
trace_distance(rho: np.ndarray, sigma: np.ndarray) -> float
solve_diamond_norm_sdp(
    choi_diff: np.ndarray,
    d_in: int,
    d_out: int,
    solver: str | None = None,
    eps: float = 1e-6,
    max_iters: int = 50_000,
) -> DiamondNormResult
diamond_norm_sdp(
    choi_diff: np.ndarray,
    d_in: int,
    d_out: int,
    solver: str | None = None,
    eps: float = 1e-6,
    max_iters: int = 50_000,
) -> float
diamond_norm_distance(
    choi_actual: np.ndarray,
    choi_ideal: np.ndarray,
    d_in: int | None = None,
    d_out: int | None = None,
) -> float
diamond_distance_proxy(
    choi_actual: np.ndarray,
    choi_ideal: np.ndarray,
    d: int | None = None,
) -> float
analytical_pauli_diamond_norm(
    probabilities_0: Mapping[str, float],
    probabilities_1: Mapping[str, float],
) -> float
analytical_depolarizing_diamond_norm(p0: float, p1: float, d: int = 2) -> float
discrimination_probability(
    choi_0: np.ndarray,
    choi_1: np.ndarray,
    d_in: int | None = None,
    d_out: int | None = None,
) -> float
```

기반 구현:

- Diamond norm SDP: Agent 3
- Fidelity: Agent 2
- Trace distance: Agent 4
- Diamond distance wrapper: Agent 2

주의:

- `diamond_norm_sdp`와 analytical formula만 diamond norm이라고 부릅니다.
- Choi nuclear norm 기반 heuristic은 반드시 `diamond_distance_proxy`로 부릅니다.

## 6. `utils.py`

역할:

- domain module들이 공통으로 쓰는 low-level helper
- plotting, cvxpy, qiskit 같은 무거운 dependency는 넣지 않습니다.

제안 함수:

```python
as_complex_matrix(matrix: Any, name: str = "matrix", square: bool = False) -> Array
dagger(matrix: np.ndarray) -> Array
hermitian_part(matrix: np.ndarray) -> Array
validate_probability(value: float, name: str = "p") -> float
infer_choi_dims(
    choi: np.ndarray,
    d_in: int | None = None,
    d_out: int | None = None,
    tol: float = 1e-8,
) -> tuple[int, int]
infer_natural_dims(
    natural: np.ndarray,
    d_in: int | None = None,
    d_out: int | None = None,
) -> tuple[int, int]
```

기반 구현:

- `dagger`: Agent 2/4
- `hermitian_part`: Agent 2/3
- `validate_probability`: Agent 1/5
- dimension inference: Agent 1/3/5

주의:

- 차원 추론은 편의 기능일 뿐입니다.
- rectangular channel이나 non-TP map에서는 명시적으로 `d_in`, `d_out`을 넣는 것이 더 안전합니다.
