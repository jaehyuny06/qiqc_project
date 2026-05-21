# Agent-4 Revision Log 한국어판

수정 날짜: 2026-05-22

## 완료된 작업

- `deterministic_comb_causality_check`를 추가해 deterministic-comb causality hierarchy와 weaker global TP check를 분리했다.
- RHP-style quantity가 full continuous RHP integral이 아니라 pseudo-inverse adjacent intermediate map을 사용하는 grid-based CP-divisibility witness임을 명확히 했다.
- `apply_choi_channel` 호출 순서를 unified API에 맞추었다.
- Dense-scaling warning을 code, notebook, README에 추가했다.
- BLP 계산이 sampled antipodal pure-state pair 위의 finite-grid approximation임을 설명했다.
- Requirements를 validation run version으로 pin했다.
- Quantum comb `T`, process tensor, `C_E` terminology를 표준화했다.
- Magnitude heatmap에 `viridis`를 사용하도록 정리했다.

## 검증

- Pytest: 7 passed.
- `main.ipynb` nbconvert execution 성공.
