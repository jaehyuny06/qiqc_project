# Agent-1 Revision Tasks

## Context

Agent-1은 `01_theory/` 폴더, 즉 이론적 기반 파트를 담당합니다. Validator들은 critical failure를 발견하지 않았습니다. Test와 notebook 실행은 통과했고, 핵심 Choi convention도 올바르며, 주요 numerical round trip도 정상입니다. Revision은 주로 스펙에서 약속한 coverage를 채우고, edge case를 문서화하며, 통합 단계에서 notation/API/style을 unified glossary와 맞추는 데 집중합니다.

## CRITICAL Tasks

없음.

## MAJOR Tasks

### Task M1: 여섯 가지 representation conversion 방향을 명확히 완성하기
- **What**: Notebook은 Kraus, Choi, Stinespring, natural form 사이의 여섯 가지 conversion direction을 모두 다룬다고 말하지만, 실제로는 direct conversion만 보여주고 나머지는 composition으로 얻는다고 설명합니다.
- **Where**: `01_theory/main.ipynb`, Section 4; 관련 helper는 `01_theory/channel_reps.py`.
- **Why it matters**: Agent-1 notebook은 프로젝트의 이론적 기반이므로, 스펙에서 요구한 conversion coverage와 실제 설명이 일치해야 합니다.
- **Suggested fix**: 여섯 가지 representation pairing을 명시적으로 나열하고, Natural -> Choi -> Kraus 같은 composed route를 하나 이상 보여주세요. 현재 direct helper가 올바르다면 대부분 notebook narrative와 간단한 sanity check 추가로 충분합니다.
- **Source**: Validator-A Agent-1 Major #1.

### Task M2: Choi-channel application API를 project glossary와 맞추기
- **What**: Agent-1은 Kraus form에 대해 `apply_channel(rho, kraus_ops)`를 제공합니다. Consistency review는 공통 Choi API로 `apply_choi_channel(choi, rho, d_in=None, d_out=None)`를 권장합니다.
- **Where**: `01_theory/channel_reps.py`, `apply_channel`; `92_validation_consistency/CONSISTENCY_REVIEW.md`, Function Signature Mismatches.
- **Why it matters**: 여러 producer 폴더의 예제를 통합할 때 API mismatch가 friction을 만들 수 있습니다.
- **Suggested fix**: 권장 이름과 argument order를 따르는 Choi-form application helper를 추가하거나 문서화하세요. 기존 Kraus helper는 notebook code가 의존한다면 그대로 유지해도 됩니다.
- **Source**: Validator-C Function Signature Mismatches.

## MINOR Tasks

### Task m1: inverse Choi routine의 dimension inference 한계 문서화
- **What**: 현재 Choi dimension inference는 TP constraint 또는 square input/output shape에 의존합니다. 일부 non-TP rectangular CP map에는 충분하지 않습니다.
- **Where**: `01_theory/channel_reps.py:68`; `choi_to_kraus`; `choi_to_natural`.
- **Why it matters**: 사용자가 helper의 적용 범위를 예제보다 넓게 오해할 수 있습니다.
- **Suggested fix**: Dimension inference가 언제 유효하고 언제 explicit dimension이 필요한지 docstring에 적어주세요. 시간이 있으면 dimension-aware optional helper를 추가할 수 있지만, 명확한 limitation note만으로도 충분합니다.
- **Source**: Validator-A Agent-1 Minor #1; Validator-B Agent-1 Suggestion #2.

### Task m2: 재현성을 위해 dependency pin 또는 freeze 제공
- **What**: `requirements.txt`가 exact version pin이 아니라 lower bound만 사용합니다.
- **Where**: `01_theory/requirements.txt:1`-`6`.
- **Why it matters**: Lower bound는 개발 중에는 편하지만, 장기 archival rerun에는 약합니다.
- **Suggested fix**: Validation을 통과한 version을 pin하거나, development lower bound임을 주석으로 명시하고 final submission용 lockfile/environment export를 제공하세요.
- **Source**: Validator-B Agent-1 Quality Issue #1; Validator-C Recommended Standards.

### Task m3: Prose에서 unified notation standard 적용
- **What**: Agent-1은 `C_E`, `C`, `E1`, `E2` 등을 사용합니다. Glossary는 channel에는 `C_\mathcal{E}`, channel에는 `\mathcal{E}`, input에는 `A`, output에는 `B`를 권장합니다.
- **Where**: `01_theory/main.ipynb`; `01_theory/README.md`; `01_theory/channel_reps.py` docstrings.
- **Why it matters**: Theory chapter가 프로젝트 전체의 notation 기준을 잡습니다.
- **Suggested fix**: Markdown equation과 설명 문장을 `92_validation_consistency/UNIFIED_GLOSSARY.md`에 맞춰 정리하세요. Code variable name은 바꾸는 비용이 크면 그대로 두어도 됩니다.
- **Source**: Validator-C Notation Inconsistencies; Validator-C Recommended Standards.

### Task m4: 최종 통합을 위한 heatmap style 표준화
- **What**: Agent-1은 자체 palette와 heatmap setting을 사용합니다. Consistency review는 signed Choi heatmap에는 zero-centered `RdBu_r`, magnitude에는 `viridis`를 권장합니다.
- **Where**: `01_theory/main.ipynb`, Choi heatmap cells.
- **Why it matters**: Figure convention이 통일되면 최종 보고서가 읽기 쉬워집니다.
- **Suggested fix**: Local palette는 유지해도 되지만, Choi real/imaginary heatmap은 shared colormap/orientation convention에 맞추세요.
- **Source**: Validator-C Visual Style Issues; Validator-C Recommended Standards.

### Task m5: 간단한 style 또는 formatting note 추가
- **What**: Validator-B는 final integration에서 style을 강제할 예정이면 작은 `pyproject.toml` 또는 formatting note를 추가하라고 제안했습니다.
- **Where**: `01_theory/README.md` 또는 local project-style note.
- **Why it matters**: Final cleanup과 future contributor에게 기준을 제공합니다.
- **Suggested fix**: 어떤 formatter/style을 가정했는지 짧게 적거나, integration 단계에서 repo-level style file을 따른다고 명시하세요.
- **Source**: Validator-B Agent-1 Suggestion #1.

## Cross-cutting Notes

`92_validation_consistency/UNIFIED_GLOSSARY.md`를 따르세요: unnormalized Choi matrix, input-first tensor order `A \otimes B`, TP condition `Tr_B(C_\mathcal{E})=I_A`, code dimension은 `d_in`, `d_out`.
