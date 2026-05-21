# Agent-5 Interactive Choi Widget

Interactive visualization deliverable for the Choi representation of qubit quantum channels.

![Widget preview](figures/widget_preview.png)

## What Is Included

- `main.ipynb`: narrative notebook with the live ipywidgets dashboard and static preview.
- `channel_utils.py`: local channel constructors and Choi utilities using the project convention
  `C_E = sum_ij |i><j| tensor E(|i><j|)`.
- `widget_core.py`: dashboard rendering, Bloch deformation, Kraus extraction, eigenspectrum, and indicators.
- `test_widget_core.py`: focused numerical checks for CP/TP status, partial trace, and channel action.
- `requirements.txt`: dependencies for this folder only.

## Supported Channels

- Depolarizing
- Amplitude damping
- Phase damping
- Bit flip
- Phase flip
- General Pauli channel
- General unital qubit map via Bloch-axis scaling
- Convex mixture of two supported channels

The unital mode intentionally permits non-CP parameter choices so the CP indicator can demonstrate the Choi-positivity condition directly.

## Run Instructions

From this folder:

```bash
pip install -r requirements.txt
jupyter notebook main.ipynb
```

For a quick non-interactive verification:

```bash
pytest -q
python -c "from widget_core import get_channel_choi, compute_indicators; print(compute_indicators(get_channel_choi('Depolarizing', {'p': 0.2})))"
```

## Notes

The widget is fully local and does not require IBM Quantum access, Qiskit credentials, or network connectivity after dependencies are installed.  The Choi matrix is unnormalized; a trace-preserving qubit channel has `trace(C) = 2`.
