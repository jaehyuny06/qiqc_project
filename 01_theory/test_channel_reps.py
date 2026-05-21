"""Unit tests for Agent-1 channel representation utilities."""

from __future__ import annotations

import numpy as np
import pytest

from channel_reps import (
    amplitude_damping_channel,
    apply_channel,
    bit_flip_channel,
    choi_rank,
    choi_to_kraus,
    choi_to_natural,
    compose_channels_choi,
    depolarizing_channel,
    identity_channel,
    is_cp,
    is_tp,
    is_unital,
    kraus_to_choi,
    kraus_to_stinespring,
    natural_to_choi,
    pauli_channel,
    phase_damping_channel,
    phase_flip_channel,
    random_channel,
    stinespring_to_kraus,
)


def assert_channel_outputs_close(kraus_a: list[np.ndarray], kraus_b: list[np.ndarray], d_in: int) -> None:
    """Compare two channels on a deterministic operator basis."""
    for i in range(d_in):
        for j in range(d_in):
            basis = np.zeros((d_in, d_in), dtype=complex)
            basis[i, j] = 1
            np.testing.assert_allclose(
                apply_channel(basis, kraus_a),
                apply_channel(basis, kraus_b),
                atol=1e-10,
            )


def test_identity_choi_matches_maximally_entangled_projector() -> None:
    kraus = identity_channel(2)
    choi = kraus_to_choi(kraus)
    omega = np.array([1, 0, 0, 1], dtype=complex)
    expected = np.outer(omega, omega.conj())
    np.testing.assert_allclose(choi, expected, atol=1e-12)


def test_standard_channels_are_cp_and_tp() -> None:
    channels = [
        bit_flip_channel(0.2),
        phase_flip_channel(0.3),
        pauli_channel(0.1, 0.2, 0.15),
        depolarizing_channel(0.4),
        amplitude_damping_channel(0.25),
        phase_damping_channel(0.5),
    ]
    for kraus in channels:
        choi = kraus_to_choi(kraus)
        assert is_cp(choi)
        assert is_tp(choi, d_in=2)


def test_amplitude_damping_maps_excited_state_downward() -> None:
    rho_one = np.array([[0, 0], [0, 1]], dtype=complex)
    out = apply_channel(rho_one, amplitude_damping_channel(0.3))
    expected = np.array([[0.3, 0], [0, 0.7]], dtype=complex)
    np.testing.assert_allclose(out, expected, atol=1e-12)


def test_phase_damping_reduces_coherence() -> None:
    rho = np.array([[0.5, 0.5], [0.5, 0.5]], dtype=complex)
    out = apply_channel(rho, phase_damping_channel(0.25))
    expected = np.array([[0.5, 0.375], [0.375, 0.5]], dtype=complex)
    np.testing.assert_allclose(out, expected, atol=1e-12)


def test_choi_to_kraus_round_trip_preserves_channel() -> None:
    np.random.seed(42)
    kraus = random_channel(2, 2, 3)
    recovered = choi_to_kraus(kraus_to_choi(kraus))
    assert_channel_outputs_close(kraus, recovered, d_in=2)


def test_stinespring_round_trip_preserves_kraus_blocks() -> None:
    kraus = amplitude_damping_channel(0.4)
    isometry = kraus_to_stinespring(kraus)
    recovered = stinespring_to_kraus(isometry, env_dim=2)
    for actual, expected in zip(recovered, kraus):
        np.testing.assert_allclose(actual, expected, atol=1e-12)


def test_natural_round_trip_square_channel() -> None:
    choi = kraus_to_choi(depolarizing_channel(0.3))
    natural = choi_to_natural(choi)
    recovered = natural_to_choi(natural)
    np.testing.assert_allclose(recovered, choi, atol=1e-12)


def test_natural_round_trip_non_square_channel() -> None:
    np.random.seed(42)
    kraus = random_channel(d_in=2, d_out=3, n_kraus=2)
    choi = kraus_to_choi(kraus)
    natural = choi_to_natural(choi)
    assert natural.shape == (9, 4)
    recovered = natural_to_choi(natural)
    np.testing.assert_allclose(recovered, choi, atol=1e-12)


def test_compose_bit_flip_channels_has_expected_probability() -> None:
    p = 0.2
    q = 0.3
    composed = compose_channels_choi(kraus_to_choi(bit_flip_channel(p)), kraus_to_choi(bit_flip_channel(q)))
    expected_probability = p + q - 2 * p * q
    expected = kraus_to_choi(bit_flip_channel(expected_probability))
    np.testing.assert_allclose(composed, expected, atol=1e-12)


def test_random_channel_is_trace_preserving() -> None:
    np.random.seed(7)
    kraus = random_channel(d_in=3, d_out=2, n_kraus=2)
    accumulator = sum(op.conj().T @ op for op in kraus)
    np.testing.assert_allclose(accumulator, np.eye(3), atol=1e-12)
    assert is_tp(kraus_to_choi(kraus), d_in=3)


def test_random_channel_rejects_impossible_dimensions() -> None:
    with pytest.raises(ValueError, match="n_kraus"):
        random_channel(d_in=4, d_out=1, n_kraus=2)


def test_cp_rejects_negative_choi_eigenvalue() -> None:
    bad = kraus_to_choi(identity_channel(2)).copy()
    bad[0, 0] = -0.1
    assert not is_cp(bad)


def test_tp_rejects_trace_decreasing_map() -> None:
    kraus = [np.sqrt(0.5) * np.eye(2, dtype=complex)]
    assert not is_tp(kraus_to_choi(kraus), d_in=2)


def test_choi_rank_equals_minimal_kraus_count_for_standard_examples() -> None:
    assert choi_rank(kraus_to_choi(identity_channel(2))) == 1
    assert choi_rank(kraus_to_choi(amplitude_damping_channel(0.4))) == 2
    assert choi_rank(kraus_to_choi(depolarizing_channel(0.5))) == 4


def test_unitality_identifies_unital_and_nonunital_channels() -> None:
    assert is_unital(kraus_to_choi(depolarizing_channel(0.4)), d_out=2)
    assert not is_unital(kraus_to_choi(amplitude_damping_channel(0.4)), d_out=2)


def test_invalid_kraus_shapes_raise() -> None:
    with pytest.raises(ValueError, match="same shape"):
        kraus_to_choi([np.eye(2), np.eye(3)])

