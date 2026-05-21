r"""Theory helpers for the Choi project.

Shared channel-representation implementations now live in :mod:`choi_common`.
This module keeps Agent-1-specific examples and lightweight compatibility
imports for older tests and notebooks.
"""

from __future__ import annotations

import numpy as np

from choi_common.channels import (
    amplitude_damping_channel,
    bit_flip_channel,
    depolarizing_channel,
    identity_channel,
    pauli_channel,
    phase_damping_channel,
    phase_flip_channel,
)
from choi_common.representations import (
    apply_kraus_channel,
    choi_to_kraus,
    choi_to_natural,
    kraus_to_choi,
    kraus_to_stinespring,
    natural_to_choi,
    stinespring_to_kraus,
)
from choi_common.validation import choi_rank, is_cp, is_tp, is_unital


Array = np.ndarray

# Backward-compatible local name. New code should import
# ``apply_kraus_channel`` from ``choi_common.representations``.
apply_channel = apply_kraus_channel


def random_channel(d_in: int, d_out: int, n_kraus: int) -> list[Array]:
    """Generate a random trace-preserving quantum channel.

    Parameters
    ----------
    d_in:
        Input Hilbert-space dimension.
    d_out:
        Output Hilbert-space dimension.
    n_kraus:
        Number of Kraus operators.

    Returns
    -------
    list[numpy.ndarray]
        Random Kraus operators satisfying ``sum_k K_k^dagger K_k = I``.
    """
    if d_in <= 0 or d_out <= 0 or n_kraus <= 0:
        raise ValueError("d_in, d_out, and n_kraus must all be positive.")
    if n_kraus * d_out < d_in:
        raise ValueError("n_kraus * d_out must be at least d_in for a TP channel.")

    ginibre = (
        np.random.normal(size=(n_kraus * d_out, d_in))
        + 1j * np.random.normal(size=(n_kraus * d_out, d_in))
    )
    q, _ = np.linalg.qr(ginibre)
    return stinespring_to_kraus(q[:, :d_in], n_kraus)
