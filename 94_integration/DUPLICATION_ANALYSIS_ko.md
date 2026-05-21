# 중복 분석 한글 요약

이 문서는 5개 생산자 폴더에서 겹치는 함수와 유틸리티를 공용 라이브러리로 옮기기 전에 정리한 한글판입니다. 기준은 `92_validation_consistency/UNIFIED_GLOSSARY.md`입니다.

공통 기준:

- Choi 행렬은 정규화하지 않은 convention을 사용합니다.
- 입력 시스템 `A`가 먼저 오고 출력 시스템 `B`가 뒤에 옵니다.
- Kraus 연산자는 `(d_out, d_in)` 모양입니다.
- trace-preserving 조건은 `Tr_B(C_E) = I_A`입니다.

## 전체 결론

가장 많이 중복된 부분은 다음입니다.

- Kraus ↔ Choi 변환
- Choi 행렬로 채널 적용하기
- CP/TP 검사
- depolarizing, amplitude damping 같은 표준 채널 생성자
- Choi heatmap, Bloch sphere 시각화
- process fidelity, diamond norm 관련 metric

공용 라이브러리의 기본 재료는 이렇게 잡는 것이 좋습니다.

- `01_theory/channel_reps.py`: 표현 변환의 가장 일반적인 기반
- `04_quantum_combs/combs_tools.py`: 일반 partial trace와 명시적 차원 인자 방식
- `03_sdp_discrimination/sdp_tools.py`: diamond norm SDP와 Choi를 바로 반환하는 채널 생성자
- `05_interactive_widget/widget_core.py`: Bloch affine map과 시각화 구조
- `02_ibm_experiment/qpt_tools.py`: process fidelity, tomography 관련 metric과 실험용 유틸리티

## 1. `kraus_to_choi`

발견 위치:

- `01_theory/channel_reps.py`
- `02_ibm_experiment/qpt_tools.py`
- `03_sdp_discrimination/sdp_tools.py`
- `04_quantum_combs/combs_tools.py`
- `05_interactive_widget/channel_utils.py`

차이점:

- 5개 모두 같은 Choi convention을 사용합니다.
- Agent 1과 5는 Kraus 연산자 모양 검증이 가장 깔끔합니다.
- Agent 1은 vectorization 방식이라 코드가 짧고 일반적입니다.
- Agent 2, 3, 4, 5는 block loop 방식입니다.
- Agent 1, 2, 3, 5는 결과를 Hermitian으로 보정합니다.
- Agent 4는 Hermitian 보정을 하지 않습니다.

권장 기반:

- Agent 1 구현을 기본으로 쓰는 것이 좋습니다.
- 다만 입력 검증은 Agent 3/5 스타일을 반영하면 더 안전합니다.

주의할 점:

- Choi ordering이나 normalization 차이는 없습니다.
- 공용 함수는 결과를 Hermitian으로 보정할지 명확히 문서화해야 합니다.

## 2. `choi_to_kraus`

발견 위치:

- `01_theory/channel_reps.py`
- `02_ibm_experiment/qpt_tools.py`
- `05_interactive_widget/channel_utils.py`
- 관련 표시용 함수: `05_interactive_widget/widget_core.py:extract_kraus_display`

차이점:

- Agent 1은 TP 조건을 이용해 `(d_in, d_out)`을 추론하려고 시도합니다.
- Agent 2와 5는 대부분 square channel이라고 보고 `sqrt(shape)`로 추론합니다.
- Agent 5의 `extract_kraus_display`는 음수 eigenvalue도 보여주기 때문에 진짜 Kraus 변환이 아니라 진단용입니다.

권장 기반:

- Agent 1을 기반으로 하되, 공용 API에는 `d_in`, `d_out` 선택 인자를 추가하는 것이 좋습니다.

주의할 점:

- `extract_kraus_display`는 visualization 전용으로 두고 `choi_to_kraus`와 섞지 않아야 합니다.

## 3. Choi ↔ Natural Representation

발견 위치:

- `01_theory/channel_reps.py`
- `04_quantum_combs/combs_tools.py`

차이점:

- Agent 1은 차원을 내부에서 추론합니다.
- Agent 4는 `d_in`, `d_out`을 명시적으로 받을 수 있습니다.
- 둘 다 column-stacking vectorization을 사용하고, 테스트한 예제에서 결과가 일치합니다.

권장 기반:

- 구현 방식은 Agent 1의 tensor transpose 방식이 간결합니다.
- 함수 signature는 Agent 4처럼 `d_in=None, d_out=None`을 받는 것이 좋습니다.

주의할 점:

- docstring에 column-stacking이라고 반드시 적어야 합니다.

## 4. Choi 행렬로 채널 적용

발견 위치:

- Kraus form: Agent 1, Agent 5
- Choi form: Agent 2, Agent 3, Agent 4, Agent 5

현재 공통 이름:

```python
apply_choi_channel(choi, rho, d_in=None, d_out=None)
```

차이점:

- Agent 2에는 예전 순서인 `apply_channel_to_state(rho, choi, ...)`가 있습니다.
- Agent 4에도 legacy wrapper가 있습니다.
- Agent 5는 qubit 전용이며 출력도 Hermitian으로 보정합니다.
- 차원 추론 방식이 폴더마다 조금 다릅니다.

권장 기반:

- Agent 2/4 스타일처럼 `rho`에서 `d_in`을 추론하고 Choi 크기에서 `d_out`을 추론하는 방식이 실용적입니다.

주의할 점:

- 공용 API에서는 인자 순서를 `choi, rho`로 고정해야 합니다.
- 예전 `(rho, choi)` 순서는 각 producer 폴더의 호환 wrapper로만 남기는 것이 좋습니다.

## 5. CP/TP 검사와 Partial Trace

발견 위치:

- Agent 1, 2, 3, 5: `is_cp`, `is_tp`, output partial trace
- Agent 4: 일반적인 `partial_trace`

차이점:

- Agent 1의 `is_cp`는 Hermitian인지 먼저 확인합니다.
- Agent 2, 3, 5는 Hermitian part를 만든 뒤 eigenvalue만 확인합니다.
- `is_tp` signature가 서로 다릅니다.

권장 signature:

```python
is_tp(choi, d_in, d_out=None, tol=1e-9)
```

권장 기반:

- 일반 `partial_trace`는 Agent 4를 기반으로 합니다.
- `is_cp`는 Agent 1처럼 Hermitian 조건을 기본으로 검사하는 것이 안전합니다.
- `is_tp`는 Agent 2처럼 `d_out`을 선택 인자로 받는 방식이 좋습니다.

주의할 점:

- Agent 5의 `is_tp(choi)`는 공용 API로 옮기면 `is_tp(choi, d_in=2, d_out=2)`로 바뀌어야 합니다.

## 6. 표준 채널 생성자

발견 위치:

- Agent 1: Kraus를 반환하는 표준 채널 함수
- Agent 5: qubit용 Kraus helper
- Agent 3: Choi를 반환하는 표준 채널 함수
- Agent 2: unitary 뒤에 noise를 붙인 실험용 Choi 생성자

대표 중복:

- identity
- bit flip
- phase flip
- Pauli channel
- depolarizing
- amplitude damping
- phase damping

가장 중요한 의미 차이:

`depolarizing p`의 뜻이 다릅니다.

- Agent 1/3:
  `p`는 replacement probability입니다.
  `E(rho) = (1-p)rho + p Tr(rho) I/d`
- Agent 2/5:
  `p`는 Pauli error 전체 확률입니다.
  qubit에서 `I: 1-p`, `X/Y/Z: p/3`입니다.

권장 해결:

```python
depolarizing_channel(p, d=2, convention="replacement")
depolarizing_channel_choi(p, d=2, convention="replacement")
```

그리고 Agent 2/5를 migration할 때는 다음처럼 명시합니다.

```python
depolarizing_channel(p, d=2, convention="pauli_error")
```

## 7. Visualization

발견 위치:

- Agent 2: `plot_choi_heatmap`, `plot_bloch_deformation`
- Agent 5: `plot_choi_heatmap`, `plot_bloch_ellipsoid`, `plot_eigenspectrum`, `bloch_affine_map`

차이점:

- Agent 2는 figure를 내부에서 새로 만듭니다.
- Agent 5는 외부에서 받은 axes에 그리므로 dashboard에 재사용하기 좋습니다.
- Agent 2는 real, imaginary, absolute 세 패널을 그립니다.
- Agent 5는 real, imaginary 중심이고 Bloch affine map이 더 좋습니다.

권장 기반:

- Agent 5의 axes-first 방식을 기반으로 하고, Agent 2의 magnitude panel 옵션을 추가합니다.

주의할 점:

- Bloch 관련 함수는 qubit 전용입니다. 입력 Choi shape이 `(4, 4)`인지 검사해야 합니다.

## 8. Metrics와 Diamond Norm

발견 위치:

- Agent 2: process fidelity, average gate fidelity, diamond norm distance, noise diagnosis
- Agent 3: diamond norm SDP, analytical diamond norm, discrimination probability
- Agent 4: trace distance

차이점:

- Agent 2의 `diamond_norm_sdp`는 float만 반환합니다.
- Agent 3은 `DiamondNormResult` dataclass를 반환하는 solver와 float wrapper를 분리했습니다.
- Agent 2의 `diamond_norm_distance`는 `0.5 * diamond norm`입니다.
- Agent 2의 nuclear-norm 값은 diamond norm이 아니라 proxy로 표시되어야 합니다.

권장 기반:

- SDP 구조는 Agent 3을 기반으로 합니다.
- fidelity 함수는 Agent 2를 기반으로 합니다.
- `trace_distance`는 Agent 4에서 가져옵니다.

주의할 점:

- 정확한 SDP 또는 해석식이 아니면 "diamond norm"이라고 부르면 안 됩니다.
- heuristic 값은 반드시 `diamond_distance_proxy`처럼 이름에 proxy를 넣어야 합니다.

## 당장 공용화하지 않는 것이 좋은 것

다음은 중복도가 낮거나 각 agent의 역할에 강하게 묶여 있으므로 1차 공용 라이브러리에서는 제외하는 것이 좋습니다.

- IBM/Qiskit 실행 함수
- tomography reconstruction 함수
- quantum comb/process tensor 생성과 causality hierarchy
- widget UI 구성 함수
- Agent 2의 `diagnose_noise`

이 함수들은 나중에 공용 함수들을 내부에서 쓰도록 정리할 수 있지만, 처음부터 `choi_common`에 넣으면 범위가 너무 커집니다.
