# Migration Log

## Summary

Step 4.2 migration completed. The root-level `choi_common/` library was created with full implementations, producer modules were refactored to use it, requirements were updated for editable local installation, and all five producer notebooks executed end-to-end with `jupyter nbconvert --execute`.

## New Files

- `choi_common/__init__.py`
  - Exposes the public shared API from channels, representations, validation, metrics, and visualization modules.
- `choi_common/README.md`
  - Documents the shared Choi convention, module layout, installation, and depolarizing convention.
- `choi_common/utils.py`
  - Adds shared matrix validation, Hermitian projection, probability validation, and dimension inference helpers.
- `choi_common/representations.py`
  - Implements Kraus/Choi/Stinespring/Natural conversions, Choi application, Kraus application, and Choi composition.
- `choi_common/channels.py`
  - Implements standard channel constructors and Choi-returning convenience constructors.
  - Adds explicit `convention` handling for depolarizing channels.
- `choi_common/validation.py`
  - Implements partial trace, CP/TP checks, unital checks, Choi rank, and TP residual.
- `choi_common/metrics.py`
  - Implements process fidelity, average gate fidelity, trace distance, diamond norm SDP, half-diamond distance, proxy distance, and discrimination probability.
- `choi_common/visualization.py`
  - Implements Choi heatmaps, Bloch affine map, Pauli transfer matrix, Bloch deformation, eigenspectrum, and display eigenoperators.
- `choi_common/tests/test_smoke.py`
  - Adds smoke tests for common conversions, channels, validation, metrics, and visualization helpers.
- `choi_common/tests/__init__.py`
  - Marks the test package.
- `pyproject.toml`
  - Adds editable-install packaging for `choi-common`.

## Modified Producer Files

### `01_theory`

- `01_theory/channel_reps.py`
  - Removed duplicated channel representation implementations.
  - Imports shared channels, conversions, and validation helpers from `choi_common`.
  - Keeps Agent-1-specific `random_channel`.
  - Keeps `apply_channel = apply_kraus_channel` as a compatibility alias.
- `01_theory/main.ipynb`
  - Updated imports to use `choi_common.channels`, `choi_common.representations`, and `choi_common.validation`.
  - Keeps `random_channel` from local `channel_reps`.
  - Updated `apply_channel(...)` calls to `apply_kraus_channel(...)`.
  - Updated composition call to `compose_choi_channels(choi_after=C2, choi_before=C1)`.
- `01_theory/test_channel_reps.py`
  - Updated tests to use the shared API directly for duplicated functions.
  - Keeps `random_channel` from local `channel_reps`.
- `01_theory/requirements.txt`
  - Added `-e ..` local editable dependency.
- `01_theory/README.md`
  - Updated composition helper reference to `choi_common.representations.compose_choi_channels`.

### `02_ibm_experiment`

- `02_ibm_experiment/qpt_tools.py`
  - Removed duplicated shared implementations.
  - Imports shared channel constructors, metrics, Choi application, validation, and visualization from `choi_common`.
  - Keeps Agent-2-specific tomography wrappers, serialization helpers, linear inversion, MLE projection, CPTP projection, diagnosis, and simulated QPT output-state generation.
  - Keeps `choi_from_unitary = unitary_channel_choi` as a compatibility alias.
- `02_ibm_experiment/main.ipynb`
  - Updated shared imports to `choi_common`.
  - Replaced `choi_from_unitary` with `unitary_channel_choi`.
  - Updated `plot_choi_heatmap` calls to use `title=...`.
  - Keeps Agent-2-specific imports from `qpt_tools`.
- `02_ibm_experiment/test_qpt_tools.py`
  - Updated duplicated-function imports to use `choi_common`.
  - Keeps Agent-2-specific tests for local reconstruction helpers.
- `02_ibm_experiment/requirements.txt`
  - Added `-e ..` local editable dependency.

### `03_sdp_discrimination`

- `03_sdp_discrimination/sdp_tools.py`
  - Removed duplicated shared channel constructors, validation helpers, Choi conversion, and diamond-norm SDP primitives.
  - Imports shared equivalents from `choi_common`.
  - Keeps Agent-3-specific optimal input state, POVM, tensor power, n-shot discrimination, and product-strategy discrimination workflows.
  - Keeps `apply_choi_to_state = apply_choi_channel` as a compatibility alias.
- `03_sdp_discrimination/main.ipynb`
  - Re-executed successfully after migration.
  - Notebook continues to use `import sdp_tools as sdp`, with shared internals delegated through `sdp_tools.py`.
- `03_sdp_discrimination/requirements.txt`
  - Added `-e ..` local editable dependency.

### `04_quantum_combs`

- `04_quantum_combs/combs_tools.py`
  - Removed duplicated Choi/Kraus conversion, Choi application, natural conversion, generic partial trace, and trace distance implementations.
  - Imports shared equivalents from `choi_common`.
  - Keeps Agent-4-specific comb construction, causality checks, Markovianity checks, and BLP/RHP measures.
- `04_quantum_combs/main.ipynb`
  - Updated shared imports to `choi_common.metrics` and `choi_common.representations`.
  - Keeps comb-specific imports from `combs_tools`.
- `04_quantum_combs/requirements.txt`
  - Added `-e ..` local editable dependency.

### `05_interactive_widget`

- `05_interactive_widget/widget_core.py`
  - Replaced local channel utility imports with `choi_common` imports.
  - Preserved Agent-5 depolarizing slider semantics by calling `depolarizing_channel(..., convention="pauli_error")`.
  - Updated TP and partial-trace calls to pass `d_in=2, d_out=2`.
  - Removed the duplicated local `apply_choi_channel` implementation and uses the shared function.
  - Keeps widget-specific UI, dashboard rendering, indicators, and formatting.
- `05_interactive_widget/channel_utils.py`
  - Converted to a compatibility layer over `choi_common`.
  - Keeps Agent-5 legacy names such as `depolarizing_kraus`, with `pauli_error` convention preserved.
- `05_interactive_widget/main.ipynb`
  - Re-executed successfully after migration.
  - Notebook continues to import widget-specific entry points from `widget_core.py`.
- `05_interactive_widget/requirements.txt`
  - Added `-e ..` local editable dependency.

## Packaging

- Ran:

```text
python -m pip install -e .
```

- Result: editable install of `choi-common==0.1.0` succeeded.
- Generated `choi_common.egg-info/` and Python cache directories were removed from the workspace afterward.

## Verification

### Pytest

Command:

```text
python -m pytest choi_common/tests 01_theory 02_ibm_experiment 03_sdp_discrimination 04_quantum_combs 05_interactive_widget -q
```

Result:

```text
48 passed
```

### Notebook Execution

Commands run:

```text
jupyter nbconvert --to notebook --execute --inplace 01_theory/main.ipynb
jupyter nbconvert --to notebook --execute --inplace 02_ibm_experiment/main.ipynb
jupyter nbconvert --to notebook --execute --inplace 03_sdp_discrimination/main.ipynb
jupyter nbconvert --to notebook --execute --inplace 04_quantum_combs/main.ipynb
jupyter nbconvert --to notebook --execute --inplace 05_interactive_widget/main.ipynb
```

Result:

- `01_theory/main.ipynb`: success
- `02_ibm_experiment/main.ipynb`: success
- `03_sdp_discrimination/main.ipynb`: success
- `04_quantum_combs/main.ipynb`: success
- `05_interactive_widget/main.ipynb`: success

All notebook executions emitted the same Windows/Tornado ZMQ runtime warning about the Proactor event loop, but execution completed successfully in every case.

## Semantic Preservation Notes

- The shared Choi convention remains unnormalized and input-first.
- `is_tp` uses `Tr_B(C_E) = I_A`.
- Agent-2 and Agent-5 depolarizing examples preserve their original Pauli-error probability semantics by using `convention="pauli_error"`.
- Agent-1 and Agent-3 depolarizing behavior continues to use replacement probability by default.
- Choi nuclear-norm heuristics remain labeled as `diamond_distance_proxy`, not as diamond norm.
