# Agent-3: SDP Channel Discrimination

This folder implements equal-prior quantum channel discrimination using the
Choi representation and Watrous's semidefinite program for the diamond norm.
All code is self-contained in this folder and follows the shared convention

```text
C_E = sum_ij |i><j| tensor E(|i><j|)
```

with the input system as the first tensor factor.

## Contents

- `sdp_tools.py` - Choi helpers, standard qubit channels, diamond-norm SDP,
  optimal input/POVM extraction, product-strategy comparison, and `n`-shot
  tensor-power discrimination.
- `test_sdp_tools.py` - pytest checks against physical constraints and
  closed-form Pauli/depolarizing results.
- `main.ipynb` - narrative notebook with the SDP formulation, case studies,
  plots, entanglement advantage, and scaling discussion.
- `requirements.txt` - local dependencies.

## Key Results

- For two channels with equal prior,
  `p_success = 1/2 + 1/4 ||E_0 - E_1||_diamond`.
- The SDP results agree numerically with closed-form one-qubit Pauli-channel
  formulas.  In particular, for qubit depolarizing channels
  `||D_p - D_q||_diamond = 3 |p-q| / 2`.
- Identity vs. the completely depolarizing qubit channel shows strict
  entanglement advantage: the ancilla-assisted optimum is `0.875`, while the
  best product-input strategy is `0.75`.

## Run Instructions

From this folder:

```bash
python -m pip install -r requirements.txt
python -m pytest -q
jupyter nbconvert --to notebook --execute main.ipynb --output executed_main.ipynb
```

`sdp_tools.py` automatically prefers MOSEK if it is installed.  Otherwise it
uses an open-source CVXPY conic solver, with SCS as the reliable fallback.

## Notes on Scaling

The SDP variable acts on input-output space, so matrix dimensions grow as
`d_in * d_out`.  The `n_shot_discrimination` helper constructs tensor-power
Choi matrices, so it should only be used for small examples such as qubit
channels with `n <= 2` or `n <= 3` depending on the available solver.
