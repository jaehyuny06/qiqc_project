"""Validation helpers for Choi matrices and tensor-product operators."""

from __future__ import annotations

from collections.abc import Sequence

import numpy as np
from numpy.typing import NDArray


Array = NDArray[np.complex128]


def partial_trace(operator: np.ndarray, dims: Sequence[int], trace_out: Sequence[int]) -> Array:
    """Trace selected tensor factors out of ``operator``."""
    raise NotImplementedError("Proposal skeleton only.")


def partial_trace_output(choi: np.ndarray, d_in: int, d_out: int) -> Array:
    """Trace the output tensor factor of an input-first Choi matrix."""
    raise NotImplementedError("Proposal skeleton only.")


def partial_trace_input(choi: np.ndarray, d_in: int, d_out: int) -> Array:
    """Trace the input tensor factor of an input-first Choi matrix."""
    raise NotImplementedError("Proposal skeleton only.")


def is_cp(choi: np.ndarray, tol: float = 1e-9, require_hermitian: bool = True) -> bool:
    """Return whether ``choi`` is positive semidefinite within ``tol``."""
    raise NotImplementedError("Proposal skeleton only.")


def is_tp(
    choi: np.ndarray,
    d_in: int,
    d_out: int | None = None,
    tol: float = 1e-9,
) -> bool:
    """Return whether ``Tr_B(C_E) = I_A`` within ``tol``."""
    raise NotImplementedError("Proposal skeleton only.")


def is_unital(
    choi: np.ndarray,
    d_in: int,
    d_out: int | None = None,
    tol: float = 1e-9,
) -> bool:
    """Return whether a square channel satisfies ``E(I) = I`` within ``tol``."""
    raise NotImplementedError("Proposal skeleton only.")


def choi_rank(choi: np.ndarray, tol: float = 1e-10) -> int:
    """Return the numerical rank of a Choi matrix."""
    raise NotImplementedError("Proposal skeleton only.")


def tp_residual(choi: np.ndarray, d_in: int, d_out: int | None = None) -> float:
    """Return ``||Tr_B(C_E) - I_A||_F`` for a Choi matrix."""
    raise NotImplementedError("Proposal skeleton only.")

