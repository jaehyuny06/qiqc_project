# choi_common

`choi_common`은 Choi Representation multi-agent project에서 공통으로 쓰이는 utility library이다. producer folder들에 중복되어 있던 channel constructor, representation conversion, CP/TP validation, metric, visualization helper를 한곳으로 모았다.

공통 Choi convention은 다음과 같다.

```text
C_E = sum_ij |i><j|_A tensor E(|i><j|)_B
```

Choi matrix는 unnormalized이고, input system이 첫 번째 tensor factor이다. Trace preservation은 다음 조건으로 확인한다.

```text
Tr_B(C_E) = I_A
```

## Modules

- `representations`: Kraus, Choi, Stinespring, natural representation 변환.
- `channels`: 표준 channel constructor와 Choi matrix convenience constructor.
- `validation`: CP/TP check, partial trace, Choi rank, residual diagnostic.
- `metrics`: process fidelity, trace distance, diamond norm SDP helper, discrimination metric.
- `visualization`: Choi heatmap과 one-qubit Bloch visualization.
- `utils`: matrix validation, dimension inference, probability helper.

## Depolarizing Convention

기본 depolarizing convention은 replacement probability이다.

```python
depolarizing_channel(p, convention="replacement")
```

이는 다음 map을 의미한다.

```text
E_p(rho) = (1-p) rho + p Tr(rho) I/d
```

Agent-2와 Agent-5의 qubit 예제처럼 `p`를 non-identity Pauli error의 총확률로 해석하려면 다음과 같이 명시한다.

```python
depolarizing_channel(p, d=2, convention="pauli_error")
```

## Installation

프로젝트 root에서 editable mode로 설치한다.

```bash
pip install -e .
```
