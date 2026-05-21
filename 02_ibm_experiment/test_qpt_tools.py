"""Focused tests for the Agent-2 offline QPT utilities."""

from __future__ import annotations

import numpy as np

from qpt_tools import (
    amplitude_damping_after_unitary,
    average_gate_fidelity,
    choi_from_unitary,
    is_cp,
    is_tp,
    linear_inversion_choi,
    mle_choi,
    process_fidelity,
    simulate_output_states_from_choi,
)


def test_unitary_choi_is_cptp_and_has_unit_fidelity() -> None:
    """The identity channel should be CP, TP, and fidelity-one with itself."""

    ident = np.eye(2, dtype=complex)
    choi = choi_from_unitary(ident)

    assert is_cp(choi)
    assert is_tp(choi, d_in=2, d_out=2)
    assert np.isclose(process_fidelity(choi, choi), 1.0)
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
