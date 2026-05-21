# 양자 채널의 Choi 표현

## 개요

이 프로젝트는 양자 채널의 Choi 표현을 이론, process tomography, semidefinite programming, non-Markovian dynamics, interactive visualization이라는 다섯 관점에서 탐구한 course project이다. 핵심 아이디어는 quantum channel을 하나의 matrix, 즉 Choi matrix로 표현하면 complete positivity, trace preservation, Choi rank, channel distance 같은 중요한 성질을 선형대수로 확인할 수 있다는 점이다.

프로젝트는 quantum information의 기본 개념을 알고 있지만 이 구현에는 처음인 독자를 대상으로 작성되었다. 각 sub-project는 narrative notebook, Python helper module, tests, reproducible examples로 구성되어 있다. 개별 notebook은 독립적으로 읽을 수 있지만, 전체적으로는 같은 Choi convention이 이론, numerical experiment, IBM hardware-ready tomography, channel discrimination, multi-time process를 어떻게 연결하는지 보여 준다.

공통 convention은 unnormalized Choi matrix이다.

```text
C_E = sum_ij |i><j|_A tensor E(|i><j|)_B
```

여기서 input system이 첫 번째 tensor factor이고 output system이 두 번째 tensor factor이다. 이 convention에서는 trace preservation을 `Tr_B(C_E) = I_A`로 확인한다.

## 프로젝트 구조

```text
.
|-- 00_master.ipynb
|-- README.md
|-- README_ko.md
|-- CHOI_PROJECT_MASTER_SPEC.md
|-- CHOI_PROJECT_MASTER_SPEC_ko.md
|-- choi_common/
|   |-- README.md
|   |-- README_ko.md
|   |-- representations.py
|   |-- channels.py
|   |-- validation.py
|   |-- metrics.py
|   |-- visualization.py
|   |-- utils.py
|   `-- tests/
|-- 01_theory/
|   |-- main.ipynb
|   |-- main_ko.ipynb
|   |-- README.md
|   `-- README_ko.md
|-- 02_ibm_experiment/
|   |-- main.ipynb
|   |-- main_ko.ipynb
|   |-- README.md
|   `-- README_ko.md
|-- 03_sdp_discrimination/
|   |-- main.ipynb
|   |-- main_ko.ipynb
|   |-- README.md
|   `-- README_ko.md
|-- 04_quantum_combs/
|   |-- main.ipynb
|   |-- main_ko.ipynb
|   |-- README.md
|   `-- README_ko.md
|-- 05_interactive_widget/
|   |-- main.ipynb
|   |-- main_ko.ipynb
|   |-- README.md
|   `-- README_ko.md
`-- 94_integration/
    |-- REFERENCES.md
    |-- REFERENCES_ko.md
    |-- CITATION_AUDIT.md
    |-- CITATION_AUDIT_ko.md
    |-- MASTER_NOTEBOOK_NOTES.md
    `-- MASTER_NOTEBOOK_NOTES_ko.md
```

## 핵심 결과

- Complete positivity는 Choi matrix의 positive semidefiniteness와 같고, trace preservation은 `Tr_B(C_E) = I_A`와 같음을 수치적으로 확인했다.
- Kraus, Choi, Stinespring, natural representation 사이의 변환이 일관되게 동작하며, numerical Choi rank가 최소 Kraus operator 개수와 연결됨을 보였다.
- Process tomography workflow는 `X`, `H`, `CNOT`에 대한 noisy stand-in channel을 재구성하고, linear inversion, CPTP projection, fidelity, diamond-distance diagnostic을 비교했다.
- Equal-prior channel discrimination은 `p_success = 1/2 + 1/4 ||E_0 - E_1||_diamond`로 diamond norm과 연결되며, ancilla-assisted advantage 예제를 확인했다.
- Multi-time example은 각 시간의 channel이 valid해도 CP-divisibility가 실패할 수 있고, 재사용된 environment가 non-factorizing quantum comb를 만들 수 있음을 보여 준다.

## 권장 읽기 순서

1. `01_theory/main_ko.ipynb`: Choi convention과 representation conversion 학습.
2. `05_interactive_widget/main_ko.ipynb`: qubit Choi matrix와 Bloch action 시각화.
3. `02_ibm_experiment/main_ko.ipynb`: process tomography data에서 Choi matrix 재구성.
4. `03_sdp_discrimination/main_ko.ipynb`: Choi matrix를 channel discrimination 문제에 사용.
5. `04_quantum_combs/main_ko.ipynb`: single-step channel을 multi-time memory process로 확장.
6. `00_master.ipynb`: 전체 흐름을 한 번에 연결한 통합 guided tour.

## 설치

Python 3.10 이상을 권장한다.

```bash
python -m venv .venv
python -m pip install --upgrade pip setuptools wheel
python -m pip install -e .
```

각 폴더를 실행하기 전에 해당 requirements를 설치한다.

```bash
python -m pip install -r 01_theory/requirements.txt
python -m pip install -r 02_ibm_experiment/requirements.txt
python -m pip install -r 03_sdp_discrimination/requirements.txt
python -m pip install -r 04_quantum_combs/requirements.txt
python -m pip install -r 05_interactive_widget/requirements.txt
```

IBM Quantum hardware submission은 선택 사항이다. 기본 notebook들은 저장된 offline/simulated data로 실행 가능하다. IBM token을 사용할 경우 `QiskitRuntimeService.save_account(...)` 패턴을 따르고, token은 repository에 commit하지 않는다.

## 실행

```bash
jupyter notebook
```

또는 notebook을 비대화식으로 실행할 수 있다.

```bash
jupyter nbconvert --to notebook --execute 00_master.ipynb --output executed_master.ipynb
```

테스트는 다음과 같이 실행한다.

```bash
python -m pytest -q
```

## 참고문헌

통합 bibliography는 [94_integration/REFERENCES_ko.md](94_integration/REFERENCES_ko.md)와 [94_integration/references.bib](94_integration/references.bib)에 정리되어 있다.

## TODO

- 팀원 이름과 contribution을 최종 정보로 채운다.
- 수업명, instructor, acknowledgement, AI tool usage disclosure를 course policy에 맞게 정리한다.
- 최종 공개 전 license를 선택한다. 기본 제안은 MIT License이다.
