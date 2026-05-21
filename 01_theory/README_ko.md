# Agent-1: 이론적 기초와 Channel Representations

이 폴더는 Choi representation project의 Agent-1 산출물이다. Finite-dimensional quantum channel의 Kraus, Choi, Stinespring, natural/Liouville representation 변환을 다룬다.

공통 convention:

```text
C_E = sum_ij |i><j|_A tensor E(|i><j|)_B
```

Input system은 첫 번째 tensor factor이고 output system은 두 번째 tensor factor이다.

## 구성

- `main.ipynb`: 영어 narrative notebook.
- `main_ko.ipynb`: 한국어 narrative notebook.
- `channel_reps.py`: representation conversion과 Agent-1 helper.
- `test_channel_reps.py`: conversion, CP/TP, standard channel, composition test.
- `requirements.txt`: 이 폴더 실행에 필요한 dependency.

## 구현된 표준 채널

- Identity
- Bit-flip
- Phase-flip
- General Pauli
- Depolarizing
- Amplitude damping
- Phase damping

## 핵심 결과

- Complete positivity는 Choi positive semidefiniteness와 같다.
- Trace preservation은 `Tr_out(C) = I_in`으로 확인한다.
- Numerical Choi rank는 필요한 Kraus operator의 최소 개수와 연결된다.
- Kraus, Choi, Stinespring, natural form 사이의 변환이 일관되게 동작한다.
- Natural form에서는 channel composition이 matrix multiplication으로 표현된다.

## 실행

```bash
pip install -r requirements.txt
python -m pytest -q
python -m nbconvert --to notebook --execute main_ko.ipynb --output executed_main_ko.ipynb
```
