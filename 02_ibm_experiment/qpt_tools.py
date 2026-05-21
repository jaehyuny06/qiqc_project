"""Utilities for IBM/Aer quantum process tomography experiments.

The module is intentionally self-contained for Agent-2.  It uses the Choi
convention from the project spec,

    C_E = sum_ij |i><j|_A tensor E(|i><j|)_B,

so the input system ``A`` is the first tensor factor and TP means
Tr_B(C_E) = I_A.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any
import json

import matplotlib.pyplot as plt
import numpy as np


ArrayLike = np.ndarray | list[list[complex]] | list[list[float]]


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
        Raw experiment data.  For Qiskit Experiments this is usually the list
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
        return np.asarray(value["real"], dtype=float) + 1j * np.asarray(
            value["imag"], dtype=float
        )
    return np.asarray(value, dtype=complex)


def matrix_to_json_dict(matrix: np.ndarray) -> dict[str, list[list[float]]]:
    """Return a JSON-safe real/imaginary representation of a complex matrix.

    Parameters
    ----------
    matrix:
        Matrix to serialize.

    Returns
    -------
    dict
        ``{"real": ..., "imag": ...}`` with nested Python lists.
    """

    arr = np.asarray(matrix, dtype=complex)
    return {"real": arr.real.tolist(), "imag": arr.imag.tolist()}


def save_json(data: dict[str, Any], path: str | Path) -> None:
    """Save JSON data, creating the parent directory if necessary."""

    out_path = Path(path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", encoding="utf-8") as handle:
        json.dump(data, handle, indent=2)


def identity(n: int) -> np.ndarray:
    """Return an ``n x n`` complex identity matrix."""

    return np.eye(n, dtype=complex)


def dagger(matrix: np.ndarray) -> np.ndarray:
    """Return the conjugate transpose of ``matrix``."""

    return np.asarray(matrix, dtype=complex).conj().T


def kraus_to_choi(kraus_ops: list[np.ndarray]) -> np.ndarray:
    """Construct a Choi matrix from Kraus operators.

    Parameters
    ----------
    kraus_ops:
        Operators of shape ``(d_out, d_in)``.

    Returns
    -------
    np.ndarray
        Choi matrix with shape ``(d_in*d_out, d_in*d_out)``.
    """

    if not kraus_ops:
        raise ValueError("kraus_ops must contain at least one operator")
    first = np.asarray(kraus_ops[0], dtype=complex)
    d_out, d_in = first.shape
    choi = np.zeros((d_in * d_out, d_in * d_out), dtype=complex)
    for op in kraus_ops:
        k = np.asarray(op, dtype=complex)
        if k.shape != (d_out, d_in):
            raise ValueError("all Kraus operators must have the same shape")
        for i in range(d_in):
            for j in range(d_in):
                block = k[:, [i]] @ dagger(k[:, [j]])
                choi[
                    i * d_out : (i + 1) * d_out,
                    j * d_out : (j + 1) * d_out,
                ] += block
    return hermitize(choi)


def choi_from_unitary(unitary: np.ndarray) -> np.ndarray:
    """Return the Choi matrix of the unitary channel ``rho -> U rho U^dagger``."""

    u = np.asarray(unitary, dtype=complex)
    if u.ndim != 2 or u.shape[0] != u.shape[1]:
        raise ValueError("unitary must be a square matrix")
    return kraus_to_choi([u])


def apply_channel_to_state(rho: np.ndarray, choi: np.ndarray, d_out: int | None = None) -> np.ndarray:
    """Apply a channel represented by its Choi matrix to ``rho``.

    Parameters
    ----------
    rho:
        Input density matrix of shape ``(d_in, d_in)``.
    choi:
        Choi matrix in the project convention.
    d_out:
        Optional output dimension.  If omitted, it is inferred.

    Returns
    -------
    np.ndarray
        Output density matrix.
    """

    state = np.asarray(rho, dtype=complex)
    d_in = state.shape[0]
    if state.shape != (d_in, d_in):
        raise ValueError("rho must be square")
    if d_out is None:
        d_out = int(round(np.asarray(choi).shape[0] / d_in))
    c = np.asarray(choi, dtype=complex).reshape(d_in, d_out, d_in, d_out)
    out = np.einsum("ij,iajb->ab", state, c)
    return hermitize(out)


def apply_choi_channel(
    choi: np.ndarray,
    rho: np.ndarray,
    d_in: int | None = None,
    d_out: int | None = None,
) -> np.ndarray:
    """Apply a Choi-represented channel using the project-standard API.

    Parameters
    ----------
    choi:
        Choi matrix ``C_E`` in input-first order ``A tensor B``.
    rho:
        Input operator on the input system.
    d_in, d_out:
        Optional input and output dimensions. If omitted, ``d_in`` is inferred
        from ``rho`` and ``d_out`` from the Choi matrix.

    Returns
    -------
    np.ndarray
        Output matrix ``E(rho)``.
    """

    state = np.asarray(rho, dtype=complex)
    if d_in is None:
        d_in = state.shape[0]
    if state.shape != (d_in, d_in):
        raise ValueError(f"rho must have shape {(d_in, d_in)}")
    if d_out is None:
        d_out = int(round(np.asarray(choi).shape[0] / d_in))
    expected = (d_in * d_out, d_in * d_out)
    if np.asarray(choi).shape != expected:
        raise ValueError(f"choi must have shape {expected}")
    return apply_channel_to_state(state, choi, d_out=d_out)


def compose_choi(choi_after: np.ndarray, choi_before: np.ndarray, d_mid: int | None = None) -> np.ndarray:
    """Compose two channels in Choi form as ``after o before``.

    Parameters
    ----------
    choi_after:
        Choi matrix of the second channel.
    choi_before:
        Choi matrix of the first channel.
    d_mid:
        Shared intermediate dimension.  If omitted, square dimensions are
        inferred.

    Returns
    -------
    np.ndarray
        Choi matrix of the composed channel.
    """

    n_before = np.asarray(choi_before).shape[0]
    n_after = np.asarray(choi_after).shape[0]
    if d_mid is None:
        d_mid = int(round(np.sqrt(n_after)))
    d_in = int(round(n_before / d_mid))
    d_out = int(round(n_after / d_mid))
    blocks: list[list[np.ndarray]] = []
    for i in range(d_in):
        row: list[np.ndarray] = []
        for j in range(d_in):
            block = choi_before[
                i * d_mid : (i + 1) * d_mid,
                j * d_mid : (j + 1) * d_mid,
            ]
            row.append(apply_channel_to_state(block, choi_after, d_out=d_out))
        blocks.append(row)
    return hermitize(np.block(blocks))


def partial_trace_output(choi: np.ndarray, d_in: int, d_out: int) -> np.ndarray:
    """Trace out the output subsystem of a Choi matrix."""

    c = np.asarray(choi, dtype=complex).reshape(d_in, d_out, d_in, d_out)
    return np.einsum("iaja->ij", c)


def hermitize(matrix: np.ndarray) -> np.ndarray:
    """Return the Hermitian part of ``matrix``."""

    arr = np.asarray(matrix, dtype=complex)
    return 0.5 * (arr + dagger(arr))


def is_cp(choi: np.ndarray, tol: float = 1e-9) -> bool:
    """Return whether a Choi matrix is positive semidefinite."""

    eigvals = np.linalg.eigvalsh(hermitize(choi))
    return bool(np.min(eigvals) >= -tol)


def is_tp(choi: np.ndarray, d_in: int, d_out: int | None = None, tol: float = 1e-9) -> bool:
    """Return whether a Choi matrix is trace-preserving."""

    if d_out is None:
        d_out = int(round(np.asarray(choi).shape[0] / d_in))
    ptr = partial_trace_output(choi, d_in, d_out)
    return bool(np.allclose(ptr, np.eye(d_in), atol=tol))


def run_process_tomography(circuit: Any, backend: Any, shots: int = 4096) -> ProcessTomographyResult:
    """Run Qiskit Experiments process tomography on a backend.

    This function is intentionally thin: it submits and analyzes the experiment
    when ``qiskit-experiments`` is installed.  It can target IBM hardware, an
    Aer simulator, or a fake backend.  Hardware job IDs should be stored from
    ``result.metadata`` so retrieval can happen later without re-submission.

    Parameters
    ----------
    circuit:
        Qiskit circuit implementing the process to characterize.
    backend:
        Qiskit backend or simulator.
    shots:
        Number of shots per tomography circuit.

    Returns
    -------
    ProcessTomographyResult
        Portable result wrapper.
    """

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
    """Reconstruct a Choi matrix by linear inversion.

    The offline path accepts either an explicit ``"choi"`` entry or one-qubit
    output states for the input labels ``"0"``, ``"1"``, ``"+"``, and ``"+i"``.
    The latter implements the standard informationally complete one-qubit QPT
    inversion.

    Parameters
    ----------
    measurement_data:
        Tomography data dictionary.

    Returns
    -------
    np.ndarray
        Linear-inversion Choi matrix.
    """

    if "choi" in measurement_data:
        return hermitize(_as_complex_array(measurement_data["choi"]))

    output_states = measurement_data.get("output_states")
    if output_states is None:
        raise ValueError(
            "measurement_data must contain either 'choi' or one-qubit 'output_states'"
        )

    rho0 = _as_complex_array(output_states["0"])
    rho1 = _as_complex_array(output_states["1"])
    rhop = _as_complex_array(output_states["+"])
    rhoi = _as_complex_array(output_states["+i"])
    a = 2.0 * rhop - rho0 - rho1
    b = 2.0 * rhoi - rho0 - rho1
    e01 = 0.5 * (a + 1j * b)
    e10 = dagger(e01)
    choi = np.block([[rho0, e01], [e10, rho1]])
    return hermitize(choi)


def mle_choi(measurement_data: dict[str, Any], d_in: int, d_out: int) -> np.ndarray:
    """Project linear-inversion data onto the CPTP Choi set.

    This is the maximum-likelihood estimator for a Gaussian least-squares
    tomography model: minimize the Frobenius distance to the linear inversion
    subject to ``C >= 0`` and ``Tr_B(C) = I_A``.  CVXPY is used when
    available; otherwise a deterministic alternating projection fallback is
    used for offline reproducibility.

    Parameters
    ----------
    measurement_data:
        Tomography data accepted by :func:`linear_inversion_choi`.
    d_in:
        Input dimension.
    d_out:
        Output dimension.

    Returns
    -------
    np.ndarray
        CPTP Choi matrix up to numerical solver tolerance.
    """

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

    objective = cp.Minimize(cp.sum_squares(cp.abs(c_var - target)))
    problem = cp.Problem(objective, constraints)
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
        if c_var.value is not None and problem.status in {
            cp.OPTIMAL,
            cp.OPTIMAL_INACCURATE,
        }:
            return hermitize(np.asarray(c_var.value, dtype=complex))

    return project_to_cptp(target, d_in=d_in, d_out=d_out)


def project_to_cptp(
    choi: np.ndarray,
    d_in: int,
    d_out: int,
    max_iter: int = 500,
    tol: float = 1e-10,
) -> np.ndarray:
    """Alternating projection onto PSD and TP constraints.

    Parameters
    ----------
    choi:
        Initial Choi estimate.
    d_in:
        Input dimension.
    d_out:
        Output dimension.
    max_iter:
        Maximum number of iterations.
    tol:
        Stopping tolerance for TP residual and negative eigenvalues.

    Returns
    -------
    np.ndarray
        Numerically CPTP Choi estimate.
    """

    current = hermitize(choi)
    ident_out = np.eye(d_out, dtype=complex)
    for _ in range(max_iter):
        correction = np.kron(
            np.eye(d_in, dtype=complex) - partial_trace_output(current, d_in, d_out),
            ident_out / d_out,
        )
        current = hermitize(current + correction)
        eigvals, eigvecs = np.linalg.eigh(current)
        current = hermitize((eigvecs * np.maximum(eigvals, 0.0)) @ dagger(eigvecs))
        min_eig = float(np.min(np.linalg.eigvalsh(current)))
        tp_error = float(
            np.linalg.norm(partial_trace_output(current, d_in, d_out) - np.eye(d_in))
        )
        if tp_error < tol and min_eig > -tol:
            break
    correction = np.kron(
        np.eye(d_in, dtype=complex) - partial_trace_output(current, d_in, d_out),
        ident_out / d_out,
    )
    return hermitize(current + correction)


def raw_process_fidelity(choi_actual: np.ndarray, choi_ideal: np.ndarray) -> float:
    """Compute unclipped ``Tr(C_ideal C_actual) / d^2``."""
    actual = np.asarray(choi_actual, dtype=complex)
    ideal = np.asarray(choi_ideal, dtype=complex)
    if actual.shape != ideal.shape:
        raise ValueError("choi_actual and choi_ideal must have the same shape")
    d = int(round(np.sqrt(actual.shape[0])))
    return float(np.trace(ideal @ actual).real / (d**2))


def process_fidelity(choi_actual: np.ndarray, choi_ideal: np.ndarray) -> float:
    """Compute clipped process fidelity ``Tr(C_ideal C_actual) / d^2``."""

    return float(np.clip(raw_process_fidelity(choi_actual, choi_ideal), 0.0, 1.0))


def average_gate_fidelity(choi_actual: np.ndarray, choi_ideal: np.ndarray, d: int) -> float:
    """Compute average gate fidelity from process fidelity.

    Parameters
    ----------
    choi_actual:
        Actual Choi matrix.
    choi_ideal:
        Ideal Choi matrix.
    d:
        Hilbert-space dimension.

    Returns
    -------
    float
        ``(d * F_pro + 1) / (d + 1)``.
    """

    f_pro = process_fidelity(choi_actual, choi_ideal)
    return float(np.clip((d * f_pro + 1.0) / (d + 1.0), 0.0, 1.0))


def choi_to_kraus(choi: np.ndarray, tol: float = 1e-10) -> list[np.ndarray]:
    """Extract Kraus operators from a Choi matrix eigendecomposition."""

    c = hermitize(choi)
    d_in = int(round(np.sqrt(c.shape[0])))
    d_out = c.shape[0] // d_in
    eigvals, eigvecs = np.linalg.eigh(c)
    order = np.argsort(eigvals)[::-1]
    kraus_ops: list[np.ndarray] = []
    for idx in order:
        eigval = float(eigvals[idx])
        if eigval <= tol:
            continue
        vec = eigvecs[:, idx]
        kraus_ops.append(np.sqrt(eigval) * vec.reshape(d_in, d_out).T)
    return kraus_ops


def choi_to_pauli_transfer(choi: np.ndarray) -> np.ndarray:
    """Return the one-qubit Pauli transfer matrix of a Choi matrix."""

    c = np.asarray(choi, dtype=complex)
    if c.shape != (4, 4):
        raise ValueError("Pauli transfer helper is implemented for one qubit")
    paulis = [
        np.array([[1, 0], [0, 1]], dtype=complex),
        np.array([[0, 1], [1, 0]], dtype=complex),
        np.array([[0, -1j], [1j, 0]], dtype=complex),
        np.array([[1, 0], [0, -1]], dtype=complex),
    ]
    r = np.zeros((4, 4), dtype=float)
    for i, p_i in enumerate(paulis):
        for j, p_j in enumerate(paulis):
            r[i, j] = 0.5 * np.trace(p_i @ apply_channel_to_state(p_j, c)).real
    return r


def diamond_norm_sdp(
    choi_diff: np.ndarray,
    d_in: int,
    d_out: int,
    solver: str | None = None,
    eps: float = 1e-6,
    max_iters: int = 50_000,
) -> float:
    """Compute the diamond norm of a channel difference by SDP.

    The SDP is the Watrous primal form for a Hermiticity-preserving map
    ``Phi`` with Choi matrix ``C_Phi`` in the project convention:
    maximize ``<C_Phi, W>`` subject to ``-rho tensor I <= W <= rho tensor I``,
    ``rho >= 0``, and ``Tr(rho) = 1``.
    """

    try:
        import cvxpy as cp
    except ImportError as exc:
        raise RuntimeError("cvxpy is required for diamond_norm_sdp") from exc

    c_phi = hermitize(choi_diff)
    dim = d_in * d_out
    if c_phi.shape != (dim, dim):
        raise ValueError(f"expected Choi shape {(dim, dim)}, got {c_phi.shape}")

    installed = set(cp.installed_solvers())
    if solver is None:
        for candidate in ("MOSEK", "CLARABEL", "SCS"):
            if candidate in installed:
                solver = candidate
                break
    elif solver not in installed:
        raise ValueError(f"requested solver {solver!r} is not installed")
    if solver is None:
        raise RuntimeError("no suitable CVXPY conic solver is installed")

    rho = cp.Variable((d_in, d_in), hermitian=True)
    witness = cp.Variable((dim, dim), hermitian=True)
    rho_tensor_identity = cp.kron(rho, np.eye(d_out, dtype=complex))
    constraints = [
        rho >> 0,
        cp.trace(rho) == 1,
        rho_tensor_identity - witness >> 0,
        rho_tensor_identity + witness >> 0,
    ]
    problem = cp.Problem(cp.Maximize(cp.real(cp.trace(c_phi @ witness))), constraints)

    kwargs: dict[str, Any] = {}
    if solver == "SCS":
        kwargs.update({"eps": eps, "max_iters": max_iters, "verbose": False})
    problem.solve(solver=solver, **kwargs)
    if problem.status not in {cp.OPTIMAL, cp.OPTIMAL_INACCURATE}:
        raise RuntimeError(f"diamond-norm SDP failed with status {problem.status!r}")
    return float(max(np.real(problem.value), 0.0))


def diamond_norm_distance(
    choi_actual: np.ndarray,
    choi_ideal: np.ndarray,
    d_in: int | None = None,
    d_out: int | None = None,
) -> float:
    """Return ``0.5 * ||E_actual - E_ideal||_diamond`` from Choi matrices."""

    actual = np.asarray(choi_actual, dtype=complex)
    ideal = np.asarray(choi_ideal, dtype=complex)
    if actual.shape != ideal.shape:
        raise ValueError("choi_actual and choi_ideal must have the same shape")
    if d_in is None or d_out is None:
        if d_in is not None or d_out is not None:
            raise ValueError("provide both d_in and d_out, or neither")
        d_in = int(round(np.sqrt(actual.shape[0])))
        d_out = actual.shape[0] // d_in
    return 0.5 * diamond_norm_sdp(actual - ideal, d_in=d_in, d_out=d_out)


def diagnose_noise(choi: np.ndarray, choi_ideal: np.ndarray) -> dict[str, Any]:
    """Summarize dominant noise mechanisms from a reconstructed Choi matrix.

    Parameters
    ----------
    choi:
        Reconstructed Choi matrix.
    choi_ideal:
        Ideal target Choi matrix.

    Returns
    -------
    dict
        Fidelity, CP/TP diagnostics, Kraus weights, true half-diamond distance,
        a separately labeled Choi-norm proxy, and a heuristic label.
    """

    c = hermitize(choi)
    d = int(round(np.sqrt(c.shape[0])))
    d_out = c.shape[0] // d
    eigvals = np.linalg.eigvalsh(c)
    kraus_weights = sorted(
        [float(max(val, 0.0) / d) for val in eigvals], reverse=True
    )
    f_pro_raw = raw_process_fidelity(c, choi_ideal)
    f_pro = process_fidelity(c, choi_ideal)
    avg_f = average_gate_fidelity(c, choi_ideal, d)
    tp_residual = float(np.linalg.norm(partial_trace_output(c, d, d_out) - np.eye(d)))

    label = "mixed/unknown"
    details: dict[str, float] = {}
    if c.shape == (4, 4):
        r_actual = choi_to_pauli_transfer(c)
        r_ideal = choi_to_pauli_transfer(choi_ideal)
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

    diamond_proxy = 0.5 * float(np.linalg.norm(c - choi_ideal, ord="nuc") / d)
    diamond_distance = diamond_norm_distance(c, choi_ideal, d_in=d, d_out=d_out)
    return {
        "process_fidelity": f_pro,
        "process_fidelity_raw": f_pro_raw,
        "average_gate_fidelity": avg_f,
        "is_cp": is_cp(c),
        "is_tp": is_tp(c, d, d_out),
        "min_choi_eigenvalue": float(np.min(eigvals)),
        "tp_residual_fro": tp_residual,
        "kraus_weights": kraus_weights,
        "diamond_distance": diamond_distance,
        "diamond_distance_proxy": diamond_proxy,
        "dominant_noise": label,
        "details": details,
    }


def plot_choi_heatmap(choi: np.ndarray, title: str) -> None:
    """Plot real, imaginary, and absolute Choi matrix heatmaps."""

    c = np.asarray(choi, dtype=complex)
    fig, axes = plt.subplots(1, 3, figsize=(11, 3.2), constrained_layout=True)
    panels = [(c.real, "Real", "RdBu_r"), (c.imag, "Imag", "RdBu_r"), (np.abs(c), "Abs", "viridis")]
    for ax, (matrix, subtitle, cmap) in zip(axes, panels):
        vmax = max(float(np.max(np.abs(matrix))), 1e-12)
        vmin = -vmax if subtitle != "Abs" else 0.0
        image = ax.imshow(matrix, cmap=cmap, vmin=vmin, vmax=vmax)
        ax.set_title(subtitle)
        ax.set_xlabel("column")
        ax.set_ylabel("row")
        fig.colorbar(image, ax=ax, fraction=0.046)
    fig.suptitle(title)
    plt.show()


def plot_bloch_deformation(choi: np.ndarray) -> None:
    """Plot one-qubit Bloch sphere samples after applying a channel."""

    if np.asarray(choi).shape != (4, 4):
        raise ValueError("Bloch deformation plot is only implemented for one qubit")

    theta = np.linspace(0, np.pi, 28)
    phi = np.linspace(0, 2 * np.pi, 56)
    points = []
    mapped = []
    for th in theta:
        for ph in phi:
            vec = np.array(
                [np.sin(th) * np.cos(ph), np.sin(th) * np.sin(ph), np.cos(th)]
            )
            rho = 0.5 * np.array(
                [[1 + vec[2], vec[0] - 1j * vec[1]], [vec[0] + 1j * vec[1], 1 - vec[2]]],
                dtype=complex,
            )
            out = apply_channel_to_state(rho, choi)
            mapped_vec = np.array(
                [
                    2 * out[0, 1].real,
                    -2 * out[0, 1].imag,
                    (out[0, 0] - out[1, 1]).real,
                ]
            )
            points.append(vec)
            mapped.append(mapped_vec)

    points_arr = np.asarray(points)
    mapped_arr = np.asarray(mapped)
    fig = plt.figure(figsize=(6.5, 5.2))
    ax = fig.add_subplot(111, projection="3d")
    ax.scatter(points_arr[:, 0], points_arr[:, 1], points_arr[:, 2], s=2, alpha=0.09, label="input")
    ax.scatter(mapped_arr[:, 0], mapped_arr[:, 1], mapped_arr[:, 2], s=4, alpha=0.55, label="output")
    ax.set_xlim(-1.05, 1.05)
    ax.set_ylim(-1.05, 1.05)
    ax.set_zlim(-1.05, 1.05)
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_zlabel("z")
    ax.set_title("Bloch sphere deformation")
    ax.legend(loc="upper left")
    plt.show()


def depolarizing_after_unitary(unitary: np.ndarray, p: float) -> np.ndarray:
    """Return Choi for a unitary followed by one-qubit depolarizing noise."""

    if unitary.shape != (2, 2):
        raise ValueError("depolarizing helper is implemented for one-qubit gates")
    pauli_x = np.array([[0, 1], [1, 0]], dtype=complex)
    pauli_y = np.array([[0, -1j], [1j, 0]], dtype=complex)
    pauli_z = np.array([[1, 0], [0, -1]], dtype=complex)
    kraus = [
        np.sqrt(max(1.0 - p, 0.0)) * unitary,
        np.sqrt(max(p / 3.0, 0.0)) * pauli_x @ unitary,
        np.sqrt(max(p / 3.0, 0.0)) * pauli_y @ unitary,
        np.sqrt(max(p / 3.0, 0.0)) * pauli_z @ unitary,
    ]
    return kraus_to_choi(kraus)


def amplitude_damping_after_unitary(unitary: np.ndarray, gamma: float) -> np.ndarray:
    """Return Choi for a unitary followed by amplitude damping."""

    if unitary.shape != (2, 2):
        raise ValueError("amplitude damping helper is implemented for one-qubit gates")
    k0 = np.array([[1, 0], [0, np.sqrt(max(1.0 - gamma, 0.0))]], dtype=complex)
    k1 = np.array([[0, np.sqrt(max(gamma, 0.0))], [0, 0]], dtype=complex)
    return kraus_to_choi([k0 @ unitary, k1 @ unitary])


def two_qubit_depolarizing_after_unitary(unitary: np.ndarray, p: float) -> np.ndarray:
    """Return Choi for a two-qubit unitary followed by global depolarizing noise."""

    if unitary.shape != (4, 4):
        raise ValueError("two_qubit_depolarizing_after_unitary expects a 4x4 unitary")
    one_qubit_paulis = [
        np.eye(2, dtype=complex),
        np.array([[0, 1], [1, 0]], dtype=complex),
        np.array([[0, -1j], [1j, 0]], dtype=complex),
        np.array([[1, 0], [0, -1]], dtype=complex),
    ]
    paulis = [np.kron(a, b) for a in one_qubit_paulis for b in one_qubit_paulis]
    kraus = [np.sqrt(max(1.0 - p, 0.0)) * unitary]
    kraus.extend(np.sqrt(max(p / 15.0, 0.0)) * p_op @ unitary for p_op in paulis[1:])
    return kraus_to_choi(kraus)


def simulate_output_states_from_choi(choi: np.ndarray) -> dict[str, np.ndarray]:
    """Generate exact one-qubit output states for QPT inputs."""

    zero = np.array([[1, 0], [0, 0]], dtype=complex)
    one = np.array([[0, 0], [0, 1]], dtype=complex)
    plus = 0.5 * np.array([[1, 1], [1, 1]], dtype=complex)
    plus_i = 0.5 * np.array([[1, -1j], [1j, 1]], dtype=complex)
    return {
        "0": apply_channel_to_state(zero, choi),
        "1": apply_channel_to_state(one, choi),
        "+": apply_channel_to_state(plus, choi),
        "+i": apply_channel_to_state(plus_i, choi),
    }
