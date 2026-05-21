# Agent-1: Theoretical Foundations and Channel Representations

This folder contains the Agent-1 deliverable for the Choi representation project. It implements the core representation conversions for finite-dimensional quantum channels using the shared convention

\[
C_\mathcal{E} = \sum_{i,j} |i\rangle\langle j| \otimes \mathcal{E}(|i\rangle\langle j|),
\]

where the input system is the first tensor factor and the output system is the second tensor factor.

## Contents

- `channel_reps.py`: typed, documented functions for Kraus, Choi, Stinespring, and natural/Liouville representations.
- `test_channel_reps.py`: pytest coverage for conversions, standard channels, CP/TP checks, composition, and edge cases.
- `main.ipynb`: narrative notebook with examples, numerical checks, plots, and round-trip conversions.
- `requirements.txt`: minimal dependencies for this folder.

## Implemented Standard Channels

- Identity
- Bit-flip
- Phase-flip
- General Pauli
- Depolarizing
- Amplitude damping
- Phase damping

## Key Results Demonstrated

- Complete positivity is equivalent to Choi positive semidefiniteness.
- Trace preservation is equivalent to `Tr_out(C) = I_in`.
- The numerical Choi rank equals the minimum number of Kraus operators.
- Kraus, Choi, Stinespring, and natural forms can be converted consistently.
- Channel composition is simple matrix multiplication in natural form and is exposed through `compose_channels_choi`.

## Run Instructions

From this folder:

```bash
pip install -r requirements.txt
python -m pytest -q
python -m nbconvert --to notebook --execute main.ipynb --output executed_main.ipynb
```

The notebook sets `np.random.seed(42)` at the start for reproducibility.
