"""SDP tools for quantum channel discrimination via Choi matrices.

This module is intentionally self-contained for Agent-3.  It uses the
project convention

    C_E = sum_ij |i><j| tensor E(|i><j|)

with the input system as the first tensor factor.
"""

from __future__ import annotations

from dataclasses import dataclass
from itertools import product
from typing import Iterable

import numpy as np
from numpy.typing import NDArray


Array = NDArray[np.complex128]


@dataclass(frozen=True)
class DiamondNormResult:
    """Container for a solved diamond-norm SDP."""

    value: float
    rho: Array
    witness: Array
    solver: str
    status: str


def _as_complex_matrix(matrix: np.ndarray, name: str) -> Array:
    arr = np.asarray(matrix, dtype=np.complex128)
    if arr.ndim != 2 or arr.shape[0] != arr.shape[1]:
        raise ValueError(f"{name} must be a square matrix.")
    return arr


def _infer_equal_dims(choi: np.ndarray) -> tuple[int, int]:
    dim = _as_complex_matrix(choi, "choi").shape[0]
    d = int(round(np.sqrt(dim)))
    if d * d != dim:
        raise ValueError(
            "Could not infer equal input/output dimensions from the Choi size; "
            "pass d_in and d_out explicitly."
        )
    return d, d


def _hermitian_part(matrix: np.ndarray) -> Array:
    arr = np.asarray(matrix, dtype=np.complex128)
    return 0.5 * (arr + arr.conj().T)


def _partial_trace_output(choi: np.ndarray, d_in: int, d_out: int) -> Array:
    arr = _as_complex_matrix(choi, "choi").reshape(d_in, d_out, d_in, d_out)
    return np.einsum("ibjb->ij", arr)


def _validate_choi_dims(choi: np.ndarray, d_in: int, d_out: int) -> Array:
    arr = _as_complex_matrix(choi, "choi")
    expected = d_in * d_out
    if arr.shape != (expected, expected):
        raise ValueError(
            f"Expected Choi shape {(expected, expected)} for d_in={d_in}, "
            f"d_out={d_out}; got {arr.shape}."
        )
    return arr


def kraus_to_choi(kraus_ops: list[np.ndarray]) -> Array:
    """Convert Kraus operators to a Choi matrix.

    Parameters
    ----------
    kraus_ops
        Kraus operators with shape ``(d_out, d_in)``.

    Returns
    -------
    np.ndarray
        Choi matrix with input system first and output system second.
    """

    if not kraus_ops:
        raise ValueError("kraus_ops must contain at least one operator.")
    ops = [np.asarray(k, dtype=np.complex128) for k in kraus_ops]
    d_out, d_in = ops[0].shape
    if any(k.shape != (d_out, d_in) for k in ops):
        raise ValueError("All Kraus operators must have the same shape.")

    choi = np.zeros((d_in * d_out, d_in * d_out), dtype=np.complex128)
    for i in range(d_in):
        for j in range(d_in):
            basis_ij = np.zeros((d_in, d_in), dtype=np.complex128)
            basis_ij[i, j] = 1.0
            image = sum(k @ basis_ij @ k.conj().T for k in ops)
            choi[
                i * d_out : (i + 1) * d_out,
                j * d_out : (j + 1) * d_out,
            ] = image
    return _hermitian_part(choi)


def apply_choi_to_state(choi: np.ndarray, rho: np.ndarray, d_in: int, d_out: int) -> Array:
    """Apply a Choi-represented channel to an input state.

    Parameters
    ----------
    choi
        Choi matrix of the channel.
    rho
        Input density matrix with shape ``(d_in, d_in)``.
    d_in
        Input Hilbert-space dimension.
    d_out
        Output Hilbert-space dimension.

    Returns
    -------
    np.ndarray
        Output matrix ``E(rho)``.
    """

    arr = _validate_choi_dims(choi, d_in, d_out).reshape(d_in, d_out, d_in, d_out)
    state = _as_complex_matrix(rho, "rho")
    if state.shape != (d_in, d_in):
        raise ValueError(f"rho must have shape {(d_in, d_in)}.")
    return np.einsum("ij,iajb->ab", state, arr)


def identity_channel_choi(d: int = 2) -> Array:
    """Return the Choi matrix of the identity channel on dimension ``d``."""

    return kraus_to_choi([np.eye(d, dtype=np.complex128)])


def unitary_channel_choi(unitary: np.ndarray) -> Array:
    """Return the Choi matrix of ``rho -> U rho U^dagger``."""

    u = _as_complex_matrix(unitary, "unitary")
    if not np.allclose(u.conj().T @ u, np.eye(u.shape[0]), atol=1e-9):
        raise ValueError("unitary must be unitary.")
    return kraus_to_choi([u])


def pauli_matrices() -> dict[str, Array]:
    """Return the one-qubit Pauli matrices."""

    return {
        "I": np.array([[1, 0], [0, 1]], dtype=np.complex128),
        "X": np.array([[0, 1], [1, 0]], dtype=np.complex128),
        "Y": np.array([[0, -1j], [1j, 0]], dtype=np.complex128),
        "Z": np.array([[1, 0], [0, -1]], dtype=np.complex128),
    }


def pauli_channel_choi(probabilities: dict[str, float]) -> Array:
    """Construct a one-qubit Pauli channel Choi matrix.

    Parameters
    ----------
    probabilities
        Mapping from ``"I"``, ``"X"``, ``"Y"``, ``"Z"`` to probabilities.
        Missing entries are treated as zero.

    Returns
    -------
    np.ndarray
        Choi matrix for ``sum_P p_P P rho P``.
    """

    paulis = pauli_matrices()
    probs = {label: float(probabilities.get(label, 0.0)) for label in paulis}
    if any(p < -1e-12 for p in probs.values()):
        raise ValueError("Pauli probabilities must be nonnegative.")
    total = sum(probs.values())
    if not np.isclose(total, 1.0, atol=1e-10):
        raise ValueError(f"Pauli probabilities must sum to 1; got {total}.")
    kraus_ops = [np.sqrt(max(prob, 0.0)) * paulis[label] for label, prob in probs.items()]
    return kraus_to_choi(kraus_ops)


def bit_flip_channel_choi(p: float) -> Array:
    """Return the one-qubit bit-flip channel Choi matrix."""

    if not 0.0 <= p <= 1.0:
        raise ValueError("p must lie in [0, 1].")
    return pauli_channel_choi({"I": 1.0 - p, "X": p, "Y": 0.0, "Z": 0.0})


def phase_flip_channel_choi(p: float) -> Array:
    """Return the one-qubit phase-flip channel Choi matrix."""

    if not 0.0 <= p <= 1.0:
        raise ValueError("p must lie in [0, 1].")
    return pauli_channel_choi({"I": 1.0 - p, "X": 0.0, "Y": 0.0, "Z": p})


def depolarizing_channel_choi(p: float, d: int = 2) -> Array:
    """Return a depolarizing-channel Choi matrix.

    For qubits this uses the Pauli form
    ``E_p(rho) = (1 - p) rho + p Tr(rho) I / 2``.
    For larger ``d`` it uses the direct Choi expression.
    """

    if not 0.0 <= p <= 1.0:
        raise ValueError("p must lie in [0, 1].")
    if d == 2:
        return pauli_channel_choi(
            {"I": 1.0 - 0.75 * p, "X": 0.25 * p, "Y": 0.25 * p, "Z": 0.25 * p}
        )

    identity_choi = identity_channel_choi(d)
    completely_mixed = np.kron(np.eye(d, dtype=np.complex128), np.eye(d) / d)
    return _hermitian_part((1.0 - p) * identity_choi + p * completely_mixed)


def amplitude_damping_channel_choi(gamma: float) -> Array:
    """Return the one-qubit amplitude-damping channel Choi matrix."""

    if not 0.0 <= gamma <= 1.0:
        raise ValueError("gamma must lie in [0, 1].")
    k0 = np.array([[1.0, 0.0], [0.0, np.sqrt(1.0 - gamma)]], dtype=np.complex128)
    k1 = np.array([[0.0, np.sqrt(gamma)], [0.0, 0.0]], dtype=np.complex128)
    return kraus_to_choi([k0, k1])


def phase_damping_channel_choi(gamma: float) -> Array:
    """Return the one-qubit phase-damping channel Choi matrix."""

    if not 0.0 <= gamma <= 1.0:
        raise ValueError("gamma must lie in [0, 1].")
    k0 = np.sqrt(1.0 - gamma) * np.eye(2, dtype=np.complex128)
    k1 = np.sqrt(gamma) * np.array([[1.0, 0.0], [0.0, 0.0]], dtype=np.complex128)
    k2 = np.sqrt(gamma) * np.array([[0.0, 0.0], [0.0, 1.0]], dtype=np.complex128)
    return kraus_to_choi([k0, k1, k2])


def z_rotation_channel_choi(theta: float) -> Array:
    """Return the one-qubit coherent Z-rotation channel Choi matrix."""

    unitary = np.array(
        [[np.exp(-0.5j * theta), 0.0], [0.0, np.exp(0.5j * theta)]],
        dtype=np.complex128,
    )
    return unitary_channel_choi(unitary)


def is_cp(choi: np.ndarray, tol: float = 1e-9) -> bool:
    """Return whether a Choi matrix is positive semidefinite."""

    eigvals = np.linalg.eigvalsh(_hermitian_part(choi))
    return bool(np.min(eigvals) >= -tol)


def is_tp(choi: np.ndarray, d_in: int, d_out: int, tol: float = 1e-9) -> bool:
    """Return whether a Choi matrix represents a trace-preserving map."""

    return bool(np.allclose(_partial_trace_output(choi, d_in, d_out), np.eye(d_in), atol=tol))


def analytical_pauli_diamond_norm(
    probabilities_0: dict[str, float], probabilities_1: dict[str, float]
) -> float:
    """Closed-form diamond norm for a difference of one-qubit Pauli channels.

    For Pauli-covariant channels, the diamond norm equals the classical
    ``l1`` distance between their Pauli probability vectors.
    """

    labels = ("I", "X", "Y", "Z")
    return float(sum(abs(probabilities_0.get(label, 0.0) - probabilities_1.get(label, 0.0)) for label in labels))


def analytical_depolarizing_diamond_norm(p0: float, p1: float, d: int = 2) -> float:
    """Closed-form diamond norm for two depolarizing channels.

    The implemented depolarizing channel is ``D_p(rho) = (1-p)rho +
    p Tr(rho) I/d``.  The diamond distance is
    ``2 * (1 - 1/d**2) * |p0-p1|``.
    """

    if d < 2:
        raise ValueError("d must be at least 2.")
    return float(2.0 * (1.0 - 1.0 / (d * d)) * abs(p0 - p1))


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
    """Solve Watrous's SDP for the diamond norm of a channel difference.

    Parameters
    ----------
    choi_diff
        Choi matrix of ``Phi = E_0 - E_1`` under the project convention.
    d_in
        Input dimension.
    d_out
        Output dimension.
    solver
        Optional CVXPY solver name.  If omitted, MOSEK is preferred when
        available, otherwise SCS is used as a reliable open-source fallback.
    eps
        Accuracy parameter passed to SCS.
    max_iters
        Iteration limit passed to SCS.

    Returns
    -------
    DiamondNormResult
        The optimum value, optimal density matrix, witness, solver, and status.
    """

    import cvxpy as cp

    j_phi = _hermitian_part(_validate_choi_dims(choi_diff, d_in, d_out))
    solver_name = _installed_cvxpy_solver(solver)
    dim = d_in * d_out

    rho = cp.Variable((d_in, d_in), hermitian=True, name="rho")
    witness = cp.Variable((dim, dim), hermitian=True, name="W")
    rho_tensor_identity = cp.kron(rho, np.eye(d_out, dtype=np.complex128))

    constraints = [
        rho >> 0,
        cp.trace(rho) == 1,
        rho_tensor_identity - witness >> 0,
        rho_tensor_identity + witness >> 0,
    ]
    objective = cp.Maximize(cp.real(cp.trace(j_phi @ witness)))
    problem = cp.Problem(objective, constraints)

    kwargs: dict[str, object] = {}
    if solver_name == "SCS":
        kwargs.update({"eps": eps, "max_iters": max_iters, "verbose": False})
    problem.solve(solver=solver_name, **kwargs)

    if problem.status not in (cp.OPTIMAL, cp.OPTIMAL_INACCURATE):
        raise RuntimeError(f"Diamond-norm SDP failed with status {problem.status!r}.")

    return DiamondNormResult(
        value=float(np.real(problem.value)),
        rho=_hermitian_part(np.asarray(rho.value, dtype=np.complex128)),
        witness=_hermitian_part(np.asarray(witness.value, dtype=np.complex128)),
        solver=solver_name,
        status=str(problem.status),
    )


def diamond_norm_sdp(choi_diff: np.ndarray, d_in: int, d_out: int) -> float:
    """Return the diamond norm of a Hermiticity-preserving map via SDP."""

    value = solve_diamond_norm_sdp(choi_diff, d_in, d_out).value
    return float(max(value, 0.0))


def discrimination_probability(
    choi_0: np.ndarray,
    choi_1: np.ndarray,
    d_in: int | None = None,
    d_out: int | None = None,
) -> float:
    """Return the optimal equal-prior two-channel discrimination probability."""

    if d_in is None or d_out is None:
        d_in, d_out = _infer_equal_dims(choi_0)
    norm = diamond_norm_sdp(np.asarray(choi_0) - np.asarray(choi_1), d_in, d_out)
    return float(np.clip(0.5 + 0.25 * norm, 0.5, 1.0))


def optimal_input_state(choi_0: np.ndarray, choi_1: np.ndarray) -> Array:
    """Return the SDP optimal input marginal for channel discrimination."""

    d_in, d_out = _infer_equal_dims(choi_0)
    result = solve_diamond_norm_sdp(np.asarray(choi_0) - np.asarray(choi_1), d_in, d_out)
    eigvals, eigvecs = np.linalg.eigh(result.rho)
    eigvals = np.maximum(eigvals, 0.0)
    if eigvals.sum() <= 0:
        return np.eye(d_in, dtype=np.complex128) / d_in
    rho = eigvecs @ np.diag(eigvals / eigvals.sum()) @ eigvecs.conj().T
    return _hermitian_part(rho)


def _purify_density_matrix(rho: np.ndarray) -> Array:
    eigvals, eigvecs = np.linalg.eigh(_hermitian_part(rho))
    eigvals = np.maximum(eigvals, 0.0)
    sqrt_rho = eigvecs @ np.diag(np.sqrt(eigvals)) @ eigvecs.conj().T
    psi = sqrt_rho.reshape(-1, order="C")
    norm = np.linalg.norm(psi)
    if norm <= 0:
        raise ValueError("Cannot purify the zero matrix.")
    return np.outer(psi / norm, (psi / norm).conj())


def optimal_povm(choi_0: np.ndarray, choi_1: np.ndarray) -> tuple[Array, Array]:
    """Return a Helstrom POVM for the SDP-derived input purification.

    The returned matrices act on reference-output space and sum to identity.
    """

    d_in, d_out = _infer_equal_dims(choi_0)
    rho = optimal_input_state(choi_0, choi_1)
    purification = _purify_density_matrix(rho).reshape(d_in, d_in, d_in, d_in)
    diff = _hermitian_part(np.asarray(choi_0) - np.asarray(choi_1)).reshape(
        d_in, d_out, d_in, d_out
    )
    helstrom = np.einsum("rasc,abcd->rbsd", purification, diff).reshape(
        d_in * d_out, d_in * d_out
    )
    eigvals, eigvecs = np.linalg.eigh(_hermitian_part(helstrom))
    positive = eigvals >= 0.0
    m0 = eigvecs[:, positive] @ eigvecs[:, positive].conj().T
    m1 = np.eye(d_in * d_out, dtype=np.complex128) - m0
    return _hermitian_part(m0), _hermitian_part(m1)


def _tensor_choi_pair(
    choi_a: np.ndarray,
    choi_b: np.ndarray,
    dims_a: tuple[int, int],
    dims_b: tuple[int, int],
) -> Array:
    d_in_a, d_out_a = dims_a
    d_in_b, d_out_b = dims_b
    arr_a = _validate_choi_dims(choi_a, d_in_a, d_out_a).reshape(
        d_in_a, d_out_a, d_in_a, d_out_a
    )
    arr_b = _validate_choi_dims(choi_b, d_in_b, d_out_b).reshape(
        d_in_b, d_out_b, d_in_b, d_out_b
    )
    tensor = np.einsum("iajb,kcld->ikacjlbd", arr_a, arr_b)
    tensor = tensor.reshape(
        d_in_a * d_in_b,
        d_out_a * d_out_b,
        d_in_a * d_in_b,
        d_out_a * d_out_b,
    )
    return _hermitian_part(tensor.reshape(d_in_a * d_in_b * d_out_a * d_out_b, -1))


def tensor_power_choi(choi: np.ndarray, n: int, d_in: int, d_out: int) -> Array:
    """Return the Choi matrix for the ``n``-fold parallel tensor power."""

    if n < 1:
        raise ValueError("n must be at least 1.")
    result = _validate_choi_dims(choi, d_in, d_out)
    current_dims = (d_in, d_out)
    for _ in range(1, n):
        result = _tensor_choi_pair(result, choi, current_dims, (d_in, d_out))
        current_dims = (current_dims[0] * d_in, current_dims[1] * d_out)
    return result


def n_shot_discrimination(choi_0: np.ndarray, choi_1: np.ndarray, n: int) -> float:
    """Return optimal parallel ``n``-use discrimination probability."""

    d_in, d_out = _infer_equal_dims(choi_0)
    choi_0_n = tensor_power_choi(choi_0, n, d_in, d_out)
    choi_1_n = tensor_power_choi(choi_1, n, d_in, d_out)
    return discrimination_probability(choi_0_n, choi_1_n, d_in**n, d_out**n)


def _qubit_pure_states(n_theta: int = 41, n_phi: int = 81) -> Iterable[Array]:
    yield np.array([[1.0], [0.0]], dtype=np.complex128)
    yield np.array([[0.0], [1.0]], dtype=np.complex128)
    yield np.array([[1.0], [1.0]], dtype=np.complex128) / np.sqrt(2.0)
    yield np.array([[1.0], [1.0j]], dtype=np.complex128) / np.sqrt(2.0)
    for theta, phi in product(
        np.linspace(0.0, np.pi, n_theta), np.linspace(0.0, 2.0 * np.pi, n_phi, endpoint=False)
    ):
        yield np.array(
            [[np.cos(theta / 2.0)], [np.exp(1j * phi) * np.sin(theta / 2.0)]],
            dtype=np.complex128,
        )


def _trace_norm_hermitian(matrix: np.ndarray) -> float:
    eigvals = np.linalg.eigvalsh(_hermitian_part(matrix))
    return float(np.sum(np.abs(eigvals)))


def product_strategy_discrimination(choi_0: np.ndarray, choi_1: np.ndarray) -> float:
    """Approximate the best no-ancilla discrimination probability.

    For one-qubit channels this performs a deterministic Bloch-sphere grid
    search over pure input states.  This is enough to display entanglement
    advantage for standard examples such as identity vs. depolarizing noise.
    """

    d_in, d_out = _infer_equal_dims(choi_0)
    diff = np.asarray(choi_0) - np.asarray(choi_1)
    if d_in != 2:
        rng = np.random.default_rng(42)
        vectors = []
        for _ in range(2048):
            vec = rng.normal(size=d_in) + 1j * rng.normal(size=d_in)
            vectors.append((vec / np.linalg.norm(vec)).reshape(d_in, 1))
    else:
        vectors = list(_qubit_pure_states())

    best_trace_norm = 0.0
    for ket in vectors:
        rho = ket @ ket.conj().T
        output_diff = apply_choi_to_state(diff, rho, d_in, d_out)
        best_trace_norm = max(best_trace_norm, _trace_norm_hermitian(output_diff))
    return float(np.clip(0.5 + 0.25 * best_trace_norm, 0.5, 1.0))
