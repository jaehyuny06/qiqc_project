"""Fidelities, distances, and channel-discrimination metrics."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass

import numpy as np
from numpy.typing import NDArray


Array = NDArray[np.complex128]


@dataclass(frozen=True)
class DiamondNormResult:
    """Container for a solved diamond-norm SDP."""

    value: float
    rho: Array
    witness: Array
    solver: str
    status: str


def raw_process_fidelity(choi_actual: np.ndarray, choi_ideal: np.ndarray) -> float:
    """Return unclipped process fidelity for unnormalized Choi matrices."""
    raise NotImplementedError("Proposal skeleton only.")


def process_fidelity(
    choi_actual: np.ndarray,
    choi_ideal: np.ndarray,
    clip: bool = True,
) -> float:
    """Return process fidelity, optionally clipped into ``[0, 1]``."""
    raise NotImplementedError("Proposal skeleton only.")


def average_gate_fidelity(choi_actual: np.ndarray, choi_ideal: np.ndarray, d: int) -> float:
    """Return average gate fidelity from process fidelity."""
    raise NotImplementedError("Proposal skeleton only.")


def trace_distance(rho: np.ndarray, sigma: np.ndarray) -> float:
    """Return the quantum trace distance ``0.5 * ||rho - sigma||_1``."""
    raise NotImplementedError("Proposal skeleton only.")


def solve_diamond_norm_sdp(
    choi_diff: np.ndarray,
    d_in: int,
    d_out: int,
    solver: str | None = None,
    eps: float = 1e-6,
    max_iters: int = 50_000,
) -> DiamondNormResult:
    """Solve Watrous's SDP for the diamond norm of a channel difference."""
    raise NotImplementedError("Proposal skeleton only.")


def diamond_norm_sdp(
    choi_diff: np.ndarray,
    d_in: int,
    d_out: int,
    solver: str | None = None,
    eps: float = 1e-6,
    max_iters: int = 50_000,
) -> float:
    """Return the diamond norm of a Hermiticity-preserving map by SDP."""
    raise NotImplementedError("Proposal skeleton only.")


def diamond_norm_distance(
    choi_actual: np.ndarray,
    choi_ideal: np.ndarray,
    d_in: int | None = None,
    d_out: int | None = None,
) -> float:
    """Return ``0.5 * ||E_actual - E_ideal||_diamond`` from Choi matrices."""
    raise NotImplementedError("Proposal skeleton only.")


def diamond_distance_proxy(
    choi_actual: np.ndarray,
    choi_ideal: np.ndarray,
    d: int | None = None,
) -> float:
    """Return a Choi nuclear-norm proxy for half-diamond distance."""
    raise NotImplementedError("Proposal skeleton only.")


def analytical_pauli_diamond_norm(
    probabilities_0: Mapping[str, float],
    probabilities_1: Mapping[str, float],
) -> float:
    """Return the exact diamond norm for a difference of one-qubit Pauli channels."""
    raise NotImplementedError("Proposal skeleton only.")


def analytical_depolarizing_diamond_norm(p0: float, p1: float, d: int = 2) -> float:
    """Return the exact diamond norm for replacement-probability depolarizing channels."""
    raise NotImplementedError("Proposal skeleton only.")


def discrimination_probability(
    choi_0: np.ndarray,
    choi_1: np.ndarray,
    d_in: int | None = None,
    d_out: int | None = None,
) -> float:
    """Return the optimal equal-prior two-channel discrimination probability."""
    raise NotImplementedError("Proposal skeleton only.")

