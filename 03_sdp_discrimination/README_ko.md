# Agent-3: SDP Channel Discrimination

이 폴더는 Choi representation과 Watrous의 diamond norm SDP를 사용해 equal-prior quantum channel discrimination을 구현한다.

공통 convention:

```text
C_E = sum_ij |i><j| tensor E(|i><j|)
```

Input system이 첫 번째 tensor factor이다. Channel difference는 `Phi = E_0 - E_1`, 그 Choi matrix는 `C_Phi`로 쓴다.

## 구성

- `main.ipynb`: 영어 SDP narrative notebook.
- `main_ko.ipynb`: 한국어 SDP narrative notebook.
- `sdp_tools.py`: Choi helper, standard qubit channel, diamond-norm SDP, optimal input/POVM extraction, product strategy, n-shot discrimination.
- `test_sdp_tools.py`: physical constraint와 closed-form result test.
- `requirements.txt`: local dependency.

## 핵심 결과

- Equal prior에서 `p_success = 1/2 + 1/4 ||E_0 - E_1||_diamond`.
- SDP 결과는 qubit Pauli/depolarizing channel의 closed-form formula와 일치한다.
- Identity vs completely depolarizing qubit channel은 entanglement advantage를 보여 준다. Ancilla-assisted optimum은 `0.875`, product-input strategy는 `0.75`이다.

## 실행

```bash
python -m pip install -r requirements.txt
python -m pytest -q
jupyter nbconvert --to notebook --execute main_ko.ipynb --output executed_main_ko.ipynb
```

Solver는 MOSEK, CLARABEL, SCS 순서로 사용한다. Solver별 tolerance 차이는 예상 가능하다.
