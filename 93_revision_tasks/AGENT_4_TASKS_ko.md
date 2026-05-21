# Agent-4 Revision Tasks

## Context

Agent-4는 `04_quantum_combs/`, 즉 non-Markovian dynamics와 quantum combs 파트를 담당합니다. Validator들은 execution failure나 critical mathematical error를 발견하지 않았지만, comb causality와 RHP/BLP witness의 정확한 status에 대해 중요한 conceptual gap을 지적했습니다. 이 폴더는 Agent-2 다음으로 revision priority가 높습니다.

## CRITICAL Tasks

없음.

## MAJOR Tasks

### Task M1: Full quantum-comb causality hierarchy 구현 또는 문서화
- **What**: `comb_partial_trace_check`는 global trace-preservation condition만 확인하고, recursive deterministic-comb causality hierarchy는 확인하지 않습니다.
- **Where**: `04_quantum_combs/combs_tools.py:393`-`407`; `04_quantum_combs/main.ipynb`, quantum comb section.
- **Why it matters**: Valid comb는 global channel TP condition뿐 아니라 recursive partial trace condition을 만족해야 합니다.
- **Suggested fix**: Demonstrated two-slot comb에 대해 correct unnormalized-Choi normalization을 포함한 hierarchy check를 추가하세요. 최소한 현재 함수 이름과 notebook text를 수정해 이것이 necessary global TP trace check일 뿐임을 명확히 하세요.
- **Source**: Validator-A Agent-4 Major #1; Validator-B Agent-4 Quality Issue #2; Validator-B Agent-4 Suggestion #1.

### Task M2: RHP quantity가 full continuous measure가 아니라 grid-based witness임을 명확히 하기
- **What**: Code는 이 quantity를 "RHP-style"이라고 부르지만, notebook에서도 full continuous RHP measure처럼 보이지 않게 해야 합니다.
- **Where**: `04_quantum_combs/combs_tools.py:461`-`486`; `04_quantum_combs/main.ipynb`, Section 2.
- **Why it matters**: 현재 구현값은 time grid와 intermediate map의 pseudo-inverse reconstruction에 의존합니다.
- **Suggested fix**: Notebook에 이것이 adjacent intermediate map의 negative Choi eigenvalue에 기반한 discrete CP-divisibility witness라는 설명을 추가하세요. Pseudo-inverse dependence도 언급하고, continuous RHP integral처럼 표현하지 마세요.
- **Source**: Validator-A Agent-4 Major #2.

### Task M3: `apply_choi_channel` argument order를 unified API와 맞추기
- **What**: Agent-4는 `apply_choi_channel(rho, choi, d_in=None, d_out=None)`를 정의합니다. Glossary는 `apply_choi_channel(choi, rho, d_in=None, d_out=None)`를 권장합니다.
- **Where**: `04_quantum_combs/combs_tools.py:92`; notebook calls in `04_quantum_combs/main.ipynb`.
- **Why it matters**: 함수 이름은 이미 권장 이름과 같기 때문에 argument order가 반대인 점은 통합 단계에서 특히 실수하기 쉽습니다.
- **Suggested fix**: 권장 order의 새 wrapper를 추가하거나 call site를 신중히 migration하세요. Backward compatibility를 유지한다면 기존 order를 명확히 문서화하고 notebook example에서는 새 order를 선호하세요.
- **Source**: Validator-C Function Signature Mismatches; Validator-C Recommended Standards.

### Task M4: Dense scaling limit 명시
- **What**: `embed_operator`는 explicit dense loop를 사용하고, comb construction은 작은 demonstration에만 현실적입니다.
- **Where**: `04_quantum_combs/combs_tools.py:191`; `04_quantum_combs/README.md`; `04_quantum_combs/main.ipynb`.
- **Why it matters**: Warning이 없으면 사용자가 infeasible한 dimension에서 construction을 시도할 수 있습니다.
- **Suggested fix**: Implementation이 intentionally dense하며 small qubit example에 적합하다는 docstring 또는 README note를 추가하세요. Future demo도 이 limit 안에서 유지하세요.
- **Source**: Validator-B Agent-4 Quality Issue #1; Validator-B Agent-4 Suggestion #2.

## MINOR Tasks

### Task m1: Notebook에 BLP finite-grid limitation 명시
- **What**: BLP helper는 finite grid의 antipodal pure-state pair를 탐색하지만, true BLP measure는 모든 state pair에 대한 optimization입니다.
- **Where**: `04_quantum_combs/combs_tools.py:438`-`458`; `04_quantum_combs/main.ipynb`, Section 2.
- **Why it matters**: 독자가 grid estimate를 exact BLP measure로 혼동하면 안 됩니다.
- **Suggested fix**: BLP plot 근처 notebook text에 finite-grid approximation이라는 한 문장을 추가하세요.
- **Source**: Validator-A Agent-4 Minor #1.

### Task m2: Dependency pin으로 재현성 개선
- **What**: `requirements.txt`가 lower bound만 사용합니다.
- **Where**: `04_quantum_combs/requirements.txt:1`-`6`.
- **Why it matters**: Lower bound는 archival rerun에 약합니다.
- **Suggested fix**: Validation을 통과한 version을 pin하거나 final submission을 위한 tested environment export를 제공하세요.
- **Source**: Validator-B Agent-4 Quality Issue #3; Validator-C Recommended Standards.

### Task m3: Comb terminology 표준화
- **What**: Agent-4는 "quantum comb", "process tensor", "multi-use channel", "memory comb"를 번갈아 사용합니다.
- **Where**: `04_quantum_combs/main.ipynb`; `04_quantum_combs/README.md`; `04_quantum_combs/combs_tools.py` docstrings.
- **Why it matters**: 최종 보고서에는 안정적인 formal vocabulary가 필요합니다.
- **Suggested fix**: Process tensor/quantum comb를 한 번 정의한 뒤, Choi operator object에는 "quantum comb", multi-time dynamics를 강조할 때는 "process tensor"를 사용하세요.
- **Source**: Validator-C Terminology Inconsistencies; Validator-C Unified Glossary.

### Task m4: Choi/comb figure style 표준화
- **What**: Agent-4는 `viridis`, `magma` 등 여러 colormap을 사용합니다. Consistency review는 signed real/imaginary Choi panel에는 `RdBu_r`, magnitude에는 `viridis`를 권장합니다.
- **Where**: `04_quantum_combs/main.ipynb`, comb and marginal heatmap cells.
- **Why it matters**: Visual convention이 통일되면 최종 보고서에서 해석 부담이 줄어듭니다.
- **Suggested fix**: Magnitude/residue plot에는 `viridis`를 사용하고, signed matrix component를 추가한다면 `RdBu_r`를 사용하세요.
- **Source**: Validator-C Visual Style Issues; Validator-C Recommended Standards.

## Cross-cutting Notes

Comb/process tensor Choi operator에는 `T`, single-time channel Choi matrix에는 `C_\mathcal{E}`를 사용하세요. Partial trace를 논의할 때 subsystem order `A0, B0, A1, B1, ...`를 명확히 유지하세요.
