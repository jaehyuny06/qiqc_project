"""Visualization helpers for Choi matrices and qubit Bloch maps."""

from __future__ import annotations

from collections.abc import Sequence
from typing import Any

import numpy as np
from numpy.typing import NDArray

from .channels import pauli_matrices
from .representations import apply_choi_channel
from .utils import hermitian_part


Array = NDArray[np.complex128]


def plot_choi_heatmap(
    choi: np.ndarray,
    *,
    title: str | None = None,
    axes: Sequence[Any] | None = None,
    include_abs: bool = True,
) -> Any:
    """Plot real, imaginary, and optionally magnitude Choi heatmaps."""
    import matplotlib.pyplot as plt

    c = np.asarray(choi, dtype=np.complex128)
    panel_specs = [(c.real, "Real", "RdBu_r"), (c.imag, "Imag", "RdBu_r")]
    if include_abs:
        panel_specs.append((np.abs(c), "Abs", "viridis"))

    if axes is None:
        fig, axes_obj = plt.subplots(1, len(panel_specs), figsize=(3.7 * len(panel_specs), 3.2), constrained_layout=True)
        axes_list = list(np.atleast_1d(axes_obj))
    else:
        axes_list = list(axes)
        if len(axes_list) < len(panel_specs):
            raise ValueError("Not enough axes provided for requested Choi panels.")
        fig = axes_list[0].figure

    for ax, (matrix, subtitle, cmap) in zip(axes_list, panel_specs, strict=False):
        vmax = max(float(np.max(np.abs(matrix))), 1e-12)
        vmin = -vmax if subtitle != "Abs" else 0.0
        image = ax.imshow(matrix, cmap=cmap, vmin=vmin, vmax=vmax)
        ax.set_title(subtitle)
        ax.set_xlabel("column")
        ax.set_ylabel("row")
        fig.colorbar(image, ax=ax, fraction=0.046, pad=0.04)
    if title is not None:
        fig.suptitle(title)
    return fig


def bloch_affine_map(choi: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """Return the qubit affine Bloch map ``r -> M r + t`` for a Choi matrix."""
    c = np.asarray(choi, dtype=np.complex128)
    if c.shape != (4, 4):
        raise ValueError("Bloch affine map is implemented only for one-qubit Choi matrices.")
    paulis = pauli_matrices()
    i2 = paulis["I"]
    xyz = (paulis["X"], paulis["Y"], paulis["Z"])
    output_identity = apply_choi_channel(c, i2 / 2.0, d_in=2, d_out=2)
    offset = np.array([np.real(np.trace(output_identity @ pauli)) for pauli in xyz], dtype=float)
    matrix = np.zeros((3, 3), dtype=float)
    for column, pauli_in in enumerate(xyz):
        rho = (i2 + pauli_in) / 2.0
        out = apply_choi_channel(c, rho, d_in=2, d_out=2)
        bloch = np.array([np.real(np.trace(out @ pauli_out)) for pauli_out in xyz], dtype=float)
        matrix[:, column] = bloch - offset
    return matrix, offset


def choi_to_pauli_transfer(choi: np.ndarray) -> Array:
    """Return the one-qubit Pauli transfer matrix for a Choi matrix."""
    c = np.asarray(choi, dtype=np.complex128)
    if c.shape != (4, 4):
        raise ValueError("Pauli transfer helper is implemented for one qubit.")
    paulis = pauli_matrices()
    basis = [paulis[label] for label in ("I", "X", "Y", "Z")]
    transfer = np.zeros((4, 4), dtype=np.float64)
    for i, p_i in enumerate(basis):
        for j, p_j in enumerate(basis):
            transfer[i, j] = 0.5 * np.trace(p_i @ apply_choi_channel(c, p_j, d_in=2, d_out=2)).real
    return transfer.astype(np.complex128)


def plot_bloch_deformation(choi: np.ndarray, ax: Any | None = None) -> Any:
    """Plot the image of the Bloch sphere under a one-qubit channel."""
    import matplotlib.pyplot as plt

    matrix, offset = bloch_affine_map(choi)
    if ax is None:
        fig = plt.figure(figsize=(6.5, 5.2))
        ax = fig.add_subplot(111, projection="3d")
    theta = np.linspace(0, 2.0 * np.pi, 40)
    phi = np.linspace(0, np.pi, 20)
    x = np.outer(np.cos(theta), np.sin(phi))
    y = np.outer(np.sin(theta), np.sin(phi))
    z = np.outer(np.ones_like(theta), np.cos(phi))
    points = np.stack([x, y, z], axis=0).reshape(3, -1)
    transformed = (matrix @ points + offset[:, None]).reshape(3, *x.shape)
    ax.plot_wireframe(transformed[0], transformed[1], transformed[2], rstride=2, cstride=2, color="#2563eb", linewidth=0.6, alpha=0.75)
    ax.scatter([offset[0]], [offset[1]], [offset[2]], color="#f97316", s=30)
    ax.set_title("Bloch deformation")
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_zlabel("z")
    ax.set_xlim(-1.05, 1.05)
    ax.set_ylim(-1.05, 1.05)
    ax.set_zlim(-1.05, 1.05)
    try:
        ax.set_box_aspect((1, 1, 1))
    except AttributeError:
        pass
    return ax.figure


def plot_eigenspectrum(choi: np.ndarray, ax: Any | None = None, tol: float = 1e-9) -> Any:
    """Plot the eigenvalues of the Hermitian part of a Choi matrix."""
    import matplotlib.pyplot as plt

    if ax is None:
        fig, ax = plt.subplots(figsize=(4.5, 3.2), constrained_layout=True)
    eigvals = np.linalg.eigvalsh(hermitian_part(choi))
    eigvals = np.sort(np.real(eigvals))[::-1]
    colors = ["#16a34a" if val >= -tol else "#dc2626" for val in eigvals]
    ax.bar(range(1, len(eigvals) + 1), eigvals, color=colors)
    ax.axhline(0.0, color="#111827", linewidth=0.8)
    ax.set_title("Choi eigenspectrum")
    ax.set_xlabel("index")
    ax.set_ylabel("eigenvalue")
    ax.set_xticks(range(1, len(eigvals) + 1))
    return ax.figure


def extract_kraus_display(choi: np.ndarray, tol: float = 1e-10) -> list[tuple[float, Array]]:
    """Return Choi eigenweights and eigenoperators for diagnostic display."""
    c = np.asarray(choi, dtype=np.complex128)
    d = int(round(np.sqrt(c.shape[0])))
    if c.shape != (d * d, d * d):
        raise ValueError("extract_kraus_display currently supports square channels.")
    eigvals, eigvecs = np.linalg.eigh(hermitian_part(c))
    order = np.argsort(eigvals)[::-1]
    pairs: list[tuple[float, Array]] = []
    for idx in order:
        weight = float(np.real(eigvals[idx]))
        if abs(weight) <= tol:
            continue
        vector = eigvecs[:, idx]
        operator = np.sqrt(abs(weight)) * vector.reshape(d, d).T
        pairs.append((weight, operator.astype(np.complex128)))
    return pairs
