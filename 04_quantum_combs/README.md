# Agent-4: Non-Markovian Dynamics and Quantum Combs

This folder extends the Choi representation from a single channel to multi-time
processes.  The implementation is self-contained and follows the project
convention

```text
C_E = sum_ij |i><j|_A tensor E(|i><j|)_B
```

with comb subsystem order `A0, B0, A1, B1, ...`.

## Contents

- `combs_tools.py`: Choi utilities, finite-memory quantum-comb construction,
  marginal channels, deterministic-comb causality checks, a product-factorization
  Markovianity check, and BLP/RHP-style non-Markovianity witnesses.
- `non_markovian_dynamics.py`: qubit toy models used in the notebook:
  exponential dephasing, oscillatory dephasing with revivals, and a collision
  model with a reused environment.
- `test_combs_tools.py`: unit tests for partial traces, Choi TP checks, comb
  construction, Markovian factorization, and non-Markovianity witnesses.
- `main.ipynb`: narrative demonstration with plots for BLP/RHP behavior and
  quantum-comb/process-tensor intuition.

## Key Results

1. A single-time channel family can be valid at every time while failing
   CP-divisibility between intermediate times.
2. The finite-grid BLP estimate detects non-Markovianity through trace-distance
   revivals over sampled antipodal pure-state pairs.
3. The RHP-style grid witness detects the same memory effect as negativity in
   the pseudo-inverse reconstructed intermediate-map Choi matrix.
4. A two-use collision model with a reused environment produces a positive
   quantum comb `T` that does not factorize into the product of its one-step
   marginals.

## Run Instructions

From this folder:

```powershell
python -m pip install -r requirements.txt
python -m pytest -q
jupyter nbconvert --to notebook --execute main.ipynb --output executed_main.ipynb
```

The notebook sets `np.random.seed(42)` and defines its plot palette near the
top, following the shared project conventions.

## Limitations

The comb constructor is intentionally scoped to small educational examples. It
builds the Choi operator of a finite-memory, multi-time channel by explicitly
looping over computational-basis operators, so the matrix dimension grows as
`4**N` for qubit `N`-step combs.  This is suitable for two-step and small
three-step demonstrations, not large-scale process-tensor tomography. The
operator embedding and comb construction are dense implementations throughout.

The RHP function is a grid-based divisibility witness rather than a continuous
optimization.  It uses a pseudoinverse for intermediate maps, which is robust
for demonstrations but should be replaced by model-aware formulas near singular
times in precision studies.

## References

- Chiribella, D'Ariano, and Perinotti, "Quantum circuit architecture", 2008.
- Pollock et al., "Non-Markovian quantum processes: Complete framework and
  efficient characterization", 2018.
- Breuer, Laine, and Piilo, "Measure for the degree of non-Markovian behavior",
  2009.
- Rivas, Huelga, and Plenio, "Entanglement and Non-Markovianity of Quantum
  Evolutions", 2010.
