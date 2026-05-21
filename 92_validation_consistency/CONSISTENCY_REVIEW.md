# Cross-Folder Consistency Review

Validator-C reviewed notation, terminology, function naming, visual style, and document voice across the five producer folders plus the master specification. Producer files were not modified.

## Notation Inconsistencies

| Concept | Agent-1 | Agent-2 | Agent-3 | Agent-4 | Agent-5 | Recommended |
|---------|---------|---------|---------|---------|---------|-------------|
| Choi matrix | `C_E`, `C` | `C`, `choi` | `C_Phi`, `choi` | `T` for comb, `C` for channel | `C`, `choi` | Use `C_\mathcal{E}` for single channels and `T` only for combs/process tensors |
| Channel | `E`, `E1`, `E2` | `E`, "process" | `\mathcal{E}_0`, `\mathcal{E}_1`, `\Phi` for differences | "family", "process tensor" | "channel" | Use `\mathcal{E}` for channels and `\Phi` only for channel differences |
| Kraus operators | `K_k`, `op` | `Kraus`, `kraus_ops` | `kraus_ops` | `kraus_ops` | `kraus_ops`, "eigenoperators" | Use `K_k` in prose and `kraus_ops` in code |
| Maximally entangled vector | `|\Omega\rangle` implied, "maximally entangled" | mostly avoided | not central | generalized Choi | not central | Use unnormalized `|\Omega\rangle = sum_i |i>|i>` |
| TP partial trace | `Tr_out(C)=I_in` | `Tr_output(C)=I_input` | `Tr_output` | global trace over outputs for comb | `Tr_B(C)=I_A` | Use `Tr_B(C_\mathcal{E})=I_A` for channel Choi; spell out output subsystem |
| Normalization | unnormalized Choi | unnormalized Choi | unnormalized Choi | unnormalized comb/channel Choi | unnormalized Choi | Keep unnormalized Choi everywhere; state `Tr(C)=d_in` for TP channels |

## Terminology Inconsistencies

- Agent-2 uses "process fidelity" and "average gate fidelity" correctly, but reports `diamond-distance proxy`; Agent-3 uses true "diamond norm". Integration should not present the proxy as a diamond norm.
- Agent-4 alternates between "quantum comb", "process tensor", "multi-use channel", and "memory comb". These are related but not identical in formal scope. For the final report, define process tensor/quantum comb once and then use "quantum comb" for the Choi operator object.
- Agent-5 labels non-physical overlap values as process fidelities in the widget indicator path. If non-CP maps are allowed for teaching, call these "Choi overlaps" outside the physical region.
- No meaningful Korean/English terminology conflict appears in the produced folders; the active notebooks are in English.

## Function Signature Mismatches

- `kraus_to_choi`
  - Agent-1: `kraus_to_choi(kraus_ops: list[np.ndarray]) -> np.ndarray`
  - Agent-2: `kraus_to_choi(kraus_ops: list[np.ndarray]) -> np.ndarray`
  - Agent-3: `kraus_to_choi(kraus_ops: list[np.ndarray]) -> Array`
  - Agent-4: `kraus_to_choi(kraus_ops: Sequence[Array]) -> Array`
  - Agent-5: `kraus_to_choi(kraus_ops: Sequence[Array]) -> Array`
  - Recommended: `kraus_to_choi(kraus_ops: Sequence[np.ndarray]) -> np.ndarray`

- Choi application
  - Agent-1: `apply_channel(rho, kraus_ops)` only applies Kraus form.
  - Agent-2: `apply_channel_to_state(rho, choi, d_out=None)`.
  - Agent-3: `apply_choi_to_state(choi, rho, d_in, d_out)`.
  - Agent-4: `apply_choi_channel(rho, choi, d_in=None, d_out=None)`.
  - Agent-5: `apply_choi_to_state(choi, rho)` for qubits only.
  - Recommended: use `apply_choi_channel(choi, rho, d_in=None, d_out=None)` in the integrated code, and document argument order.

- Dimension variables
  - Agents use `d`, `dim`, `d_in`, `d_out`, `d_A`, and `d_B`.
  - Recommended: use `d_in`, `d_out` in code; use `A` for input and `B` for output in prose.

- Depolarizing parameters
  - All agents use `p`, but the Pauli-channel meaning of `p` differs from the replacement-channel meaning in explanatory text.
  - Recommended: reserve `p` for the replacement depolarizing strength `E(rho)=(1-p)rho+p I/d`, and use `p_x,p_y,p_z` for Pauli probabilities.

## Visual Style Issues

- Each notebook defines a palette, but the palettes differ:
  - Agent-1: dictionary palette in `01_theory/main.ipynb`
  - Agent-2: `#2F4858`, `#33658A`, `#86BBD8`, `#F6AE2D`, `#F26419`
  - Agent-3: `#2E86AB`, `#F18F01`, `#C73E1D`, `#6A994E`, `#5B2A86`
  - Agent-4: dictionary palette in `04_quantum_combs/main.ipynb`
  - Agent-5: dictionary palette in `05_interactive_widget/widget_core.py`
- Heatmaps use different colormaps (`RdBu_r`, `viridis`, `magma`). This is not wrong, but final integrated figures should standardize Choi real/imaginary heatmaps to `RdBu_r` centered at zero and absolute-value heatmaps to `viridis`.
- Figure sizes are generally reasonable and outputs are not excessively long.

## Reference and Document Voice Issues

- README structures are broadly similar: overview, files, run instructions, key results.
- Agent-1 and Agent-3 are more mathematically formal; Agent-5 is more interface-focused. This is appropriate for the subtopics but should be harmonized in the final report introduction.
- Citations are mostly textbook/documentation references rather than full bibliography entries. The integrated report should use one bibliography format.

## Recommended Standards (to be applied in revision round)

- Choi matrix: `C_\mathcal{E}` for a channel, `C_\Phi` for a channel difference, `T` for a comb/process tensor.
- Channel notation: `\mathcal{E}` for one channel, `\mathcal{E}_0,\mathcal{E}_1` for discrimination, `\Phi=\mathcal{E}_0-\mathcal{E}_1` for differences.
- Tensor order: input first, output second, stated as `A \otimes B`.
- TP condition: `Tr_B(C_\mathcal{E})=I_A`.
- Choi normalization: unnormalized Choi matrices throughout.
- Code dimensions: `d_in`, `d_out`.
- Code function names: prefer `kraus_to_choi`, `choi_to_kraus`, `choi_to_natural`, `natural_to_choi`, `apply_choi_channel`.
- Heatmaps: `RdBu_r` for signed real/imaginary parts; `viridis` for magnitudes.
- Dependencies: pin versions for the final reproducible release.
