# Code Quality and Reproducibility Review

Validator-B ran each notebook and test suite in the existing `qiskit_2025_1` environment. Execution logs are saved under `execution_logs/`. Producer files were not modified.

## Execution Results

| Agent | Notebook runs? | Tests pass? | Warnings | Errors |
|-------|----------------|-------------|----------|--------|
| Agent-1 | Yes | Yes, 16 passed | 1 Windows ZMQ runtime warning | 0 |
| Agent-2 | Yes | Yes, 3 passed | 1 Windows ZMQ warning, 1 notebook missing-id warning | 0 |
| Agent-3 | Yes | Yes, 6 passed | 1 Windows ZMQ runtime warning | 0 |
| Agent-4 | Yes | Yes, 6 passed | 1 Windows ZMQ runtime warning | 0 |
| Agent-5 | Yes | Yes, 5 passed | 1 Windows ZMQ runtime warning | 0 |

The full combined test suite also passed earlier as `36 passed`. The ZMQ warnings are environment-specific on Windows and did not affect execution.

## Per-Agent Findings

### Agent-1

#### Blockers (notebook fails or wrong results)
- None.

#### Quality issues
- `01_theory/requirements.txt:1`-`6` uses lower bounds rather than pinned versions. This is reproducible enough for course development, but not for archival reruns.
- Public functions are typed and documented. Test functions intentionally lack docstrings, which is normal for pytest and not a producer-code issue.

#### Suggestions
- Add a small `pyproject.toml` or formatting note if the final integrated project will enforce style.
- Consider adding a public dimension-aware inverse helper for non-square or non-TP Choi matrices.

### Agent-2

#### Blockers (notebook fails or wrong results)
- None. The offline QPT path runs without IBM credentials.

#### Quality issues
- `02_ibm_experiment/qpt_tools.py:586` exposes a `diamond_distance_proxy`, not the SDP requested by the spec. This is primarily a math deliverable gap, but it also affects API expectations.
- `02_ibm_experiment/qpt_tools.py:394` passes SCS-specific options inside a loop that also tries CLARABEL. If SCS is unavailable and CLARABEL is used, those keyword arguments can be solver-incompatible. In the current environment SCS is installed, so execution passes.
- `02_ibm_experiment/requirements.txt:1`-`11` is broad and unpinned. Qiskit packages can change APIs quickly, so this folder is the highest risk for future reproducibility drift.

#### Suggestions
- Pin or at least cap Qiskit-family versions known to work with this notebook.
- Save IBM hardware job submission and retrieval examples as separate scripts so notebook execution stays offline by default.

### Agent-3

#### Blockers (notebook fails or wrong results)
- None.

#### Quality issues
- `03_sdp_discrimination/sdp_tools.py:301` prefers MOSEK, then CLARABEL, then SCS. This is good, but the README should mention that numerical values can vary slightly by solver.
- `03_sdp_discrimination/requirements.txt:1`-`8` is not pinned. CVXPY solver behavior can shift across releases.

#### Suggestions
- Add a test marker for "slow SDP" if more examples are added later.
- Log the solver name in notebook output wherever SDP values are shown.

### Agent-4

#### Blockers (notebook fails or wrong results)
- None.

#### Quality issues
- `04_quantum_combs/combs_tools.py:191` implements a general embedding by explicit dense loops. It is fine for two-qubit demonstrations but will scale poorly.
- `04_quantum_combs/combs_tools.py:393` names `comb_partial_trace_check` as if it validates comb causality, but it checks only a necessary global trace condition.
- `04_quantum_combs/requirements.txt:1`-`6` is unpinned.

#### Suggestions
- Rename or document `comb_partial_trace_check` as `global_tp_trace_check` unless the full hierarchy is added.
- Keep future comb demos to small dimensions or add warnings before dense construction.

### Agent-5

#### Blockers (notebook fails or wrong results)
- None.

#### Quality issues
- `05_interactive_widget/widget_core.py:321` re-renders the full Matplotlib dashboard on every slider update. It is responsive for the current qubit-only widget, but would become sluggish if larger channels are added.
- `05_interactive_widget/requirements.txt:1`-`6` is unpinned.

#### Suggestions
- Debounce slider changes or split heavy plots from scalar indicators if widget responsiveness becomes an issue.
- Add a short note that the widget is intentionally qubit-only.

## Cross-Cutting Observations

- All notebooks set `np.random.seed(42)` and define a palette near the top.
- All notebooks execute top-to-bottom in the current environment.
- All test suites pass.
- Requirements files consistently use lower bounds rather than exact pins. This is the largest reproducibility weakness across the project.
- Notebook warnings are non-fatal, but Agent-2 should normalize notebook cell IDs to avoid future `nbformat` hard errors.
