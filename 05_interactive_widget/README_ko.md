# Agent-5: Interactive Choi Widget

이 폴더는 qubit quantum channel의 Choi matrix를 시각화하는 interactive widget을 제공한다.

## 구성

- `main.ipynb`: 영어 widget notebook.
- `main_ko.ipynb`: 한국어 widget notebook.
- `channel_utils.py`: legacy compatibility helper.
- `widget_core.py`: dashboard rendering, Bloch deformation, Kraus extraction, eigenspectrum, indicator logic.
- `test_widget_core.py`: CP/TP, partial trace, channel action test.
- `figures/widget_preview.png`: static preview.

## 지원 채널

- Depolarizing
- Amplitude damping
- Phase damping
- Bit flip
- Phase flip
- General Pauli channel
- General unital qubit map via Bloch-axis scaling
- 두 supported channel의 convex mixture

Unital mode는 의도적으로 non-CP parameter를 허용한다. 이를 통해 `C_E >= 0` 조건이 CP indicator와 어떻게 연결되는지 직접 볼 수 있다.

## 실행

```bash
pip install -r requirements.txt
jupyter notebook main_ko.ipynb
```

비대화식 빠른 확인:

```bash
pytest -q
python -c "from widget_core import get_channel_choi, compute_indicators; print(compute_indicators(get_channel_choi('Depolarizing', {'p': 0.2})))"
```

Widget은 local에서 실행되며 IBM Quantum access, Qiskit credential, network connection이 필요 없다.
