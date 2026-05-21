# Agent-3 Revision Log 한국어판

수정 날짜: 2026-05-22

## 완료된 작업

- `kraus_to_choi`와 `apply_choi_channel(choi, rho, d_in=None, d_out=None)`를 unified API에 맞추었다.
- `optimal_input_state`가 full reference-system input이 아니라 system `A`의 marginal임을 notebook에 명확히 썼다.
- Solver preference(MOSEK, CLARABEL, SCS)와 solver-dependent numerical variation을 README에 설명했다.
- Notebook SDP output에 solver name과 status를 출력하도록 수정했다.
- CVXPY/solver dependency를 validated environment version으로 pin했다.
- `C_E`, `C_Phi` notation과 glossary terminology를 정리했다.

## 생략된 작업

- 새 slow SDP test를 추가하지 않았으므로 slow marker 작업은 생략했다.

## 검증

- Pytest: 7 passed.
- `main.ipynb` nbconvert execution 성공.
