# Migration Plan

This is a proposal only. No producer files should change until the common API is reviewed and accepted.

## Global Decisions Before Implementation

1. Standard Choi convention remains unnormalized input-first:
   `C_E = sum_ij |i><j|_A tensor E(|i><j|)_B`.
2. Standard Choi application is:
   `apply_choi_channel(choi, rho, d_in=None, d_out=None)`.
3. Standard TP check is:
   `is_tp(choi, d_in, d_out=None, tol=1e-9)`.
4. Standard depolarizing default should be replacement probability:
   `E_p(rho) = (1-p)rho + p Tr(rho) I/d`.
5. Agent 2 and Agent 5 currently use Pauli-error depolarizing probability. Their migrations must pass `convention="pauli_error"` or use compatibility wrappers.

## Agent 1: `01_theory`

Current notebook import:

```python
from channel_reps import (
    amplitude_damping_channel,
    apply_channel,
    bit_flip_channel,
    choi_rank,
    choi_to_kraus,
    choi_to_natural,
    compose_channels_choi,
    depolarizing_channel,
    identity_channel,
    is_cp,
    is_tp,
    is_unital,
    kraus_to_choi,
    kraus_to_stinespring,
    natural_to_choi,
    pauli_channel,
    phase_damping_channel,
    phase_flip_channel,
    random_channel,
    stinespring_to_kraus,
)
```

Proposed common imports:

```python
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
    compose_choi_channels,
    kraus_to_choi,
    kraus_to_stinespring,
    natural_to_choi,
    stinespring_to_kraus,
)
from choi_common.validation import choi_rank, is_cp, is_tp, is_unital
```

Needed call-site changes:

- `apply_channel(rho, kraus_ops)` -> `apply_kraus_channel(rho, kraus_ops)`.
- `compose_channels_choi(choi1, choi2)` currently returns `E2 o E1`; migrate to `compose_choi_channels(choi_after=choi2, choi_before=choi1)` or keep a local compatibility wrapper.
- `random_channel` is not duplicated. Either keep in `channel_reps.py` or add later to `choi_common.channels` only if multiple folders need it.
- `is_tp(choi, d_in=2)` remains valid with the proposed signature.

## Agent 2: `02_ibm_experiment`

Current notebook import:

```python
from qpt_tools import (
    amplitude_damping_after_unitary,
    choi_from_unitary,
    depolarizing_after_unitary,
    diagnose_noise,
    is_cp,
    is_tp,
    linear_inversion_choi,
    matrix_to_json_dict,
    mle_choi,
    plot_bloch_deformation,
    plot_choi_heatmap,
    save_json,
    simulate_output_states_from_choi,
    two_qubit_depolarizing_after_unitary,
)
```

Proposed common imports for shared functions:

```python
from choi_common.channels import (
    amplitude_damping_after_unitary,
    depolarizing_after_unitary,
    two_qubit_depolarizing_after_unitary,
    unitary_channel_choi,
)
from choi_common.validation import is_cp, is_tp
from choi_common.visualization import plot_bloch_deformation, plot_choi_heatmap
```

Keep local in `qpt_tools.py` for now:

```python
from qpt_tools import (
    diagnose_noise,
    linear_inversion_choi,
    matrix_to_json_dict,
    mle_choi,
    save_json,
    simulate_output_states_from_choi,
)
```

Needed call-site changes:

- `choi_from_unitary(U)` -> `unitary_channel_choi(U)`, unless `qpt_tools.py` keeps a compatibility alias.
- `depolarizing_after_unitary(U, p)` should call common `depolarizing_after_unitary(U, p, convention="pauli_error")` to preserve current Agent-2 behavior.
- `plot_choi_heatmap(choi, title)` may become `plot_choi_heatmap(choi, title=title)` if the common visualization API uses keyword-only options.
- `is_tp(choi, d_in=2, d_out=2)` remains valid.

Recommended migration style:

- First change `qpt_tools.py` internals to import from `choi_common` and keep the old function names as wrappers.
- Then update the notebook only after tests pass. This avoids breaking saved educational notebooks immediately.

## Agent 3: `03_sdp_discrimination`

Current notebook import:

```python
import sdp_tools as sdp
```

Proposed implementation-level imports inside `sdp_tools.py`:

```python
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
from choi_common.validation import is_cp, is_tp
```

Needed call-site changes:

- The notebook can continue `import sdp_tools as sdp` if `sdp_tools.py` remains an Agent-3 facade.
- If migrating directly to common imports, calls such as `sdp.depolarizing_channel_choi(p)` become `depolarizing_channel_choi(p)`.
- Agent 3's `depolarizing_channel_choi(p)` already matches the proposed default `convention="replacement"`, so no parameter change is needed.
- `diamond_norm_sdp(choi_diff, d_in, d_out)` remains valid. The common version should preserve optional solver parameters without requiring them.

Keep local in `sdp_tools.py` for now:

- `optimal_input_state`
- `optimal_povm`
- `tensor_power_choi`
- `n_shot_discrimination`
- `product_strategy_discrimination`

These are Agent-3-specific discrimination workflows, even though they can call common metrics and representation helpers.

## Agent 4: `04_quantum_combs`

Current notebook import:

```python
from combs_tools import (
    apply_choi_channel,
    blp_measure,
    choi_to_natural,
    comb_global_trace_preservation_check,
    deterministic_comb_causality_check,
    is_markovian,
    marginal_channel,
    natural_to_choi,
    rhp_measure,
    trace_distance,
)
```

Proposed common imports for shared functions:

```python
from choi_common.metrics import trace_distance
from choi_common.representations import (
    apply_choi_channel,
    choi_to_natural,
    natural_to_choi,
)
from choi_common.validation import partial_trace
```

Keep local in `combs_tools.py` for now:

```python
from combs_tools import (
    blp_measure,
    comb_global_trace_preservation_check,
    deterministic_comb_causality_check,
    is_markovian,
    marginal_channel,
    rhp_measure,
)
```

Needed call-site changes:

- Notebook calls to `apply_choi_channel(choi, rho)` remain valid.
- Notebook calls to `choi_to_natural(C, 2, 2)` and `natural_to_choi(S, 2, 2)` remain valid.
- `partial_trace` is not imported by the notebook now, but `combs_tools.py` can import it from common during implementation.
- `apply_choi_channel_legacy(rho, choi, ...)` should remain only as a local compatibility wrapper if still needed.

## Agent 5: `05_interactive_widget`

Current notebook import:

```python
from widget_core import (
    CHANNEL_TYPES,
    apply_choi_channel,
    build_widget,
    compute_indicators,
    format_indicator_text,
    get_channel_choi,
    render_dashboard_figure,
)
```

The notebook can keep importing from `widget_core.py`. The internal migration should replace `channel_utils.py` math with common imports.

Current `widget_core.py` imports from `channel_utils.py`:

```python
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
```

Proposed common imports:

```python
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
from choi_common.representations import apply_choi_channel, kraus_to_choi
from choi_common.validation import is_cp, is_tp, partial_trace_output
```

Needed call-site changes:

- `identity_kraus()` -> `identity_channel(2)`.
- `depolarizing_kraus(p)` -> `depolarizing_channel(p, d=2, convention="pauli_error")` to preserve current widget slider semantics.
- `amplitude_damping_kraus(gamma)` -> `amplitude_damping_channel(gamma)`.
- `phase_damping_kraus(gamma)` -> `phase_damping_channel(gamma)`.
- `bit_flip_kraus(p)` -> `bit_flip_channel(p)`.
- `phase_flip_kraus(p)` -> `phase_flip_channel(p)`.
- `pauli_kraus(p_x, p_y, p_z)` -> `pauli_channel(p_x, p_y, p_z)`.
- `unital_choi(...)` -> `unital_qubit_channel_choi(...)`.
- `partial_trace_output(choi)` -> `partial_trace_output(choi, d_in=2, d_out=2)`.
- `is_tp(choi)` -> `is_tp(choi, d_in=2, d_out=2)`.
- `PAULIS` can be derived as `(pauli_matrices()["X"], pauli_matrices()["Y"], pauli_matrices()["Z"])`.
- `I2` can be `pauli_matrices()["I"]`.

Keep local in `widget_core.py` for now:

- `CHANNEL_TYPES`
- `get_channel_choi`
- `build_widget`
- `compute_indicators`
- `format_indicator_text`
- `render_dashboard_figure`
- Widget-specific plotting composition, unless later moved to `choi_common.visualization`.

## Proposed Compatibility Strategy

During Step 4.2 implementation, avoid migrating notebooks and producer code in one large jump. Safer sequence:

1. Implement root-level `choi_common`.
2. Add tests for cross-folder equivalence, especially `kraus_to_choi`, natural conversion round trips, `is_tp`, and depolarizing parameter conventions.
3. Update producer modules to import from `choi_common` internally while preserving old public names.
4. Update notebooks to direct common imports only where that improves clarity.
5. Remove compatibility wrappers later only after notebooks and tests no longer use them.

## Signature Change Checklist

- `apply_channel` should become `apply_kraus_channel`.
- `compose_channels_choi(choi1, choi2)` should become `compose_choi_channels(choi_after, choi_before)` or use named arguments.
- `is_tp(choi)` in Agent 5 should become `is_tp(choi, d_in=2, d_out=2)`.
- `partial_trace_output(choi)` in Agent 5 should become `partial_trace_output(choi, d_in=2, d_out=2)`.
- `choi_from_unitary` should become `unitary_channel_choi`.
- `depolarizing_kraus(p)` and `depolarizing_after_unitary(U, p)` need explicit `convention="pauli_error"` if the slider/example semantics are preserved.
- `plot_choi_heatmap(choi, title)` may need `title=` depending on the final common visualization API.
