"""Low-level helpers for Choi-common modules.

The implementation phase should keep this module free of plotting, solver, and
notebook dependencies.
"""

from __future__ import annotations

from typing import Any

import numpy as np
from numpy.typing import NDArray


Array = NDArray[np.complex128]


def as_complex_matrix(matrix: Any, name: str = "matrix", square: bool = False) -> Array:
    """Return a two-dimensional complex array, optionally requiring it to be square."""
    raise NotImplementedError("Proposal skeleton only.")


def dagger(matrix: np.ndarray) -> Array:
    """Return the conjugate transpose of ``matrix``."""
    raise NotImplementedError("Proposal skeleton only.")


def hermitian_part(matrix: np.ndarray) -> Array:
    """Return ``(matrix + matrix.conj().T) / 2`` as a complex array."""
    raise NotImplementedError("Proposal skeleton only.")


def validate_probability(value: float, name: str = "p") -> float:
    """Validate that ``value`` is in ``[0, 1]`` and return it as ``float``."""
    raise NotImplementedError("Proposal skeleton only.")


def infer_choi_dims(
    choi: np.ndarray,
    d_in: int | None = None,
    d_out: int | None = None,
    tol: float = 1e-8,
) -> tuple[int, int]:
    """Infer ``(d_in, d_out)`` for an input-first unnormalized Choi matrix."""
    raise NotImplementedError("Proposal skeleton only.")


def infer_natural_dims(
    natural: np.ndarray,
    d_in: int | None = None,
    d_out: int | None = None,
) -> tuple[int, int]:
    """Infer ``(d_in, d_out)`` for a natural representation matrix."""
    raise NotImplementedError("Proposal skeleton only.")

