"""Validation helpers for Choi matrices and tensor-product operators."""

from __future__ import annotations

from collections.abc import Sequence

import numpy as np
from numpy.typing import NDArray

from .utils import as_complex_matrix, hermitian_part, infer_choi_dims


Array = NDArray[np.complex128]


def partial_trace(operator: np.ndarray, dims: Sequence[int], trace_out: Sequence[int]) -> Array:
    """Trace selected tensor factors out of an operator.

    Parameters
    ----------
    operator:
        Square matrix acting on ``tensor_i C^{dims[i]}``.
    dims:
        Tensor-factor dimensions.
    trace_out:
        Indices of tensor factors to trace out.

    Returns
    -------
    numpy.ndarray
        Reduced operator on the untraced tensor factors, in the original order.
    """
    dims_list = [int(dim) for dim in dims]
    if any(dim <= 0 for dim in dims_list):
        raise ValueError("All tensor-factor dimensions must be positive.")
    total_dim = int(np.prod(dims_list, dtype=int))
    matrix = np.asarray(operator, dtype=np.complex128)
    if matrix.shape != (total_dim, total_dim):
        raise ValueError("operator shape is incompatible with dims.")

    tensor = matrix.reshape(dims_list + dims_list)
    for axis in sorted(set(trace_out), reverse=True):
        if axis < 0 or axis >= len(dims_list):
            raise ValueError(f"trace axis {axis} is outside dims.")
        tensor = np.trace(tensor, axis1=axis, axis2=axis + len(dims_list))
        dims_list.pop(axis)

    remaining_dim = int(np.prod(dims_list, dtype=int)) if dims_list else 1
    return tensor.reshape(remaining_dim, remaining_dim)


def partial_trace_output(choi: np.ndarray, d_in: int, d_out: int) -> Array:
    """Trace the output tensor factor of an input-first Choi matrix."""
    arr = as_complex_matrix(choi, "choi", square=True)
    if arr.shape != (d_in * d_out, d_in * d_out):
        raise ValueError(f"choi must have shape {(d_in * d_out, d_in * d_out)}.")
    tensor = arr.reshape(d_in, d_out, d_in, d_out)
    return np.trace(tensor, axis1=1, axis2=3)


def partial_trace_input(choi: np.ndarray, d_in: int, d_out: int) -> Array:
    """Trace the input tensor factor of an input-first Choi matrix."""
    arr = as_complex_matrix(choi, "choi", square=True)
    if arr.shape != (d_in * d_out, d_in * d_out):
        raise ValueError(f"choi must have shape {(d_in * d_out, d_in * d_out)}.")
    tensor = arr.reshape(d_in, d_out, d_in, d_out)
    return np.trace(tensor, axis1=0, axis2=2)


def is_cp(choi: np.ndarray, tol: float = 1e-9, require_hermitian: bool = True) -> bool:
    """Return whether a Choi matrix is positive semidefinite within tolerance."""
    try:
        arr = as_complex_matrix(choi, "choi", square=True)
    except ValueError:
        return False
    if require_hermitian and not np.allclose(arr, arr.conj().T, atol=tol):
        return False
    eigvals = np.linalg.eigvalsh(hermitian_part(arr))
    return bool(np.min(eigvals) >= -tol)


def is_tp(
    choi: np.ndarray,
    d_in: int,
    d_out: int | None = None,
    tol: float = 1e-9,
) -> bool:
    """Return whether ``Tr_B(C_E) = I_A`` within tolerance."""
    try:
        arr = as_complex_matrix(choi, "choi", square=True)
        if d_out is None:
            d_in, d_out = infer_choi_dims(arr, d_in=d_in)
        reduced = partial_trace_output(arr, d_in, d_out)
    except ValueError:
        return False
    return bool(np.allclose(reduced, np.eye(d_in), atol=tol))


def is_unital(
    choi: np.ndarray,
    d_in: int,
    d_out: int | None = None,
    tol: float = 1e-9,
) -> bool:
    """Return whether a square channel satisfies ``E(I) = I`` within tolerance."""
    try:
        arr = as_complex_matrix(choi, "choi", square=True)
        if d_out is None:
            d_in, d_out = infer_choi_dims(arr, d_in=d_in)
        if d_in != d_out:
            return False
        reduced = partial_trace_input(arr, d_in, d_out)
    except ValueError:
        return False
    return bool(np.allclose(reduced, np.eye(d_out), atol=tol))


def choi_rank(choi: np.ndarray, tol: float = 1e-10) -> int:
    """Return the numerical rank of a Choi matrix."""
    arr = as_complex_matrix(choi, "choi", square=True)
    eigvals = np.linalg.eigvalsh(hermitian_part(arr))
    return int(np.count_nonzero(eigvals > tol))


def tp_residual(choi: np.ndarray, d_in: int, d_out: int | None = None) -> float:
    """Return ``||Tr_B(C_E) - I_A||_F`` for a Choi matrix."""
    arr = as_complex_matrix(choi, "choi", square=True)
    if d_out is None:
        d_in, d_out = infer_choi_dims(arr, d_in=d_in)
    return float(np.linalg.norm(partial_trace_output(arr, d_in, d_out) - np.eye(d_in)))
