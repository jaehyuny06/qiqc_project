# Migration Plan 한글판

이 문서는 `choi_common` 공용 라이브러리를 실제로 구현한 뒤, 5개 producer 폴더를 어떻게 옮길지에 대한 제안입니다. 지금 단계에서는 producer 파일을 수정하지 않습니다.

## 먼저 확정해야 할 전역 결정

1. Choi convention은 그대로 유지합니다.
   `C_E = sum_ij |i><j|_A tensor E(|i><j|)_B`
2. Choi 행렬로 채널을 적용하는 표준 함수는 다음으로 통일합니다.
   `apply_choi_channel(choi, rho, d_in=None, d_out=None)`
3. TP 검사의 표준 함수는 다음으로 통일합니다.
   `is_tp(choi, d_in, d_out=None, tol=1e-9)`
4. depolarizing channel의 기본 `p` 의미는 replacement probability로 둡니다.
   `E_p(rho) = (1-p)rho + p Tr(rho) I/d`
5. Agent 2와 Agent 5는 현재 `p`를 Pauli error 전체 확률로 쓰므로 migration 때 `convention="pauli_error"`를 명시해야 합니다.

## Agent 1: `01_theory`

현재 주요 import:

```python
from channel_reps import (
    amplitude_damping_channel,
    apply_channel,
    bit_flip_channel,
    choi_rank,
    choi_to_kraus,
    choi_to_natural,
    compose_channels_choi,
    depolarizing_channel,
    identity_channel,
    is_cp,
    is_tp,
    is_unital,
    kraus_to_choi,
    kraus_to_stinespring,
    natural_to_choi,
    pauli_channel,
    phase_damping_channel,
    phase_flip_channel,
    random_channel,
    stinespring_to_kraus,
)
```

공용 라이브러리 적용 후:

```python
from choi_common.channels import (
    amplitude_damping_channel,
    bit_flip_channel,
    depolarizing_channel,
    identity_channel,
    pauli_channel,
    phase_damping_channel,
    phase_flip_channel,
)
from choi_common.representations import (
    apply_kraus_channel,
    choi_to_kraus,
    choi_to_natural,
    compose_choi_channels,
    kraus_to_choi,
    kraus_to_stinespring,
    natural_to_choi,
    stinespring_to_kraus,
)
from choi_common.validation import choi_rank, is_cp, is_tp, is_unital
```

수정할 호출:

- `apply_channel(rho, kraus_ops)` -> `apply_kraus_channel(rho, kraus_ops)`
- `compose_channels_choi(choi1, choi2)`는 의미가 `E2 o E1`입니다.
  공용에서는 다음처럼 명시하는 것이 좋습니다.

```python
compose_choi_channels(choi_after=choi2, choi_before=choi1)
```

주의:

- `random_channel`은 현재 중복이 아니므로 일단 Agent 1에 남겨도 됩니다.
- `is_tp(choi, d_in=2)`는 공용 signature에서도 그대로 동작합니다.

## Agent 2: `02_ibm_experiment`

현재 주요 import:

```python
from qpt_tools import (
    amplitude_damping_after_unitary,
    choi_from_unitary,
    depolarizing_after_unitary,
    diagnose_noise,
    is_cp,
    is_tp,
    linear_inversion_choi,
    matrix_to_json_dict,
    mle_choi,
    plot_bloch_deformation,
    plot_choi_heatmap,
    save_json,
    simulate_output_states_from_choi,
    two_qubit_depolarizing_after_unitary,
)
```

공용으로 옮길 수 있는 import:

```python
from choi_common.channels import (
    amplitude_damping_after_unitary,
    depolarizing_after_unitary,
    two_qubit_depolarizing_after_unitary,
    unitary_channel_choi,
)
from choi_common.validation import is_cp, is_tp
from choi_common.visualization import plot_bloch_deformation, plot_choi_heatmap
```

Agent 2에 남기는 것이 좋은 함수:

```python
from qpt_tools import (
    diagnose_noise,
    linear_inversion_choi,
    matrix_to_json_dict,
    mle_choi,
    save_json,
    simulate_output_states_from_choi,
)
```

수정할 호출:

- `choi_from_unitary(U)` -> `unitary_channel_choi(U)`
- `depolarizing_after_unitary(U, p)`는 현재 의미를 보존하려면 다음처럼 써야 합니다.

```python
depolarizing_after_unitary(U, p, convention="pauli_error")
```

- `plot_choi_heatmap(choi, title)`는 공용 API가 keyword-only라면 다음처럼 바뀔 수 있습니다.

```python
plot_choi_heatmap(choi, title=title)
```

추천 순서:

1. 먼저 `qpt_tools.py` 내부에서 `choi_common`을 import합니다.
2. 기존 함수 이름은 wrapper로 남깁니다.
3. 테스트가 통과하면 notebook import를 천천히 바꿉니다.

## Agent 3: `03_sdp_discrimination`

현재 notebook은 이렇게 씁니다.

```python
import sdp_tools as sdp
```

가장 안전한 migration:

- notebook은 당장 그대로 둡니다.
- `sdp_tools.py` 내부 구현만 `choi_common`을 사용하도록 바꿉니다.

`sdp_tools.py` 내부에서 공용화할 수 있는 import:

```python
from choi_common.channels import (
    amplitude_damping_channel_choi,
    bit_flip_channel_choi,
    depolarizing_channel_choi,
    identity_channel_choi,
    pauli_channel_choi,
    pauli_matrices,
    phase_damping_channel_choi,
    phase_flip_channel_choi,
    unitary_channel_choi,
    z_rotation_channel_choi,
)
from choi_common.metrics import (
    DiamondNormResult,
    analytical_depolarizing_diamond_norm,
    analytical_pauli_diamond_norm,
    diamond_norm_sdp,
    discrimination_probability,
    solve_diamond_norm_sdp,
)
from choi_common.representations import apply_choi_channel, kraus_to_choi
from choi_common.validation import is_cp, is_tp
```

Agent 3에 남기는 것이 좋은 함수:

- `optimal_input_state`
- `optimal_povm`
- `tensor_power_choi`
- `n_shot_discrimination`
- `product_strategy_discrimination`

주의:

- Agent 3의 `depolarizing_channel_choi(p)`는 이미 replacement probability convention입니다.
- 따라서 공용 기본값과 충돌하지 않습니다.

## Agent 4: `04_quantum_combs`

현재 주요 import:

```python
from combs_tools import (
    apply_choi_channel,
    blp_measure,
    choi_to_natural,
    comb_global_trace_preservation_check,
    deterministic_comb_causality_check,
    is_markovian,
    marginal_channel,
    natural_to_choi,
    rhp_measure,
    trace_distance,
)
```

공용으로 옮길 수 있는 import:

```python
from choi_common.metrics import trace_distance
from choi_common.representations import (
    apply_choi_channel,
    choi_to_natural,
    natural_to_choi,
)
from choi_common.validation import partial_trace
```

Agent 4에 남기는 것이 좋은 함수:

```python
from combs_tools import (
    blp_measure,
    comb_global_trace_preservation_check,
    deterministic_comb_causality_check,
    is_markovian,
    marginal_channel,
    rhp_measure,
)
```

수정할 호출:

- `apply_choi_channel(choi, rho)`는 그대로 유지됩니다.
- `choi_to_natural(C, 2, 2)`도 그대로 유지됩니다.
- `natural_to_choi(S, 2, 2)`도 그대로 유지됩니다.
- legacy 함수 `apply_choi_channel_legacy(rho, choi, ...)`는 필요하면 Agent 4 내부 wrapper로만 남깁니다.

## Agent 5: `05_interactive_widget`

현재 notebook은 `widget_core.py`를 import합니다.

```python
from widget_core import (
    CHANNEL_TYPES,
    apply_choi_channel,
    build_widget,
    compute_indicators,
    format_indicator_text,
    get_channel_choi,
    render_dashboard_figure,
)
```

추천 migration:

- notebook은 당장 그대로 둡니다.
- `widget_core.py` 내부에서 `channel_utils.py` 대신 `choi_common`을 사용합니다.

현재 `widget_core.py`가 `channel_utils.py`에서 가져오는 것:

```python
from channel_utils import (
    I2,
    PAULIS,
    amplitude_damping_kraus,
    bit_flip_kraus,
    depolarizing_kraus,
    identity_kraus,
    is_cp,
    is_tp,
    kraus_to_choi,
    mixed_choi,
    partial_trace_output,
    pauli_kraus,
    phase_damping_kraus,
    phase_flip_kraus,
    unital_choi,
)
```

공용 라이브러리 적용 후:

```python
from choi_common.channels import (
    amplitude_damping_channel,
    bit_flip_channel,
    depolarizing_channel,
    identity_channel,
    mixed_choi,
    pauli_channel,
    pauli_matrices,
    phase_damping_channel,
    phase_flip_channel,
    unital_qubit_channel_choi,
)
from choi_common.representations import apply_choi_channel, kraus_to_choi
from choi_common.validation import is_cp, is_tp, partial_trace_output
```

수정할 호출:

```python
identity_kraus()
```

를 다음으로 변경:

```python
identity_channel(2)
```

```python
depolarizing_kraus(p)
```

를 다음으로 변경:

```python
depolarizing_channel(p, d=2, convention="pauli_error")
```

나머지 변경:

- `amplitude_damping_kraus(gamma)` -> `amplitude_damping_channel(gamma)`
- `phase_damping_kraus(gamma)` -> `phase_damping_channel(gamma)`
- `bit_flip_kraus(p)` -> `bit_flip_channel(p)`
- `phase_flip_kraus(p)` -> `phase_flip_channel(p)`
- `pauli_kraus(p_x, p_y, p_z)` -> `pauli_channel(p_x, p_y, p_z)`
- `unital_choi(...)` -> `unital_qubit_channel_choi(...)`
- `partial_trace_output(choi)` -> `partial_trace_output(choi, d_in=2, d_out=2)`
- `is_tp(choi)` -> `is_tp(choi, d_in=2, d_out=2)`

상수 변경:

```python
paulis = pauli_matrices()
I2 = paulis["I"]
PAULIS = (paulis["X"], paulis["Y"], paulis["Z"])
```

Agent 5에 남기는 것이 좋은 것:

- `CHANNEL_TYPES`
- `get_channel_choi`
- `build_widget`
- `compute_indicators`
- `format_indicator_text`
- `render_dashboard_figure`
- widget-specific dashboard layout

## 안전한 적용 순서

Step 4.2에서 실제 구현할 때는 한 번에 다 바꾸지 않는 것이 좋습니다.

권장 순서:

1. root에 실제 `choi_common` 패키지를 구현합니다.
2. 공통 함수 equivalence test를 추가합니다.
   특히 `kraus_to_choi`, `choi_to_natural`, `natural_to_choi`, `is_tp`, depolarizing convention을 확인합니다.
3. producer module 내부에서 `choi_common`을 import하도록 바꿉니다.
4. 기존 public 함수 이름은 wrapper로 남겨 notebook이 깨지지 않게 합니다.
5. 테스트가 통과하면 notebook import를 직접 `choi_common`으로 바꿉니다.
6. 나중에 더 이상 쓰지 않는 wrapper를 제거합니다.

## Signature 변경 체크리스트

아래 항목은 실제 migration 때 꼭 확인해야 합니다.

- `apply_channel` -> `apply_kraus_channel`
- `compose_channels_choi(choi1, choi2)` -> `compose_choi_channels(choi_after, choi_before)`
- Agent 5의 `is_tp(choi)` -> `is_tp(choi, d_in=2, d_out=2)`
- Agent 5의 `partial_trace_output(choi)` -> `partial_trace_output(choi, d_in=2, d_out=2)`
- `choi_from_unitary` -> `unitary_channel_choi`
- Agent 2/5의 depolarizing 함수는 `convention="pauli_error"` 명시
- `plot_choi_heatmap(choi, title)`는 필요하면 `plot_choi_heatmap(choi, title=title)`로 변경
