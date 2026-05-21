"""Utilities for simple quantum-comb and non-Markovianity calculations."""

from __future__ import annotations

from collections.abc import Callable, Sequence
from itertools import product

import numpy as np

from choi_common.metrics import trace_distance
from choi_common.representations import apply_choi_channel, choi_to_natural, kraus_to_choi, natural_to_choi
from choi_common.utils import dagger, hermitian_part
from choi_common.validation import partial_trace


Array = np.ndarray


def _ravel_index(indices: Sequence[int], dims: Sequence[int]) -> int:
    return int(np.ravel_multi_index(tuple(indices), tuple(dims)))


def _unravel_index(index: int, dims: Sequence[int]) -> tuple[int, ...]:
    return tuple(int(x) for x in np.unravel_index(index, tuple(dims)))


def embed_operator(operator: Array, dims: Sequence[int], targets: Sequence[int]) -> Array:
    """Embed a local operator into a tensor-product Hilbert space."""
    dims_list = list(dims)
    targets_list = list(targets)
    target_dims = [dims_list[t] for t in targets_list]
    local_dim = int(np.prod(target_dims))
    local = np.asarray(operator, dtype=complex)
    if local.shape != (local_dim, local_dim):
        raise ValueError("operator shape is incompatible with target dimensions")

    full_dim = int(np.prod(dims_list))
    full = np.zeros((full_dim, full_dim), dtype=complex)
    target_set = set(targets_list)

    for col in range(full_dim):
        col_multi = list(_unravel_index(col, dims_list))
        local_col = _ravel_index([col_multi[t] for t in targets_list], target_dims)
        for local_row in range(local_dim):
            value = local[local_row, local_col]
            if abs(value) == 0.0:
                continue
            local_row_multi = _unravel_index(local_row, target_dims)
            row_multi = col_multi.copy()
            for target, target_value in zip(targets_list, local_row_multi, strict=True):
                row_multi[target] = target_value
            if any(row_multi[t] != col_multi[t] for t in range(len(dims_list)) if t not in target_set):
                continue
            row = _ravel_index(row_multi, dims_list)
            full[row, col] = value
    return full


def _apply_memory_channel(operator: Array, system_env_unitaries: Sequence[Array], env_init: Array) -> Array:
    """Apply a sequential memory channel to all input time slots."""
    n_steps = len(system_env_unitaries)
    d_system_n = operator.shape[0]
    d_system = int(round(d_system_n ** (1 / n_steps)))
    d_env = env_init.shape[0]
    dims = [d_system] * n_steps + [d_env]

    state = np.kron(np.asarray(operator, dtype=complex), np.asarray(env_init, dtype=complex))
    for step, unitary in enumerate(system_env_unitaries):
        full_u = embed_operator(unitary, dims, [step, n_steps])
        state = full_u @ state @ dagger(full_u)
    return partial_trace(state, dims, [n_steps])


def _grouped_choi_to_comb_order(choi: Array, n_steps: int, d_system: int) -> Array:
    """Permute ``A_all, B_all`` Choi order into ``A0, B0, A1, B1, ...``."""
    dims_grouped = [d_system] * n_steps + [d_system] * n_steps
    tensor = np.asarray(choi, dtype=complex).reshape(dims_grouped + dims_grouped)
    row_perm: list[int] = []
    col_perm: list[int] = []
    for step in range(n_steps):
        row_perm.extend([step, n_steps + step])
        col_perm.extend([2 * n_steps + step, 3 * n_steps + step])
    permuted = np.transpose(tensor, row_perm + col_perm)
    return permuted.reshape(choi.shape)


def _comb_order_to_grouped_choi(comb: Array, n_steps: int, d_system: int) -> Array:
    """Permute ``A0, B0, A1, B1, ...`` comb order into ``A_all, B_all``."""
    dims_comb = [d_system, d_system] * n_steps
    tensor = np.asarray(comb, dtype=complex).reshape(dims_comb + dims_comb)
    row_perm = list(range(0, 2 * n_steps, 2)) + list(range(1, 2 * n_steps, 2))
    col_perm = [2 * n_steps + i for i in row_perm]
    permuted = np.transpose(tensor, row_perm + col_perm)
    return permuted.reshape(comb.shape)


def construct_process_tensor(
    system_env_unitaries: list[Array],
    env_init: Array,
    n_steps: int,
) -> Array:
    """Construct a finite-memory N-use process tensor as a comb Choi matrix."""
    if n_steps != len(system_env_unitaries):
        raise ValueError("n_steps must match the number of unitaries")
    if n_steps < 1:
        raise ValueError("n_steps must be positive")

    env = np.asarray(env_init, dtype=complex)
    d_env = env.shape[0]
    if env.shape != (d_env, d_env):
        raise ValueError("env_init must be a square density matrix")

    first_unitary = np.asarray(system_env_unitaries[0], dtype=complex)
    if first_unitary.shape[0] % d_env != 0:
        raise ValueError("unitary dimension is incompatible with env_init")
    d_system = first_unitary.shape[0] // d_env
    for unitary in system_env_unitaries:
        if np.asarray(unitary).shape != (d_system * d_env, d_system * d_env):
            raise ValueError("all unitaries must have shape (d_system*d_env)^2")

    d_total_in = d_system**n_steps
    choi_grouped = np.zeros((d_total_in * d_total_in, d_total_in * d_total_in), dtype=complex)
    for i in range(d_total_in):
        for j in range(d_total_in):
            basis_op = np.zeros((d_total_in, d_total_in), dtype=complex)
            basis_op[i, j] = 1.0
            block = _apply_memory_channel(basis_op, system_env_unitaries, env)
            row = i * d_total_in
            col = j * d_total_in
            choi_grouped[row : row + d_total_in, col : col + d_total_in] = block

    comb = _grouped_choi_to_comb_order(choi_grouped, n_steps, d_system)
    return hermitian_part(comb)


def _infer_qubit_steps_from_comb(process_tensor: Array) -> int:
    size = np.asarray(process_tensor).shape[0]
    n_steps = int(round(np.log(size) / np.log(4)))
    if 4**n_steps != size:
        raise ValueError("only qubit combs with matrix size 4**n_steps are inferred automatically")
    return n_steps


def marginal_channel(process_tensor: Array, step: int) -> Array:
    """Return the single-slot marginal Choi matrix of a qubit comb."""
    n_steps = _infer_qubit_steps_from_comb(process_tensor)
    if step < 0 or step >= n_steps:
        raise ValueError("step is outside the comb")

    dims = [2, 2] * n_steps
    keep = {2 * step, 2 * step + 1}
    trace_out = [idx for idx in range(2 * n_steps) if idx not in keep]
    reduced = partial_trace(process_tensor, dims, trace_out)
    normalization = 2 ** (n_steps - 1)
    return reduced / normalization


def is_markovian(process_tensor: Array, n_steps: int, tol: float = 1e-8) -> bool:
    """Test whether a qubit comb factorizes into its single-step marginals."""
    if n_steps != _infer_qubit_steps_from_comb(process_tensor):
        raise ValueError("n_steps is incompatible with process_tensor size")

    product_choi = marginal_channel(process_tensor, 0)
    for step in range(1, n_steps):
        product_choi = np.kron(product_choi, marginal_channel(process_tensor, step))

    diff_norm = np.linalg.norm(process_tensor - product_choi, ord="fro")
    scale = max(1.0, np.linalg.norm(process_tensor, ord="fro"))
    return bool(diff_norm / scale <= tol)


def comb_global_trace_preservation_check(comb: Array, dims: list[int], tol: float = 1e-8) -> bool:
    """Check the necessary global trace-preservation condition for a comb."""
    if len(dims) % 2 != 0:
        raise ValueError("dims must be [A0, B0, A1, B1, ...]")
    trace_outputs = list(range(1, len(dims), 2))
    traced = partial_trace(comb, dims, trace_outputs)
    input_dim = int(np.prod(dims[::2]))
    return bool(np.allclose(traced, np.eye(input_dim, dtype=complex), atol=tol))


def deterministic_comb_causality_check(comb: Array, dims: list[int], tol: float = 1e-8) -> bool:
    """Check the recursive causality hierarchy for a deterministic quantum comb."""
    dims_list = list(dims)
    if len(dims_list) % 2 != 0:
        raise ValueError("dims must be [A0, B0, A1, B1, ...]")
    if not dims_list:
        raise ValueError("at least one input-output slot is required")

    current = np.asarray(comb, dtype=complex)
    current_dims = dims_list
    n_slots = len(dims_list) // 2
    total_dim = int(np.prod(dims_list))
    if current.shape != (total_dim, total_dim):
        raise ValueError("comb shape is incompatible with dims")

    for slot in reversed(range(n_slots)):
        output_axis = 2 * slot + 1
        input_dim = current_dims[2 * slot]
        traced_dims = current_dims[:output_axis] + current_dims[output_axis + 1 :]
        traced = partial_trace(current, current_dims, [output_axis])

        if slot == 0:
            target = np.eye(input_dim, dtype=complex)
            if not np.allclose(traced, target, atol=tol):
                return False
            continue

        previous_dims = current_dims[: 2 * slot]
        previous = partial_trace(traced, traced_dims, [len(traced_dims) - 1]) / input_dim
        target = np.kron(previous, np.eye(input_dim, dtype=complex))
        if not np.allclose(traced, target, atol=tol):
            return False

        current = previous
        current_dims = previous_dims

    return True


def comb_partial_trace_check(comb: Array, dims: list[int]) -> bool:
    """Deprecated alias for :func:`deterministic_comb_causality_check`."""
    return deterministic_comb_causality_check(comb, dims)


def _pure_state_from_bloch(theta: float, phi: float) -> Array:
    ket = np.array([np.cos(theta / 2), np.exp(1j * phi) * np.sin(theta / 2)], dtype=complex)
    return np.outer(ket, ket.conj())


def _antipodal_qubit_pairs() -> list[tuple[Array, Array]]:
    pairs: list[tuple[Array, Array]] = []
    angles = [
        (0.0, 0.0),
        (np.pi, 0.0),
        (np.pi / 2, 0.0),
        (np.pi / 2, np.pi),
        (np.pi / 2, np.pi / 2),
        (np.pi / 2, 3 * np.pi / 2),
    ]
    for theta, phi in angles[::2]:
        rho = _pure_state_from_bloch(theta, phi)
        sigma = _pure_state_from_bloch(np.pi - theta, phi + np.pi)
        pairs.append((rho, sigma))

    for theta in np.linspace(0.2, np.pi - 0.2, 5):
        for phi in np.linspace(0.0, 2 * np.pi, 8, endpoint=False):
            rho = _pure_state_from_bloch(theta, phi)
            sigma = _pure_state_from_bloch(np.pi - theta, phi + np.pi)
            pairs.append((rho, sigma))
    return pairs


def blp_measure(channel_family: Callable[[float], Array], t_grid: Array) -> float:
    """Estimate the BLP non-Markovianity measure on a time grid."""
    times = np.asarray(t_grid, dtype=float)
    if times.ndim != 1 or times.size < 2:
        raise ValueError("t_grid must be a one-dimensional grid with at least two points")

    best = 0.0
    for rho, sigma in _antipodal_qubit_pairs():
        distances = []
        for time in times:
            choi = channel_family(float(time))
            distances.append(trace_distance(apply_choi_channel(choi, rho), apply_choi_channel(choi, sigma)))
        increments = np.diff(distances)
        best = max(best, float(np.sum(increments[increments > 0.0])))
    return best


def rhp_measure(channel_family: Callable[[float], Array], t_grid: Array) -> float:
    """Estimate an RHP-style CP-divisibility violation on a time grid."""
    times = np.asarray(t_grid, dtype=float)
    if times.ndim != 1 or times.size < 2:
        raise ValueError("t_grid must be a one-dimensional grid with at least two points")

    total = 0.0
    for t0, t1 in zip(times[:-1], times[1:], strict=True):
        choi_0 = channel_family(float(t0))
        choi_1 = channel_family(float(t1))
        d = int(round(np.sqrt(choi_0.shape[0])))
        natural_0 = choi_to_natural(choi_0, d, d)
        natural_1 = choi_to_natural(choi_1, d, d)
        intermediate = natural_1 @ np.linalg.pinv(natural_0, rcond=1e-10)
        choi_intermediate = natural_to_choi(intermediate, d, d)
        eigenvalues = np.linalg.eigvalsh(hermitian_part(choi_intermediate))
        total += float(np.sum(np.abs(eigenvalues[eigenvalues < -1e-8])) / d)
    return total
