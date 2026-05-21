"""Conversions among Kraus, Choi, Stinespring, and natural representations.

All Choi matrices use the unnormalized input-first convention
``C_E = sum_ij |i><j|_A tensor E(|i><j|)_B``. Kraus operators have shape
``(d_out, d_in)``.
"""

from __future__ import annotations

from collections.abc import Sequence

import numpy as np
from numpy.typing import NDArray


Array = NDArray[np.complex128]


def kraus_to_choi(kraus_ops: Sequence[np.ndarray]) -> Array:
    """Convert Kraus operators with shape ``(d_out, d_in)`` to a Choi matrix."""
    raise NotImplementedError("Proposal skeleton only.")


def choi_to_kraus(
    choi: np.ndarray,
    tol: float = 1e-10,
    d_in: int | None = None,
    d_out: int | None = None,
) -> list[Array]:
    """Recover Kraus operators from a positive Choi matrix by eigendecomposition."""
    raise NotImplementedError("Proposal skeleton only.")


def kraus_to_stinespring(kraus_ops: Sequence[np.ndarray]) -> Array:
    """Construct a Stinespring isometry by stacking Kraus operators."""
    raise NotImplementedError("Proposal skeleton only.")


def stinespring_to_kraus(isometry: np.ndarray, env_dim: int) -> list[Array]:
    """Slice a Stinespring isometry into ``env_dim`` Kraus operators."""
    raise NotImplementedError("Proposal skeleton only.")


def choi_to_natural(
    choi: np.ndarray,
    d_in: int | None = None,
    d_out: int | None = None,
) -> Array:
    """Convert a Choi matrix to the natural representation using column stacking."""
    raise NotImplementedError("Proposal skeleton only.")


def natural_to_choi(
    natural: np.ndarray,
    d_in: int | None = None,
    d_out: int | None = None,
) -> Array:
    """Convert a natural representation matrix to an input-first Choi matrix."""
    raise NotImplementedError("Proposal skeleton only.")


def apply_kraus_channel(rho: np.ndarray, kraus_ops: Sequence[np.ndarray]) -> Array:
    """Apply a Kraus-represented channel to an input operator ``rho``."""
    raise NotImplementedError("Proposal skeleton only.")


def apply_choi_channel(
    choi: np.ndarray,
    rho: np.ndarray,
    d_in: int | None = None,
    d_out: int | None = None,
) -> Array:
    """Apply a Choi-represented channel to ``rho`` using the project-standard API."""
    raise NotImplementedError("Proposal skeleton only.")


def compose_choi_channels(
    choi_after: np.ndarray,
    choi_before: np.ndarray,
    d_mid: int | None = None,
) -> Array:
    """Return the Choi matrix of ``choi_after`` composed after ``choi_before``."""
    raise NotImplementedError("Proposal skeleton only.")

