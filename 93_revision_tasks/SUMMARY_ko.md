# Revision Task Summary

## Scope

이번 coordination pass는 Phase 2 validation output을 읽고 producer별 실행 가능한 revision list로 변환했습니다. Producer 파일은 수정하지 않았습니다. Task 파일은 다음과 같습니다.

- `AGENT_1_TASKS.md`
- `AGENT_2_TASKS.md`
- `AGENT_3_TASKS.md`
- `AGENT_4_TASKS.md`
- `AGENT_5_TASKS.md`

한국어 번역본은 같은 이름에 `_ko.md`를 붙인 파일입니다.

## Task Counts

| Producer | Folder | Critical | Major | Minor | Total | Estimated Complexity |
|----------|--------|----------|-------|-------|-------|----------------------|
| Agent-1 | `01_theory/` | 0 | 2 | 5 | 7 | Medium |
| Agent-2 | `02_ibm_experiment/` | 0 | 5 | 4 | 9 | High |
| Agent-3 | `03_sdp_discrimination/` | 0 | 1 | 6 | 7 | Low-Medium |
| Agent-4 | `04_quantum_combs/` | 0 | 4 | 4 | 8 | High |
| Agent-5 | `05_interactive_widget/` | 0 | 1 | 5 | 6 | Low-Medium |
| **Total** |  | **0** | **13** | **24** | **37** |  |

## Recommended Order of Execution

1. **Agent-2 first**: 가장 중요한 deliverable gap이 있습니다. Final integration에서 tomography result에 대한 quantitative claim을 하려면 diamond-distance proxy를 true SDP diamond norm으로 대체 또는 보강해야 합니다.
2. **Agent-4 second**: Comb causality hierarchy issue는 non-Markovian/comb section의 conceptual correctness에 직접 영향을 줍니다. 이를 먼저 고치면 관련 text와 function name의 수정 범위도 명확해집니다.
3. **Agent-3 third**: 수학적으로 sound하며, Agent-2가 참고할 stable SDP/API reference 역할을 하도록 정리하면 됩니다.
4. **Agent-1 fourth**: Foundation은 sound하지만, final report integration 전에 conversion coverage와 notation cleanup을 마무리해야 합니다.
5. **Agent-5 fifth**: Widget은 이미 작동합니다. Revision은 대부분 labeling, API wrapper, reproducibility polish입니다.

## De-duplication Decisions

- Agent-2의 `diamond_distance_proxy`는 Validator-A, Validator-B, Validator-C가 모두 지적했습니다. 모두 같은 underlying gap, 즉 proxy가 required diamond norm SDP가 아니라는 문제를 가리키므로 하나의 Major task로 합쳤습니다.
- Agent-4의 `comb_partial_trace_check`는 Validator-A와 Validator-B가 지적했습니다. 둘 다 global TP trace condition만 확인하고 full comb causality hierarchy를 확인하지 않는다는 같은 문제이므로 하나의 Major task로 합쳤습니다.
- Dependency pinning은 Validator-B가 모든 폴더에 대해 지적했고, Validator-C의 project-wide standard도 이를 뒷받침합니다. 각 folder가 별도 `requirements.txt`를 갖고 있으므로 producer별 task로 따로 남겼습니다.
- Choi helper naming과 argument-order mismatch는 Validator-C가 지적했습니다. Local API가 `UNIFIED_GLOSSARY.md`와 다른 producer에 대해 producer-specific task로 포함했습니다.
- Visual palette와 heatmap issue는 main deliverable correctness에 직접 영향을 주지 않는 한 Minor로 분류했습니다. Validator들은 어떤 plot도 mathematically wrong하다고 보지는 않았습니다.

## Conflicts or Ambiguities

- Validator들 사이의 직접적인 contradiction은 발견되지 않았습니다.
- 일부 Validator-C recommendation은 local correctness bug라기보다 integration standard입니다. Function signature나 argument order처럼 integration bug를 만들 수 있는 항목은 Major로, notation/plot style/document voice cleanup은 Minor로 분류했습니다.
- Agent-4의 RHP implementation은 validator들이 wrong이라고 판단하지 않았습니다. 이는 grid-based witness입니다. Revision task는 full continuous RHP implementation으로 교체하는 것이 아니라 정확히 labeling하고 설명하는 것입니다.
- Agent-5는 교육 목적으로 non-CP map을 의도적으로 허용합니다. Task는 이 기능을 제거하는 것이 아니라, non-physical overlap을 process fidelity라고 부르지 않도록 하는 것입니다.

## Global Revision Standards

모든 agent는 revision 중 `92_validation_consistency/UNIFIED_GLOSSARY.md`를 참고해야 합니다.

- Unnormalized Choi matrix를 사용합니다.
- Input-first tensor order `A \otimes B`를 사용합니다.
- Channel Choi matrix에는 `C_\mathcal{E}`, channel difference에는 `C_\Phi`를 사용합니다.
- Quantum comb/process tensor Choi operator에는 `T`를 사용합니다.
- Trace preservation은 `Tr_B(C_\mathcal{E})=I_A`로 씁니다.
- Code에서는 `d_in`, `d_out`를 선호합니다.
- Choi-form channel application에는 `apply_choi_channel(choi, rho, d_in=None, d_out=None)`를 선호합니다.
- "Diamond norm"은 SDP 또는 analytic exact value에만 사용하고, heuristic quantity는 "proxy"라고 부릅니다.
- Signed real/imaginary Choi heatmap에는 `RdBu_r`, magnitude에는 `viridis`를 사용합니다.
