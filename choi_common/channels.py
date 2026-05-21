"""Standard quantum-channel constructors."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Literal

import numpy as np
from numpy.typing import NDArray

from .representations import kraus_to_choi
from .utils import as_complex_matrix, hermitian_part, validate_probability


Array = NDArray[np.complex128]
DepolarizingConvention = Literal["replacement", "pauli_error"]


def pauli_matrices() -> dict[str, Array]:
    """Return one-qubit Pauli matrices labeled ``I``, ``X``, ``Y``, and ``Z``."""
    return {
        "I": np.array([[1, 0], [0, 1]], dtype=np.complex128),
        "X": np.array([[0, 1], [1, 0]], dtype=np.complex128),
        "Y": np.array([[0, -1j], [1j, 0]], dtype=np.complex128),
        "Z": np.array([[1, 0], [0, -1]], dtype=np.complex128),
    }


def identity_channel(d: int = 2) -> list[Array]:
    """Return Kraus operators for the ``d``-dimensional identity channel."""
    if d <= 0:
        raise ValueError("d must be positive.")
    return [np.eye(d, dtype=np.complex128)]


def identity_channel_choi(d: int = 2) -> Array:
    """Return the Choi matrix of the ``d``-dimensional identity channel."""
    return kraus_to_choi(identity_channel(d))


def unitary_channel_choi(unitary: np.ndarray, check_unitary: bool = True) -> Array:
    """Return the Choi matrix of ``rho -> U rho U^dagger``."""
    u = as_complex_matrix(unitary, "unitary", square=True)
    if check_unitary and not np.allclose(u.conj().T @ u, np.eye(u.shape[0]), atol=1e-9):
        raise ValueError("unitary must be unitary.")
    return kraus_to_choi([u])


def pauli_channel(px: float, py: float, pz: float) -> list[Array]:
    """Return Kraus operators for a one-qubit Pauli channel.

    The probabilities are for applying ``X``, ``Y``, and ``Z``. The identity
    probability is ``1 - px - py - pz``.
    """
    px = validate_probability(px, "px")
    py = validate_probability(py, "py")
    pz = validate_probability(pz, "pz")
    p_identity = 1.0 - px - py - pz
    if p_identity < -1e-12:
        raise ValueError("p_x + p_y + p_z must be at most 1.")
    p_identity = max(0.0, p_identity)
    paulis = pauli_matrices()
    return [
        np.sqrt(p_identity) * paulis["I"],
        np.sqrt(px) * paulis["X"],
        np.sqrt(py) * paulis["Y"],
        np.sqrt(pz) * paulis["Z"],
    ]


def pauli_channel_choi(probabilities: Mapping[str, float]) -> Array:
    """Return the Choi matrix of a one-qubit Pauli channel."""
    paulis = pauli_matrices()
    probs = {label: float(probabilities.get(label, 0.0)) for label in paulis}
    if any(value < -1e-12 for value in probs.values()):
        raise ValueError("Pauli probabilities must be nonnegative.")
    total = sum(probs.values())
    if not np.isclose(total, 1.0, atol=1e-10):
        raise ValueError(f"Pauli probabilities must sum to 1; got {total}.")
    kraus_ops = [np.sqrt(max(probs[label], 0.0)) * paulis[label] for label in ("I", "X", "Y", "Z")]
    return kraus_to_choi(kraus_ops)


def bit_flip_channel(p: float) -> list[Array]:
    """Return Kraus operators for the one-qubit bit-flip channel."""
    p = validate_probability(p, "p")
    paulis = pauli_matrices()
    return [np.sqrt(1.0 - p) * paulis["I"], np.sqrt(p) * paulis["X"]]


def bit_flip_channel_choi(p: float) -> Array:
    """Return the Choi matrix of the one-qubit bit-flip channel."""
    return kraus_to_choi(bit_flip_channel(p))


def phase_flip_channel(p: float) -> list[Array]:
    """Return Kraus operators for the one-qubit phase-flip channel."""
    p = validate_probability(p, "p")
    paulis = pauli_matrices()
    return [np.sqrt(1.0 - p) * paulis["I"], np.sqrt(p) * paulis["Z"]]


def phase_flip_channel_choi(p: float) -> Array:
    """Return the Choi matrix of the one-qubit phase-flip channel."""
    return kraus_to_choi(phase_flip_channel(p))


def depolarizing_channel(
    p: float,
    d: int = 2,
    convention: DepolarizingConvention = "replacement",
) -> list[Array]:
    """Return Kraus operators for a depolarizing channel.

    Parameters
    ----------
    p:
        Depolarizing strength.
    d:
        Hilbert-space dimension.
    convention:
        ``"replacement"`` implements ``(1-p)rho + p Tr(rho) I/d``.
        ``"pauli_error"`` is the qubit convention with total non-identity
        Pauli-error probability ``p``.
    """
    p = validate_probability(p, "p")
    if d <= 0:
        raise ValueError("d must be positive.")
    if convention == "pauli_error":
        if d != 2:
            raise ValueError("pauli_error convention is implemented only for qubits.")
        paulis = pauli_matrices()
        return [np.sqrt(1.0 - p) * paulis["I"]] + [
            np.sqrt(p / 3.0) * paulis[label] for label in ("X", "Y", "Z")
        ]
    if convention != "replacement":
        raise ValueError("convention must be 'replacement' or 'pauli_error'.")

    if d == 2:
        return pauli_channel(p / 4.0, p / 4.0, p / 4.0)

    kraus_ops: list[Array] = [np.sqrt(1.0 - p) * np.eye(d, dtype=np.complex128)]
    scale = np.sqrt(p / d)
    for row in range(d):
        for col in range(d):
            op = np.zeros((d, d), dtype=np.complex128)
            op[row, col] = scale
            kraus_ops.append(op)
    return kraus_ops


def depolarizing_channel_choi(
    p: float,
    d: int = 2,
    convention: DepolarizingConvention = "replacement",
) -> Array:
    """Return the Choi matrix of a depolarizing channel."""
    if convention == "replacement" and d > 2:
        p = validate_probability(p, "p")
        identity_choi = identity_channel_choi(d)
        completely_mixed = np.kron(np.eye(d, dtype=np.complex128), np.eye(d, dtype=np.complex128) / d)
        return hermitian_part((1.0 - p) * identity_choi + p * completely_mixed)
    return kraus_to_choi(depolarizing_channel(p, d=d, convention=convention))


def amplitude_damping_channel(gamma: float) -> list[Array]:
    """Return Kraus operators for the one-qubit amplitude-damping channel."""
    gamma = validate_probability(gamma, "gamma")
    return [
        np.array([[1.0, 0.0], [0.0, np.sqrt(1.0 - gamma)]], dtype=np.complex128),
        np.array([[0.0, np.sqrt(gamma)], [0.0, 0.0]], dtype=np.complex128),
    ]


def amplitude_damping_channel_choi(gamma: float) -> Array:
    """Return the Choi matrix of the one-qubit amplitude-damping channel."""
    return kraus_to_choi(amplitude_damping_channel(gamma))


def phase_damping_channel(gamma: float) -> list[Array]:
    """Return Kraus operators for the one-qubit phase-damping channel."""
    gamma = validate_probability(gamma, "gamma")
    p0 = np.array([[1.0, 0.0], [0.0, 0.0]], dtype=np.complex128)
    p1 = np.array([[0.0, 0.0], [0.0, 1.0]], dtype=np.complex128)
    return [np.sqrt(1.0 - gamma) * np.eye(2, dtype=np.complex128), np.sqrt(gamma) * p0, np.sqrt(gamma) * p1]


def phase_damping_channel_choi(gamma: float) -> Array:
    """Return the Choi matrix of the one-qubit phase-damping channel."""
    return kraus_to_choi(phase_damping_channel(gamma))


def z_rotation_channel_choi(theta: float) -> Array:
    """Return the Choi matrix of a one-qubit coherent Z-rotation channel."""
    unitary = np.array(
        [[np.exp(-0.5j * theta), 0.0], [0.0, np.exp(0.5j * theta)]],
        dtype=np.complex128,
    )
    return unitary_channel_choi(unitary)


def unital_qubit_channel_choi(lambda_x: float, lambda_y: float, lambda_z: float) -> Array:
    """Return a Pauli-diagonal unital qubit map from Bloch-axis scaling factors.

    Scaling factors outside the CP tetrahedron intentionally produce non-CP
    maps, which is useful for diagnostics and visualization.
    """
    lambdas = np.array([lambda_x, lambda_y, lambda_z], dtype=float)
    probabilities = np.array(
        [
            (1.0 + lambdas[0] + lambdas[1] + lambdas[2]) / 4.0,
            (1.0 + lambdas[0] - lambdas[1] - lambdas[2]) / 4.0,
            (1.0 - lambdas[0] + lambdas[1] - lambdas[2]) / 4.0,
            (1.0 - lambdas[0] - lambdas[1] + lambdas[2]) / 4.0,
        ],
        dtype=float,
    )
    paulis = pauli_matrices()
    choi = np.zeros((4, 4), dtype=np.complex128)
    for coeff, op in zip(probabilities, (paulis["I"], paulis["X"], paulis["Y"], paulis["Z"]), strict=True):
        vector = op.T.reshape(4)
        choi += coeff * np.outer(vector, vector.conj())
    return hermitian_part(choi)


def mixed_choi(choi_a: np.ndarray, choi_b: np.ndarray, alpha: float) -> Array:
    """Return the convex mixture ``(1-alpha) * choi_a + alpha * choi_b``."""
    alpha = validate_probability(alpha, "alpha")
    arr_a = np.asarray(choi_a, dtype=np.complex128)
    arr_b = np.asarray(choi_b, dtype=np.complex128)
    if arr_a.shape != arr_b.shape:
        raise ValueError("Choi matrices must have matching shapes.")
    return (1.0 - alpha) * arr_a + alpha * arr_b


def depolarizing_after_unitary(
    unitary: np.ndarray,
    p: float,
    convention: DepolarizingConvention = "pauli_error",
) -> Array:
    """Return a Choi matrix for a unitary followed by one-qubit depolarizing noise."""
    u = as_complex_matrix(unitary, "unitary", square=True)
    if u.shape != (2, 2):
        raise ValueError("depolarizing helper is implemented for one-qubit gates.")
    if convention == "pauli_error":
        p = validate_probability(p, "p")
        paulis = pauli_matrices()
        kraus = [np.sqrt(1.0 - p) * u]
        kraus.extend(np.sqrt(p / 3.0) * paulis[label] @ u for label in ("X", "Y", "Z"))
        return kraus_to_choi(kraus)
    return kraus_to_choi([op @ u for op in depolarizing_channel(p, d=2, convention=convention)])


def amplitude_damping_after_unitary(unitary: np.ndarray, gamma: float) -> Array:
    """Return a Choi matrix for a unitary followed by amplitude damping."""
    u = as_complex_matrix(unitary, "unitary", square=True)
    if u.shape != (2, 2):
        raise ValueError("amplitude damping helper is implemented for one-qubit gates.")
    return kraus_to_choi([op @ u for op in amplitude_damping_channel(gamma)])


def two_qubit_depolarizing_after_unitary(
    unitary: np.ndarray,
    p: float,
    convention: Literal["pauli_error"] = "pauli_error",
) -> Array:
    """Return a Choi matrix for a two-qubit unitary followed by global depolarizing noise."""
    if convention != "pauli_error":
        raise ValueError("Only pauli_error convention is supported for this helper.")
    u = as_complex_matrix(unitary, "unitary", square=True)
    if u.shape != (4, 4):
        raise ValueError("two_qubit_depolarizing_after_unitary expects a 4x4 unitary.")
    p = validate_probability(p, "p")
    paulis = pauli_matrices()
    one_qubit_paulis = [paulis[label] for label in ("I", "X", "Y", "Z")]
    two_qubit_paulis = [np.kron(a, b) for a in one_qubit_paulis for b in one_qubit_paulis]
    kraus = [np.sqrt(1.0 - p) * u]
    kraus.extend(np.sqrt(p / 15.0) * op @ u for op in two_qubit_paulis[1:])
    return kraus_to_choi(kraus)
