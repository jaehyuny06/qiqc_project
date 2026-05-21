# Unified Glossary for Revision Round

## Core Objects

- Quantum channel: `\mathcal{E}: L(H_A) -> L(H_B)`.
- Input system: `A`, dimension `d_in`.
- Output system: `B`, dimension `d_out`.
- Kraus operators: `K_k`, with shape `(d_out, d_in)`.
- Choi matrix: `C_\mathcal{E}`.
- Channel difference: `\Phi = \mathcal{E}_0 - \mathcal{E}_1`, Choi matrix `C_\Phi`.
- Quantum comb/process tensor: `T`, ordered as `A0, B0, A1, B1, ...`.

## Shared Conventions

- Use the unnormalized Choi convention:

```text
C_E = sum_ij |i><j|_A tensor E(|i><j|)_B
```

- Trace preservation:

```text
Tr_B(C_E) = I_A
```

- Complete positivity:

```text
C_E >= 0
```

- A trace-preserving channel has:

```text
Tr(C_E) = d_in
```

## Recommended Code Names

- `kraus_to_choi(kraus_ops)`
- `choi_to_kraus(choi, tol=...)`
- `choi_to_natural(choi, d_in=None, d_out=None)`
- `natural_to_choi(natural, d_in=None, d_out=None)`
- `apply_choi_channel(choi, rho, d_in=None, d_out=None)`
- `is_cp(choi, tol=...)`
- `is_tp(choi, d_in, d_out=None, tol=...)`

## Plotting Standards

- Real/imaginary Choi heatmaps: `RdBu_r`, centered at zero.
- Magnitude Choi heatmaps: `viridis`.
- Use axis labels or tick labels that identify Choi basis ordering where space permits.
- Put `np.random.seed(42)` and palette definitions near the top of every notebook.

## Terminology Notes

- Use "diamond norm" only for the SDP or an analytically exact value.
- Use "diamond-distance proxy" only for heuristic Choi norm quantities.
- Use "quantum comb" for the Choi operator and "process tensor" when emphasizing multi-time dynamics.
- Use "process tomography" for the experimental protocol and "channel tomography" only as a broad synonym.
