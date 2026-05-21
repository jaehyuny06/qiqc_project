# Agent-2 Revision Log 한국어판

수정 날짜: 2026-05-22

## 완료된 작업

- True SDP diamond norm 기반 `diamond_norm_sdp`, `diamond_norm_distance`를 추가하고, Choi nuclear-norm quantity는 `diamond_distance_proxy`로 명확히 구분했다.
- MLE 필요성을 보여 주기 위해 non-physical linear-inversion example을 notebook에 추가했다.
- CVXPY MLE loop에서 SCS-specific option을 SCS solver에만 전달하도록 수정했다.
- Qiskit-family dependency를 validated environment version으로 pin했다.
- `apply_choi_channel(choi, rho, d_in=None, d_out=None)` shared API signature를 추가했다.
- Unclipped process fidelity diagnostic인 `raw_process_fidelity`를 추가했다.
- IBM hardware submission/retrieval이 offline notebook execution과 분리되어 있음을 README에 명확히 썼다.
- Diamond norm/proxy terminology를 정리했다.

## 검증

- Pytest: 5 passed.
- `main.ipynb` nbconvert execution 성공.
