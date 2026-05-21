# Agent-3 Revision Tasks

## Context

Agent-3는 `03_sdp_discrimination/`, 즉 SDP channel discrimination 파트를 담당합니다. Validator들은 critical 또는 major mathematical problem을 발견하지 않았습니다. Watrous SDP form은 project convention과 일치하고, Pauli/depolarizing closed-form check도 통과했으며, notebook/test도 정상 실행됩니다. Revision은 주로 설명 보강과 integration-oriented cleanup입니다.

## CRITICAL Tasks

없음.

## MAJOR Tasks

### Task M1: Choi helper naming을 unified API와 맞추기
- **What**: Agent-3는 `apply_choi_to_state(choi, rho, d_in, d_out)`와 `kraus_to_choi(kraus_ops: list[np.ndarray])`를 사용합니다. Consistency review는 `apply_choi_channel(choi, rho, d_in=None, d_out=None)`와 `kraus_to_choi(kraus_ops: Sequence[np.ndarray])`를 권장합니다.
- **Where**: `03_sdp_discrimination/sdp_tools.py:74`; `03_sdp_discrimination/sdp_tools.py:108`; `92_validation_consistency/CONSISTENCY_REVIEW.md`, Function Signature Mismatches.
- **Why it matters**: SDP folder는 Agent-2와 final integration에서 재사용될 가능성이 높으므로 helper naming이 기준에서 벗어나면 안 됩니다.
- **Suggested fix**: 권장 argument order를 따르는 `apply_choi_channel` compatibility wrapper를 추가하세요. Low-risk라면 `kraus_to_choi` annotation도 `Sequence[np.ndarray]`를 받도록 완화하세요.
- **Source**: Validator-C Function Signature Mismatches; Validator-C Recommended Standards.

## MINOR Tasks

### Task m1: `optimal_input_state`가 marginal을 반환한다는 점 명확히 하기
- **What**: 이 함수는 full reference-system input state가 아니라 optimal input marginal을 반환합니다.
- **Where**: `03_sdp_discrimination/sdp_tools.py:396`; explanatory text in `03_sdp_discrimination/main.ipynb`.
- **Why it matters**: Channel discrimination에서는 entangled reference가 필요할 수 있으므로, marginal과 full state를 혼동하면 독자가 오해할 수 있습니다.
- **Suggested fix**: Notebook에 이 marginal을 purify하면 full input을 얻을 수 있으며, POVM helper path에서 그 과정이 구현되어 있다는 한 문장을 추가하세요.
- **Source**: Validator-A Agent-3 Minor #1.

### Task m2: Solver-dependent numerical variation 문서화
- **What**: Code는 MOSEK, CLARABEL, SCS 순서로 solver를 선호하지만, README는 solver에 따라 작은 수치 차이가 생길 수 있음을 명확히 말하지 않습니다.
- **Where**: `03_sdp_discrimination/sdp_tools.py:301`; `03_sdp_discrimination/README.md`.
- **Why it matters**: SDP 결과는 solver와 tolerance에 따라 작은 차이가 있을 수 있습니다.
- **Suggested fix**: README에 solver priority와 tolerance-level variation이 expected된다는 짧은 note를 추가하세요.
- **Source**: Validator-B Agent-3 Quality Issue #1.

### Task m3: Notebook SDP output에 solver name 출력
- **What**: Notebook은 SDP value를 보고하지만 어떤 solver가 사용되었는지 일관되게 보여주지 않습니다.
- **Where**: `03_sdp_discrimination/main.ipynb`, SDP example cells.
- **Why it matters**: Solver name은 numerical result를 재현하고 debugging하는 데 도움이 됩니다.
- **Suggested fix**: 가능하면 result-returning solver function을 호출해 numerical value와 함께 `result.solver`를 출력하세요.
- **Source**: Validator-B Agent-3 Suggestion #2.

### Task m4: CVXPY 및 solver-related dependency pin
- **What**: `requirements.txt`가 lower bound만 사용합니다.
- **Where**: `03_sdp_discrimination/requirements.txt:1`-`8`.
- **Why it matters**: CVXPY와 conic solver behavior는 release에 따라 바뀔 수 있습니다.
- **Suggested fix**: Validation을 통과한 version을 pin하거나 final reproducibility를 위한 tested environment export를 제공하세요.
- **Source**: Validator-B Agent-3 Quality Issue #2; Validator-C Recommended Standards.

### Task m5: Test suite가 커질 경우 slow SDP marker 추가
- **What**: Validator-B는 더 비싼 SDP example이 추가되면 "slow SDP" test marker를 사용하라고 제안했습니다.
- **Where**: `03_sdp_discrimination/test_sdp_tools.py`.
- **Why it matters**: Routine validation은 빠르게 유지하면서 deeper numerical check도 분리할 수 있습니다.
- **Suggested fix**: 현재 즉시 code change는 필요 없습니다. 새 slow test를 추가할 때 marker를 붙이고 실행 방법을 문서화하세요.
- **Source**: Validator-B Agent-3 Suggestion #1.

### Task m6: Cleanup 중 unified notation 및 visual standard 적용
- **What**: Agent-3는 대체로 일관되지만, project-wide glossary는 `C_\Phi`, `\Phi`, dimension name, Choi heatmap style에 대해 정확한 용어를 권장합니다.
- **Where**: `03_sdp_discrimination/main.ipynb`; `03_sdp_discrimination/README.md`; any revised plots.
- **Why it matters**: Agent-3는 다른 folder가 참고할 diamond-norm standard를 제공합니다.
- **Suggested fix**: Channel difference의 Choi matrix에는 `C_\Phi`를 쓰고, "diamond norm"은 exact SDP 또는 analytic value에만 사용하세요. 수정되는 figure에는 shared heatmap/palette convention을 적용하세요.
- **Source**: Validator-C Notation Inconsistencies; Validator-C Visual Style Issues; Validator-C Unified Glossary.

## Cross-cutting Notes

Agent-3에는 critical mathematical change가 없습니다. 다른 agent들이 이 폴더를 reference SDP implementation으로 사용할 수 있도록 API compatibility와 solver reproducibility note를 우선하세요.
