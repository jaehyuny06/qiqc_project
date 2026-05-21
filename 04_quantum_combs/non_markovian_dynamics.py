"""Toy models for non-Markovian dynamics and quantum-comb demonstrations."""

from __future__ import annotations

from collections.abc import Callable

import numpy as np

from combs_tools import construct_process_tensor, kraus_to_choi, marginal_channel


Array = np.ndarray

I2 = np.eye(2, dtype=complex)
X = np.array([[0, 1], [1, 0]], dtype=complex)
Y = np.array([[0, -1j], [1j, 0]], dtype=complex)
Z = np.array([[1, 0], [0, -1]], dtype=complex)


def ket0() -> Array:
    """Return the computational basis vector ``|0>``."""

    return np.array([1.0, 0.0], dtype=complex)


def density(ket: Array) -> Array:
    """Return the rank-one density matrix ``|ket><ket|``."""

    vec = np.asarray(ket, dtype=complex)
    return np.outer(vec, vec.conj())


def pure_dephasing_choi(coherence: float) -> Array:
    """Return the Choi matrix of a qubit dephasing channel.

    Parameters
    ----------
    coherence
        Coherence multiplier ``g`` in ``rho_01 -> g rho_01``.  Complete
        positivity requires ``-1 <= g <= 1``.

    Returns
    -------
    np.ndarray
        Choi matrix of the Pauli dephasing channel.
    """

    g = float(np.clip(coherence, -1.0, 1.0))
    p_identity = (1.0 + g) / 2.0
    p_phase = (1.0 - g) / 2.0
    return kraus_to_choi([np.sqrt(p_identity) * I2, np.sqrt(p_phase) * Z])


def markovian_dephasing_family(rate: float = 0.35) -> Callable[[float], Array]:
    """Return a CP-divisible exponential dephasing channel family."""

    def family(time: float) -> Array:
        return pure_dephasing_choi(float(np.exp(-rate * time)))

    return family


def oscillatory_dephasing_family(rate: float = 0.12, frequency: float = 2.4) -> Callable[[float], Array]:
    """Return a dephasing family with coherence revivals.

    The multiplier ``g(t) = exp(-rate t) cos(frequency t)`` remains in
    ``[-1, 1]`` for all positive times, so each map from 0 to ``t`` is a
    valid channel.  Revivals in ``|g(t)|`` violate CP-divisibility.
    """

    def family(time: float) -> Array:
        g = float(np.exp(-rate * time) * np.cos(frequency * time))
        return pure_dephasing_choi(g)

    return family


def partial_swap_unitary(theta: float) -> Array:
    """Return a two-qubit partial-swap unitary for system-environment collisions."""

    swap = np.array(
        [
            [1, 0, 0, 0],
            [0, 0, 1, 0],
            [0, 1, 0, 0],
            [0, 0, 0, 1],
        ],
        dtype=complex,
    )
    return np.cos(theta) * np.eye(4, dtype=complex) - 1j * np.sin(theta) * swap


def controlled_phase_memory_unitary(theta: float) -> Array:
    """Return a two-qubit unitary that imprints phase information on memory."""

    phases = np.diag([1.0, np.exp(1j * theta), np.exp(-1j * theta), 1.0]).astype(complex)
    return phases


def collision_model_comb(theta: float = 0.7, n_steps: int = 2, env_state: Array | None = None) -> Array:
    """Build a qubit memory comb from repeated partial-swap collisions."""

    if env_state is None:
        env_state = density(ket0())
    unitary = partial_swap_unitary(theta)
    return construct_process_tensor([unitary for _ in range(n_steps)], env_state, n_steps)


def memoryless_product_comb(theta: float = 0.7, n_steps: int = 2, env_state: Array | None = None) -> Array:
    """Return the Markovian approximation built from all comb marginals."""

    comb = collision_model_comb(theta=theta, n_steps=n_steps, env_state=env_state)
    product = marginal_channel(comb, 0)
    for step in range(1, n_steps):
        product = np.kron(product, marginal_channel(comb, step))
    return product


def comb_correlation_norm(comb: Array, n_steps: int = 2) -> float:
    """Return the relative distance between a comb and its product marginals."""

    product = marginal_channel(comb, 0)
    for step in range(1, n_steps):
        product = np.kron(product, marginal_channel(comb, step))
    return float(np.linalg.norm(comb - product, ord="fro") / max(1.0, np.linalg.norm(comb, ord="fro")))


def choi_abs_matrix(choi: Array) -> Array:
    """Return ``abs(choi)`` as a real matrix for heatmap plotting."""

    return np.abs(np.asarray(choi, dtype=complex))
