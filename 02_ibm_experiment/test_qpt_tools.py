"""Focused tests for the Agent-2 offline QPT utilities."""

from __future__ import annotations

import numpy as np

from qpt_tools import (
    apply_channel_to_state,
    apply_choi_channel,
    amplitude_damping_after_unitary,
    average_gate_fidelity,
    choi_from_unitary,
    depolarizing_after_unitary,
    diamond_norm_distance,
    is_cp,
    is_tp,
    linear_inversion_choi,
    mle_choi,
    process_fidelity,
    raw_process_fidelity,
    simulate_output_states_from_choi,
)


def test_unitary_choi_is_cptp_and_has_unit_fidelity() -> None:
    """The identity channel should be CP, TP, and fidelity-one with itself."""

    ident = np.eye(2, dtype=complex)
    choi = choi_from_unitary(ident)

    assert is_cp(choi)
    assert is_tp(choi, d_in=2, d_out=2)
    assert np.isclose(process_fidelity(choi, choi), 1.0)
    assert np.isclose(raw_process_fidelity(choi, choi), 1.0)
    assert np.isclose(average_gate_fidelity(choi, choi, d=2), 1.0)


def test_linear_inversion_recovers_exact_one_qubit_channel() -> None:
    """Exact informationally complete states reconstruct the original Choi."""

    hadamard = np.array([[1, 1], [1, -1]], dtype=complex) / np.sqrt(2)
    choi = amplitude_damping_after_unitary(hadamard, gamma=0.12)
    output_states = simulate_output_states_from_choi(choi)

    reconstructed = linear_inversion_choi({"output_states": output_states})

    assert np.allclose(reconstructed, choi, atol=1e-10)
    assert is_cp(reconstructed)
    assert is_tp(reconstructed, d_in=2, d_out=2)


def test_mle_projection_repairs_nonphysical_linear_inversion() -> None:
    """MLE projection should return a CP/TP matrix from a perturbed estimate."""

    x_gate = np.array([[0, 1], [1, 0]], dtype=complex)
    ideal = choi_from_unitary(x_gate)
    nonphysical = ideal.copy()
    nonphysical[0, 0] -= 0.35
    nonphysical[3, 3] += 0.15

    projected = mle_choi({"choi": nonphysical}, d_in=2, d_out=2)

    assert is_cp(projected, tol=5e-6)
    assert is_tp(projected, d_in=2, d_out=2, tol=5e-6)
    assert 0.0 <= process_fidelity(projected, ideal) <= 1.0


def test_apply_choi_channel_wrapper_matches_legacy_helper() -> None:
    """The project-standard Choi API should match the original helper."""

    choi = amplitude_damping_after_unitary(np.eye(2, dtype=complex), gamma=0.2)
    rho = np.array([[0.7, 0.1 - 0.2j], [0.1 + 0.2j, 0.3]], dtype=complex)

    expected = apply_channel_to_state(rho, choi)
    actual = apply_choi_channel(choi, rho)

    assert np.allclose(actual, expected)


def test_diamond_norm_distance_matches_depolarizing_closed_form() -> None:
    """The local SDP should compute the true half-diamond distance."""

    ident = choi_from_unitary(np.eye(2, dtype=complex))
    depol = depolarizing_after_unitary(np.eye(2, dtype=complex), p=1.0)

    assert np.isclose(diamond_norm_distance(depol, ident, d_in=2, d_out=2), 1.0, atol=2e-3)
