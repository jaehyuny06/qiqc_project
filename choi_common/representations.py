"""Conversions among Kraus, Choi, Stinespring, and natural representations.

All Choi matrices use the unnormalized input-first convention
``C_E = sum_ij |i><j|_A tensor E(|i><j|)_B``. Kraus operators have shape
``(d_out, d_in)``.
"""

from __future__ import annotations

from collections.abc import Sequence

import numpy as np
from numpy.typing import NDArray

from .utils import as_complex_matrix, hermitian_part, infer_choi_dims, infer_natural_dims


Array = NDArray[np.complex128]


def _validate_kraus_ops(kraus_ops: Sequence[np.ndarray]) -> tuple[list[Array], int, int]:
    if not kraus_ops:
        raise ValueError("kraus_ops must contain at least one matrix.")
    ops = [as_complex_matrix(op, f"kraus_ops[{idx}]") for idx, op in enumerate(kraus_ops)]
    d_out, d_in = ops[0].shape
    for op in ops:
        if op.shape != (d_out, d_in):
            raise ValueError("All Kraus operators must have the same shape.")
    return ops, d_out, d_in


def kraus_to_choi(kraus_ops: Sequence[np.ndarray]) -> Array:
    """Convert Kraus operators to an input-first Choi matrix.

    Parameters
    ----------
    kraus_ops:
        Sequence of Kraus operators, each with shape ``(d_out, d_in)``.

    Returns
    -------
    numpy.ndarray
        Choi matrix with shape ``(d_in * d_out, d_in * d_out)``.
    """
    ops, d_out, d_in = _validate_kraus_ops(kraus_ops)
    choi = np.zeros((d_in * d_out, d_in * d_out), dtype=np.complex128)
    for op in ops:
        vec = op.T.reshape(d_in * d_out)
        choi += np.outer(vec, vec.conj())
    return hermitian_part(choi)


def choi_to_kraus(
    choi: np.ndarray,
    tol: float = 1e-10,
    d_in: int | None = None,
    d_out: int | None = None,
) -> list[Array]:
    """Recover Kraus operators from a positive Choi matrix.

    Eigenvalues at or below ``tol`` are discarded. The returned operators have
    shape ``(d_out, d_in)`` and are sorted by descending Choi eigenvalue.
    """
    arr = as_complex_matrix(choi, "choi", square=True)
    d_in, d_out = infer_choi_dims(arr, d_in=d_in, d_out=d_out)
    eigvals, eigvecs = np.linalg.eigh(hermitian_part(arr))
    order = np.argsort(eigvals)[::-1]

    kraus_ops: list[Array] = []
    for idx in order:
        eigval = float(np.real(eigvals[idx]))
        if eigval > tol:
            vec = eigvecs[:, idx]
            kraus_ops.append(np.sqrt(eigval) * vec.reshape(d_in, d_out).T)
    return kraus_ops


def kraus_to_stinespring(kraus_ops: Sequence[np.ndarray]) -> Array:
    """Construct a Stinespring isometry by vertically stacking Kraus operators."""
    ops, _, _ = _validate_kraus_ops(kraus_ops)
    return np.vstack(ops).astype(np.complex128)


def stinespring_to_kraus(isometry: np.ndarray, env_dim: int) -> list[Array]:
    """Slice a Stinespring isometry into ``env_dim`` Kraus operators."""
    arr = as_complex_matrix(isometry, "isometry")
    if env_dim <= 0:
        raise ValueError("env_dim must be positive.")
    if arr.shape[0] % env_dim != 0:
        raise ValueError("isometry row count must be divisible by env_dim.")
    d_out = arr.shape[0] // env_dim
    return [arr[k * d_out : (k + 1) * d_out, :].copy() for k in range(env_dim)]


def choi_to_natural(
    choi: np.ndarray,
    d_in: int | None = None,
    d_out: int | None = None,
) -> Array:
    """Convert a Choi matrix to the natural representation.

    The natural representation ``S`` is defined by ``vec(E(rho)) = S @
    vec(rho)`` using column-stacking vectorization.
    """
    arr = as_complex_matrix(choi, "choi", square=True)
    d_in, d_out = infer_choi_dims(arr, d_in=d_in, d_out=d_out)
    tensor = arr.reshape(d_in, d_out, d_in, d_out)
    return tensor.transpose(1, 3, 0, 2).reshape(d_out * d_out, d_in * d_in)


def natural_to_choi(
    natural: np.ndarray,
    d_in: int | None = None,
    d_out: int | None = None,
) -> Array:
    """Convert a natural representation matrix to an input-first Choi matrix."""
    arr = as_complex_matrix(natural, "natural")
    d_in, d_out = infer_natural_dims(arr, d_in=d_in, d_out=d_out)
    tensor = arr.reshape(d_out, d_out, d_in, d_in)
    return tensor.transpose(2, 0, 3, 1).reshape(d_in * d_out, d_in * d_out)


def apply_kraus_channel(rho: np.ndarray, kraus_ops: Sequence[np.ndarray]) -> Array:
    """Apply a Kraus-represented channel to an input operator ``rho``."""
    ops, d_out, d_in = _validate_kraus_ops(kraus_ops)
    state = as_complex_matrix(rho, "rho")
    if state.shape != (d_in, d_in):
        raise ValueError("rho shape must match the Kraus input dimension.")
    out = np.zeros((d_out, d_out), dtype=np.complex128)
    for op in ops:
        out += op @ state @ op.conj().T
    return out


def apply_choi_channel(
    choi: np.ndarray,
    rho: np.ndarray,
    d_in: int | None = None,
    d_out: int | None = None,
) -> Array:
    """Apply a Choi-represented channel using the project-standard API."""
    state = as_complex_matrix(rho, "rho")
    if d_in is None:
        d_in = state.shape[0]
    if state.shape != (d_in, d_in):
        raise ValueError(f"rho must have shape {(d_in, d_in)}.")
    arr = as_complex_matrix(choi, "choi", square=True)
    d_in, d_out = infer_choi_dims(arr, d_in=d_in, d_out=d_out)
    tensor = arr.reshape(d_in, d_out, d_in, d_out)
    return np.einsum("ij,iajb->ab", state, tensor)


def compose_choi_channels(
    choi_after: np.ndarray,
    choi_before: np.ndarray,
    d_mid: int | None = None,
) -> Array:
    """Return the Choi matrix of ``choi_after`` composed after ``choi_before``."""
    after = as_complex_matrix(choi_after, "choi_after", square=True)
    before = as_complex_matrix(choi_before, "choi_before", square=True)
    if d_mid is None:
        d_mid = int(round(np.sqrt(after.shape[0])))
    d_in = before.shape[0] // d_mid
    d_out = after.shape[0] // d_mid
    if before.shape[0] != d_in * d_mid or after.shape[0] != d_mid * d_out:
        raise ValueError("Choi dimensions are incompatible for composition.")

    blocks: list[list[Array]] = []
    for i in range(d_in):
        row: list[Array] = []
        for j in range(d_in):
            block = before[
                i * d_mid : (i + 1) * d_mid,
                j * d_mid : (j + 1) * d_mid,
            ]
            row.append(apply_choi_channel(after, block, d_in=d_mid, d_out=d_out))
        blocks.append(row)
    return hermitian_part(np.block(blocks))
