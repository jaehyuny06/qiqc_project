# Agent-2: IBM Quantum Process Tomography

이 폴더는 Choi representation project의 quantum process tomography(QPT) workflow를 담고 있다. 기본 실행은 offline reproducible하게 설계되어 있어 IBM credentials 없이도 실행할 수 있으며, 실제 IBM Quantum hardware submission은 별도 절차로 분리되어 있다.

공통 convention은 unnormalized Choi matrix이며, input system `A`가 먼저 오고 output system `B`가 두 번째이다. Trace preservation은 `Tr_B(C_E) = I_A`로 확인한다.

## 구성

- `main.ipynb`: 영어 QPT notebook.
- `main_ko.ipynb`: 한국어 QPT notebook.
- `qpt_tools.py`: Choi construction, linear inversion, CPTP/MLE projection, SDP diamond diagnostics, plotting, optional Qiskit submission helper.
- `test_qpt_tools.py`: offline numerical routine test.
- `data/raw_results.json`: reproducibility를 위한 sample simulated result.
- `data/sample_simulated_results.json`: 빠른 확인용 compact output.
- `requirements.txt`: Qiskit/IBM workflow 포함 dependency.

## Offline Reproducible Design

Notebook은 기본적으로 IBM hardware를 호출하지 않는다. `X`, `H`, `CNOT` ideal Choi matrix를 만들고 deterministic noisy stand-in을 사용한다.

- `X`: unitary 뒤 amplitude damping.
- `H`: unitary 뒤 depolarizing noise.
- `CNOT`: two-qubit unitary 뒤 global depolarizing noise.

One-qubit gate에서는 `|0>`, `|1>`, `|+>`, `|+i>` 입력을 사용해 linear inversion을 수행한다. MLE step은 nearest CPTP Choi projection을 CVXPY로 푼다.

## IBM Hardware Flow

실제 hardware submission은 queue time 때문에 notebook 기본 실행에서 제외되어 있다. IBM account를 설정한 뒤 backend를 선택하고, `run_process_tomography`를 호출해 job ID와 raw result를 저장한다. 이후 job이 완료되면 저장된 ID로 결과를 회수해 local analysis를 다시 실행한다.

## 실행

```bash
python -m pip install -r requirements.txt
python -m pytest -q
jupyter nbconvert --to notebook --execute main_ko.ipynb --output executed_main_ko.ipynb
```

## 핵심 출력

Sample data는 process fidelity, raw process fidelity, average gate fidelity, CP/TP status, Kraus weights, true half-diamond distance, Choi-norm proxy, heuristic noise label을 제공한다. 값은 simulated result이며 hardware claim이 아니다.
