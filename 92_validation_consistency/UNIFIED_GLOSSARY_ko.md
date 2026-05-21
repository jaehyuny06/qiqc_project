# Revision Round용 통합 용어집

## 핵심 객체

- Quantum channel: `\mathcal{E}: L(H_A) -> L(H_B)`.
- Input system: `A`, dimension `d_in`.
- Output system: `B`, dimension `d_out`.
- Kraus operators: `K_k`, shape `(d_out, d_in)`.
- Choi matrix: `C_\mathcal{E}`.
- Channel difference: `\Phi = \mathcal{E}_0 - \mathcal{E}_1`, Choi matrix `C_\Phi`.
- Quantum comb/process tensor: `T`, subsystem order는 `A0, B0, A1, B1, ...`.

## 공통 Convention

- Unnormalized Choi convention을 사용합니다.

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

- Trace-preserving channel은 다음을 만족합니다.

```text
Tr(C_E) = d_in
```

## 권장 Code Name

- `kraus_to_choi(kraus_ops)`
- `choi_to_kraus(choi, tol=...)`
- `choi_to_natural(choi, d_in=None, d_out=None)`
- `natural_to_choi(natural, d_in=None, d_out=None)`
- `apply_choi_channel(choi, rho, d_in=None, d_out=None)`
- `is_cp(choi, tol=...)`
- `is_tp(choi, d_in, d_out=None, tol=...)`

## Plotting 표준

- Real/imaginary Choi heatmap: `RdBu_r`, zero-centered.
- Magnitude Choi heatmap: `viridis`.
- 공간이 허락하면 Choi basis ordering을 알 수 있도록 axis label 또는 tick label을 넣습니다.
- 모든 notebook 앞부분에 `np.random.seed(42)`와 palette definition을 둡니다.

## Terminology Notes

- "diamond norm"은 SDP 또는 analytically exact value에만 사용합니다.
- Heuristic Choi norm quantity에는 "diamond-distance proxy"라고 명확히 씁니다.
- Multi-time dynamics를 강조할 때는 "process tensor", Choi operator를 가리킬 때는 "quantum comb"를 사용합니다.
- Experimental protocol에는 "process tomography"를 사용하고, "channel tomography"는 넓은 의미의 동의어로만 사용합니다.
