"""Fidelities, distances, and channel-discrimination metrics."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass

import numpy as np
from numpy.typing import NDArray

from .utils import as_complex_matrix, hermitian_part, infer_choi_dims


Array = NDArray[np.complex128]


@dataclass(frozen=True)
class DiamondNormResult:
    """Container for a solved diamond-norm SDP."""

    value: float
    rho: Array
    witness: Array
    solver: str
    status: str


def raw_process_fidelity(choi_actual: np.ndarray, choi_ideal: np.ndarray) -> float:
    """Return unclipped process fidelity for unnormalized Choi matrices."""
    actual = as_complex_matrix(choi_actual, "choi_actual", square=True)
    ideal = as_complex_matrix(choi_ideal, "choi_ideal", square=True)
    if actual.shape != ideal.shape:
        raise ValueError("choi_actual and choi_ideal must have the same shape.")
    d = int(round(np.sqrt(actual.shape[0])))
    return float(np.trace(ideal @ actual).real / (d**2))


def process_fidelity(
    choi_actual: np.ndarray,
    choi_ideal: np.ndarray,
    clip: bool = True,
) -> float:
    """Return process fidelity, optionally clipped into ``[0, 1]``."""
    value = raw_process_fidelity(choi_actual, choi_ideal)
    return float(np.clip(value, 0.0, 1.0)) if clip else float(value)


def average_gate_fidelity(choi_actual: np.ndarray, choi_ideal: np.ndarray, d: int) -> float:
    """Return average gate fidelity from process fidelity."""
    f_pro = process_fidelity(choi_actual, choi_ideal)
    return float(np.clip((d * f_pro + 1.0) / (d + 1.0), 0.0, 1.0))


def trace_distance(rho: np.ndarray, sigma: np.ndarray) -> float:
    """Return the quantum trace distance ``0.5 * ||rho - sigma||_1``."""
    diff = np.asarray(rho, dtype=np.complex128) - np.asarray(sigma, dtype=np.complex128)
    singular_values = np.linalg.svd(diff, compute_uv=False)
    return float(0.5 * np.sum(singular_values))


def _installed_cvxpy_solver(preferred: str | None = None) -> str:
    import cvxpy as cp

    installed = set(cp.installed_solvers())
    if preferred is not None:
        if preferred not in installed:
            raise ValueError(f"Requested solver {preferred!r} is not installed.")
        return preferred
    for candidate in ("MOSEK", "CLARABEL", "SCS"):
        if candidate in installed:
            return candidate
    raise RuntimeError("No suitable CVXPY conic solver is installed.")


def solve_diamond_norm_sdp(
    choi_diff: np.ndarray,
    d_in: int,
    d_out: int,
    solver: str | None = None,
    eps: float = 1e-6,
    max_iters: int = 50_000,
) -> DiamondNormResult:
    """Solve Watrous's SDP for the diamond norm of a channel difference."""
    try:
        import cvxpy as cp
    except ImportError as exc:
        raise RuntimeError("cvxpy is required for diamond-norm SDP.") from exc

    j_phi = hermitian_part(as_complex_matrix(choi_diff, "choi_diff", square=True))
    dim = d_in * d_out
    if j_phi.shape != (dim, dim):
        raise ValueError(f"expected Choi shape {(dim, dim)}, got {j_phi.shape}.")

    solver_name = _installed_cvxpy_solver(solver)
    rho = cp.Variable((d_in, d_in), hermitian=True, name="rho")
    witness = cp.Variable((dim, dim), hermitian=True, name="W")
    rho_tensor_identity = cp.kron(rho, np.eye(d_out, dtype=np.complex128))
    constraints = [
        rho >> 0,
        cp.trace(rho) == 1,
        rho_tensor_identity - witness >> 0,
        rho_tensor_identity + witness >> 0,
    ]
    problem = cp.Problem(cp.Maximize(cp.real(cp.trace(j_phi @ witness))), constraints)

    kwargs: dict[str, object] = {}
    if solver_name == "SCS":
        kwargs.update({"eps": eps, "max_iters": max_iters, "verbose": False})
    problem.solve(solver=solver_name, **kwargs)

    if problem.status not in (cp.OPTIMAL, cp.OPTIMAL_INACCURATE):
        raise RuntimeError(f"Diamond-norm SDP failed with status {problem.status!r}.")

    return DiamondNormResult(
        value=float(np.real(problem.value)),
        rho=hermitian_part(np.asarray(rho.value, dtype=np.complex128)),
        witness=hermitian_part(np.asarray(witness.value, dtype=np.complex128)),
        solver=solver_name,
        status=str(problem.status),
    )


def diamond_norm_sdp(
    choi_diff: np.ndarray,
    d_in: int,
    d_out: int,
    solver: str | None = None,
    eps: float = 1e-6,
    max_iters: int = 50_000,
) -> float:
    """Return the diamond norm of a Hermiticity-preserving map by SDP."""
    value = solve_diamond_norm_sdp(choi_diff, d_in, d_out, solver=solver, eps=eps, max_iters=max_iters).value
    return float(max(value, 0.0))


def diamond_norm_distance(
    choi_actual: np.ndarray,
    choi_ideal: np.ndarray,
    d_in: int | None = None,
    d_out: int | None = None,
) -> float:
    """Return ``0.5 * ||E_actual - E_ideal||_diamond`` from Choi matrices."""
    actual = as_complex_matrix(choi_actual, "choi_actual", square=True)
    ideal = as_complex_matrix(choi_ideal, "choi_ideal", square=True)
    if actual.shape != ideal.shape:
        raise ValueError("choi_actual and choi_ideal must have the same shape.")
    if d_in is None or d_out is None:
        if d_in is not None or d_out is not None:
            raise ValueError("provide both d_in and d_out, or neither.")
        d_in, d_out = infer_choi_dims(actual)
    return 0.5 * diamond_norm_sdp(actual - ideal, d_in=d_in, d_out=d_out)


def diamond_distance_proxy(
    choi_actual: np.ndarray,
    choi_ideal: np.ndarray,
    d: int | None = None,
) -> float:
    """Return a Choi nuclear-norm proxy for half-diamond distance."""
    actual = as_complex_matrix(choi_actual, "choi_actual", square=True)
    ideal = as_complex_matrix(choi_ideal, "choi_ideal", square=True)
    if actual.shape != ideal.shape:
        raise ValueError("choi_actual and choi_ideal must have the same shape.")
    if d is None:
        d = int(round(np.sqrt(actual.shape[0])))
    return 0.5 * float(np.linalg.norm(actual - ideal, ord="nuc") / d)


def analytical_pauli_diamond_norm(
    probabilities_0: Mapping[str, float],
    probabilities_1: Mapping[str, float],
) -> float:
    """Return the exact diamond norm for a difference of one-qubit Pauli channels."""
    labels = ("I", "X", "Y", "Z")
    return float(sum(abs(probabilities_0.get(label, 0.0) - probabilities_1.get(label, 0.0)) for label in labels))


def analytical_depolarizing_diamond_norm(p0: float, p1: float, d: int = 2) -> float:
    """Return the exact diamond norm for replacement-probability depolarizing channels."""
    if d < 2:
        raise ValueError("d must be at least 2.")
    return float(2.0 * (1.0 - 1.0 / (d * d)) * abs(p0 - p1))


def discrimination_probability(
    choi_0: np.ndarray,
    choi_1: np.ndarray,
    d_in: int | None = None,
    d_out: int | None = None,
) -> float:
    """Return the optimal equal-prior two-channel discrimination probability."""
    arr_0 = as_complex_matrix(choi_0, "choi_0", square=True)
    arr_1 = as_complex_matrix(choi_1, "choi_1", square=True)
    if d_in is None or d_out is None:
        d_in, d_out = infer_choi_dims(arr_0)
    norm = diamond_norm_sdp(arr_0 - arr_1, d_in, d_out)
    return float(np.clip(0.5 + 0.25 * norm, 0.5, 1.0))
