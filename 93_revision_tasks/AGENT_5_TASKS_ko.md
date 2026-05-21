# Agent-5 Revision Tasks

## Context

Agent-5는 `05_interactive_widget/`, 즉 interactive visualization widget 파트를 담당합니다. Validator들은 critical 또는 major mathematical failure를 발견하지 않았습니다. Test는 통과했고 notebook도 실행되며, standard channel에 대한 Bloch ellipsoid behavior도 기대와 일치합니다. Revision은 integration-facing API consistency, non-physical indicator labeling, 작은 reproducibility/responsiveness 개선에 집중합니다.

## CRITICAL Tasks

없음.

## MAJOR Tasks

### Task M1: Qubit-only Choi application helper를 unified API와 맞추거나 명확히 문서화
- **What**: Agent-5는 qubit 전용 `apply_choi_to_state(choi, rho)`를 정의합니다. Consistency review는 공통 API로 `apply_choi_channel(choi, rho, d_in=None, d_out=None)`를 권장합니다.
- **Where**: `05_interactive_widget/widget_core.py:390`; `92_validation_consistency/CONSISTENCY_REVIEW.md`, Function Signature Mismatches.
- **Why it matters**: Widget helper의 이름과 scope가 integration standard와 다릅니다.
- **Suggested fix**: 권장 argument order를 따르는 작은 wrapper `apply_choi_channel`을 추가하고, 이 widget은 qubit Choi matrix만 지원한다고 문서화하세요. 내부 widget code가 기존 helper에 의존한다면 기존 helper는 유지해도 됩니다.
- **Source**: Validator-C Function Signature Mismatches; Validator-C Recommended Standards.

## MINOR Tasks

### Task m1: Non-physical process fidelity indicator를 Choi overlap으로 rename
- **What**: Widget은 process fidelity indicator를 `[-1, 1]`로 clip하며, intentionally non-CP map에서도 이를 표시할 수 있습니다.
- **Where**: `05_interactive_widget/widget_core.py:264`-`267`; indicator labels in `05_interactive_widget/widget_core.py`.
- **Why it matters**: "Process fidelity"는 CP/TP channel에서 물리적으로 의미가 있지만, widget은 교육 목적상 non-physical region에 들어갈 수 있습니다.
- **Suggested fix**: `is_cp` 또는 `is_tp`가 false일 때 이 quantity를 "Choi overlap indicator"로 표시하거나 raw unclipped value와 warning을 함께 보여주세요. Physical channel에서는 process fidelity label을 유지해도 됩니다.
- **Source**: Validator-A Agent-5 Minor #1; Validator-C Terminology Inconsistencies.

### Task m2: Widget responsiveness note 또는 debounce plan 추가
- **What**: Widget은 slider update마다 전체 Matplotlib dashboard를 다시 렌더링합니다.
- **Where**: `05_interactive_widget/widget_core.py:321`-`345`.
- **Why it matters**: 현재 qubit example에서는 충분히 빠르지만, 더 큰 channel이나 무거운 plot이 추가되면 느려질 수 있습니다.
- **Suggested fix**: README에 현재 widget이 qubit-only이며 full plot을 re-render한다는 note를 추가하세요. Performance issue가 생기면 slider update를 debounce하거나 scalar indicator update와 heavy plot rendering을 분리하세요.
- **Source**: Validator-B Agent-5 Quality Issue #1; Validator-B Agent-5 Suggestion #1; Validator-B Agent-5 Suggestion #2.

### Task m3: Dependency pin으로 재현성 개선
- **What**: `requirements.txt`가 lower bound만 사용합니다.
- **Where**: `05_interactive_widget/requirements.txt:1`-`6`.
- **Why it matters**: Widget과 Jupyter dependency는 release에 따라 behavior가 바뀔 수 있습니다.
- **Suggested fix**: Validation을 통과한 version을 pin하거나 final submission을 위한 tested environment export를 제공하세요.
- **Source**: Validator-B Agent-5 Quality Issue #2; Validator-C Recommended Standards.

### Task m4: Widget notation과 label을 glossary에 맞추기
- **What**: Agent-5는 대체로 일관되지만, glossary는 `C_\mathcal{E}`, `K_k`, unnormalized `Tr(C)=d_in`, `Tr_B(C_\mathcal{E})=I_A` terminology를 권장합니다.
- **Where**: `05_interactive_widget/main.ipynb`; `05_interactive_widget/README.md`; `05_interactive_widget/widget_core.py` display strings.
- **Why it matters**: Widget은 보고서와 함께 교육용 도구로 사용될 가능성이 큽니다.
- **Suggested fix**: Visible markdown과 indicator text를 `92_validation_consistency/UNIFIED_GLOSSARY.md`에 맞게 정리하세요. 특히 Choi normalization과 Kraus/eigenoperator naming을 점검하세요.
- **Source**: Validator-C Notation Inconsistencies; Validator-C Unified Glossary.

### Task m5: Final report screenshot을 위한 heatmap style 표준화
- **What**: Widget은 이미 real/imaginary heatmap에 `RdBu_r`를 사용하지만, final screenshot은 shared figure convention을 따라야 합니다.
- **Where**: `05_interactive_widget/widget_core.py:116`-`137`; `05_interactive_widget/figures/widget_preview.png`.
- **Why it matters**: Widget preview가 나머지 통합 프로젝트 figure와 시각적으로 맞아야 합니다.
- **Suggested fix**: Signed real/imaginary panel에는 `RdBu_r`를 유지하고, magnitude panel이 추가되면 `viridis`를 사용하세요. Label 또는 style 변경이 screenshot에 영향을 주면 preview를 재생성하세요.
- **Source**: Validator-C Visual Style Issues; Validator-C Recommended Standards.

## Cross-cutting Notes

Agent-5는 local and IBM-free 상태를 유지해야 합니다. API alignment change는 현재 interactive behavior와 qubit-only assumption을 깨지 않도록 진행하세요.
