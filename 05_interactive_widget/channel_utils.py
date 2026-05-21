"""Local qubit channel utilities for the Agent-5 interactive widget.

The Choi convention used here is

    C_E = sum_ij |i><j| tensor E(|i><j|)

with the input system as the first tensor factor.  The Choi matrices are
unnormalized, so a trace-preserving qubit channel has ``trace(C) = 2``.
"""

from __future__ import annotations

from collections.abc import Sequence

import numpy as np


Array = np.ndarray

I2: Array = np.array([[1, 0], [0, 1]], dtype=complex)
X: Array = np.array([[0, 1], [1, 0]], dtype=complex)
Y: Array = np.array([[0, -1j], [1j, 0]], dtype=complex)
Z: Array = np.array([[1, 0], [0, -1]], dtype=complex)
PAULIS: tuple[Array, Array, Array] = (X, Y, Z)


def validate_probability(value: float, name: str) -> float:
    """Validate a scalar probability.

    Parameters
    ----------
    value:
        Candidate probability.
    name:
        Parameter name used in the error message.

    Returns
    -------
    float
        The validated probability.

    Raises
    ------
    ValueError
        If ``value`` is not in the interval ``[0, 1]``.
    """
    value = float(value)
    if not 0.0 <= value <= 1.0:
        raise ValueError(f"{name} must be in [0, 1], got {value!r}.")
    return value


def kraus_to_choi(kraus_ops: Sequence[Array]) -> Array:
    """Convert Kraus operators to an unnormalized Choi matrix.

    Parameters
    ----------
    kraus_ops:
        Sequence of Kraus operators with shape ``(d_out, d_in)``.

    Returns
    -------
    numpy.ndarray
        Choi matrix with shape ``(d_in * d_out, d_in * d_out)``.
    """
    if not kraus_ops:
        raise ValueError("At least one Kraus operator is required.")
    d_out, d_in = kraus_ops[0].shape
    choi = np.zeros((d_in * d_out, d_in * d_out), dtype=complex)
    for op in kraus_ops:
        op = np.asarray(op, dtype=complex)
        if op.shape != (d_out, d_in):
            raise ValueError("All Kraus operators must have the same shape.")
        for i in range(d_in):
            for j in range(d_in):
                block = np.outer(op[:, i], op[:, j].conj())
                row = slice(i * d_out, (i + 1) * d_out)
                col = slice(j * d_out, (j + 1) * d_out)
                choi[row, col] += block
    return 0.5 * (choi + choi.conj().T)


def choi_to_kraus(choi: Array, tol: float = 1e-10) -> list[Array]:
    """Extract Kraus operators from a positive semidefinite Choi matrix.

    Parameters
    ----------
    choi:
        Choi matrix in the local input-first convention.
    tol:
        Eigenvalue threshold below which terms are discarded.

    Returns
    -------
    list[numpy.ndarray]
        Kraus operators sorted by descending Choi eigenvalue.
    """
    choi = np.asarray(choi, dtype=complex)
    d_in, d_out = infer_channel_dims(choi)
    eigvals, eigvecs = np.linalg.eigh(0.5 * (choi + choi.conj().T))
    order = np.argsort(eigvals)[::-1]
    kraus_ops: list[Array] = []
    for idx in order:
        eigval = float(np.real(eigvals[idx]))
        if eigval <= tol:
            continue
        vec = eigvecs[:, idx]
        kraus = np.sqrt(eigval) * vec.reshape(d_in, d_out).T
        kraus_ops.append(kraus)
    return kraus_ops


def apply_channel(rho: Array, kraus_ops: Sequence[Array]) -> Array:
    """Apply a Kraus-represented channel to a density matrix.

    Parameters
    ----------
    rho:
        Input density matrix.
    kraus_ops:
        Kraus representation of the channel.

    Returns
    -------
    numpy.ndarray
        Output density matrix.
    """
    rho = np.asarray(rho, dtype=complex)
    out_dim = kraus_ops[0].shape[0]
    output = np.zeros((out_dim, out_dim), dtype=complex)
    for op in kraus_ops:
        output += op @ rho @ op.conj().T
    return 0.5 * (output + output.conj().T)


def infer_channel_dims(choi: Array) -> tuple[int, int]:
    """Infer equal input/output dimensions from a square Choi matrix.

    Parameters
    ----------
    choi:
        Candidate Choi matrix.

    Returns
    -------
    tuple[int, int]
        ``(d_in, d_out)``.  The widget is intentionally qubit-oriented, but
        this helper works for square ``d x d`` channels.
    """
    choi = np.asarray(choi)
    if choi.ndim != 2 or choi.shape[0] != choi.shape[1]:
        raise ValueError("Choi matrix must be square.")
    dim = int(round(np.sqrt(choi.shape[0])))
    if dim * dim != choi.shape[0]:
        raise ValueError("Only square-input/output Choi matrices are supported.")
    return dim, dim


def partial_trace_output(choi: Array) -> Array:
    """Trace out the output tensor factor of a Choi matrix.

    Parameters
    ----------
    choi:
        Choi matrix using the input-first convention.

    Returns
    -------
    numpy.ndarray
        Matrix on the input system, equal to the identity for TP channels.
    """
    d_in, d_out = infer_channel_dims(choi)
    tensor = np.asarray(choi, dtype=complex).reshape(d_in, d_out, d_in, d_out)
    return np.einsum("ibjb->ij", tensor)


def is_cp(choi: Array, tol: float = 1e-9) -> bool:
    """Check complete positivity from Choi eigenvalues.

    Parameters
    ----------
    choi:
        Choi matrix.
    tol:
        Numerical tolerance.

    Returns
    -------
    bool
        ``True`` when the smallest Hermitian eigenvalue is at least ``-tol``.
    """
    hermitian = 0.5 * (choi + choi.conj().T)
    return bool(np.min(np.linalg.eigvalsh(hermitian)) >= -tol)


def is_tp(choi: Array, tol: float = 1e-9) -> bool:
    """Check trace preservation by tracing out the output system.

    Parameters
    ----------
    choi:
        Choi matrix.
    tol:
        Numerical tolerance.

    Returns
    -------
    bool
        ``True`` when ``Tr_out(C)`` is numerically the identity.
    """
    d_in, _ = infer_channel_dims(choi)
    return bool(np.linalg.norm(partial_trace_output(choi) - np.eye(d_in)) <= tol)


def identity_kraus() -> list[Array]:
    """Return Kraus operators for the identity channel.

    Returns
    -------
    list[numpy.ndarray]
        Single identity Kraus operator.
    """
    return [I2.copy()]


def depolarizing_kraus(p: float) -> list[Array]:
    """Return Kraus operators for the qubit depolarizing channel.

    Parameters
    ----------
    p:
        Probability of replacing the state by a uniformly random Pauli error.

    Returns
    -------
    list[numpy.ndarray]
        Kraus operators for ``(1-p) rho + p/3 sum_P P rho P``.
    """
    p = validate_probability(p, "p")
    return [np.sqrt(1.0 - p) * I2] + [np.sqrt(p / 3.0) * op for op in PAULIS]


def amplitude_damping_kraus(gamma: float) -> list[Array]:
    """Return Kraus operators for amplitude damping.

    Parameters
    ----------
    gamma:
        Excited-state decay probability.

    Returns
    -------
    list[numpy.ndarray]
        Two Kraus operators for amplitude damping.
    """
    gamma = validate_probability(gamma, "gamma")
    return [
        np.array([[1.0, 0.0], [0.0, np.sqrt(1.0 - gamma)]], dtype=complex),
        np.array([[0.0, np.sqrt(gamma)], [0.0, 0.0]], dtype=complex),
    ]


def phase_damping_kraus(gamma: float) -> list[Array]:
    """Return Kraus operators for phase damping.

    Parameters
    ----------
    gamma:
        Dephasing strength.  Off-diagonal density-matrix entries are scaled by
        ``1 - gamma``.

    Returns
    -------
    list[numpy.ndarray]
        Three Kraus operators for pure dephasing.
    """
    gamma = validate_probability(gamma, "gamma")
    return [
        np.sqrt(1.0 - gamma) * I2,
        np.sqrt(gamma) * np.array([[1.0, 0.0], [0.0, 0.0]], dtype=complex),
        np.sqrt(gamma) * np.array([[0.0, 0.0], [0.0, 1.0]], dtype=complex),
    ]


def bit_flip_kraus(p: float) -> list[Array]:
    """Return Kraus operators for the bit-flip channel.

    Parameters
    ----------
    p:
        Bit-flip probability.

    Returns
    -------
    list[numpy.ndarray]
        Identity and Pauli-X Kraus operators.
    """
    p = validate_probability(p, "p")
    return [np.sqrt(1.0 - p) * I2, np.sqrt(p) * X]


def phase_flip_kraus(p: float) -> list[Array]:
    """Return Kraus operators for the phase-flip channel.

    Parameters
    ----------
    p:
        Phase-flip probability.

    Returns
    -------
    list[numpy.ndarray]
        Identity and Pauli-Z Kraus operators.
    """
    p = validate_probability(p, "p")
    return [np.sqrt(1.0 - p) * I2, np.sqrt(p) * Z]


def pauli_kraus(p_x: float, p_y: float, p_z: float) -> list[Array]:
    """Return Kraus operators for a general Pauli channel.

    Parameters
    ----------
    p_x, p_y, p_z:
        Probabilities for Pauli ``X``, ``Y``, and ``Z`` errors.  Their sum must
        be no larger than one.

    Returns
    -------
    list[numpy.ndarray]
        Kraus operators for the corresponding Pauli channel.
    """
    probs = np.array(
        [
            validate_probability(p_x, "p_x"),
            validate_probability(p_y, "p_y"),
            validate_probability(p_z, "p_z"),
        ],
        dtype=float,
    )
    if float(np.sum(probs)) > 1.0 + 1e-12:
        raise ValueError("p_x + p_y + p_z must be <= 1.")
    p_i = max(0.0, 1.0 - float(np.sum(probs)))
    return [np.sqrt(p_i) * I2] + [np.sqrt(prob) * op for prob, op in zip(probs, PAULIS)]


def unital_choi(lambda_x: float, lambda_y: float, lambda_z: float) -> Array:
    """Build a Pauli-diagonal unital qubit map from Bloch scaling factors.

    Parameters
    ----------
    lambda_x, lambda_y, lambda_z:
        Scaling factors applied to the Bloch vector axes.  Values outside the
        CP tetrahedron intentionally produce non-CP maps, which is useful for
        the widget's CP status indicator.

    Returns
    -------
    numpy.ndarray
        Choi matrix for the trace-preserving unital map.
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
    choi = np.zeros((4, 4), dtype=complex)
    for coeff, op in zip(probabilities, (I2, X, Y, Z)):
        vector = op.T.reshape(4)
        choi += coeff * np.outer(vector, vector.conj())
    return 0.5 * (choi + choi.conj().T)


def mixed_choi(choi_a: Array, choi_b: Array, alpha: float) -> Array:
    """Convexly mix two Choi matrices.

    Parameters
    ----------
    choi_a, choi_b:
        Choi matrices of the same shape.
    alpha:
        Mixing weight.  ``0`` returns ``choi_a`` and ``1`` returns ``choi_b``.

    Returns
    -------
    numpy.ndarray
        Convex mixture of the input matrices.
    """
    alpha = validate_probability(alpha, "alpha")
    if choi_a.shape != choi_b.shape:
        raise ValueError("Choi matrices must have matching shapes.")
    return (1.0 - alpha) * choi_a + alpha * choi_b
