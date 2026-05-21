"""Visualization helpers for Choi matrices and qubit Bloch maps."""

from __future__ import annotations

from collections.abc import Sequence
from typing import Any

import numpy as np
from numpy.typing import NDArray


Array = NDArray[np.complex128]


def plot_choi_heatmap(
    choi: np.ndarray,
    *,
    title: str | None = None,
    axes: Sequence[Any] | None = None,
    include_abs: bool = True,
) -> Any:
    """Plot real, imaginary, and optionally magnitude Choi heatmaps."""
    raise NotImplementedError("Proposal skeleton only.")


def bloch_affine_map(choi: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """Return the qubit affine Bloch map ``r -> M r + t`` for a Choi matrix."""
    raise NotImplementedError("Proposal skeleton only.")


def choi_to_pauli_transfer(choi: np.ndarray) -> Array:
    """Return the one-qubit Pauli transfer matrix for a Choi matrix."""
    raise NotImplementedError("Proposal skeleton only.")


def plot_bloch_deformation(choi: np.ndarray, ax: Any | None = None) -> Any:
    """Plot the image of the Bloch sphere under a one-qubit channel."""
    raise NotImplementedError("Proposal skeleton only.")


def plot_eigenspectrum(choi: np.ndarray, ax: Any | None = None, tol: float = 1e-9) -> Any:
    """Plot the eigenvalues of the Hermitian part of a Choi matrix."""
    raise NotImplementedError("Proposal skeleton only.")


def extract_kraus_display(choi: np.ndarray, tol: float = 1e-10) -> list[tuple[float, Array]]:
    """Return Choi eigenweights and eigenoperators for diagnostic display."""
    raise NotImplementedError("Proposal skeleton only.")
