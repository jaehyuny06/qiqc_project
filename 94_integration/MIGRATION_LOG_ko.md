# Migration Log 한국어판

## 요약

Step 4.2 migration이 완료되었다. Root-level `choi_common/` shared library를 만들고, producer module들이 중복 구현 대신 이 library를 사용하도록 refactor했다. Requirements에는 editable local installation(`-e ..`)을 추가했고, 다섯 producer notebook 모두 `jupyter nbconvert --execute`로 end-to-end 실행을 확인했다.

## 새 파일

- `choi_common/__init__.py`: public shared API 노출.
- `choi_common/README.md`: convention, module layout, installation, depolarizing convention 설명.
- `choi_common/utils.py`: matrix validation, Hermitian projection, probability validation, dimension inference.
- `choi_common/representations.py`: Kraus/Choi/Stinespring/Natural conversion, Choi/Kraus application, composition.
- `choi_common/channels.py`: standard channel constructor와 Choi convenience constructor.
- `choi_common/validation.py`: partial trace, CP/TP check, unital check, Choi rank, TP residual.
- `choi_common/metrics.py`: process fidelity, average gate fidelity, trace distance, diamond norm SDP, discrimination probability.
- `choi_common/visualization.py`: Choi heatmap, Bloch affine map, Pauli transfer matrix, Bloch deformation, eigenspectrum.
- `choi_common/tests/test_smoke.py`: shared library smoke tests.
- `pyproject.toml`: editable install packaging.

## Producer별 변경 요약

- `01_theory`: duplicated representation implementation을 제거하고 `choi_common` import로 대체. `random_channel`은 Agent-1 local helper로 유지.
- `02_ibm_experiment`: shared channel/metric/validation/visualization helper를 `choi_common`으로 이동. Tomography-specific wrapper와 MLE/linear inversion/diagnosis는 local에 유지.
- `03_sdp_discrimination`: duplicated shared SDP primitive와 channel helper를 제거하고 shared API를 사용. Optimal input, POVM, n-shot workflow는 local에 유지.
- `04_quantum_combs`: Choi/Kraus conversion, application, generic partial trace, trace distance를 shared API로 대체. Comb construction과 BLP/RHP witness는 local에 유지.
- `05_interactive_widget`: widget-specific UI는 유지하고 channel/validation/application helper를 `choi_common`으로 대체. Depolarizing slider semantics는 `convention="pauli_error"`로 보존.

## 검증

Pytest:

```text
48 passed
```

Notebook execution:

- `01_theory/main.ipynb`: success
- `02_ibm_experiment/main.ipynb`: success
- `03_sdp_discrimination/main.ipynb`: success
- `04_quantum_combs/main.ipynb`: success
- `05_interactive_widget/main.ipynb`: success

Windows/Tornado ZMQ runtime warning은 모든 실행에서 non-fatal로 나타났지만, notebook execution은 모두 성공했다.

## Semantic Preservation

- Choi convention은 unnormalized, input-first로 유지된다.
- `is_tp`는 `Tr_B(C_E) = I_A`를 사용한다.
- Agent-2/Agent-5의 depolarizing example은 `pauli_error` convention을 사용해 기존 의미를 보존한다.
- Agent-1/Agent-3의 기본 depolarizing behavior는 replacement probability이다.
- Choi nuclear-norm heuristic은 diamond norm이 아니라 `diamond_distance_proxy`로 표시된다.
