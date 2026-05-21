r"""Channel representation utilities for the Choi project.

The Choi convention throughout this module is

.. math::

    C_E = \sum_{i,j} |i\rangle\langle j| \otimes E(|i\rangle\langle j|),

so the input system is the first tensor factor and the output system is the
second tensor factor. Kraus operators have shape ``(d_out, d_in)``.
"""

from __future__ import annotations

from math import isclose
from typing import Iterable

import numpy as np


Array = np.ndarray


def _as_complex_matrix(matrix: Array, name: str) -> Array:
    """Return ``matrix`` as a two-dimensional complex array."""
    arr = np.asarray(matrix, dtype=complex)
    if arr.ndim != 2:
        raise ValueError(f"{name} must be a two-dimensional matrix.")
    return arr


def _validate_kraus_ops(kraus_ops: list[Array]) -> tuple[int, int]:
    """Validate a Kraus list and return ``(d_out, d_in)``."""
    if not kraus_ops:
        raise ValueError("kraus_ops must contain at least one matrix.")

    first = _as_complex_matrix(kraus_ops[0], "kraus_ops[0]")
    d_out, d_in = first.shape
    for idx, op in enumerate(kraus_ops):
        arr = _as_complex_matrix(op, f"kraus_ops[{idx}]")
        if arr.shape != (d_out, d_in):
            raise ValueError("All Kraus operators must have the same shape.")
        kraus_ops[idx] = arr
    return d_out, d_in


def _factor_pairs(n: int) -> Iterable[tuple[int, int]]:
    """Yield positive factor pairs ``(a, b)`` with ``a * b == n``."""
    for a in range(1, int(np.sqrt(n)) + 1):
        if n % a == 0:
            yield a, n // a
            if a != n // a:
                yield n // a, a


def _partial_trace_output(choi: Array, d_in: int, d_out: int) -> Array:
    """Trace the output tensor factor of a Choi matrix."""
    tensor = choi.reshape(d_in, d_out, d_in, d_out)
    return np.trace(tensor, axis1=1, axis2=3)


def _partial_trace_input(choi: Array, d_in: int, d_out: int) -> Array:
    """Trace the input tensor factor of a Choi matrix."""
    tensor = choi.reshape(d_in, d_out, d_in, d_out)
    return np.trace(tensor, axis1=0, axis2=2)


def _infer_choi_dims(choi: Array, tol: float = 1e-8) -> tuple[int, int]:
    """Infer ``(d_in, d_out)`` for a Choi matrix when possible.

    The public API intentionally follows the project specification, whose
    conversion functions do not include dimension arguments. For trace-
    preserving channels, the condition ``Tr_out(C) = I_in`` usually determines
    the factorization. If it does not, this helper falls back to square
    channels.
    """
    arr = _as_complex_matrix(choi, "choi")
    if arr.shape[0] != arr.shape[1]:
        raise ValueError("choi must be a square matrix.")

    total_dim = arr.shape[0]
    candidates: list[tuple[int, int]] = []
    for d_in, d_out in _factor_pairs(total_dim):
        reduced = _partial_trace_output(arr, d_in, d_out)
        if np.allclose(reduced, np.eye(d_in), atol=tol):
            candidates.append((d_in, d_out))

    if len(candidates) == 1:
        return candidates[0]

    d_square = int(round(np.sqrt(total_dim)))
    if d_square * d_square == total_dim:
        return d_square, d_square

    raise ValueError(
        "Could not infer Choi dimensions. Use a trace-preserving Choi matrix "
        "or a square input/output channel."
    )


def _infer_natural_dims(natural: Array) -> tuple[int, int]:
    """Infer ``(d_in, d_out)`` from a natural representation matrix."""
    arr = _as_complex_matrix(natural, "natural")
    d_out = int(round(np.sqrt(arr.shape[0])))
    d_in = int(round(np.sqrt(arr.shape[1])))
    if d_out * d_out != arr.shape[0] or d_in * d_in != arr.shape[1]:
        raise ValueError("natural must have shape (d_out**2, d_in**2).")
    return d_in, d_out


def _check_probability(value: float, name: str) -> None:
    """Validate that a probability-like parameter is in ``[0, 1]``."""
    if not 0.0 <= value <= 1.0:
        raise ValueError(f"{name} must be between 0 and 1.")


def kraus_to_choi(kraus_ops: list[Array]) -> Array:
    """Convert Kraus operators to a Choi matrix.

    Parameters
    ----------
    kraus_ops:
        List of Kraus operators, each with shape ``(d_out, d_in)``.

    Returns
    -------
    np.ndarray
        Choi matrix with shape ``(d_in * d_out, d_in * d_out)`` using the
        input-first convention.
    """
    d_out, d_in = _validate_kraus_ops(kraus_ops)
    choi = np.zeros((d_in * d_out, d_in * d_out), dtype=complex)

    for op in kraus_ops:
        vec = op.T.reshape(d_in * d_out)
        choi += np.outer(vec, vec.conj())

    return (choi + choi.conj().T) / 2


def choi_to_kraus(choi: Array, tol: float = 1e-10) -> list[Array]:
    """Recover a Kraus representation from a positive Choi matrix.

    Parameters
    ----------
    choi:
        Choi matrix in the input-first convention.
    tol:
        Eigenvalues at or below this tolerance are discarded.

    Returns
    -------
    list[np.ndarray]
        Kraus operators with shape ``(d_out, d_in)``.
    """
    arr = _as_complex_matrix(choi, "choi")
    d_in, d_out = _infer_choi_dims(arr)
    hermitian = (arr + arr.conj().T) / 2
    eigenvalues, eigenvectors = np.linalg.eigh(hermitian)

    kraus_ops: list[Array] = []
    for eig, vec in zip(eigenvalues[::-1], eigenvectors.T[::-1]):
        if eig > tol:
            op = np.sqrt(eig) * vec.reshape(d_in, d_out).T
            kraus_ops.append(op)

    return kraus_ops


def kraus_to_stinespring(kraus_ops: list[Array]) -> Array:
    """Construct a Stinespring isometry by vertically stacking Kraus operators.

    Parameters
    ----------
    kraus_ops:
        List of Kraus operators, each with shape ``(d_out, d_in)``.

    Returns
    -------
    np.ndarray
        Isometry ``V`` with shape ``(n_kraus * d_out, d_in)``. The row space is
        ordered as environment first, then output.
    """
    _validate_kraus_ops(kraus_ops)
    return np.vstack(kraus_ops).astype(complex)


def stinespring_to_kraus(isometry: Array, env_dim: int) -> list[Array]:
    """Slice a Stinespring isometry into Kraus operators.

    Parameters
    ----------
    isometry:
        Matrix with shape ``(env_dim * d_out, d_in)``.
    env_dim:
        Number of environment basis states, equal to the number of Kraus
        operators in this representation.

    Returns
    -------
    list[np.ndarray]
        Kraus operators with shape ``(d_out, d_in)``.
    """
    arr = _as_complex_matrix(isometry, "isometry")
    if env_dim <= 0:
        raise ValueError("env_dim must be positive.")
    if arr.shape[0] % env_dim != 0:
        raise ValueError("isometry row count must be divisible by env_dim.")

    d_out = arr.shape[0] // env_dim
    return [arr[k * d_out : (k + 1) * d_out, :].copy() for k in range(env_dim)]


def choi_to_natural(choi: Array) -> Array:
    """Convert a Choi matrix to the natural/Liouville representation.

    The natural representation ``S`` is defined by
    ``vec(E(rho)) = S @ vec(rho)`` with column-stacking vectorization.

    Parameters
    ----------
    choi:
        Choi matrix in the input-first convention.

    Returns
    -------
    np.ndarray
        Natural representation with shape ``(d_out**2, d_in**2)``.
    """
    arr = _as_complex_matrix(choi, "choi")
    d_in, d_out = _infer_choi_dims(arr)
    tensor = arr.reshape(d_in, d_out, d_in, d_out)
    return tensor.transpose(1, 3, 0, 2).reshape(d_out * d_out, d_in * d_in)


def natural_to_choi(natural: Array) -> Array:
    """Convert a natural/Liouville representation to a Choi matrix.

    Parameters
    ----------
    natural:
        Superoperator matrix with shape ``(d_out**2, d_in**2)`` under
        column-stacking vectorization.

    Returns
    -------
    np.ndarray
        Choi matrix with shape ``(d_in * d_out, d_in * d_out)``.
    """
    arr = _as_complex_matrix(natural, "natural")
    d_in, d_out = _infer_natural_dims(arr)
    tensor = arr.reshape(d_out, d_out, d_in, d_in)
    return tensor.transpose(2, 0, 3, 1).reshape(d_in * d_out, d_in * d_out)


def is_cp(choi: Array, tol: float = 1e-9) -> bool:
    """Check complete positivity via Choi positive semidefiniteness.

    Parameters
    ----------
    choi:
        Choi matrix to test.
    tol:
        Numerical tolerance for the smallest eigenvalue.

    Returns
    -------
    bool
        ``True`` when the Choi matrix is Hermitian and positive semidefinite
        within tolerance.
    """
    arr = _as_complex_matrix(choi, "choi")
    if arr.shape[0] != arr.shape[1]:
        return False
    if not np.allclose(arr, arr.conj().T, atol=tol):
        return False
    return bool(np.linalg.eigvalsh((arr + arr.conj().T) / 2).min() >= -tol)


def is_tp(choi: Array, d_in: int, tol: float = 1e-9) -> bool:
    """Check trace preservation via ``Tr_out(C) = I_in``.

    Parameters
    ----------
    choi:
        Choi matrix in the input-first convention.
    d_in:
        Input Hilbert-space dimension.
    tol:
        Numerical tolerance.

    Returns
    -------
    bool
        ``True`` if the output partial trace equals the input identity.
    """
    arr = _as_complex_matrix(choi, "choi")
    if arr.shape[0] != arr.shape[1] or arr.shape[0] % d_in != 0:
        return False
    d_out = arr.shape[0] // d_in
    reduced = _partial_trace_output(arr, d_in, d_out)
    return bool(np.allclose(reduced, np.eye(d_in), atol=tol))


def apply_channel(rho: Array, kraus_ops: list[Array]) -> Array:
    """Apply a channel in Kraus form to a density matrix or operator.

    Parameters
    ----------
    rho:
        Input operator with shape ``(d_in, d_in)``.
    kraus_ops:
        List of Kraus operators with shape ``(d_out, d_in)``.

    Returns
    -------
    np.ndarray
        Output operator with shape ``(d_out, d_out)``.
    """
    d_out, d_in = _validate_kraus_ops(kraus_ops)
    state = _as_complex_matrix(rho, "rho")
    if state.shape != (d_in, d_in):
        raise ValueError("rho shape must match the Kraus input dimension.")

    out = np.zeros((d_out, d_out), dtype=complex)
    for op in kraus_ops:
        out += op @ state @ op.conj().T
    return out


def compose_channels_choi(choi1: Array, choi2: Array) -> Array:
    """Compose two channels represented by Choi matrices.

    This returns the Choi matrix of ``E2(E1(rho))``.

    Parameters
    ----------
    choi1:
        Choi matrix of the first channel ``E1``.
    choi2:
        Choi matrix of the second channel ``E2``.

    Returns
    -------
    np.ndarray
        Choi matrix of the composed channel ``E2 o E1``.
    """
    s1 = choi_to_natural(choi1)
    s2 = choi_to_natural(choi2)
    if s1.shape[0] != s2.shape[1]:
        raise ValueError("Output dimension of choi1 must match input dimension of choi2.")
    return natural_to_choi(s2 @ s1)


def random_channel(d_in: int, d_out: int, n_kraus: int) -> list[Array]:
    """Generate a random trace-preserving quantum channel.

    Parameters
    ----------
    d_in:
        Input Hilbert-space dimension.
    d_out:
        Output Hilbert-space dimension.
    n_kraus:
        Number of Kraus operators.

    Returns
    -------
    list[np.ndarray]
        Random Kraus operators satisfying ``sum_k K_k^dagger K_k = I``.
    """
    if d_in <= 0 or d_out <= 0 or n_kraus <= 0:
        raise ValueError("d_in, d_out, and n_kraus must all be positive.")
    if n_kraus * d_out < d_in:
        raise ValueError("n_kraus * d_out must be at least d_in for a TP channel.")

    ginibre = (
        np.random.normal(size=(n_kraus * d_out, d_in))
        + 1j * np.random.normal(size=(n_kraus * d_out, d_in))
    )
    q, _ = np.linalg.qr(ginibre)
    return stinespring_to_kraus(q[:, :d_in], n_kraus)


def identity_channel(d: int = 2) -> list[Array]:
    """Return Kraus operators for the ``d``-dimensional identity channel."""
    if d <= 0:
        raise ValueError("d must be positive.")
    return [np.eye(d, dtype=complex)]


def bit_flip_channel(p: float) -> list[Array]:
    """Return Kraus operators for the qubit bit-flip channel."""
    _check_probability(p, "p")
    x = np.array([[0, 1], [1, 0]], dtype=complex)
    return [np.sqrt(1 - p) * np.eye(2, dtype=complex), np.sqrt(p) * x]


def phase_flip_channel(p: float) -> list[Array]:
    """Return Kraus operators for the qubit phase-flip channel."""
    _check_probability(p, "p")
    z = np.array([[1, 0], [0, -1]], dtype=complex)
    return [np.sqrt(1 - p) * np.eye(2, dtype=complex), np.sqrt(p) * z]


def pauli_channel(px: float, py: float, pz: float) -> list[Array]:
    """Return Kraus operators for a general qubit Pauli channel.

    The probabilities are for applying ``X``, ``Y``, and ``Z``. The identity
    probability is ``1 - px - py - pz``.
    """
    for value, name in [(px, "px"), (py, "py"), (pz, "pz")]:
        _check_probability(value, name)
    p_identity = 1 - px - py - pz
    if p_identity < -1e-15:
        raise ValueError("px + py + pz must be at most 1.")
    p_identity = max(0.0, p_identity)

    x = np.array([[0, 1], [1, 0]], dtype=complex)
    y = np.array([[0, -1j], [1j, 0]], dtype=complex)
    z = np.array([[1, 0], [0, -1]], dtype=complex)
    return [
        np.sqrt(p_identity) * np.eye(2, dtype=complex),
        np.sqrt(px) * x,
        np.sqrt(py) * y,
        np.sqrt(pz) * z,
    ]


def depolarizing_channel(p: float) -> list[Array]:
    """Return Kraus operators for the qubit depolarizing channel.

    This implements ``E(rho) = (1 - p) rho + p I / 2`` for ``0 <= p <= 1``.
    """
    _check_probability(p, "p")
    return pauli_channel(p / 4, p / 4, p / 4)


def amplitude_damping_channel(gamma: float) -> list[Array]:
    """Return Kraus operators for the qubit amplitude damping channel."""
    _check_probability(gamma, "gamma")
    return [
        np.array([[1, 0], [0, np.sqrt(1 - gamma)]], dtype=complex),
        np.array([[0, np.sqrt(gamma)], [0, 0]], dtype=complex),
    ]


def phase_damping_channel(gamma: float) -> list[Array]:
    """Return Kraus operators for the qubit phase damping channel.

    Diagonal entries are fixed and off-diagonal entries are multiplied by
    ``1 - gamma``.
    """
    _check_probability(gamma, "gamma")
    p0 = np.array([[1, 0], [0, 0]], dtype=complex)
    p1 = np.array([[0, 0], [0, 1]], dtype=complex)
    return [np.sqrt(1 - gamma) * np.eye(2, dtype=complex), np.sqrt(gamma) * p0, np.sqrt(gamma) * p1]


def choi_rank(choi: Array, tol: float = 1e-10) -> int:
    """Return the numerical rank of a Choi matrix."""
    arr = _as_complex_matrix(choi, "choi")
    eigvals = np.linalg.eigvalsh((arr + arr.conj().T) / 2)
    return int(np.count_nonzero(eigvals > tol))


def is_unital(choi: Array, d_out: int, tol: float = 1e-9) -> bool:
    """Check unitality for square channels via ``E(I) = I``.

    Parameters
    ----------
    choi:
        Choi matrix in the input-first convention.
    d_out:
        Output dimension. For a square channel this equals the input dimension.
    tol:
        Numerical tolerance.

    Returns
    -------
    bool
        ``True`` when the input partial trace is the output identity.
    """
    arr = _as_complex_matrix(choi, "choi")
    if arr.shape[0] % d_out != 0:
        return False
    d_in = arr.shape[0] // d_out
    if not isclose(d_in, d_out):
        return False
    reduced = _partial_trace_input(arr, d_in, d_out)
    return bool(np.allclose(reduced, np.eye(d_out), atol=tol))
