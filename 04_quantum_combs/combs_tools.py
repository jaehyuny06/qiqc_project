"""Utilities for simple quantum-comb and non-Markovianity calculations.

The Choi convention used throughout this module is

    C_E = sum_ij |i><j|_A tensor E(|i><j|)_B,

with the input space first.  For an N-use comb we store subsystem order
``A0, B0, A1, B1, ...`` so that one time slot is contiguous.
"""

from __future__ import annotations

from collections.abc import Callable, Sequence
from itertools import product

import numpy as np
from scipy.linalg import svdvals


Array = np.ndarray


def dagger(matrix: Array) -> Array:
    """Return the conjugate transpose of a matrix."""

    return np.asarray(matrix).conj().T


def partial_trace(operator: Array, dims: Sequence[int], trace_out: Sequence[int]) -> Array:
    """Trace selected tensor factors out of an operator.

    Parameters
    ----------
    operator
        Square matrix acting on ``tensor_i C^{dims[i]}``.
    dims
        Tensor-factor dimensions.
    trace_out
        Indices of tensor factors to trace out.

    Returns
    -------
    np.ndarray
        Reduced operator on the untraced tensor factors, in the original order.
    """

    dims_list = list(dims)
    total_dim = int(np.prod(dims_list))
    matrix = np.asarray(operator, dtype=complex)
    if matrix.shape != (total_dim, total_dim):
        raise ValueError("operator shape is incompatible with dims")

    tensor = matrix.reshape(dims_list + dims_list)
    for axis in sorted(set(trace_out), reverse=True):
        if axis < 0 or axis >= len(dims_list):
            raise ValueError(f"trace axis {axis} is outside dims")
        tensor = np.trace(tensor, axis1=axis, axis2=axis + len(dims_list))
        dims_list.pop(axis)

    remaining_dim = int(np.prod(dims_list, dtype=int)) if dims_list else 1
    return tensor.reshape(remaining_dim, remaining_dim)


def kraus_to_choi(kraus_ops: Sequence[Array]) -> Array:
    """Convert Kraus operators to a Choi matrix.

    Parameters
    ----------
    kraus_ops
        Kraus operators with shape ``(d_out, d_in)``.

    Returns
    -------
    np.ndarray
        Choi matrix with shape ``(d_in * d_out, d_in * d_out)``.
    """

    if not kraus_ops:
        raise ValueError("at least one Kraus operator is required")

    d_out, d_in = np.asarray(kraus_ops[0]).shape
    choi = np.zeros((d_in * d_out, d_in * d_out), dtype=complex)
    for i in range(d_in):
        for j in range(d_in):
            basis_op = np.zeros((d_in, d_in), dtype=complex)
            basis_op[i, j] = 1.0
            block = sum(k @ basis_op @ dagger(k) for k in kraus_ops)
            choi[i * d_out : (i + 1) * d_out, j * d_out : (j + 1) * d_out] = block
    return choi


def apply_choi_channel(rho: Array, choi: Array, d_in: int | None = None, d_out: int | None = None) -> Array:
    """Apply a channel represented by its Choi matrix to a density operator.

    Parameters
    ----------
    rho
        Input operator.
    choi
        Choi matrix in the convention ``input tensor output``.
    d_in, d_out
        Optional input and output dimensions.  If omitted, ``d_in`` is read
        from ``rho`` and ``d_out`` is inferred from the Choi size.

    Returns
    -------
    np.ndarray
        Output operator ``E(rho)``.
    """

    rho_arr = np.asarray(rho, dtype=complex)
    if d_in is None:
        d_in = rho_arr.shape[0]
    if rho_arr.shape != (d_in, d_in):
        raise ValueError("rho shape is incompatible with d_in")

    choi_arr = np.asarray(choi, dtype=complex)
    if d_out is None:
        if choi_arr.shape[0] % d_in != 0:
            raise ValueError("cannot infer d_out from choi and d_in")
        d_out = choi_arr.shape[0] // d_in
    if choi_arr.shape != (d_in * d_out, d_in * d_out):
        raise ValueError("choi shape is incompatible with dimensions")

    out = np.zeros((d_out, d_out), dtype=complex)
    for i in range(d_in):
        for j in range(d_in):
            block = choi_arr[i * d_out : (i + 1) * d_out, j * d_out : (j + 1) * d_out]
            out += rho_arr[i, j] * block
    return out


def choi_to_natural(choi: Array, d_in: int | None = None, d_out: int | None = None) -> Array:
    """Convert a Choi matrix to the natural superoperator representation.

    The natural representation satisfies ``vec(E(X)) = S vec(X)`` using
    column-major vectorization.
    """

    choi_arr = np.asarray(choi, dtype=complex)
    if d_in is None and d_out is None:
        root = int(round(np.sqrt(choi_arr.shape[0])))
        d_in = root
        d_out = root
    elif d_in is None or d_out is None:
        raise ValueError("provide both d_in and d_out, or neither for square channels")

    assert d_in is not None and d_out is not None
    natural = np.zeros((d_out * d_out, d_in * d_in), dtype=complex)
    for i in range(d_in):
        for j in range(d_in):
            block = choi_arr[i * d_out : (i + 1) * d_out, j * d_out : (j + 1) * d_out]
            natural[:, i + j * d_in] = block.reshape(-1, order="F")
    return natural


def natural_to_choi(natural: Array, d_in: int | None = None, d_out: int | None = None) -> Array:
    """Convert a natural superoperator to a Choi matrix."""

    natural_arr = np.asarray(natural, dtype=complex)
    if d_in is None and d_out is None:
        d_out = int(round(np.sqrt(natural_arr.shape[0])))
        d_in = int(round(np.sqrt(natural_arr.shape[1])))
    elif d_in is None or d_out is None:
        raise ValueError("provide both d_in and d_out, or neither")

    assert d_in is not None and d_out is not None
    choi = np.zeros((d_in * d_out, d_in * d_out), dtype=complex)
    for i in range(d_in):
        for j in range(d_in):
            block = natural_arr[:, i + j * d_in].reshape((d_out, d_out), order="F")
            choi[i * d_out : (i + 1) * d_out, j * d_out : (j + 1) * d_out] = block
    return choi


def trace_distance(rho: Array, sigma: Array) -> float:
    """Return the quantum trace distance ``0.5 * ||rho - sigma||_1``."""

    diff = np.asarray(rho, dtype=complex) - np.asarray(sigma, dtype=complex)
    return float(0.5 * np.sum(svdvals(diff)))


def _ravel_index(indices: Sequence[int], dims: Sequence[int]) -> int:
    return int(np.ravel_multi_index(tuple(indices), tuple(dims)))


def _unravel_index(index: int, dims: Sequence[int]) -> tuple[int, ...]:
    return tuple(int(x) for x in np.unravel_index(index, tuple(dims)))


def embed_operator(operator: Array, dims: Sequence[int], targets: Sequence[int]) -> Array:
    """Embed a local operator into a tensor-product Hilbert space.

    Parameters
    ----------
    operator
        Operator on the tensor product of ``dims[target]`` for each target,
        ordered as given by ``targets``.
    dims
        Dimensions of the full tensor-product space.
    targets
        Subsystems on which ``operator`` acts.

    Returns
    -------
    np.ndarray
        Full-space operator.
    """

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
    """Construct a finite-memory N-use process tensor as a comb Choi matrix.

    The model is a collision process: each system time slot interacts once
    with the same environment, which is then passed to the next slot.  The
    resulting object is the Choi matrix of the induced multi-use channel,
    stored in comb order ``A0, B0, A1, B1, ...``.  This is a compact and
    explicit way to expose temporal correlations from a shared environment.

    Parameters
    ----------
    system_env_unitaries
        List of unitaries acting on ``system tensor environment``.
    env_init
        Initial environment density matrix.
    n_steps
        Number of time slots/uses.

    Returns
    -------
    np.ndarray
        Positive semidefinite comb Choi operator.
    """

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
    return 0.5 * (comb + dagger(comb))


def _infer_qubit_steps_from_comb(process_tensor: Array) -> int:
    size = np.asarray(process_tensor).shape[0]
    n_steps = int(round(np.log(size) / np.log(4)))
    if 4**n_steps != size:
        raise ValueError("only qubit combs with matrix size 4**n_steps are inferred automatically")
    return n_steps


def marginal_channel(process_tensor: Array, step: int) -> Array:
    """Return the single-slot marginal Choi matrix of a qubit comb.

    Parameters
    ----------
    process_tensor
        Comb matrix in order ``A0, B0, A1, B1, ...``.
    step
        Time-slot index to keep.

    Returns
    -------
    np.ndarray
        Choi matrix for the requested marginal channel.
    """

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


def comb_partial_trace_check(comb: Array, dims: list[int]) -> bool:
    """Check the deterministic-comb trace-preservation condition.

    This verifies the channel-level causality condition
    ``Tr_{B0...BN}(T) = I_{A0...AN}`` for a comb stored as
    ``A0, B0, A1, B1, ...``.  It is a necessary trace condition and is exact
    for the finite-memory combs constructed by :func:`construct_process_tensor`.
    """

    if len(dims) % 2 != 0:
        raise ValueError("dims must be [A0, B0, A1, B1, ...]")
    trace_outputs = list(range(1, len(dims), 2))
    traced = partial_trace(comb, dims, trace_outputs)
    input_dim = int(np.prod(dims[::2]))
    return bool(np.allclose(traced, np.eye(input_dim, dtype=complex), atol=1e-8))


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
    """Estimate the BLP non-Markovianity measure on a time grid.

    The Breuer-Laine-Piilo measure integrates positive increases in trace
    distance, maximized over state pairs.  For qubit examples this function
    searches deterministic antipodal pure-state pairs on the Bloch sphere.
    """

    times = np.asarray(t_grid, dtype=float)
    if times.ndim != 1 or times.size < 2:
        raise ValueError("t_grid must be a one-dimensional grid with at least two points")

    best = 0.0
    for rho, sigma in _antipodal_qubit_pairs():
        distances = []
        for time in times:
            choi = channel_family(float(time))
            distances.append(trace_distance(apply_choi_channel(rho, choi), apply_choi_channel(sigma, choi)))
        increments = np.diff(distances)
        best = max(best, float(np.sum(increments[increments > 0.0])))
    return best


def rhp_measure(channel_family: Callable[[float], Array], t_grid: Array) -> float:
    """Estimate an RHP-style CP-divisibility violation on a time grid.

    For each adjacent pair of times, the intermediate map is reconstructed as
    ``E(t_{k+1}) E(t_k)^+`` in natural representation.  Negative eigenvalues
    of the intermediate Choi matrix are summed as a discrete divisibility
    witness.  A CP-divisible family gives zero up to numerical tolerance.
    """

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
        hermitian = 0.5 * (choi_intermediate + dagger(choi_intermediate))
        eigenvalues = np.linalg.eigvalsh(hermitian)
        total += float(np.sum(np.abs(eigenvalues[eigenvalues < -1e-8])) / d)
    return total
