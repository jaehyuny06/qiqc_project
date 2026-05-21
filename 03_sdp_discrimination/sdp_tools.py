"""SDP tools for quantum channel discrimination via Choi matrices.

Shared channel constructors, representation conversions, validation checks,
and diamond-norm SDP primitives now come from :mod:`choi_common`.
"""

from __future__ import annotations

from itertools import product
from typing import Iterable

import numpy as np
from numpy.typing import NDArray

from choi_common.channels import (
    amplitude_damping_channel_choi,
    bit_flip_channel_choi,
    depolarizing_channel_choi,
    identity_channel_choi,
    pauli_channel_choi,
    pauli_matrices,
    phase_damping_channel_choi,
    phase_flip_channel_choi,
    unitary_channel_choi,
    z_rotation_channel_choi,
)
from choi_common.metrics import (
    DiamondNormResult,
    analytical_depolarizing_diamond_norm,
    analytical_pauli_diamond_norm,
    diamond_norm_sdp,
    discrimination_probability,
    solve_diamond_norm_sdp,
)
from choi_common.representations import apply_choi_channel, kraus_to_choi
from choi_common.utils import as_complex_matrix, hermitian_part, infer_choi_dims
from choi_common.validation import is_cp, is_tp


Array = NDArray[np.complex128]
apply_choi_to_state = apply_choi_channel


def _infer_equal_dims(choi: np.ndarray) -> tuple[int, int]:
    d_in, d_out = infer_choi_dims(choi)
    if d_in != d_out:
        raise ValueError("Expected equal input/output dimensions.")
    return d_in, d_out


def _validate_choi_dims(choi: np.ndarray, d_in: int, d_out: int) -> Array:
    arr = as_complex_matrix(choi, "choi", square=True)
    expected = d_in * d_out
    if arr.shape != (expected, expected):
        raise ValueError(
            f"Expected Choi shape {(expected, expected)} for d_in={d_in}, "
            f"d_out={d_out}; got {arr.shape}."
        )
    return arr


def optimal_input_state(choi_0: np.ndarray, choi_1: np.ndarray) -> Array:
    """Return the SDP optimal input marginal for channel discrimination."""
    d_in, d_out = _infer_equal_dims(choi_0)
    result = solve_diamond_norm_sdp(np.asarray(choi_0) - np.asarray(choi_1), d_in, d_out)
    eigvals, eigvecs = np.linalg.eigh(result.rho)
    eigvals = np.maximum(eigvals, 0.0)
    if eigvals.sum() <= 0:
        return np.eye(d_in, dtype=np.complex128) / d_in
    rho = eigvecs @ np.diag(eigvals / eigvals.sum()) @ eigvecs.conj().T
    return hermitian_part(rho)


def _purify_density_matrix(rho: np.ndarray) -> Array:
    eigvals, eigvecs = np.linalg.eigh(hermitian_part(rho))
    eigvals = np.maximum(eigvals, 0.0)
    sqrt_rho = eigvecs @ np.diag(np.sqrt(eigvals)) @ eigvecs.conj().T
    psi = sqrt_rho.reshape(-1, order="C")
    norm = np.linalg.norm(psi)
    if norm <= 0:
        raise ValueError("Cannot purify the zero matrix.")
    return np.outer(psi / norm, (psi / norm).conj())


def optimal_povm(choi_0: np.ndarray, choi_1: np.ndarray) -> tuple[Array, Array]:
    """Return a Helstrom POVM for the SDP-derived input purification."""
    d_in, d_out = _infer_equal_dims(choi_0)
    rho = optimal_input_state(choi_0, choi_1)
    purification = _purify_density_matrix(rho).reshape(d_in, d_in, d_in, d_in)
    diff = hermitian_part(np.asarray(choi_0) - np.asarray(choi_1)).reshape(
        d_in, d_out, d_in, d_out
    )
    helstrom = np.einsum("rasc,abcd->rbsd", purification, diff).reshape(
        d_in * d_out, d_in * d_out
    )
    eigvals, eigvecs = np.linalg.eigh(hermitian_part(helstrom))
    positive = eigvals >= 0.0
    m0 = eigvecs[:, positive] @ eigvecs[:, positive].conj().T
    m1 = np.eye(d_in * d_out, dtype=np.complex128) - m0
    return hermitian_part(m0), hermitian_part(m1)


def _tensor_choi_pair(
    choi_a: np.ndarray,
    choi_b: np.ndarray,
    dims_a: tuple[int, int],
    dims_b: tuple[int, int],
) -> Array:
    d_in_a, d_out_a = dims_a
    d_in_b, d_out_b = dims_b
    arr_a = _validate_choi_dims(choi_a, d_in_a, d_out_a).reshape(
        d_in_a, d_out_a, d_in_a, d_out_a
    )
    arr_b = _validate_choi_dims(choi_b, d_in_b, d_out_b).reshape(
        d_in_b, d_out_b, d_in_b, d_out_b
    )
    tensor = np.einsum("iajb,kcld->ikacjlbd", arr_a, arr_b)
    tensor = tensor.reshape(
        d_in_a * d_in_b,
        d_out_a * d_out_b,
        d_in_a * d_in_b,
        d_out_a * d_out_b,
    )
    return hermitian_part(tensor.reshape(d_in_a * d_in_b * d_out_a * d_out_b, -1))


def tensor_power_choi(choi: np.ndarray, n: int, d_in: int, d_out: int) -> Array:
    """Return the Choi matrix for the ``n``-fold parallel tensor power."""
    if n < 1:
        raise ValueError("n must be at least 1.")
    result = _validate_choi_dims(choi, d_in, d_out)
    current_dims = (d_in, d_out)
    for _ in range(1, n):
        result = _tensor_choi_pair(result, choi, current_dims, (d_in, d_out))
        current_dims = (current_dims[0] * d_in, current_dims[1] * d_out)
    return result


def n_shot_discrimination(choi_0: np.ndarray, choi_1: np.ndarray, n: int) -> float:
    """Return optimal parallel ``n``-use discrimination probability."""
    d_in, d_out = _infer_equal_dims(choi_0)
    choi_0_n = tensor_power_choi(choi_0, n, d_in, d_out)
    choi_1_n = tensor_power_choi(choi_1, n, d_in, d_out)
    return discrimination_probability(choi_0_n, choi_1_n, d_in**n, d_out**n)


def _qubit_pure_states(n_theta: int = 41, n_phi: int = 81) -> Iterable[Array]:
    yield np.array([[1.0], [0.0]], dtype=np.complex128)
    yield np.array([[0.0], [1.0]], dtype=np.complex128)
    yield np.array([[1.0], [1.0]], dtype=np.complex128) / np.sqrt(2.0)
    yield np.array([[1.0], [1.0j]], dtype=np.complex128) / np.sqrt(2.0)
    for theta, phi in product(
        np.linspace(0.0, np.pi, n_theta),
        np.linspace(0.0, 2.0 * np.pi, n_phi, endpoint=False),
    ):
        yield np.array(
            [[np.cos(theta / 2.0)], [np.exp(1j * phi) * np.sin(theta / 2.0)]],
            dtype=np.complex128,
        )


def _trace_norm_hermitian(matrix: np.ndarray) -> float:
    eigvals = np.linalg.eigvalsh(hermitian_part(matrix))
    return float(np.sum(np.abs(eigvals)))


def product_strategy_discrimination(choi_0: np.ndarray, choi_1: np.ndarray) -> float:
    """Approximate the best no-ancilla discrimination probability."""
    d_in, d_out = _infer_equal_dims(choi_0)
    diff = np.asarray(choi_0) - np.asarray(choi_1)
    if d_in != 2:
        rng = np.random.default_rng(42)
        vectors = []
        for _ in range(2048):
            vec = rng.normal(size=d_in) + 1j * rng.normal(size=d_in)
            vectors.append((vec / np.linalg.norm(vec)).reshape(d_in, 1))
    else:
        vectors = list(_qubit_pure_states())

    best_trace_norm = 0.0
    for ket in vectors:
        rho = ket @ ket.conj().T
        output_diff = apply_choi_channel(diff, rho, d_in=d_in, d_out=d_out)
        best_trace_norm = max(best_trace_norm, _trace_norm_hermitian(output_diff))
    return float(np.clip(0.5 + 0.25 * best_trace_norm, 0.5, 1.0))
