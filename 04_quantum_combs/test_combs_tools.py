"""Tests for Agent-4 comb and non-Markovianity utilities."""

from __future__ import annotations

import numpy as np

from combs_tools import (
    blp_measure,
    comb_partial_trace_check,
    construct_process_tensor,
    dagger,
    is_markovian,
    kraus_to_choi,
    marginal_channel,
    partial_trace,
    rhp_measure,
)
from non_markovian_dynamics import (
    I2,
    collision_model_comb,
    markovian_dephasing_family,
    memoryless_product_comb,
    oscillatory_dephasing_family,
)


def test_partial_trace_bell_state_is_maximally_mixed() -> None:
    """Tracing one half of a Bell state gives I/2."""

    bell = np.array([1, 0, 0, 1], dtype=complex) / np.sqrt(2)
    rho = np.outer(bell, bell.conj())
    reduced = partial_trace(rho, [2, 2], [1])
    np.testing.assert_allclose(reduced, 0.5 * I2, atol=1e-12)


def test_kraus_to_choi_identity_is_cp_and_tp() -> None:
    """The identity channel Choi matrix is positive and trace preserving."""

    choi = kraus_to_choi([I2])
    eigs = np.linalg.eigvalsh(0.5 * (choi + dagger(choi)))
    assert eigs.min() >= -1e-12
    traced_output = partial_trace(choi, [2, 2], [1])
    np.testing.assert_allclose(traced_output, I2, atol=1e-12)


def test_construct_process_tensor_identity_collisions_is_markovian() -> None:
    """Two identity collisions produce a product comb."""

    env_init = np.array([[1, 0], [0, 0]], dtype=complex)
    comb = construct_process_tensor([np.eye(4), np.eye(4)], env_init, n_steps=2)
    assert comb.shape == (16, 16)
    assert comb_partial_trace_check(comb, [2, 2, 2, 2])
    assert is_markovian(comb, n_steps=2)

    marginal = marginal_channel(comb, 0)
    np.testing.assert_allclose(marginal, kraus_to_choi([I2]), atol=1e-12)


def test_collision_comb_has_memory_correlations() -> None:
    """A reused environment generates a non-factorizing two-use comb."""

    comb = collision_model_comb(theta=0.72, n_steps=2)
    product = memoryless_product_comb(theta=0.72, n_steps=2)
    assert comb_partial_trace_check(comb, [2, 2, 2, 2])
    assert not is_markovian(comb, n_steps=2, tol=1e-3)
    assert np.linalg.norm(comb - product, ord="fro") > 1e-2


def test_blp_measure_distinguishes_revival_from_decay() -> None:
    """Exponential dephasing has no trace-distance revival; oscillatory dephasing does."""

    t_grid = np.linspace(0.0, 3.0, 90)
    markovian = blp_measure(markovian_dephasing_family(rate=0.4), t_grid)
    non_markovian = blp_measure(oscillatory_dephasing_family(rate=0.08, frequency=2.6), t_grid)

    assert markovian < 1e-8
    assert non_markovian > 0.25


def test_rhp_measure_detects_cp_divisibility_violation() -> None:
    """The RHP-style witness vanishes for CP-divisible decay and grows for revivals."""

    t_grid = np.linspace(0.0, 2.7, 80)
    markovian = rhp_measure(markovian_dephasing_family(rate=0.35), t_grid)
    non_markovian = rhp_measure(oscillatory_dephasing_family(rate=0.08, frequency=2.3), t_grid)

    assert markovian < 1e-8
    assert non_markovian > 0.1
