from __future__ import annotations

import numpy as np

from choi_common.channels import (
    amplitude_damping_channel,
    amplitude_damping_channel_choi,
    depolarizing_channel,
    depolarizing_channel_choi,
    identity_channel,
    identity_channel_choi,
    unitary_channel_choi,
)
from choi_common.metrics import average_gate_fidelity, process_fidelity, trace_distance
from choi_common.representations import (
    apply_choi_channel,
    choi_to_kraus,
    choi_to_natural,
    kraus_to_choi,
    natural_to_choi,
)
from choi_common.validation import choi_rank, is_cp, is_tp, partial_trace
from choi_common.visualization import bloch_affine_map, choi_to_pauli_transfer


def test_identity_channel_is_cptp() -> None:
    choi = kraus_to_choi(identity_channel(2))
    assert choi.shape == (4, 4)
    assert is_cp(choi)
    assert is_tp(choi, d_in=2, d_out=2)
    assert choi_rank(choi) == 1


def test_choi_natural_round_trip() -> None:
    choi = kraus_to_choi(amplitude_damping_channel(0.25))
    natural = choi_to_natural(choi, d_in=2, d_out=2)
    assert natural.shape == (4, 4)
    np.testing.assert_allclose(natural_to_choi(natural, d_in=2, d_out=2), choi)


def test_apply_choi_channel_matches_amplitude_damping() -> None:
    gamma = 0.3
    choi = amplitude_damping_channel_choi(gamma)
    excited = np.array([[0, 0], [0, 1]], dtype=complex)
    out = apply_choi_channel(choi, excited, d_in=2, d_out=2)
    expected = np.array([[gamma, 0], [0, 1 - gamma]], dtype=complex)
    np.testing.assert_allclose(out, expected, atol=1e-12)


def test_depolarizing_conventions_are_distinct() -> None:
    replacement = depolarizing_channel_choi(0.4, convention="replacement")
    pauli_error = kraus_to_choi(depolarizing_channel(0.4, convention="pauli_error"))
    assert not np.allclose(replacement, pauli_error)
    assert is_tp(replacement, 2, 2)
    assert is_tp(pauli_error, 2, 2)


def test_metrics_and_pauli_transfer() -> None:
    ident = identity_channel_choi(2)
    assert process_fidelity(ident, ident) == 1.0
    assert average_gate_fidelity(ident, ident, d=2) == 1.0
    transfer = choi_to_pauli_transfer(ident)
    np.testing.assert_allclose(transfer.real, np.eye(4), atol=1e-12)


def test_partial_trace_and_kraus_recovery() -> None:
    bell = np.array([1, 0, 0, 1], dtype=complex) / np.sqrt(2)
    rho = np.outer(bell, bell.conj())
    reduced = partial_trace(rho, [2, 2], [1])
    np.testing.assert_allclose(reduced, np.eye(2) / 2, atol=1e-12)

    choi = amplitude_damping_channel_choi(0.1)
    recovered = choi_to_kraus(choi, d_in=2, d_out=2)
    assert len(recovered) == 2


def test_unitary_and_bloch_helpers() -> None:
    x_gate = np.array([[0, 1], [1, 0]], dtype=complex)
    choi = unitary_channel_choi(x_gate)
    matrix, offset = bloch_affine_map(choi)
    assert matrix.shape == (3, 3)
    assert offset.shape == (3,)
    assert trace_distance(np.eye(2) / 2, np.eye(2) / 2) == 0.0
