# choi_common

`choi_common` contains shared utilities for the Choi Representation multi-agent
project. It centralizes duplicated code from the producer folders while keeping
the project convention consistent:

```text
C_E = sum_ij |i><j|_A tensor E(|i><j|)_B
```

The Choi matrix is unnormalized, the input system is first, and trace
preservation is checked as:

```text
Tr_B(C_E) = I_A
```

## Modules

- `representations`: Kraus, Choi, Stinespring, and natural representation conversions.
- `channels`: Standard channel constructors and Choi convenience constructors.
- `validation`: CP/TP checks, partial traces, Choi rank, and residual diagnostics.
- `metrics`: Process fidelity, trace distance, diamond-norm SDP helpers, and discrimination metrics.
- `visualization`: Choi heatmaps and one-qubit Bloch visualizations.
- `utils`: Low-level matrix, dimension, and probability helpers.

## Depolarizing Convention

The default depolarizing convention is:

```python
depolarizing_channel(p, convention="replacement")
```

This means:

```text
E_p(rho) = (1-p) rho + p Tr(rho) I/d
```

For the Agent-2 and Agent-5 qubit examples that interpret `p` as total
non-identity Pauli-error probability, pass:

```python
depolarizing_channel(p, d=2, convention="pauli_error")
```

## Installation

From the project root:

```bash
pip install -e .
```
