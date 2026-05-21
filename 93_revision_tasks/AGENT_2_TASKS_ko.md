# Agent-2 Revision Tasks

## Context

Agent-2는 `02_ibm_experiment/`, 즉 IBM Quantum process tomography 파트를 담당합니다. Validator들은 execution blocker를 발견하지 않았습니다. Offline notebook은 IBM credential 없이 실행되고 test도 통과합니다. 다만 revision 부담은 큽니다. Diamond-distance proxy를 실제 SDP 기반 diamond norm으로 대체 또는 보강해야 하고, MLE 필요성을 더 명확히 보여야 하며, Qiskit dependency와 solver behavior의 재현성 risk를 줄여야 합니다.

## CRITICAL Tasks

없음.

## MAJOR Tasks

### Task M1: Diamond-distance proxy를 true SDP diamond norm으로 교체 또는 보강
- **What**: `diamond_distance_proxy`는 Choi difference의 scaled nuclear norm이며, Agent-2 스펙이 요구한 diamond norm SDP가 아닙니다.
- **Where**: `02_ibm_experiment/qpt_tools.py:586`; diagnostics return near `02_ibm_experiment/qpt_tools.py:595`; notebook discussion around `02_ibm_experiment/main.ipynb:248`.
- **Why it matters**: Proxy를 diamond-distance result처럼 제시하면 수학적으로 오해를 만들고, Agent-3의 exact SDP treatment와도 일관되지 않습니다.
- **Suggested fix**: Reconstructed Choi와 ideal Choi 사이의 diamond norm을 계산하는 local CVXPY SDP implementation을 추가하세요. Nuclear-norm quantity는 필요하다면 명확히 "fast proxy"로만 유지하세요.
- **Source**: Validator-A Agent-2 Major #1; Validator-B Agent-2 Quality Issue #1; Validator-C Terminology Inconsistencies.

### Task M2: MLE 필요성을 보여주는 non-physical linear-inversion 예시 추가
- **What**: Notebook은 finite-shot data가 linear inversion을 non-physical하게 만들 수 있다고 말하지만, deterministic example은 이미 physical합니다.
- **Where**: `02_ibm_experiment/main.ipynb:200`, Section 4.
- **Why it matters**: MLE section은 왜 CP/TP projection이 필요한지 눈에 보이게 보여야 합니다.
- **Suggested fix**: Finite-shot, bootstrap, 또는 의도적으로 perturb한 one-qubit tomography example을 하나 추가해 linear-inversion Choi matrix에 negative eigenvalue가 생기는 사례를 보여주세요. 이후 `mle_choi`가 CP/TP matrix로 projection함을 보여주세요.
- **Source**: Validator-A Agent-2 Major #2.

### Task M3: MLE CVXPY loop의 solver-option handling 수정
- **What**: SCS-specific option이 CLARABEL도 시도하는 loop 안에서 함께 전달될 수 있습니다. SCS가 없는 환경에서는 solver-incompatible keyword 문제가 생길 수 있습니다.
- **Where**: `02_ibm_experiment/qpt_tools.py:390`-`394`.
- **Why it matters**: 현재 환경에서는 통과하지만 solver installation이 조금 달라지면 실패할 수 있습니다.
- **Suggested fix**: `eps`, `max_iters`는 SCS로 solve할 때만 전달하세요. CLARABEL에는 CLARABEL-compatible option을 쓰거나 별도 option 없이 호출하세요.
- **Source**: Validator-B Agent-2 Quality Issue #2.

### Task M4: Qiskit 계열 dependency pin 또는 upper cap 추가
- **What**: Requirements file이 API 변화가 빠른 package들에 대해 broad lower bound만 사용합니다.
- **Where**: `02_ibm_experiment/requirements.txt:1`-`11`.
- **Why it matters**: Agent-2는 Qiskit, Qiskit Experiments, IBM Runtime API 변화 때문에 future reproducibility drift 위험이 가장 큽니다.
- **Suggested fix**: Validation을 통과한 Qiskit-family version을 pin하거나 upper cap을 추가하세요. Exact pin이 너무 강하면 README에 tested-version table 또는 environment export를 넣으세요.
- **Source**: Validator-B Agent-2 Quality Issue #3; Validator-B Agent-2 Suggestion #1; Validator-C Recommended Standards.

### Task M5: Choi helper signature를 unified API와 맞추기
- **What**: Agent-2는 `apply_channel_to_state(rho, choi, d_out=None)`를 사용합니다. Glossary는 `apply_choi_channel(choi, rho, d_in=None, d_out=None)`를 권장합니다.
- **Where**: `02_ibm_experiment/qpt_tools.py:142`; `92_validation_consistency/CONSISTENCY_REVIEW.md`, Function Signature Mismatches.
- **Why it matters**: Argument order 불일치는 통합 단계에서 흔한 버그 원인이 됩니다.
- **Suggested fix**: 권장 이름과 argument order를 따르는 wrapper를 추가하거나 rename path를 마련하세요. 기존 notebook cell과의 backward compatibility는 유지해도 됩니다.
- **Source**: Validator-C Function Signature Mismatches; Validator-C Recommended Standards.

## MINOR Tasks

### Task m1: Unclipped process fidelity diagnostic 노출
- **What**: `process_fidelity`가 결과를 `[0, 1]`로 clip하여 numerical/modeling issue를 숨길 수 있습니다.
- **Where**: `02_ibm_experiment/qpt_tools.py:457`-`466`.
- **Why it matters**: Reconstruction이 의심스러운 값을 만들 때 diagnostic은 이를 드러내야 합니다.
- **Suggested fix**: Raw value를 clipped presentation value와 함께 return 또는 log하세요. Clipping은 display용으로만 유지하는 것이 좋습니다.
- **Source**: Validator-A Agent-2 Minor #1.

### Task m2: IBM hardware submission/retrieval을 offline notebook 실행과 분리
- **What**: Validator-B는 hardware job submission/retrieval을 별도 script로 두어 notebook execution이 offline default로 유지되게 하라고 제안했습니다.
- **Where**: `02_ibm_experiment/README.md`; optional scripts in `02_ibm_experiment/`.
- **Why it matters**: Queue wait 또는 credential issue가 reproducible notebook run을 깨뜨리지 않게 합니다.
- **Suggested fix**: Submit/retrieve flow를 위한 짧은 script 또는 documented command를 추가하고, `main.ipynb`는 deterministic offline path를 유지하세요.
- **Source**: Validator-B Agent-2 Suggestion #2.

### Task m3: Notebook cell ID normalize
- **What**: Agent-2는 nbconvert 중 notebook missing-id warning을 냈습니다.
- **Where**: `02_ibm_experiment/main.ipynb`; `91_validation_code/execution_logs/02_ibm_experiment_nbconvert.log`.
- **Why it matters**: `nbformat`은 missing cell ID가 future version에서 hard error가 될 수 있다고 경고합니다.
- **Suggested fix**: 최신 Jupyter로 notebook을 열고 저장하거나, 내용은 바꾸지 않고 cell ID를 추가하는 normalization step을 실행하세요.
- **Source**: Validator-B Cross-Cutting Observations.

### Task m4: Diamond norm과 proxy terminology를 명확히 분리
- **What**: Agent-2 diagnostic은 Agent-3의 true diamond norm과 함께 통합될 예정이므로, proxy language가 명확해야 합니다.
- **Where**: `02_ibm_experiment/main.ipynb`; `02_ibm_experiment/README.md`; `02_ibm_experiment/qpt_tools.py`.
- **Why it matters**: 통합 보고서에서 heuristic Choi norm과 diamond norm이 혼동되면 안 됩니다.
- **Suggested fix**: Task M1 이후, "diamond norm"은 SDP result에만 사용하고 heuristic norm은 항상 "diamond-distance proxy"라고 부르세요.
- **Source**: Validator-C Terminology Inconsistencies; Validator-C Unified Glossary.

## Cross-cutting Notes

Choi matrix에는 `C_\mathcal{E}`, channel에는 `\mathcal{E}`, trace preservation에는 `Tr_B(C_\mathcal{E})=I_A`를 사용하세요. Choi heatmap을 수정할 때는 signed real/imaginary panel에 `RdBu_r`, magnitude에 `viridis`를 사용하세요.
