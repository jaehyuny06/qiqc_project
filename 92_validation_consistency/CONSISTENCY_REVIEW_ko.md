# 폴더 간 일관성 검토

Validator-C는 다섯 producer 폴더와 master specification을 기준으로 notation, terminology, function naming, visual style, document voice를 검토했습니다. Producer 파일은 수정하지 않았습니다.

## Notation 불일치

| Concept | Agent-1 | Agent-2 | Agent-3 | Agent-4 | Agent-5 | 권장안 |
|---------|---------|---------|---------|---------|---------|--------|
| Choi matrix | `C_E`, `C` | `C`, `choi` | `C_Phi`, `choi` | comb에는 `T`, channel에는 `C` | `C`, `choi` | Single channel에는 `C_\mathcal{E}`, comb/process tensor에는 `T`만 사용 |
| Channel | `E`, `E1`, `E2` | `E`, "process" | `\mathcal{E}_0`, `\mathcal{E}_1`, difference에는 `\Phi` | "family", "process tensor" | "channel" | Channel에는 `\mathcal{E}`, channel difference에는 `\Phi`만 사용 |
| Kraus operators | `K_k`, `op` | `Kraus`, `kraus_ops` | `kraus_ops` | `kraus_ops` | `kraus_ops`, "eigenoperators" | Prose에서는 `K_k`, code에서는 `kraus_ops` |
| Maximally entangled vector | `|\Omega\rangle` 암시, "maximally entangled" | 거의 사용하지 않음 | 중심 개념 아님 | generalized Choi | 중심 개념 아님 | Unnormalized `|\Omega\rangle = sum_i |i>|i>` 사용 |
| TP partial trace | `Tr_out(C)=I_in` | `Tr_output(C)=I_input` | `Tr_output` | comb output 전체 trace | `Tr_B(C)=I_A` | Channel Choi에는 `Tr_B(C_\mathcal{E})=I_A` 사용 |
| Normalization | unnormalized Choi | unnormalized Choi | unnormalized Choi | unnormalized comb/channel Choi | unnormalized Choi | 모든 곳에서 unnormalized Choi 유지, TP channel은 `Tr(C)=d_in` 명시 |

## Terminology 불일치

- Agent-2는 "process fidelity"와 "average gate fidelity"를 적절히 사용하지만, `diamond-distance proxy`를 보고합니다. Agent-3의 true "diamond norm"과 통합할 때 proxy를 diamond norm처럼 제시하면 안 됩니다.
- Agent-4는 "quantum comb", "process tensor", "multi-use channel", "memory comb"를 번갈아 사용합니다. 서로 관련된 용어지만 formal scope가 완전히 같지는 않습니다. 최종 보고서에서는 process tensor/quantum comb를 한 번 정의한 뒤, Choi operator object에는 "quantum comb"를 일관되게 쓰는 것이 좋습니다.
- Agent-5는 non-physical overlap value를 widget indicator에서 process fidelity라고 부릅니다. 교육 목적상 non-CP map을 허용한다면, physical region 밖에서는 "Choi overlap"이라고 부르는 것이 더 안전합니다.
- 생성된 producer 폴더에는 의미 있는 Korean/English terminology conflict가 없습니다. 현재 notebook들은 영어로 작성되어 있습니다.

## Function Signature 불일치

- `kraus_to_choi`
  - Agent-1: `kraus_to_choi(kraus_ops: list[np.ndarray]) -> np.ndarray`
  - Agent-2: `kraus_to_choi(kraus_ops: list[np.ndarray]) -> np.ndarray`
  - Agent-3: `kraus_to_choi(kraus_ops: list[np.ndarray]) -> Array`
  - Agent-4: `kraus_to_choi(kraus_ops: Sequence[Array]) -> Array`
  - Agent-5: `kraus_to_choi(kraus_ops: Sequence[Array]) -> Array`
  - 권장안: `kraus_to_choi(kraus_ops: Sequence[np.ndarray]) -> np.ndarray`

- Choi application
  - Agent-1: `apply_channel(rho, kraus_ops)`는 Kraus form만 적용합니다.
  - Agent-2: `apply_channel_to_state(rho, choi, d_out=None)`.
  - Agent-3: `apply_choi_to_state(choi, rho, d_in, d_out)`.
  - Agent-4: `apply_choi_channel(rho, choi, d_in=None, d_out=None)`.
  - Agent-5: `apply_choi_to_state(choi, rho)`, qubit 전용.
  - 권장안: 통합 코드에서는 `apply_choi_channel(choi, rho, d_in=None, d_out=None)`를 사용하고 argument order를 문서화하세요.

- Dimension variables
  - Agents는 `d`, `dim`, `d_in`, `d_out`, `d_A`, `d_B`를 섞어 씁니다.
  - 권장안: code에서는 `d_in`, `d_out`; prose에서는 input에 `A`, output에 `B`.

- Depolarizing parameters
  - 모든 agent가 `p`를 쓰지만, Pauli-channel probability와 replacement-channel depolarizing strength의 의미가 다를 수 있습니다.
  - 권장안: `p`는 `E(rho)=(1-p)rho+p I/d`의 replacement depolarizing strength로 예약하고, Pauli probability에는 `p_x,p_y,p_z`를 사용하세요.

## Visual Style 이슈

- 각 notebook은 palette를 정의하지만 서로 다릅니다.
  - Agent-1: `01_theory/main.ipynb` 안의 dictionary palette
  - Agent-2: `#2F4858`, `#33658A`, `#86BBD8`, `#F6AE2D`, `#F26419`
  - Agent-3: `#2E86AB`, `#F18F01`, `#C73E1D`, `#6A994E`, `#5B2A86`
  - Agent-4: `04_quantum_combs/main.ipynb` 안의 dictionary palette
  - Agent-5: `05_interactive_widget/widget_core.py` 안의 dictionary palette
- Heatmap colormap도 `RdBu_r`, `viridis`, `magma` 등으로 다릅니다. 틀린 것은 아니지만, 최종 통합 figure에서는 real/imaginary Choi heatmap은 zero-centered `RdBu_r`, absolute-value heatmap은 `viridis`로 통일하는 것이 좋습니다.
- Figure size는 대체로 적절하며, 과도하게 긴 output은 없습니다.

## Reference 및 문서 tone 이슈

- README 구조는 대체로 비슷합니다: overview, files, run instructions, key results.
- Agent-1과 Agent-3은 수학적 formalism이 더 강하고, Agent-5는 interface 중심입니다. 주제 특성상 자연스럽지만 최종 보고서 introduction에서는 tone을 맞추는 것이 좋습니다.
- Citation은 대부분 textbook/documentation reference 수준입니다. 통합 보고서에서는 하나의 bibliography format을 쓰는 것이 좋습니다.

## Revision round 권장 표준

- Choi matrix: channel에는 `C_\mathcal{E}`, channel difference에는 `C_\Phi`, comb/process tensor에는 `T`.
- Channel notation: 하나의 channel에는 `\mathcal{E}`, discrimination에는 `\mathcal{E}_0,\mathcal{E}_1`, difference에는 `\Phi=\mathcal{E}_0-\mathcal{E}_1`.
- Tensor order: input first, output second, `A \otimes B`로 명시.
- TP condition: `Tr_B(C_\mathcal{E})=I_A`.
- Choi normalization: 전체 프로젝트에서 unnormalized Choi matrix 사용.
- Code dimensions: `d_in`, `d_out`.
- Code function names: `kraus_to_choi`, `choi_to_kraus`, `choi_to_natural`, `natural_to_choi`, `apply_choi_channel` 선호.
- Heatmap: signed real/imaginary part에는 `RdBu_r`, magnitude에는 `viridis`.
- Dependencies: 최종 reproducible release에서는 version pin을 적용.
