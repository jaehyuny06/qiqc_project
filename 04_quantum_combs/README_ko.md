# Agent-4: Non-Markovian Dynamics와 Quantum Combs

이 폴더는 Choi representation을 single channel에서 multi-time process로 확장한다. Quantum comb/process tensor는 시간 사이 memory와 correlation을 표현하는 generalized Choi operator이다.

공통 channel convention:

```text
C_E = sum_ij |i><j|_A tensor E(|i><j|)_B
```

Comb subsystem order는 `A0, B0, A1, B1, ...`이다.

## 구성

- `main.ipynb`: 영어 narrative notebook.
- `main_ko.ipynb`: 한국어 narrative notebook.
- `combs_tools.py`: comb construction, marginal channel, causality check, Markovianity check, BLP/RHP witness.
- `non_markovian_dynamics.py`: exponential dephasing, oscillatory dephasing, collision model.
- `test_combs_tools.py`: partial trace, TP check, comb construction, witness test.

## 핵심 결과

1. 각 time의 channel family가 valid해도 intermediate map의 CP-divisibility가 실패할 수 있다.
2. BLP finite-grid estimate는 trace-distance revival을 통해 memory effect를 감지한다.
3. RHP-style grid witness는 pseudo-inverse intermediate map의 Choi negativity로 memory effect를 감지한다.
4. 재사용된 environment를 가진 two-use collision model은 one-step marginal product로 factorize되지 않는 quantum comb를 만든다.

## 실행

```bash
python -m pip install -r requirements.txt
python -m pytest -q
jupyter nbconvert --to notebook --execute main_ko.ipynb --output executed_main_ko.ipynb
```

## 한계

Comb constructor는 small educational example용 dense implementation이다. Qubit `N`-step comb도 matrix dimension이 `4**N` by `4**N`로 증가하므로 large-scale process tensor tomography에는 적합하지 않다.
