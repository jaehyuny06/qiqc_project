"""Utilities for IBM/Aer quantum process tomography experiments.

Shared Choi conversions, validation, metrics, channels, and visualization now
come from :mod:`choi_common`. This module keeps Agent-2-specific tomography
wrappers, reconstruction routines, serialization helpers, and noise diagnosis.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any
import json

import numpy as np

from choi_common.channels import (
    amplitude_damping_after_unitary,
    depolarizing_after_unitary,
    two_qubit_depolarizing_after_unitary,
    unitary_channel_choi,
)
from choi_common.metrics import (
    average_gate_fidelity,
    diamond_distance_proxy,
    diamond_norm_distance,
    process_fidelity,
    raw_process_fidelity,
)
from choi_common.representations import apply_choi_channel, choi_to_kraus
from choi_common.utils import dagger, hermitian_part
from choi_common.validation import is_cp, is_tp, partial_trace_output
from choi_common.visualization import choi_to_pauli_transfer, plot_bloch_deformation, plot_choi_heatmap


ArrayLike = np.ndarray | list[list[complex]] | list[list[float]]
choi_from_unitary = unitary_channel_choi


@dataclass
class ProcessTomographyResult:
    """Portable wrapper around tomography results.

    Parameters
    ----------
    choi:
        Reconstructed Choi matrix, if the backend/analysis produced one.
    metadata:
        Backend, shot count, mode, and analysis metadata.
    raw_data:
        Raw experiment data. For Qiskit Experiments this is usually the list
        returned by ``ExperimentData.data()``.
    analysis_results:
        Optional native analysis result objects or JSON-safe summaries.
    """

    choi: np.ndarray | None
    metadata: dict[str, Any]
    raw_data: Any | None = None
    analysis_results: Any | None = None


def _as_complex_array(value: Any) -> np.ndarray:
    """Convert JSON-friendly or array-like matrix data to complex ndarray."""
    if isinstance(value, np.ndarray):
        return np.asarray(value, dtype=complex)
    if isinstance(value, dict) and "real" in value and "imag" in value:
        return np.asarray(value["real"], dtype=float) + 1j * np.asarray(value["imag"], dtype=float)
    return np.asarray(value, dtype=complex)


def matrix_to_json_dict(matrix: np.ndarray) -> dict[str, list[list[float]]]:
    """Return a JSON-safe real/imaginary representation of a complex matrix."""
    arr = np.asarray(matrix, dtype=complex)
    return {"real": arr.real.tolist(), "imag": arr.imag.tolist()}


def save_json(data: dict[str, Any], path: str | Path) -> None:
    """Save JSON data, creating the parent directory if necessary."""
    out_path = Path(path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", encoding="utf-8") as handle:
        json.dump(data, handle, indent=2)


def run_process_tomography(circuit: Any, backend: Any, shots: int = 4096) -> ProcessTomographyResult:
    """Run Qiskit Experiments process tomography on a backend."""
    try:
        from qiskit_experiments.library import ProcessTomography
    except ImportError as exc:
        raise ImportError(
            "run_process_tomography requires qiskit-experiments. "
            "Install requirements.txt or use the offline simulated examples."
        ) from exc

    experiment = ProcessTomography(circuit)
    experiment_data = experiment.run(backend=backend, shots=shots)
    experiment_data.block_for_results()

    choi: np.ndarray | None = None
    analysis_summaries: list[dict[str, Any]] = []
    for analysis_result in experiment_data.analysis_results():
        summary = {"name": analysis_result.name, "quality": analysis_result.quality}
        value = analysis_result.value
        if analysis_result.name.lower() in {"state", "choi"} and hasattr(value, "data"):
            choi = np.asarray(value.data, dtype=complex)
            summary["shape"] = list(choi.shape)
        analysis_summaries.append(summary)

    job_ids = []
    for datum in experiment_data.data():
        job_id = datum.get("job_id")
        if job_id is not None:
            job_ids.append(job_id)

    backend_name_attr = getattr(backend, "name", None)
    backend_name = backend_name_attr() if callable(backend_name_attr) else backend_name_attr
    metadata = {
        "mode": "qiskit_experiments",
        "backend": backend_name or "unknown",
        "shots": shots,
        "experiment_id": experiment_data.experiment_id,
        "job_ids": sorted(set(job_ids)),
    }
    return ProcessTomographyResult(
        choi=choi,
        metadata=metadata,
        raw_data=experiment_data.data(),
        analysis_results=analysis_summaries,
    )


def linear_inversion_choi(measurement_data: dict[str, Any]) -> np.ndarray:
    """Reconstruct a Choi matrix by linear inversion."""
    if "choi" in measurement_data:
        return hermitian_part(_as_complex_array(measurement_data["choi"]))

    output_states = measurement_data.get("output_states")
    if output_states is None:
        raise ValueError("measurement_data must contain either 'choi' or one-qubit 'output_states'")

    rho0 = _as_complex_array(output_states["0"])
    rho1 = _as_complex_array(output_states["1"])
    rhop = _as_complex_array(output_states["+"])
    rhoi = _as_complex_array(output_states["+i"])
    a = 2.0 * rhop - rho0 - rho1
    b = 2.0 * rhoi - rho0 - rho1
    e01 = 0.5 * (a + 1j * b)
    e10 = dagger(e01)
    return hermitian_part(np.block([[rho0, e01], [e10, rho1]]))


def mle_choi(measurement_data: dict[str, Any], d_in: int, d_out: int) -> np.ndarray:
    """Project linear-inversion data onto the CPTP Choi set."""
    target = linear_inversion_choi(measurement_data)
    n = d_in * d_out
    if target.shape != (n, n):
        raise ValueError(f"expected Choi shape {(n, n)}, got {target.shape}")

    try:
        import cvxpy as cp
    except ImportError:
        return project_to_cptp(target, d_in=d_in, d_out=d_out)

    c_var = cp.Variable((n, n), hermitian=True)
    constraints: list[Any] = [c_var >> 0]
    for i in range(d_in):
        for j in range(d_in):
            expr = sum(c_var[i * d_out + b, j * d_out + b] for b in range(d_out))
            constraints.append(expr == (1.0 if i == j else 0.0))

    problem = cp.Problem(cp.Minimize(cp.sum_squares(cp.abs(c_var - target))), constraints)
    for solver in ("SCS", "CLARABEL"):
        if solver not in cp.installed_solvers():
            continue
        try:
            kwargs: dict[str, Any] = {"verbose": False}
            if solver == "SCS":
                kwargs.update({"eps": 1e-7, "max_iters": 20000})
            problem.solve(solver=solver, **kwargs)
        except Exception:
            continue
        if c_var.value is not None and problem.status in {cp.OPTIMAL, cp.OPTIMAL_INACCURATE}:
            return hermitian_part(np.asarray(c_var.value, dtype=complex))
    return project_to_cptp(target, d_in=d_in, d_out=d_out)


def project_to_cptp(
    choi: np.ndarray,
    d_in: int,
    d_out: int,
    max_iter: int = 500,
    tol: float = 1e-10,
) -> np.ndarray:
    """Alternating projection onto PSD and TP constraints."""
    current = hermitian_part(choi)
    ident_out = np.eye(d_out, dtype=complex)
    for _ in range(max_iter):
        correction = np.kron(np.eye(d_in, dtype=complex) - partial_trace_output(current, d_in, d_out), ident_out / d_out)
        current = hermitian_part(current + correction)
        eigvals, eigvecs = np.linalg.eigh(current)
        current = hermitian_part((eigvecs * np.maximum(eigvals, 0.0)) @ dagger(eigvecs))
        min_eig = float(np.min(np.linalg.eigvalsh(current)))
        tp_error = float(np.linalg.norm(partial_trace_output(current, d_in, d_out) - np.eye(d_in)))
        if tp_error < tol and min_eig > -tol:
            break
    correction = np.kron(np.eye(d_in, dtype=complex) - partial_trace_output(current, d_in, d_out), ident_out / d_out)
    return hermitian_part(current + correction)


def diagnose_noise(choi: np.ndarray, choi_ideal: np.ndarray) -> dict[str, Any]:
    """Summarize dominant noise mechanisms from a reconstructed Choi matrix."""
    c = hermitian_part(choi)
    d = int(round(np.sqrt(c.shape[0])))
    d_out = c.shape[0] // d
    eigvals = np.linalg.eigvalsh(c)
    kraus_weights = sorted([float(max(val, 0.0) / d) for val in eigvals], reverse=True)
    f_pro_raw = raw_process_fidelity(c, choi_ideal)
    f_pro = process_fidelity(c, choi_ideal)
    avg_f = average_gate_fidelity(c, choi_ideal, d)
    tp_res = float(np.linalg.norm(partial_trace_output(c, d, d_out) - np.eye(d)))

    label = "mixed/unknown"
    details: dict[str, float] = {}
    if c.shape == (4, 4):
        r_actual = choi_to_pauli_transfer(c).real
        r_ideal = choi_to_pauli_transfer(choi_ideal).real
        residual = r_actual @ np.linalg.pinv(r_ideal)
        bloch = residual[1:, 1:]
        translation = residual[1:, 0]
        singular_values = np.linalg.svd(bloch, compute_uv=False)
        details = {
            "bloch_translation_norm": float(np.linalg.norm(translation)),
            "bloch_singular_value_spread": float(np.max(singular_values) - np.min(singular_values)),
            "mean_bloch_shrinkage": float(np.mean(singular_values)),
        }
        if details["bloch_translation_norm"] >= 0.05:
            label = "amplitude-damping-like relaxation"
        elif details["bloch_singular_value_spread"] < 0.06 and details["mean_bloch_shrinkage"] < 0.98:
            label = "depolarizing-like isotropic shrinkage"
        elif details["bloch_singular_value_spread"] >= 0.06:
            label = "axis-biased Pauli/dephasing noise"
        elif kraus_weights[0] > 0.98 and f_pro < 0.995:
            label = "mostly coherent unitary error"
        else:
            label = "near-ideal"
    elif kraus_weights[0] > 0.97 and f_pro < 0.995:
        label = "mostly coherent or calibration error"
    elif f_pro < 0.95:
        label = "appreciable stochastic noise"
    else:
        label = "near-ideal"

    return {
        "process_fidelity": f_pro,
        "process_fidelity_raw": f_pro_raw,
        "average_gate_fidelity": avg_f,
        "is_cp": is_cp(c),
        "is_tp": is_tp(c, d, d_out),
        "min_choi_eigenvalue": float(np.min(eigvals)),
        "tp_residual_fro": tp_res,
        "kraus_weights": kraus_weights,
        "diamond_distance": diamond_norm_distance(c, choi_ideal, d_in=d, d_out=d_out),
        "diamond_distance_proxy": diamond_distance_proxy(c, choi_ideal, d=d),
        "dominant_noise": label,
        "details": details,
    }


def simulate_output_states_from_choi(choi: np.ndarray) -> dict[str, np.ndarray]:
    """Generate exact one-qubit output states for QPT inputs."""
    zero = np.array([[1, 0], [0, 0]], dtype=complex)
    one = np.array([[0, 0], [0, 1]], dtype=complex)
    plus = 0.5 * np.array([[1, 1], [1, 1]], dtype=complex)
    plus_i = 0.5 * np.array([[1, -1j], [1j, 1]], dtype=complex)
    return {
        "0": apply_choi_channel(choi, zero, d_in=2, d_out=2),
        "1": apply_choi_channel(choi, one, d_in=2, d_out=2),
        "+": apply_choi_channel(choi, plus, d_in=2, d_out=2),
        "+i": apply_choi_channel(choi, plus_i, d_in=2, d_out=2),
    }
