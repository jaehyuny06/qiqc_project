# Agent-2: IBM Quantum Process Tomography

This folder contains a self-contained quantum process tomography (QPT) workflow for the Choi representation project.  The implementation is offline-reproducible by default and can be pointed at IBM Quantum hardware separately when credentials and queue time are available.

## Contents

- `main.ipynb` - narrative notebook covering QPT theory, offline simulated X/H/CNOT reconstructions, Choi diagnostics, and hardware submission notes.
- `qpt_tools.py` - local helper module for Choi construction, linear inversion, CVXPY-based CPTP/MLE projection, diagnostics, plotting, and optional Qiskit Experiments submission.
- `test_qpt_tools.py` - pytest coverage for the core offline numerical routines.
- `data/raw_results.json` - sample simulated result summary generated for reproducibility.
- `data/sample_simulated_results.json` - compact placeholder/sample output for quick inspection.
- `requirements.txt` - dependencies for the full notebook and optional IBM/Qiskit workflow.

## Offline Reproducible Design

The notebook does not require IBM credentials to run.  It builds ideal Choi matrices for `X`, `H`, and `CNOT`, then creates deterministic noisy stand-ins:

- `X`: unitary followed by amplitude damping.
- `H`: unitary followed by depolarizing noise.
- `CNOT`: two-qubit unitary followed by global depolarizing noise.

For one-qubit gates, the linear inversion path uses the informationally complete inputs `|0>`, `|1>`, `|+>`, and `|+i>`.  The MLE step solves the nearest CPTP Choi projection with CVXPY/SCS:

```text
minimize ||C - C_linear||_F^2
subject to C >= 0
           Tr_output(C) = I_input
```

If CVXPY is unavailable, `qpt_tools.project_to_cptp` provides a deterministic alternating-projection fallback so the examples remain inspectable offline.

## IBM Hardware Submission and Retrieval

Hardware submission is intentionally separate from the offline notebook run because IBM queues can be long.  The intended hardware flow is:

1. Install the full requirements.
2. Configure credentials outside the notebook, for example with `QiskitRuntimeService.save_account(...)` or an environment-managed account.
3. Select a backend such as `ibm_brisbane` using `qiskit-ibm-runtime`.
4. Build the target circuit and call `run_process_tomography(circuit, backend, shots=4096)`.
5. Save `result.metadata["job_ids"]` and the raw result payload to `data/raw_results.json`.
6. Retrieve queued/completed jobs later using the IBM Runtime service and the saved job IDs, then rerun analysis locally.

The notebook includes a commented code cell showing this pattern.  It is not executed by default.

## Run Instructions

From this folder:

```powershell
python -m pip install -r requirements.txt
python -m pytest -q
jupyter nbconvert --to notebook --execute main.ipynb --output executed_main.ipynb
```

The optional Qiskit/IBM dependencies are only needed for real backend submission.  The tests and default notebook path exercise the reproducible offline implementation.

## Key Results in the Sample Output

The sample data report process fidelity, average gate fidelity, CP/TP status, Kraus weights, and a heuristic noise label for three gates.  The values are simulated, not hardware claims.  They are meant to make downstream validation deterministic while preserving the same Choi-based analysis path used for hardware data.
