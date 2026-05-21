"""Compatibility imports for Agent-5 qubit channel utilities.

The duplicated implementations now live in :mod:`choi_common`. New code should
import from ``choi_common`` directly.
"""

from __future__ import annotations

import numpy as np

from choi_common.channels import (
    amplitude_damping_channel,
    bit_flip_channel,
    depolarizing_channel,
    identity_channel,
    mixed_choi,
    pauli_channel,
    pauli_matrices,
    phase_damping_channel,
    phase_flip_channel,
    unital_qubit_channel_choi,
)
from choi_common.representations import apply_kraus_channel as apply_channel
from choi_common.representations import choi_to_kraus, kraus_to_choi
from choi_common.utils import infer_choi_dims as infer_channel_dims
from choi_common.utils import validate_probability
from choi_common.validation import is_cp
from choi_common.validation import is_tp as _is_tp
from choi_common.validation import partial_trace_output as _partial_trace_output


Array = np.ndarray
_PAULIS = pauli_matrices()
I2: Array = _PAULIS["I"]
X: Array = _PAULIS["X"]
Y: Array = _PAULIS["Y"]
Z: Array = _PAULIS["Z"]
PAULIS: tuple[Array, Array, Array] = (X, Y, Z)

identity_kraus = identity_channel
amplitude_damping_kraus = amplitude_damping_channel
phase_damping_kraus = phase_damping_channel
bit_flip_kraus = bit_flip_channel
phase_flip_kraus = phase_flip_channel
pauli_kraus = pauli_channel
unital_choi = unital_qubit_channel_choi


def depolarizing_kraus(p: float) -> list[Array]:
    """Return qubit depolarizing Kraus operators using Agent-5 slider semantics."""
    return depolarizing_channel(p, d=2, convention="pauli_error")


def partial_trace_output(choi: Array) -> Array:
    """Trace out the output tensor factor of a square Choi matrix."""
    d_in, d_out = infer_channel_dims(choi)
    return _partial_trace_output(choi, d_in=d_in, d_out=d_out)


def is_tp(choi: Array, tol: float = 1e-9) -> bool:
    """Check trace preservation for a square Choi matrix."""
    d_in, d_out = infer_channel_dims(choi)
    return _is_tp(choi, d_in=d_in, d_out=d_out, tol=tol)
