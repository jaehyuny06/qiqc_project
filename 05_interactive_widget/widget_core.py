"""Interactive visualization core for qubit Choi matrices.

The public entry point is :func:`build_widget`, which returns an ipywidgets
dashboard.  All computations are local and simulator-free, so the deliverable
works without IBM Quantum credentials.
"""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.axes import Axes
from numpy.typing import NDArray

from channel_utils import (
    I2,
    PAULIS,
    amplitude_damping_kraus,
    bit_flip_kraus,
    depolarizing_kraus,
    identity_kraus,
    is_cp,
    is_tp,
    kraus_to_choi,
    mixed_choi,
    partial_trace_output,
    pauli_kraus,
    phase_damping_kraus,
    phase_flip_kraus,
    unital_choi,
)


Array = NDArray[np.complex128]
PALETTE: dict[str, str] = {
    "blue": "#2563eb",
    "green": "#16a34a",
    "orange": "#f97316",
    "red": "#dc2626",
    "purple": "#7c3aed",
    "gray": "#475569",
}

CHANNEL_TYPES: tuple[str, ...] = (
    "Depolarizing",
    "Amplitude damping",
    "Phase damping",
    "Bit flip",
    "Phase flip",
    "Pauli",
    "Unital",
    "Mix two channels",
)


def get_channel_choi(channel_type: str, params: Mapping[str, Any] | None = None) -> Array:
    """Return a qubit Choi matrix for the requested channel.

    Parameters
    ----------
    channel_type:
        Human-readable channel type.
    params:
        Channel parameters.  Missing values are replaced with educational
        defaults so the widget always has a valid first render.

    Returns
    -------
    numpy.ndarray
        ``4 x 4`` Choi matrix in the input-first convention.
    """
    params = dict(params or {})
    normalized = channel_type.strip().lower().replace("_", " ")
    if normalized == "identity":
        return kraus_to_choi(identity_kraus())
    if normalized == "depolarizing":
        return kraus_to_choi(depolarizing_kraus(float(params.get("p", 0.2))))
    if normalized == "amplitude damping":
        return kraus_to_choi(amplitude_damping_kraus(float(params.get("gamma", 0.25))))
    if normalized == "phase damping":
        return kraus_to_choi(phase_damping_kraus(float(params.get("gamma", 0.25))))
    if normalized == "bit flip":
        return kraus_to_choi(bit_flip_kraus(float(params.get("p", 0.2))))
    if normalized == "phase flip":
        return kraus_to_choi(phase_flip_kraus(float(params.get("p", 0.2))))
    if normalized == "pauli":
        return kraus_to_choi(
            pauli_kraus(
                float(params.get("p_x", 0.08)),
                float(params.get("p_y", 0.04)),
                float(params.get("p_z", 0.12)),
            )
        )
    if normalized == "unital":
        return unital_choi(
            float(params.get("lambda_x", 0.75)),
            float(params.get("lambda_y", 0.55)),
            float(params.get("lambda_z", 0.35)),
        )
    if normalized == "mix two channels":
        channel_a = str(params.get("channel_a", "Depolarizing"))
        channel_b = str(params.get("channel_b", "Amplitude damping"))
        if channel_a == "Mix two channels":
            channel_a = "Depolarizing"
        if channel_b == "Mix two channels":
            channel_b = "Amplitude damping"
        choi_a = get_channel_choi(channel_a, params)
        choi_b = get_channel_choi(channel_b, params)
        return mixed_choi(choi_a, choi_b, float(params.get("alpha", 0.5)))
    raise ValueError(f"Unsupported channel type: {channel_type!r}")


def plot_choi_heatmap(choi: Array, ax_real: Axes, ax_imag: Axes) -> None:
    """Plot real and imaginary parts of a Choi matrix.

    Parameters
    ----------
    choi:
        Choi matrix to visualize.
    ax_real, ax_imag:
        Matplotlib axes for the real and imaginary heatmaps.
    """
    vmax = max(1e-12, float(np.max(np.abs([choi.real, choi.imag]))))
    for ax, values, title in (
        (ax_real, choi.real, "Re(C)"),
        (ax_imag, choi.imag, "Im(C)"),
    ):
        image = ax.imshow(values, cmap="RdBu_r", vmin=-vmax, vmax=vmax)
        ax.set_title(title)
        ax.set_xticks(range(choi.shape[0]))
        ax.set_yticks(range(choi.shape[0]))
        ax.figure.colorbar(image, ax=ax, fraction=0.046, pad=0.04)


def plot_bloch_ellipsoid(choi: Array, ax_3d: Axes) -> None:
    """Plot the image of the Bloch sphere under a qubit channel.

    Parameters
    ----------
    choi:
        Qubit Choi matrix.
    ax_3d:
        Three-dimensional Matplotlib axis.
    """
    matrix, offset = bloch_affine_map(choi)
    theta = np.linspace(0, 2.0 * np.pi, 40)
    phi = np.linspace(0, np.pi, 20)
    x = np.outer(np.cos(theta), np.sin(phi))
    y = np.outer(np.sin(theta), np.sin(phi))
    z = np.outer(np.ones_like(theta), np.cos(phi))
    points = np.stack([x, y, z], axis=0).reshape(3, -1)
    transformed = (matrix @ points + offset[:, None]).reshape(3, *x.shape)

    ax_3d.plot_wireframe(
        transformed[0],
        transformed[1],
        transformed[2],
        rstride=2,
        cstride=2,
        color=PALETTE["blue"],
        linewidth=0.6,
        alpha=0.75,
    )
    ax_3d.scatter([offset[0]], [offset[1]], [offset[2]], color=PALETTE["orange"], s=30)
    ax_3d.set_title("Bloch deformation")
    ax_3d.set_xlabel("x")
    ax_3d.set_ylabel("y")
    ax_3d.set_zlabel("z")
    ax_3d.set_xlim(-1.05, 1.05)
    ax_3d.set_ylim(-1.05, 1.05)
    ax_3d.set_zlim(-1.05, 1.05)
    try:
        ax_3d.set_box_aspect((1, 1, 1))
    except AttributeError:
        pass


def extract_kraus_display(choi: Array) -> list[tuple[float, Array]]:
    """Return Choi eigenweights and eigenoperators for display.

    Parameters
    ----------
    choi:
        Choi matrix.

    Returns
    -------
    list[tuple[float, numpy.ndarray]]
        Pairs of ``(eigenvalue, eigenoperator)`` sorted descending.  For CP
        maps these are Kraus operators; negative weights indicate a non-CP map
        and are retained for diagnostic display.
    """
    hermitian = 0.5 * (choi + choi.conj().T)
    eigvals, eigvecs = np.linalg.eigh(hermitian)
    order = np.argsort(eigvals)[::-1]
    pairs: list[tuple[float, Array]] = []
    for idx in order:
        weight = float(np.real(eigvals[idx]))
        if abs(weight) <= 1e-10:
            continue
        vector = eigvecs[:, idx]
        kraus = np.sqrt(abs(weight)) * vector.reshape(2, 2).T
        pairs.append((weight, kraus.astype(complex)))
    return pairs


def plot_eigenspectrum(choi: Array, ax: Axes) -> None:
    """Plot Choi eigenvalues as a bar chart.

    Parameters
    ----------
    choi:
        Choi matrix.
    ax:
        Matplotlib axis.
    """
    eigvals = np.linalg.eigvalsh(0.5 * (choi + choi.conj().T))
    eigvals = np.sort(np.real(eigvals))[::-1]
    colors = [PALETTE["green"] if val >= -1e-9 else PALETTE["red"] for val in eigvals]
    ax.bar(range(1, len(eigvals) + 1), eigvals, color=colors)
    ax.axhline(0.0, color="#111827", linewidth=0.8)
    ax.set_title("Choi eigenspectrum")
    ax.set_xlabel("index")
    ax.set_ylabel("eigenvalue")
    ax.set_xticks(range(1, len(eigvals) + 1))


def compute_indicators(choi: Array) -> dict[str, float | bool | int]:
    """Compute status and fidelity indicators for a qubit channel.

    Parameters
    ----------
    choi:
        Choi matrix.

    Returns
    -------
    dict
        CP/TP flags, rank, process fidelities, trace, TP residual, and minimum
        Choi eigenvalue.
    """
    hermitian = 0.5 * (choi + choi.conj().T)
    eigvals = np.linalg.eigvalsh(hermitian)
    identity_choi = get_channel_choi("Identity", {})
    process_fidelity_identity = float(np.real(np.trace(choi @ identity_choi)) / 4.0)

    matrix, _ = bloch_affine_map(choi)
    mean_shrink = float(np.trace(matrix).real / 3.0)
    depol_p = float(np.clip(0.75 * (1.0 - mean_shrink), 0.0, 1.0))
    depol_choi = get_channel_choi("Depolarizing", {"p": depol_p})
    process_fidelity_depolarized = float(np.real(np.trace(choi @ depol_choi)) / 4.0)
    tp_residual = float(np.linalg.norm(partial_trace_output(choi) - I2))

    return {
        "is_cp": is_cp(choi),
        "is_tp": is_tp(choi),
        "rank": int(np.sum(eigvals > 1e-9)),
        "trace": float(np.real(np.trace(choi))),
        "min_eigenvalue": float(np.min(np.real(eigvals))),
        "tp_residual": tp_residual,
        "process_fidelity_identity": float(np.clip(process_fidelity_identity, -1.0, 1.0)),
        "process_fidelity_depolarized": float(
            np.clip(process_fidelity_depolarized, -1.0, 1.0)
        ),
        "nearest_depolarizing_p": depol_p,
    }


def build_widget() -> Any:
    """Build the synchronized ipywidgets dashboard.

    Returns
    -------
    ipywidgets.Widget
        A VBox containing controls and live visualization output.
    """
    import ipywidgets as widgets
    from IPython.display import clear_output, display

    style = {"description_width": "120px"}
    channel = widgets.Dropdown(options=CHANNEL_TYPES, value="Depolarizing", description="Channel", style=style)
    channel_a = widgets.Dropdown(
        options=CHANNEL_TYPES[:-1], value="Depolarizing", description="Mix A", style=style
    )
    channel_b = widgets.Dropdown(
        options=CHANNEL_TYPES[:-1], value="Amplitude damping", description="Mix B", style=style
    )
    p = widgets.FloatSlider(value=0.2, min=0.0, max=1.0, step=0.01, description="p", readout_format=".2f", style=style)
    gamma = widgets.FloatSlider(
        value=0.25, min=0.0, max=1.0, step=0.01, description="gamma", readout_format=".2f", style=style
    )
    p_x = widgets.FloatSlider(value=0.08, min=0.0, max=1.0, step=0.01, description="p_X", readout_format=".2f", style=style)
    p_y = widgets.FloatSlider(value=0.04, min=0.0, max=1.0, step=0.01, description="p_Y", readout_format=".2f", style=style)
    p_z = widgets.FloatSlider(value=0.12, min=0.0, max=1.0, step=0.01, description="p_Z", readout_format=".2f", style=style)
    lambda_x = widgets.FloatSlider(
        value=0.75, min=-1.0, max=1.0, step=0.01, description="lambda_x", readout_format=".2f", style=style
    )
    lambda_y = widgets.FloatSlider(
        value=0.55, min=-1.0, max=1.0, step=0.01, description="lambda_y", readout_format=".2f", style=style
    )
    lambda_z = widgets.FloatSlider(
        value=0.35, min=-1.0, max=1.0, step=0.01, description="lambda_z", readout_format=".2f", style=style
    )
    alpha = widgets.FloatSlider(
        value=0.5, min=0.0, max=1.0, step=0.01, description="mix alpha", readout_format=".2f", style=style
    )
    output = widgets.Output()

    controls = widgets.VBox(
        [
            widgets.HBox([channel, channel_a, channel_b]),
            widgets.HBox([p, gamma, alpha]),
            widgets.HBox([p_x, p_y, p_z]),
            widgets.HBox([lambda_x, lambda_y, lambda_z]),
        ]
    )

    def render(_: Any | None = None) -> None:
        params = {
            "p": p.value,
            "gamma": gamma.value,
            "p_x": p_x.value,
            "p_y": p_y.value,
            "p_z": p_z.value,
            "lambda_x": lambda_x.value,
            "lambda_y": lambda_y.value,
            "lambda_z": lambda_z.value,
            "alpha": alpha.value,
            "channel_a": channel_a.value,
            "channel_b": channel_b.value,
        }
        with output:
            clear_output(wait=True)
            try:
                choi = get_channel_choi(channel.value, params)
            except ValueError as exc:
                print(f"Parameter error: {exc}")
                return
            fig = render_dashboard_figure(choi, channel.value)
            display(fig)
            plt.close(fig)
            print(format_indicator_text(compute_indicators(choi)))

    for control in (
        channel,
        channel_a,
        channel_b,
        p,
        gamma,
        p_x,
        p_y,
        p_z,
        lambda_x,
        lambda_y,
        lambda_z,
        alpha,
    ):
        control.observe(render, names="value")
    render()
    return widgets.VBox([controls, output])


def bloch_affine_map(choi: Array) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
    """Compute the affine Bloch map ``r -> M r + t``.

    Parameters
    ----------
    choi:
        Qubit Choi matrix.

    Returns
    -------
    tuple[numpy.ndarray, numpy.ndarray]
        Real ``3 x 3`` matrix and real length-3 translation vector.
    """
    output_identity = apply_choi_to_state(choi, I2 / 2.0)
    offset = np.array([np.real(np.trace(output_identity @ pauli)) for pauli in PAULIS])
    matrix = np.zeros((3, 3), dtype=float)
    for column, pauli_in in enumerate(PAULIS):
        rho = (I2 + pauli_in) / 2.0
        out = apply_choi_to_state(choi, rho)
        bloch = np.array([np.real(np.trace(out @ pauli_out)) for pauli_out in PAULIS])
        matrix[:, column] = bloch - offset
    return matrix, offset


def apply_choi_to_state(choi: Array, rho: Array) -> Array:
    """Apply a qubit map directly from its Choi matrix.

    Parameters
    ----------
    choi:
        Choi matrix using the input-first convention.
    rho:
        Qubit input density matrix.

    Returns
    -------
    numpy.ndarray
        Channel output, computed linearly from Choi blocks.
    """
    blocks = np.asarray(choi, dtype=complex).reshape(2, 2, 2, 2)
    output = np.einsum("ij,ibjo->bo", np.asarray(rho, dtype=complex), blocks)
    return 0.5 * (output + output.conj().T)


def render_dashboard_figure(choi: Array, title: str = "Channel") -> plt.Figure:
    """Create a static dashboard figure for notebooks and README previews.

    Parameters
    ----------
    choi:
        Choi matrix to visualize.
    title:
        Figure title.

    Returns
    -------
    matplotlib.figure.Figure
        Dashboard-style figure.
    """
    fig = plt.figure(figsize=(13, 8), constrained_layout=True)
    grid = fig.add_gridspec(2, 3)
    ax_real = fig.add_subplot(grid[0, 0])
    ax_imag = fig.add_subplot(grid[0, 1])
    ax_bloch = fig.add_subplot(grid[:, 2], projection="3d")
    ax_eigs = fig.add_subplot(grid[1, 0])
    ax_text = fig.add_subplot(grid[1, 1])

    plot_choi_heatmap(choi, ax_real, ax_imag)
    plot_bloch_ellipsoid(choi, ax_bloch)
    plot_eigenspectrum(choi, ax_eigs)
    draw_kraus_table(choi, ax_text)
    fig.suptitle(title, fontsize=15)
    return fig


def draw_kraus_table(choi: Array, ax: Axes) -> None:
    """Draw a compact text table of Kraus weights and operators.

    Parameters
    ----------
    choi:
        Choi matrix.
    ax:
        Matplotlib axis used as a text canvas.
    """
    ax.axis("off")
    rows = ["Choi eigenoperators"]
    for idx, (weight, op) in enumerate(extract_kraus_display(choi)[:4], start=1):
        tag = "non-CP" if weight < -1e-10 else "Kraus"
        rows.append(f"{tag} {idx}, weight={weight:.4f}")
        rows.append(np.array2string(np.round(op, 3), precision=3, suppress_small=True))
    ax.text(0.0, 1.0, "\n".join(rows), va="top", ha="left", family="monospace", fontsize=9)


def format_indicator_text(indicators: Mapping[str, float | bool | int]) -> str:
    """Format computed indicators for notebook display.

    Parameters
    ----------
    indicators:
        Dictionary returned by :func:`compute_indicators`.

    Returns
    -------
    str
        Human-readable one-block summary.
    """
    cp = "yes" if indicators["is_cp"] else "no"
    tp = "yes" if indicators["is_tp"] else "no"
    return (
        f"CP: {cp} | TP: {tp} | rank: {indicators['rank']} | "
        f"trace(C): {indicators['trace']:.6f} | min eig: {indicators['min_eigenvalue']:.3e}\n"
        f"TP residual: {indicators['tp_residual']:.3e} | "
        f"F_process(identity): {indicators['process_fidelity_identity']:.6f} | "
        f"F_process(depol fit p={indicators['nearest_depolarizing_p']:.3f}): "
        f"{indicators['process_fidelity_depolarized']:.6f}"
    )


if __name__ == "__main__":
    demo = get_channel_choi("Amplitude damping", {"gamma": 0.35})
    fig = render_dashboard_figure(demo, "Amplitude damping preview")
    fig.savefig("figures/widget_preview.png", dpi=160)
