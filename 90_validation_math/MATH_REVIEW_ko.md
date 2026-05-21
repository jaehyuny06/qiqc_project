# 수학적 및 물리적 정확성 검토

Validator-A는 다섯 producer 폴더를 공통 Choi convention에 맞춰 검토했습니다.

```text
C_E = sum_ij |i><j| tensor E(|i><j|)
```

여기서 input system이 첫 번째 tensor factor입니다. Producer 코드는 수정하지 않았습니다. 독립적인 수치 검증은 `scratch/verify_math_claims.py`와 `scratch/verify_math_claims.log`에 있습니다.

## Agent-1 검토 결과

### Critical (반드시 수정)
- [ ] 발견되지 않음.

### Major (수정 권장)
- [ ] 노트북은 Kraus, Choi, Stinespring, natural form 사이의 "All 6 directions" 변환을 다룬다고 되어 있지만, `01_theory/main.ipynb`는 직접 변환과 나머지 변환을 composition으로 얻는다는 설명만 보여줍니다. 수학적으로는 타당하지만, 스펙과 맞추려면 여섯 가지 변환 쌍을 명시하고 Natural -> Choi -> Kraus 같은 composed route를 하나 이상 보여주는 것이 좋습니다.

### Minor (개선 사항)
- [ ] `01_theory/channel_reps.py:68`은 TP 조건 또는 square shape를 이용해 Choi dimension을 추론합니다. 현재 예제에는 충분하지만, non-TP rectangular CP map에는 명시적 dimension이 필요하다는 점을 inverse Choi 함수 설명에 적어두는 것이 좋습니다.

## Agent-2 검토 결과

### Critical (반드시 수정)
- [ ] 발견되지 않음.

### Major (수정 권장)
- [ ] `02_ibm_experiment/qpt_tools.py:586`의 `diamond_distance_proxy`는 Choi difference의 scaled nuclear norm입니다. Agent-2 스펙은 Agent-3의 SDP formulation을 독립적으로 재구현해 diamond norm distance를 계산하라고 요구합니다. 현재 "proxy"라고 정직하게 표기되어 있긴 하지만, 수학적 deliverable을 완전히 만족하지는 않습니다. 수정 방향: reconstructed Choi와 ideal Choi 사이의 diamond norm을 계산하는 작은 CVXPY SDP를 추가하고, nuclear norm은 빠른 선택적 diagnostic으로 유지하세요.
- [ ] `02_ibm_experiment/main.ipynb:200`은 exact simulated one-qubit data가 이미 physical이라고 설명합니다. deterministic fixture에 대해서는 맞지만, MLE가 왜 필요한지 보여주려면 finite-shot 또는 의도적으로 perturb한 linear inversion 예시를 하나 추가해 negative Choi eigenvalue가 나오는 사례를 보여주는 것이 좋습니다.

### Minor (개선 사항)
- [ ] `02_ibm_experiment/qpt_tools.py:457`은 process fidelity를 `[0, 1]`로 clip합니다. 발표용으로는 편하지만, numerical/modeling issue가 숨겨질 수 있으므로 unclipped value도 diagnostic에 노출하는 것이 좋습니다.

## Agent-3 검토 결과

### Critical (반드시 수정)
- [ ] 발견되지 않음.

### Major (수정 권장)
- [ ] 발견되지 않음. `03_sdp_discrimination/sdp_tools.py:345`-`355`의 SDP는 project tensor convention에 맞는 Watrous primal form과 일치하며, 독립 검증에서도 Pauli closed form을 재현했습니다.

### Minor (개선 사항)
- [ ] `03_sdp_discrimination/sdp_tools.py:396`은 optimal input marginal을 반환합니다. 노트북 설명에서 이것이 full reference-system input state가 아니라 marginal이라는 점을 더 분명히 하면 좋습니다. purification step은 뒤에서 구현되어 있습니다.

## Agent-4 검토 결과

### Critical (반드시 수정)
- [ ] 발견되지 않음.

### Major (수정 권장)
- [ ] `04_quantum_combs/combs_tools.py:393`-`407`은 global trace-preservation condition인 `Tr_{B0...BN}(T)=I_{A0...AN}`만 확인합니다. Validator checklist는 quantum-comb causality hierarchy를 요구합니다. deterministic comb에는 global channel TP 조건뿐 아니라 recursive constraint가 필요합니다. 예를 들어 two-slot에서는 unnormalized Choi convention에 맞는 normalization과 함께 `Tr_{B1}(T_2)=I_{A1} tensor T_1`, `Tr_{B0}(T_1)=I_{A0}` 형태의 hierarchy를 함수와 노트북 설명에 추가하는 것이 좋습니다.
- [ ] `04_quantum_combs/combs_tools.py:461`은 RHP quantity를 "RHP-style" witness라고 부릅니다. 이 표현은 적절하지만, 노트북에서는 이것을 full continuous RHP measure처럼 보이지 않게 주의해야 합니다. 현재 구현은 grid-based sum of intermediate-map Choi negativity이며, `combs_tools.py:481`의 pseudo-inverse에 의존합니다.

### Minor (개선 사항)
- [ ] `04_quantum_combs/combs_tools.py:438`은 BLP 계산에서 finite grid의 antipodal pure-state pair만 탐색합니다. README에는 언급되어 있지만, true BLP measure는 모든 state pair에 대한 optimization이라는 점을 노트북에도 명시하면 좋습니다.

## Agent-5 검토 결과

### Critical (반드시 수정)
- [ ] 발견되지 않음.

### Major (수정 권장)
- [ ] 발견되지 않음. 독립 검증 결과, depolarizing channel은 centered isotropic contraction으로, amplitude damping은 off-center ellipsoid로 나타나 기대한 Bloch behavior와 일치했습니다.

### Minor (개선 사항)
- [ ] `05_interactive_widget/widget_core.py:264`-`267`은 process fidelity indicator를 `[-1, 1]`로 clip합니다. 물리적인 CP/TP channel에서는 이 값이 `[0, 1]`에 있어야 합니다. widget이 교육 목적으로 non-CP map을 허용한다면, physical region 밖에서는 "overlap indicator"라고 부르거나 unclipped raw value를 표시하는 것이 좋습니다.

## 요약

- Critical issue 수: 0
- Major issue 수: 4
- Minor issue 수: 4
- 전체 수학적 신뢰도: B+

핵심 Choi convention, CP/TP check, Agent-1 round trip, Agent-3 SDP example, Agent-4 Markovianity witness, Agent-5 Bloch geometry는 대표 수치 검증을 통과했습니다. 가장 중요한 revision point는 Agent-2의 true diamond-norm SDP 추가와 Agent-4의 comb causality hierarchy 보강입니다.
