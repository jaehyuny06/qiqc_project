# Agent-5 Revision Log 한국어판

수정 날짜: 2026-05-22

## 완료된 작업

- `apply_choi_channel(choi, rho, d_in=None, d_out=None)` helper를 추가하고 qubit Choi matrix만 지원함을 문서화했다.
- Non-CP 또는 non-TP map에서는 process fidelity label 대신 raw Choi overlap indicator와 warning을 표시하도록 수정했다.
- Widget이 qubit-only이고 slider/dropdown update마다 full Matplotlib dashboard를 다시 그린다는 점을 README와 notebook에 설명했다.
- Requirements를 validated version으로 pin했다.
- Shared unnormalized Choi convention, `Tr_B(C_E)=I_A`, `Tr(C_E)=d_in` 표기를 README, notebook, helper doc, display label에 반영했다.
- Signed real/imaginary Choi heatmap에는 `RdBu_r`를 유지하고 preview image를 regenerate했다.

## 검증

- Pytest 통과.
- `main.ipynb` nbconvert execution 성공.
