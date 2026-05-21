"""Focused tests for the Agent-5 widget utilities."""

from __future__ import annotations

import numpy as np

from channel_utils import (
    I2,
    amplitude_damping_kraus,
    depolarizing_kraus,
    is_cp,
    is_tp,
    kraus_to_choi,
    partial_trace_output,
)
from widget_core import (
    apply_choi_to_state,
    compute_indicators,
    get_channel_choi,
)


def test_identity_choi_is_cp_tp_and_rank_one() -> None:
    """The identity channel should have a rank-one unnormalized Choi matrix."""
    choi = get_channel_choi("Identity", {})
    indicators = compute_indicators(choi)
    assert indicators["is_cp"] is True
    assert indicators["is_tp"] is True
    assert indicators["rank"] == 1
    assert np.isclose(indicators["process_fidelity_identity"], 1.0)


def test_partial_trace_output_for_depolarizing_channel() -> None:
    """Depolarizing channels are trace preserving for all valid probabilities."""
    choi = kraus_to_choi(depolarizing_kraus(0.37))
    assert is_cp(choi)
    assert is_tp(choi)
    assert np.allclose(partial_trace_output(choi), I2)


def test_amplitude_damping_action_on_excited_state() -> None:
    """Amplitude damping should move population from |1> to |0>."""
    gamma = 0.4
    choi = kraus_to_choi(amplitude_damping_kraus(gamma))
    excited = np.array([[0.0, 0.0], [0.0, 1.0]], dtype=complex)
    output = apply_choi_to_state(choi, excited)
    expected = np.array([[gamma, 0.0], [0.0, 1.0 - gamma]], dtype=complex)
    assert np.allclose(output, expected)


def test_unital_map_can_show_non_cp_status() -> None:
    """The unital sliders intentionally expose non-CP regions."""
    choi = get_channel_choi(
        "Unital",
        {"lambda_x": 1.0, "lambda_y": 1.0, "lambda_z": -1.0},
    )
    indicators = compute_indicators(choi)
    assert indicators["is_tp"] is True
    assert indicators["is_cp"] is False


def test_pauli_probability_validation() -> None:
    """Invalid Pauli probabilities should fail fast."""
    try:
        get_channel_choi("Pauli", {"p_x": 0.5, "p_y": 0.5, "p_z": 0.5})
    except ValueError as exc:
        assert "p_x + p_y + p_z" in str(exc)
    else:
        raise AssertionError("Expected invalid Pauli probabilities to raise ValueError.")

