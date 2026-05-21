"""Tests for Agent-3 SDP channel-discrimination tools."""

from __future__ import annotations

import numpy as np
import pytest

import sdp_tools as sdp


def test_standard_channel_choi_are_cp_and_tp() -> None:
    """Standard examples should produce physical Choi matrices."""

    channels = [
        sdp.identity_channel_choi(),
        sdp.bit_flip_channel_choi(0.2),
        sdp.phase_flip_channel_choi(0.3),
        sdp.depolarizing_channel_choi(0.4),
        sdp.amplitude_damping_channel_choi(0.25),
        sdp.phase_damping_channel_choi(0.35),
        sdp.z_rotation_channel_choi(0.17),
    ]
    for choi in channels:
        assert choi.shape == (4, 4)
        assert np.allclose(choi, choi.conj().T)
        assert sdp.is_cp(choi)
        assert sdp.is_tp(choi, d_in=2, d_out=2)


def test_same_channel_has_zero_diamond_norm_and_half_success_probability() -> None:
    """A channel cannot be distinguished from itself."""

    choi = sdp.depolarizing_channel_choi(0.2)
    assert sdp.diamond_norm_sdp(choi - choi, d_in=2, d_out=2) == pytest.approx(0.0, abs=2e-5)
    assert sdp.discrimination_probability(choi, choi) == pytest.approx(0.5, abs=2e-5)


def test_bit_flip_diamond_norm_matches_pauli_closed_form() -> None:
    """The SDP should agree with the Pauli-channel analytical formula."""

    p0 = 0.1
    p1 = 0.35
    choi_0 = sdp.bit_flip_channel_choi(p0)
    choi_1 = sdp.bit_flip_channel_choi(p1)
    expected = sdp.analytical_pauli_diamond_norm(
        {"I": 1.0 - p0, "X": p0}, {"I": 1.0 - p1, "X": p1}
    )
    actual = sdp.diamond_norm_sdp(choi_0 - choi_1, d_in=2, d_out=2)
    assert actual == pytest.approx(expected, abs=2e-3)


def test_depolarizing_diamond_norm_matches_closed_form() -> None:
    """The SDP should match the qubit depolarizing closed form."""

    p0 = 0.05
    p1 = 0.45
    choi_0 = sdp.depolarizing_channel_choi(p0)
    choi_1 = sdp.depolarizing_channel_choi(p1)
    expected = sdp.analytical_depolarizing_diamond_norm(p0, p1, d=2)
    actual = sdp.diamond_norm_sdp(choi_0 - choi_1, d_in=2, d_out=2)
    assert actual == pytest.approx(expected, abs=2e-3)
    assert sdp.discrimination_probability(choi_0, choi_1) == pytest.approx(
        0.5 + 0.25 * expected, abs=2e-3
    )


def test_entanglement_advantage_identity_vs_completely_depolarizing() -> None:
    """Ancilla-assisted discrimination should beat product inputs here."""

    identity = sdp.identity_channel_choi(2)
    depolarizing = sdp.depolarizing_channel_choi(1.0)

    entangled = sdp.discrimination_probability(identity, depolarizing)
    product = sdp.product_strategy_discrimination(identity, depolarizing)

    assert entangled == pytest.approx(0.875, abs=2e-3)
    assert product == pytest.approx(0.75, abs=2e-3)
    assert entangled > product + 0.1


def test_optimal_input_state_and_povm_are_valid() -> None:
    """Extracted SDP objects should be normalized positive operators."""

    choi_0 = sdp.depolarizing_channel_choi(0.1)
    choi_1 = sdp.depolarizing_channel_choi(0.4)

    rho = sdp.optimal_input_state(choi_0, choi_1)
    assert rho.shape == (2, 2)
    assert np.allclose(rho, rho.conj().T)
    assert np.trace(rho).real == pytest.approx(1.0, abs=1e-7)
    assert np.min(np.linalg.eigvalsh(rho)) >= -1e-7

    m0, m1 = sdp.optimal_povm(choi_0, choi_1)
    assert m0.shape == (4, 4)
    assert np.allclose(m0, m0.conj().T)
    assert np.allclose(m1, m1.conj().T)
    assert np.allclose(m0 + m1, np.eye(4), atol=1e-7)
    assert np.min(np.linalg.eigvalsh(m0)) >= -1e-7
    assert np.min(np.linalg.eigvalsh(m1)) >= -1e-7
