"""Independent numerical checks for Validator-A.

This script imports producer modules read-only and checks representative
mathematical claims used in the validation report.
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[2]


def load_module(name: str, relative_path: str):
    path = ROOT / relative_path
    sys.path.insert(0, str(path.parent))
    try:
        spec = importlib.util.spec_from_file_location(name, path)
        if spec is None or spec.loader is None:
            raise RuntimeError(f"cannot load {relative_path}")
        module = importlib.util.module_from_spec(spec)
        sys.modules[name] = module
        spec.loader.exec_module(module)
        return module
    finally:
        sys.path.pop(0)


def main() -> None:
    np.set_printoptions(precision=6, suppress=True)

    theory = load_module("theory_channel_reps", "01_theory/channel_reps.py")
    qpt = load_module("agent2_qpt_tools", "02_ibm_experiment/qpt_tools.py")
    sdp = load_module("agent3_sdp_tools", "03_sdp_discrimination/sdp_tools.py")
    combs = load_module("agent4_combs_tools", "04_quantum_combs/combs_tools.py")
    dynamics = load_module("agent4_non_markovian_dynamics", "04_quantum_combs/non_markovian_dynamics.py")
    widget = load_module("agent5_widget_core", "05_interactive_widget/widget_core.py")

    print("Agent-1 round trip")
    kraus = theory.random_channel(2, 2, 3)
    choi = theory.kraus_to_choi(kraus)
    recovered = theory.choi_to_kraus(choi)
    rho = np.array([[0.7, 0.2 - 0.1j], [0.2 + 0.1j, 0.3]], dtype=complex)
    err = np.linalg.norm(theory.apply_channel(rho, kraus) - theory.apply_channel(rho, recovered))
    print(f"  Kraus -> Choi -> Kraus channel error: {err:.3e}")

    print("Agent-2 QPT and MLE")
    s_gate = np.diag([1.0, 1.0j])
    s_choi = qpt.choi_from_unitary(s_gate)
    data = {"output_states": qpt.simulate_output_states_from_choi(s_choi)}
    lin = qpt.linear_inversion_choi(data)
    mle = qpt.mle_choi(data, 2, 2)
    print(f"  linear inversion S-gate Choi error: {np.linalg.norm(lin - s_choi):.3e}")
    print(f"  MLE CP/TP: {qpt.is_cp(mle)} / {qpt.is_tp(mle, 2, 2)}")

    print("Agent-3 SDP")
    p0 = {"I": 1.0, "X": 0.0, "Y": 0.0, "Z": 0.0}
    p1 = {"I": 0.7, "X": 0.3, "Y": 0.0, "Z": 0.0}
    c0 = sdp.pauli_channel_choi(p0)
    c1 = sdp.pauli_channel_choi(p1)
    numerical = sdp.diamond_norm_sdp(c0 - c1, 2, 2)
    analytical = sdp.analytical_pauli_diamond_norm(p0, p1)
    print(f"  Pauli diamond norm numerical/analytical: {numerical:.6f} / {analytical:.6f}")
    print(f"  discrimination probability: {sdp.discrimination_probability(c0, c1):.6f}")

    print("Agent-4 non-Markovianity")
    times = np.linspace(0.0, 5.0, 60)
    markov = dynamics.markovian_dephasing_family(rate=0.4)
    revival = dynamics.oscillatory_dephasing_family(rate=0.12, frequency=2.4)
    print(f"  BLP Markovian/revival: {combs.blp_measure(markov, times):.6e} / {combs.blp_measure(revival, times):.6e}")
    print(f"  RHP Markovian/revival: {combs.rhp_measure(markov, times):.6e} / {combs.rhp_measure(revival, times):.6e}")
    comb = dynamics.collision_model_comb(theta=0.7, n_steps=2)
    print(f"  global comb trace condition: {combs.comb_partial_trace_check(comb, [2, 2, 2, 2])}")

    print("Agent-5 Bloch maps")
    depol = widget.get_channel_choi("Depolarizing", {"p": 0.2})
    depol_matrix, depol_offset = widget.bloch_affine_map(depol)
    amp = widget.get_channel_choi("Amplitude damping", {"gamma": 0.35})
    amp_matrix, amp_offset = widget.bloch_affine_map(amp)
    print(f"  depolarizing M diagonal: {np.diag(depol_matrix)} offset: {depol_offset}")
    print(f"  amplitude damping M diagonal: {np.diag(amp_matrix)} offset: {amp_offset}")


if __name__ == "__main__":
    main()
