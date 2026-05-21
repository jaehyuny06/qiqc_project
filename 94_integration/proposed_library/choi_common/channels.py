"""Standard quantum-channel constructors for the proposed shared library."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Literal

import numpy as np
from numpy.typing import NDArray


Array = NDArray[np.complex128]
DepolarizingConvention = Literal["replacement", "pauli_error"]


def pauli_matrices() -> dict[str, Array]:
    """Return one-qubit Pauli matrices labeled ``I``, ``X``, ``Y``, and ``Z``."""
    raise NotImplementedError("Proposal skeleton only.")


def identity_channel(d: int = 2) -> list[Array]:
    """Return Kraus operators for the ``d``-dimensional identity channel."""
    raise NotImplementedError("Proposal skeleton only.")


def identity_channel_choi(d: int = 2) -> Array:
    """Return the Choi matrix of the ``d``-dimensional identity channel."""
    raise NotImplementedError("Proposal skeleton only.")


def unitary_channel_choi(unitary: np.ndarray, check_unitary: bool = True) -> Array:
    """Return the Choi matrix of ``rho -> U rho U^dagger``."""
    raise NotImplementedError("Proposal skeleton only.")


def pauli_channel(px: float, py: float, pz: float) -> list[Array]:
    """Return Kraus operators for a one-qubit Pauli channel."""
    raise NotImplementedError("Proposal skeleton only.")


def pauli_channel_choi(probabilities: Mapping[str, float]) -> Array:
    """Return the Choi matrix of a one-qubit Pauli channel."""
    raise NotImplementedError("Proposal skeleton only.")


def bit_flip_channel(p: float) -> list[Array]:
    """Return Kraus operators for the one-qubit bit-flip channel."""
    raise NotImplementedError("Proposal skeleton only.")


def bit_flip_channel_choi(p: float) -> Array:
    """Return the Choi matrix of the one-qubit bit-flip channel."""
    raise NotImplementedError("Proposal skeleton only.")


def phase_flip_channel(p: float) -> list[Array]:
    """Return Kraus operators for the one-qubit phase-flip channel."""
    raise NotImplementedError("Proposal skeleton only.")


def phase_flip_channel_choi(p: float) -> Array:
    """Return the Choi matrix of the one-qubit phase-flip channel."""
    raise NotImplementedError("Proposal skeleton only.")


def depolarizing_channel(
    p: float,
    d: int = 2,
    convention: DepolarizingConvention = "replacement",
) -> list[Array]:
    """Return Kraus operators for a depolarizing channel under an explicit convention."""
    raise NotImplementedError("Proposal skeleton only.")


def depolarizing_channel_choi(
    p: float,
    d: int = 2,
    convention: DepolarizingConvention = "replacement",
) -> Array:
    """Return the Choi matrix of a depolarizing channel under an explicit convention."""
    raise NotImplementedError("Proposal skeleton only.")


def amplitude_damping_channel(gamma: float) -> list[Array]:
    """Return Kraus operators for the one-qubit amplitude-damping channel."""
    raise NotImplementedError("Proposal skeleton only.")


def amplitude_damping_channel_choi(gamma: float) -> Array:
    """Return the Choi matrix of the one-qubit amplitude-damping channel."""
    raise NotImplementedError("Proposal skeleton only.")


def phase_damping_channel(gamma: float) -> list[Array]:
    """Return Kraus operators for the one-qubit phase-damping channel."""
    raise NotImplementedError("Proposal skeleton only.")


def phase_damping_channel_choi(gamma: float) -> Array:
    """Return the Choi matrix of the one-qubit phase-damping channel."""
    raise NotImplementedError("Proposal skeleton only.")


def z_rotation_channel_choi(theta: float) -> Array:
    """Return the Choi matrix of a one-qubit coherent Z-rotation channel."""
    raise NotImplementedError("Proposal skeleton only.")


def unital_qubit_channel_choi(lambda_x: float, lambda_y: float, lambda_z: float) -> Array:
    """Return a Pauli-diagonal unital qubit map from Bloch-axis scaling factors."""
    raise NotImplementedError("Proposal skeleton only.")


def mixed_choi(choi_a: np.ndarray, choi_b: np.ndarray, alpha: float) -> Array:
    """Return the convex mixture ``(1-alpha) * choi_a + alpha * choi_b``."""
    raise NotImplementedError("Proposal skeleton only.")


def depolarizing_after_unitary(
    unitary: np.ndarray,
    p: float,
    convention: DepolarizingConvention = "pauli_error",
) -> Array:
    """Return a Choi matrix for a unitary followed by depolarizing noise."""
    raise NotImplementedError("Proposal skeleton only.")


def amplitude_damping_after_unitary(unitary: np.ndarray, gamma: float) -> Array:
    """Return a Choi matrix for a unitary followed by amplitude damping."""
    raise NotImplementedError("Proposal skeleton only.")


def two_qubit_depolarizing_after_unitary(
    unitary: np.ndarray,
    p: float,
    convention: Literal["pauli_error"] = "pauli_error",
) -> Array:
    """Return a Choi matrix for a two-qubit unitary followed by global depolarizing noise."""
    raise NotImplementedError("Proposal skeleton only.")

