# 코드 품질 및 재현성 검토

Validator-B는 기존 `qiskit_2025_1` 환경에서 각 notebook과 test suite를 실행했습니다. 실행 로그는 `execution_logs/`에 저장되어 있습니다. Producer 파일은 수정하지 않았습니다.

## 실행 결과

| Agent | Notebook 실행? | Test 통과? | Warning | Error |
|-------|----------------|------------|---------|-------|
| Agent-1 | Yes | Yes, 16 passed | Windows ZMQ runtime warning 1개 | 0 |
| Agent-2 | Yes | Yes, 3 passed | Windows ZMQ warning 1개, notebook missing-id warning 1개 | 0 |
| Agent-3 | Yes | Yes, 6 passed | Windows ZMQ runtime warning 1개 | 0 |
| Agent-4 | Yes | Yes, 6 passed | Windows ZMQ runtime warning 1개 | 0 |
| Agent-5 | Yes | Yes, 5 passed | Windows ZMQ runtime warning 1개 | 0 |

전체 combined test suite도 이전에 `36 passed`로 통과했습니다. ZMQ warning은 Windows 환경 특이 경고이며 실행에는 영향을 주지 않았습니다.

## Agent별 검토 결과

### Agent-1

#### Blockers (notebook 실패 또는 잘못된 결과)
- 없음.

#### 품질 이슈
- `01_theory/requirements.txt:1`-`6`은 정확한 version pin이 아니라 lower bound를 사용합니다. course development에는 충분하지만 장기 archival rerun에는 약합니다.
- Public function은 type hint와 docstring을 갖추고 있습니다. Test function에 docstring이 없는 것은 pytest에서는 일반적이므로 producer-code issue로 보지 않았습니다.

#### 제안
- 최종 통합 프로젝트에서 style을 강제할 예정이면 작은 `pyproject.toml` 또는 formatting note를 추가하세요.
- non-square 또는 non-TP Choi matrix를 다룰 수 있는 public dimension-aware inverse helper를 고려하세요.

### Agent-2

#### Blockers (notebook 실패 또는 잘못된 결과)
- 없음. Offline QPT path는 IBM credential 없이 실행됩니다.

#### 품질 이슈
- `02_ibm_experiment/qpt_tools.py:586`은 SDP로 계산한 diamond norm이 아니라 `diamond_distance_proxy`를 제공합니다. 이는 주로 수학 deliverable gap이지만 API 기대와도 관련됩니다.
- `02_ibm_experiment/qpt_tools.py:394`는 SCS-specific option을 SCS와 CLARABEL을 모두 시도하는 loop 안에서 사용합니다. 현재 환경에는 SCS가 설치되어 있어 통과하지만, SCS가 없고 CLARABEL만 쓰이는 환경에서는 solver-incompatible keyword 문제가 생길 수 있습니다.
- `02_ibm_experiment/requirements.txt:1`-`11`은 broad lower bound이며 pin이 없습니다. Qiskit 계열 package는 API 변화가 빠르므로 future reproducibility risk가 가장 큽니다.

#### 제안
- 현재 notebook과 호환되는 Qiskit-family version을 pin하거나 최소한 upper cap을 두세요.
- Notebook은 offline default로 유지하고, IBM hardware job submission/retrieval example은 별도 script로 저장하는 것이 좋습니다.

### Agent-3

#### Blockers (notebook 실패 또는 잘못된 결과)
- 없음.

#### 품질 이슈
- `03_sdp_discrimination/sdp_tools.py:301`은 MOSEK, CLARABEL, SCS 순서로 solver를 선호합니다. 좋은 방식이지만, README에서 solver별 수치값이 약간 달라질 수 있음을 언급하면 좋습니다.
- `03_sdp_discrimination/requirements.txt:1`-`8`은 pin이 없습니다. CVXPY solver behavior는 release에 따라 달라질 수 있습니다.

#### 제안
- 앞으로 더 많은 SDP 예제를 추가한다면 "slow SDP" test marker를 추가하세요.
- Notebook에서 SDP value를 보여줄 때 solver name도 같이 출력하세요.

### Agent-4

#### Blockers (notebook 실패 또는 잘못된 결과)
- 없음.

#### 품질 이슈
- `04_quantum_combs/combs_tools.py:191`은 dense loop로 general embedding을 구현합니다. 현재 two-qubit demo에는 충분하지만 scaling은 좋지 않습니다.
- `04_quantum_combs/combs_tools.py:393`의 `comb_partial_trace_check`는 이름상 comb causality를 검증하는 것처럼 보이지만 실제로는 necessary global trace condition만 확인합니다.
- `04_quantum_combs/requirements.txt:1`-`6`은 pin이 없습니다.

#### 제안
- Full hierarchy를 추가하지 않는다면 `comb_partial_trace_check`를 `global_tp_trace_check`처럼 더 정확한 이름으로 바꾸거나 문서화하세요.
- Future comb demo는 small dimension으로 제한하거나 dense construction 전에 warning을 추가하세요.

### Agent-5

#### Blockers (notebook 실패 또는 잘못된 결과)
- 없음.

#### 품질 이슈
- `05_interactive_widget/widget_core.py:321`은 slider update마다 전체 Matplotlib dashboard를 다시 렌더링합니다. 현재 qubit-only widget에서는 반응성이 충분하지만, 더 큰 channel을 추가하면 느려질 수 있습니다.
- `05_interactive_widget/requirements.txt:1`-`6`은 pin이 없습니다.

#### 제안
- Widget responsiveness 문제가 생기면 slider change를 debounce하거나 scalar indicator와 무거운 plot을 분리하세요.
- Widget이 의도적으로 qubit-only임을 짧게 명시하세요.

## 공통 관찰

- 모든 notebook은 `np.random.seed(42)`를 설정하고, 앞부분에 palette를 정의합니다.
- 모든 notebook은 현재 환경에서 top-to-bottom 실행됩니다.
- 모든 test suite가 통과합니다.
- 모든 requirements 파일이 exact pin 대신 lower bound를 사용합니다. 이는 프로젝트 전체에서 가장 큰 reproducibility weakness입니다.
- Notebook warning은 fatal하지 않지만, Agent-2는 future `nbformat` hard error를 피하기 위해 notebook cell ID를 normalize하는 것이 좋습니다.
