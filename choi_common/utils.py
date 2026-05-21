"""Low-level helpers for Choi-representation utilities."""

from __future__ import annotations

from typing import Any

import numpy as np
from numpy.typing import NDArray


Array = NDArray[np.complex128]


def as_complex_matrix(matrix: Any, name: str = "matrix", square: bool = False) -> Array:
    """Return ``matrix`` as a two-dimensional complex array.

    Parameters
    ----------
    matrix:
        Array-like object to validate.
    name:
        Name used in error messages.
    square:
        If ``True``, require the matrix to be square.

    Returns
    -------
    numpy.ndarray
        Complex-valued two-dimensional array.
    """
    arr = np.asarray(matrix, dtype=np.complex128)
    if arr.ndim != 2:
        raise ValueError(f"{name} must be a two-dimensional matrix.")
    if square and arr.shape[0] != arr.shape[1]:
        raise ValueError(f"{name} must be a square matrix.")
    return arr


def dagger(matrix: np.ndarray) -> Array:
    """Return the conjugate transpose of ``matrix``."""
    return np.asarray(matrix, dtype=np.complex128).conj().T


def hermitian_part(matrix: np.ndarray) -> Array:
    """Return the Hermitian part of ``matrix``."""
    arr = np.asarray(matrix, dtype=np.complex128)
    return 0.5 * (arr + arr.conj().T)


def validate_probability(value: float, name: str = "p") -> float:
    """Validate that a scalar probability lies in ``[0, 1]``.

    Parameters
    ----------
    value:
        Candidate probability.
    name:
        Parameter name used in error messages.

    Returns
    -------
    float
        Validated probability.
    """
    probability = float(value)
    if not 0.0 <= probability <= 1.0:
        raise ValueError(f"{name} must be between 0 and 1.")
    return probability


def _factor_pairs(n: int) -> list[tuple[int, int]]:
    pairs: list[tuple[int, int]] = []
    for a in range(1, int(np.sqrt(n)) + 1):
        if n % a == 0:
            pairs.append((a, n // a))
            if a != n // a:
                pairs.append((n // a, a))
    return pairs


def _partial_trace_output_raw(choi: Array, d_in: int, d_out: int) -> Array:
    tensor = choi.reshape(d_in, d_out, d_in, d_out)
    return np.trace(tensor, axis1=1, axis2=3)


def infer_choi_dims(
    choi: np.ndarray,
    d_in: int | None = None,
    d_out: int | None = None,
    tol: float = 1e-8,
) -> tuple[int, int]:
    """Infer ``(d_in, d_out)`` for an input-first Choi matrix.

    Explicit dimensions are preferred. If neither dimension is provided, this
    helper first searches for a unique trace-preserving factorization and then
    falls back to equal input/output dimensions when possible.
    """
    arr = as_complex_matrix(choi, "choi", square=True)
    total_dim = arr.shape[0]

    if d_in is not None and d_out is not None:
        if d_in <= 0 or d_out <= 0:
            raise ValueError("d_in and d_out must be positive.")
        if total_dim != d_in * d_out:
            raise ValueError(f"choi must have shape {(d_in * d_out, d_in * d_out)}.")
        return int(d_in), int(d_out)

    if d_in is not None:
        if d_in <= 0 or total_dim % d_in != 0:
            raise ValueError("Could not infer d_out from Choi size and d_in.")
        return int(d_in), int(total_dim // d_in)

    if d_out is not None:
        if d_out <= 0 or total_dim % d_out != 0:
            raise ValueError("Could not infer d_in from Choi size and d_out.")
        return int(total_dim // d_out), int(d_out)

    candidates: list[tuple[int, int]] = []
    for cand_in, cand_out in _factor_pairs(total_dim):
        reduced = _partial_trace_output_raw(arr, cand_in, cand_out)
        if np.allclose(reduced, np.eye(cand_in), atol=tol):
            candidates.append((cand_in, cand_out))
    if len(candidates) == 1:
        return candidates[0]

    d_square = int(round(np.sqrt(total_dim)))
    if d_square * d_square == total_dim:
        return d_square, d_square

    raise ValueError(
        "Could not infer Choi dimensions. Provide d_in and d_out explicitly."
    )


def infer_natural_dims(
    natural: np.ndarray,
    d_in: int | None = None,
    d_out: int | None = None,
) -> tuple[int, int]:
    """Infer ``(d_in, d_out)`` from a natural representation matrix."""
    arr = as_complex_matrix(natural, "natural")
    if d_in is not None and d_out is not None:
        if arr.shape != (d_out * d_out, d_in * d_in):
            raise ValueError(f"natural must have shape {(d_out * d_out, d_in * d_in)}.")
        return int(d_in), int(d_out)
    if d_in is not None or d_out is not None:
        raise ValueError("Provide both d_in and d_out, or neither.")

    inferred_out = int(round(np.sqrt(arr.shape[0])))
    inferred_in = int(round(np.sqrt(arr.shape[1])))
    if inferred_out * inferred_out != arr.shape[0] or inferred_in * inferred_in != arr.shape[1]:
        raise ValueError("natural must have shape (d_out**2, d_in**2).")
    return inferred_in, inferred_out
