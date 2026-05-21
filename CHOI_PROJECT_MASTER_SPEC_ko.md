# Choi Representation of Quantum Channels - Multi-Agent Project Specification 한국어판

이 문서는 프로젝트 초기 multi-agent 작업 사양의 한국어 companion 문서이다. 원문 `CHOI_PROJECT_MASTER_SPEC.md`에는 Phase 1 producer 작업과 Phase 2 validator 작업의 상세 지시가 들어 있다. 이 한글판은 현재 repository를 이해하고 관리하기 위한 읽기 쉬운 요약 사양이다.

## 0. 프로젝트 개요

주제는 **양자 채널의 Choi 표현**이다. Choi-Jamiołkowski isomorphism을 사용하면 quantum channel을 matrix로 나타낼 수 있고, 이 matrix를 통해 physical property와 practical computation을 다룰 수 있다.

공통 이론 배경:

- Kraus form: `E(rho) = sum_k K_k rho K_k^dagger`
- Choi matrix: channel을 input-output matrix로 표현한 것
- Stinespring dilation: 더 큰 system에서 unitary/isometry와 partial trace로 channel을 표현
- Natural/Liouville form: vectorized density matrix에 작용하는 superoperator

핵심 성질:

- `E`가 CP이면, 그리고 그때에만 `C_E >= 0`
- `E`가 TP이면, 그리고 그때에만 `Tr_B(C_E) = I_A`
- `rank(C_E)`는 최소 Kraus operator 개수와 연결된다.

## 1. Producer Layer

| Agent | Folder | 역할 |
| --- | --- | --- |
| Agent-1 | `01_theory/` | 이론적 기초와 channel representation 변환 |
| Agent-2 | `02_ibm_experiment/` | IBM Quantum process tomography 및 Choi matrix 재구성 |
| Agent-3 | `03_sdp_discrimination/` | Diamond norm SDP를 이용한 channel discrimination |
| Agent-4 | `04_quantum_combs/` | Non-Markovian dynamics와 quantum comb/process tensor |
| Agent-5 | `05_interactive_widget/` | Choi matrix와 Bloch deformation interactive widget |

각 producer는 `main.ipynb`, supporting Python module, `README.md`, `requirements.txt`, 가능하면 tests를 만든다. 현재 repository에는 한글판 `main_ko.ipynb`와 `README_ko.md`도 추가되어 있다.

## 2. Validator Layer

| Validator | Folder | 검토 초점 |
| --- | --- | --- |
| Validator-A | `90_validation_math/` | 수학적/물리적 정확성 |
| Validator-B | `91_validation_code/` | 코드 품질, 실행 가능성, 재현성 |
| Validator-C | `92_validation_consistency/` | notation, terminology, style, cross-folder consistency |

Validator는 producer code를 직접 고치지 않고 report를 작성한다. 이후 revision phase에서 producer 또는 integrator가 수정한다.

## 3. 공통 Convention

- Python 3.10+
- 핵심 library: NumPy, SciPy, Matplotlib
- Choi matrix convention:

```text
C_E = sum_ij |i><j|_A tensor E(|i><j|)_B
```

- Input system `A`가 첫 번째 tensor factor
- Output system `B`가 두 번째 tensor factor
- Trace preservation: `Tr_B(C_E) = I_A`
- 모든 notebook은 reproducibility를 위해 `np.random.seed(42)`를 설정한다.

## 4. Phase 흐름

1. Phase 1 Production: 5개 producer folder에서 독립적으로 구현.
2. Phase 2 Validation: 3개 validator가 수학/코드/일관성 검토.
3. Phase 3 Revision: validation report에 따라 producer 산출물 수정.
4. Phase 4 Integration: `choi_common`, bibliography, root README, master notebook으로 통합.

현재 repository는 Phase 4 통합까지 상당 부분 진행된 상태이다.

## 5. 현재 통합 산출물

- `choi_common/`: 중복 구현을 모은 shared library
- `00_master.ipynb`: 전체 프로젝트 통합 guided tour
- `94_integration/`: duplication analysis, library structure, migration plan/log, references, citation audit
- `main_ko.ipynb`: 각 producer notebook의 한글판
- `README_ko.md`: 주요 README의 한글 companion 문서

## 6. 주의 사항

원문 spec은 초기 독립 개발 규칙을 설명한다. 현재는 integration phase가 진행되어 `choi_common`을 공유 library로 사용한다. 따라서 새 구현이나 수정에서는 원문 spec의 “서로 import하지 않는다” 규칙보다 현재 통합 상태와 `choi_common` API를 우선적으로 확인해야 한다.
