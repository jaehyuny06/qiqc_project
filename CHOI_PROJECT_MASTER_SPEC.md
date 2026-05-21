# Choi Representation of Quantum Channels — Multi-Agent Project Specification

> **For Codex / Coding Agents**: This document specifies a multi-agent parallel workflow for a quantum computing course project. The workflow has **two layers**:
> - **Producer Layer**: 5 agents work in parallel, each in their own folder, on different sub-topics (Agent-1 through Agent-5).
> - **Validator Layer**: 3 agents review the producers' outputs across three dimensions — mathematics, code quality, and consistency (Validator-A through Validator-C).
>
> Validators do **not** rewrite producer code; they generate review reports that drive a revision round. Final integration happens in a later phase and is out of scope for this specification.

---

## 0. Project Overview

### 0.1 Topic
**Choi Representation of Quantum Channels** — exploring how the Choi-Jamiołkowski isomorphism represents quantum channels as matrices, how this representation reveals physical properties of channels, and how it enables practical computations across quantum information science.

### 0.2 Core Theoretical Foundation (shared context for all agents)
A quantum channel $\mathcal{E}: \mathcal{L}(\mathcal{H}_A) \to \mathcal{L}(\mathcal{H}_B)$ has multiple equivalent representations:

- **Kraus form**: $\mathcal{E}(\rho) = \sum_k K_k \rho K_k^\dagger$ with $\sum_k K_k^\dagger K_k = I$
- **Choi matrix**: $C_\mathcal{E} = (\mathcal{E} \otimes \mathcal{I})(|\Omega\rangle\langle\Omega|)$ where $|\Omega\rangle = \sum_i |i\rangle|i\rangle$
- **Stinespring dilation**: $\mathcal{E}(\rho) = \text{Tr}_E[U(\rho \otimes |0\rangle\langle 0|_E)U^\dagger]$
- **Natural (Liouville) form**: superoperator on vectorized density matrices

Key properties of the Choi matrix:
- $\mathcal{E}$ is **CP** $\iff C_\mathcal{E} \succeq 0$
- $\mathcal{E}$ is **TP** $\iff \text{Tr}_B(C_\mathcal{E}) = I_A$
- $\text{rank}(C_\mathcal{E})$ = minimum number of Kraus operators

### 0.3 Team Structure (5 producers + 3 validators)

**Producer Layer** (work in parallel, first phase):
| Agent ID | Folder | Sub-task |
|----------|--------|----------|
| Agent-1 | `01_theory/` | Theoretical foundations & channel representations |
| Agent-2 | `02_ibm_experiment/` | IBM Quantum process tomography |
| Agent-3 | `03_sdp_discrimination/` | SDP for channel discrimination |
| Agent-4 | `04_quantum_combs/` | Non-Markovian dynamics & quantum combs |
| Agent-5 | `05_interactive_widget/` | Interactive visualization widget |

**Validator Layer** (work in parallel, second phase, after all producers finish):
| Agent ID | Folder | Review Focus |
|----------|--------|--------------|
| Validator-A | `90_validation_math/` | Mathematical & physical correctness |
| Validator-B | `91_validation_code/` | Code quality, bugs, reproducibility |
| Validator-C | `92_validation_consistency/` | Cross-folder notation, style, terminology |

### 0.3.1 Two-Phase Workflow
1. **Phase 1 — Production**: Agent-1 through Agent-5 run in parallel. Each produces a complete deliverable in their folder.
2. **Phase 2 — Validation**: Validator-A, B, C run in parallel. Each reads all 5 producer folders and writes review reports.
3. **Phase 3 — Revision** (handled by user + producers): Each producer addresses the issues flagged in the validation reports.
4. **Phase 4 — Integration** (out of scope for this document): Merging into unified report and presentation.

### 0.4 Common Deliverable Format
Every agent produces:
1. **Primary Jupyter notebook** (`main.ipynb`) — complete narrative with theory, code, results, and visualizations
2. **Supporting Python modules** (`*.py`) — reusable functions imported by the notebook
3. **README.md** — sub-task summary, key results, dependencies, run instructions
4. **`requirements.txt`** — Python dependencies specific to this sub-task

### 0.5 Shared Conventions (all agents must follow)
- **Language**: Python 3.10+
- **Core libraries**: NumPy, SciPy, Matplotlib
- **Quantum libraries**: Qiskit ≥ 1.0 (preferred) or QuTiP 5+ as fallback
- **Code style**: type hints on all public functions, docstrings in NumPy format
- **Notation**: Choi matrix is `(d_A * d_B) × (d_A * d_B)` matrix; we use the convention $C_\mathcal{E} = \sum_{ij} |i\rangle\langle j| \otimes \mathcal{E}(|i\rangle\langle j|)$ (i.e., system A is the *first* tensor factor)
- **Reproducibility**: every notebook sets `np.random.seed(42)` at start
- **Visualizations**: use a shared color palette (specify hex codes in each notebook header)

### 0.6 Independence Rule
**Each agent works completely independently in its own folder.** No agent imports from another agent's folder. If a function is needed by multiple agents (e.g., Choi matrix construction), each agent reimplements it locally. Integration and de-duplication happen in a later phase.

---

## Agent-1: Theoretical Foundations (`01_theory/`)

### 1.1 Mission
Build the rigorous mathematical scaffolding that the entire project rests on: define all four channel representations, prove the Choi-Jamiołkowski isomorphism, derive properties, and implement clean conversion functions between representations.

### 1.2 Notebook Structure (`01_theory/main.ipynb`)

**Section 1 — Channel Representations**
- Define and motivate Kraus, Choi, Stinespring, Natural forms
- Worked examples on small channels (identity, bit-flip, depolarizing, amplitude damping)
- Print the Choi matrix of each example and verify CP/TP conditions

**Section 2 — Choi-Jamiołkowski Isomorphism**
- Statement and proof sketch
- Visualization: how $\mathcal{E}$ acting on half of $|\Omega\rangle$ produces $C_\mathcal{E}$
- Numerical verification: pick random Kraus operators, compute Choi matrix, recover Kraus from eigendecomposition, check $\mathcal{E}(\rho) \approx \sum_k K_k \rho K_k^\dagger$

**Section 3 — Properties Revealed by Choi Matrix**
- CP ⟺ $C \succeq 0$: numerical demos with eigenvalue inspection
- TP ⟺ $\text{Tr}_B(C) = I_A$: partial trace check
- Rank = minimum Kraus operators
- Unitality, Hermiticity preservation
- Special classes: entanglement-breaking (Choi is separable), unital channels

**Section 4 — Conversions Between Representations**
- All 6 directions (Kraus↔Choi, Kraus↔Stinespring, Choi↔Natural, etc.)
- Sanity-check round-trip conversions on random channels

**Section 5 — Composition and Channel Algebra**
- How $\mathcal{E}_2 \circ \mathcal{E}_1$ looks in each representation
- "Link product" formula for Choi matrices

### 1.3 Key Functions to Implement (`01_theory/channel_reps.py`)
```python
def kraus_to_choi(kraus_ops: list[np.ndarray]) -> np.ndarray: ...
def choi_to_kraus(choi: np.ndarray, tol: float = 1e-10) -> list[np.ndarray]: ...
def kraus_to_stinespring(kraus_ops: list[np.ndarray]) -> np.ndarray: ...
def stinespring_to_kraus(isometry: np.ndarray, env_dim: int) -> list[np.ndarray]: ...
def choi_to_natural(choi: np.ndarray) -> np.ndarray: ...
def natural_to_choi(natural: np.ndarray) -> np.ndarray: ...
def is_cp(choi: np.ndarray, tol: float = 1e-9) -> bool: ...
def is_tp(choi: np.ndarray, d_in: int, tol: float = 1e-9) -> bool: ...
def apply_channel(rho: np.ndarray, kraus_ops: list[np.ndarray]) -> np.ndarray: ...
def compose_channels_choi(choi1: np.ndarray, choi2: np.ndarray) -> np.ndarray: ...
def random_channel(d_in: int, d_out: int, n_kraus: int) -> list[np.ndarray]: ...
```

### 1.4 Deliverables Checklist
- [ ] `main.ipynb` runs end-to-end without errors
- [ ] `channel_reps.py` with all functions listed above, fully type-hinted and docstringed
- [ ] Unit tests in `test_channel_reps.py` (pytest, ≥20 tests covering edge cases)
- [ ] `README.md` summarizing key results
- [ ] All standard channels (depolarizing, amplitude damping, phase damping, Pauli, bit-flip, phase-flip) implemented as functions returning Kraus operators

### 1.5 Key References
- Nielsen & Chuang, *Quantum Computation and Quantum Information*, Ch. 8
- Watrous, *The Theory of Quantum Information*, Ch. 2
- Wilde, *Quantum Information Theory*, Ch. 4

---

## Agent-2: IBM Quantum Process Tomography (`02_ibm_experiment/`)

### 2.1 Mission
Run quantum process tomography (QPT) on real IBM Quantum hardware, reconstruct the Choi matrices of actual noisy gates, and diagnose the dominant noise mechanisms by inspecting the recovered Choi matrices.

### 2.2 Notebook Structure (`02_ibm_experiment/main.ipynb`)

**Section 1 — QPT Theory Primer**
- Why process tomography ≡ state tomography on $C_\mathcal{E}$
- Informationally complete input states (for 1-qubit: $|0\rangle, |1\rangle, |+\rangle, |+i\rangle$)
- Linear inversion vs. Maximum Likelihood Estimation (MLE)
- Why MLE matters: linear inversion can produce non-physical (non-CP) Choi matrices

**Section 2 — Implementation**
- Use `qiskit-experiments` `ProcessTomography` class
- Targets to characterize:
  - Ideal vs. real `X` gate (1-qubit)
  - Ideal vs. real `H` gate (1-qubit)
  - Ideal vs. real `CNOT` gate (2-qubit)
  - A custom circuit with deliberately injected noise (delay + gates)

**Section 3 — Experimental Run**
- Backend selection (use free IBM Quantum backends like `ibm_brisbane` or simulator fallback `AerSimulator` with realistic noise model from a real backend)
- Shot count: ≥4096 shots per circuit
- Save raw results to `data/raw_results.json` for reproducibility

**Section 4 — Choi Matrix Reconstruction**
- Linear inversion implementation (show non-physicality)
- MLE implementation with CP/TP constraints (CVXPY-based)
- Side-by-side comparison

**Section 5 — Diagnosis**
- Process fidelity vs. ideal: $F_{\text{pro}} = \text{Tr}(C_{\text{ideal}} C_{\text{actual}}) / d^2$
- Average gate fidelity
- Diamond norm distance (use Agent-3's formulation independently; reimplement locally)
- Eigendecomposition of $C_{\text{actual}}$ to extract dominant Kraus operators
- Classify dominant noise: depolarizing? amplitude damping? coherent error? Pauli error?

**Section 6 — Visualization**
- Heatmap of $|C_{\text{ideal}}|$ vs. $|C_{\text{actual}}|$ (real and imaginary parts)
- Bloch sphere deformation under ideal vs. real gate
- Bar chart of Kraus operator weights

### 2.3 Key Functions to Implement (`02_ibm_experiment/qpt_tools.py`)
```python
def run_process_tomography(circuit, backend, shots: int = 4096) -> ProcessTomographyResult: ...
def linear_inversion_choi(measurement_data: dict) -> np.ndarray: ...
def mle_choi(measurement_data: dict, d_in: int, d_out: int) -> np.ndarray: ...
def process_fidelity(choi_actual: np.ndarray, choi_ideal: np.ndarray) -> float: ...
def average_gate_fidelity(choi_actual: np.ndarray, choi_ideal: np.ndarray, d: int) -> float: ...
def diagnose_noise(choi: np.ndarray, choi_ideal: np.ndarray) -> dict: ...
def plot_choi_heatmap(choi: np.ndarray, title: str) -> None: ...
def plot_bloch_deformation(choi: np.ndarray) -> None: ...
```

### 2.4 Fallback Plan (no IBM access)
If IBM Quantum credentials are unavailable, use `AerSimulator.from_backend(FakeBrisbane())` to simulate realistic noise. Note clearly in the notebook which mode was used.

### 2.5 Deliverables Checklist
- [ ] `main.ipynb` with both ideal-vs-real comparison
- [ ] `qpt_tools.py` with all helper functions
- [ ] `data/` folder containing raw experimental results (or simulated equivalents)
- [ ] At least 3 gates analyzed (X, H, CNOT minimum)
- [ ] MLE implementation that always returns a CP/TP Choi matrix
- [ ] Clear diagnosis paragraph for each analyzed gate

### 2.6 Key References
- Nielsen & Chuang, Ch. 8 (process tomography)
- Qiskit Experiments documentation: `ProcessTomography`
- Knee et al., "Quantum process tomography via completely positive and trace-preserving projection" (2018)

---

## Agent-3: SDP Channel Discrimination (`03_sdp_discrimination/`)

### 3.1 Mission
Implement and solve the channel discrimination problem as a semidefinite program (SDP) using the Choi representation. Demonstrate how Choi matrices enable convex optimization-based analysis of channel-level questions that would be intractable in Kraus form.

### 3.2 Notebook Structure (`03_sdp_discrimination/main.ipynb`)

**Section 1 — Problem Statement**
- Two-channel discrimination: given $\mathcal{E}_0$ or $\mathcal{E}_1$ (equal prior), find the max success probability
- Connection to diamond norm: $p_{\text{succ}}^{\max} = \frac{1}{2} + \frac{1}{4}\|\mathcal{E}_0 - \mathcal{E}_1\|_\diamond$
- Why this is hard without Choi: optimization over all input states (including entangled with reference) is needed

**Section 2 — SDP Formulation (Watrous 2009)**
- Primal SDP for diamond norm in terms of Choi matrices
- Dual SDP and operational interpretation
- Constraints: positivity, partial trace conditions

**Section 3 — CVXPY Implementation**
- Encode SDP variables (Hermitian PSD matrices)
- Solve with `MOSEK` (preferred) or `SCS` (fallback)
- Verification: compare with closed-form diamond norm for special cases (e.g., difference of two Pauli channels)

**Section 4 — Case Studies**
- **Case A**: Two depolarizing channels with different noise rates $p_1, p_2$
  - Plot: success probability vs. $|p_1 - p_2|$
- **Case B**: Amplitude damping vs. Phase damping (same parameter)
  - When are they most distinguishable?
- **Case C**: Coherent vs. incoherent noise (rotation error vs. depolarizing)
- **Case D**: Demonstrate entanglement advantage — show that entangled input strictly outperforms product input

**Section 5 — Multi-Use Discrimination**
- $n$-shot parallel strategy: discrimination on $\mathcal{E}_0^{\otimes n}$ vs. $\mathcal{E}_1^{\otimes n}$
- Plot success probability as function of $n$
- Asymptotic discrimination rate (touch on quantum Stein's lemma if time permits)

**Section 6 — Extracting Optimal Strategy**
- From SDP dual, extract optimal input state and optimal POVM
- Visualize on Bloch sphere (for qubit channels)

### 3.3 Key Functions to Implement (`03_sdp_discrimination/sdp_tools.py`)
```python
def diamond_norm_sdp(choi_diff: np.ndarray, d_in: int, d_out: int) -> float: ...
def discrimination_probability(choi_0: np.ndarray, choi_1: np.ndarray) -> float: ...
def optimal_input_state(choi_0: np.ndarray, choi_1: np.ndarray) -> np.ndarray: ...
def optimal_povm(choi_0: np.ndarray, choi_1: np.ndarray) -> tuple[np.ndarray, np.ndarray]: ...
def n_shot_discrimination(choi_0: np.ndarray, choi_1: np.ndarray, n: int) -> float: ...
def product_strategy_discrimination(choi_0: np.ndarray, choi_1: np.ndarray) -> float: ...
```

### 3.4 Deliverables Checklist
- [ ] `main.ipynb` covering all 4 case studies
- [ ] `sdp_tools.py` with verified SDP solver
- [ ] At least one plot showing strict entanglement advantage
- [ ] Numerical agreement with at least one known closed-form result (for validation)
- [ ] Discussion of computational complexity and SDP scaling

### 3.5 Key References
- Watrous, "Semidefinite programs for completely bounded norms" (2009)
- Watrous, *The Theory of Quantum Information*, Ch. 3 & 4
- Khatri & Wilde, *Principles of Quantum Communication Theory* — SDP chapter

---

## Agent-4: Non-Markovian Dynamics & Quantum Combs (`04_quantum_combs/`)

### 4.1 Mission
Extend the Choi representation from single-time-step channels to multi-time quantum processes. Implement process tensors (quantum combs), distinguish Markovian from non-Markovian dynamics, and quantify memory effects.

### 4.2 Notebook Structure (`04_quantum_combs/main.ipynb`)

**Section 1 — Motivation**
- Single-time channel is insufficient for systems with environmental memory
- Concrete failure example: a 2-step dynamics where $\mathcal{E}_{20} \neq \mathcal{E}_{21} \circ \mathcal{E}_{10}$
- Introduce process tensor $\mathcal{T}^{(N)}$ as the natural generalization

**Section 2 — Quantum Combs Formalism**
- Definition: $N$-step comb as a positive operator on $\bigotimes_{i=0}^{N-1} \mathcal{H}_{A_i} \otimes \mathcal{H}_{B_i}$
- Causality hierarchy: nested partial trace conditions
- Choi-like representation of a comb (the comb *is* a generalized Choi operator)

**Section 3 — Markovian vs. Non-Markovian**
- Markovianity ⟺ comb factorizes into product of individual channel Chois
- Divisibility (CP-divisibility) criterion
- BLP measure (trace distance non-monotonicity)
- RHP measure (divisibility violation)

**Section 4 — Simulating a Non-Markovian Process**
- Toy model: qubit coupled to a small environment (e.g., 1–2 ancilla qubits)
- Closed dynamics on system+environment, then partial trace
- Construct the 2-step process tensor by:
  - Preparing maximally entangled states at intermediate times
  - Reading out the full comb Choi operator
- Compare with the "Markovian approximation" (product of marginal channels)

**Section 5 — Quantifying Non-Markovianity**
- Implement BLP measure: $\mathcal{N}_{\text{BLP}} = \max_{\rho_{1,2}} \int_{\sigma > 0} \frac{d}{dt} D(\rho_1(t), \rho_2(t)) dt$
- Implement RHP measure based on intermediate map negativity
- Apply both to the toy model with varying system-environment coupling

**Section 6 — Connection to Hardware**
- Discussion: how short-time repeated gates on a real device might exhibit non-Markovian behavior
- (Optional) Use Qiskit simulator with correlated noise to demonstrate

### 4.3 Key Functions to Implement (`04_quantum_combs/combs_tools.py`)
```python
def construct_process_tensor(system_env_unitaries: list[np.ndarray], 
                              env_init: np.ndarray, 
                              n_steps: int) -> np.ndarray: ...
def is_markovian(process_tensor: np.ndarray, n_steps: int, tol: float = 1e-8) -> bool: ...
def marginal_channel(process_tensor: np.ndarray, step: int) -> np.ndarray: ...
def blp_measure(channel_family: callable, t_grid: np.ndarray) -> float: ...
def rhp_measure(channel_family: callable, t_grid: np.ndarray) -> float: ...
def comb_partial_trace_check(comb: np.ndarray, dims: list[int]) -> bool: ...
```

### 4.4 Scope Management
This is the most theoretically advanced sub-task. Recommended scope:
- **Minimum**: 2-step process tensor, BLP measure, one toy model
- **Stretch goal**: 3-step comb, both BLP and RHP, hardware-inspired example

### 4.5 Deliverables Checklist
- [ ] `main.ipynb` with at least one fully worked non-Markovian example
- [ ] `combs_tools.py` with process tensor construction and at least one non-Markovianity measure
- [ ] Clear visualization showing Markovian vs. non-Markovian Choi structure
- [ ] Honest discussion of limitations (dimensionality blow-up, etc.)

### 4.6 Key References
- Chiribella, D'Ariano, Perinotti, "Quantum circuit architecture" (2008)
- Pollock et al., "Non-Markovian quantum processes: Complete framework and efficient characterization" (2018)
- Breuer, Laine, Piilo, "Measure for the degree of non-Markovian behavior" (BLP, 2009)
- Rivas, Huelga, Plenio, "Entanglement and Non-Markovianity of Quantum Evolutions" (RHP, 2010)

---

## Agent-5: Interactive Visualization Widget (`05_interactive_widget/`)

### 5.1 Mission
Build an interactive, parameter-driven visualization tool that lets a user manipulate channel parameters via sliders and immediately see the resulting Choi matrix, Bloch sphere deformation, Kraus operators, eigenspectrum, and fidelity metrics update in real time.

### 5.2 Notebook Structure (`05_interactive_widget/main.ipynb`)

**Section 1 — Design Goals**
- Make abstract Choi matrices concrete and tangible
- Support educational use: a viewer should learn by playing
- Side-by-side visual links between parameter, matrix, and Bloch geometry

**Section 2 — Architecture**
- Recommended primary: **ipywidgets** inside Jupyter (lowest friction)
- Recommended secondary: **Streamlit** version for browser deployment
- Layout: 4-panel synchronized dashboard

**Section 3 — Implementation: ipywidgets Version**
- Sliders for parameters of each channel type
- Live update of all panels via `interact` / `interactive_output`

**Section 4 — Implementation: Streamlit Version (Optional)**
- Same layout, deployable to Hugging Face Spaces or Streamlit Cloud
- Provide deployment instructions

**Section 5 — Panels**

Each panel updates whenever any slider moves.

1. **Choi Matrix Heatmap** — real and imaginary parts, side by side, with colorbar
2. **Bloch Sphere Deformation** — unit sphere of pure states → ellipsoid after channel; 3D plot
3. **Kraus Operators Table** — extracted from current Choi via eigendecomposition; show matrices and weights
4. **Eigenvalue Spectrum** — bar chart of Choi eigenvalues; visual rank
5. **Fidelity Indicators** — process fidelity with identity, with current channel's depolarized version, CP/TP status indicators

**Section 6 — Channel Library**
The widget supports at minimum:
- Depolarizing (1 parameter)
- Amplitude damping (1 parameter)
- Phase damping (1 parameter)
- Bit-flip / phase-flip (1 parameter)
- General Pauli channel (3 parameters $p_X, p_Y, p_Z$)
- General qubit unital channel (3 parameters, axis rotation)
- "Mix two channels" mode (interpolation slider between any two of the above)

**Section 7 — Educational Mode (Optional Stretch)**
- "Guess the channel" quiz: random Choi shown, user clicks correct channel type
- "Compose two channels" mode: pick two channels, see resulting Choi

### 5.3 Key Functions to Implement (`05_interactive_widget/widget_core.py`)
```python
def get_channel_choi(channel_type: str, params: dict) -> np.ndarray: ...
def plot_choi_heatmap(choi: np.ndarray, ax_real, ax_imag) -> None: ...
def plot_bloch_ellipsoid(choi: np.ndarray, ax_3d) -> None: ...
def extract_kraus_display(choi: np.ndarray) -> list[tuple[float, np.ndarray]]: ...
def plot_eigenspectrum(choi: np.ndarray, ax) -> None: ...
def compute_indicators(choi: np.ndarray) -> dict: ...
def build_widget() -> ipywidgets.Widget: ...  # main entry point
```

### 5.4 Deliverables Checklist
- [ ] `main.ipynb` containing the full working widget
- [ ] `widget_core.py` with all rendering and computation logic
- [ ] At least one screenshot / GIF in `README.md` demonstrating the widget
- [ ] All channel types listed in Section 6 working
- [ ] Layout is responsive and panels stay synchronized
- [ ] (Stretch) Streamlit version in `streamlit_app.py`

### 5.5 Key References
- ipywidgets documentation
- Plotly documentation (for 3D Bloch sphere if matplotlib feels limiting)
- Streamlit documentation (if web-deployed version is attempted)

---

# Validator Layer

> **Important**: Validators run in **Phase 2**, after all 5 producers have completed Phase 1. Each validator has **read access to all 5 producer folders** and produces a written review report. Validators do NOT modify producer code — they only generate findings that drive a revision round.

## Validator-A: Mathematical & Physical Correctness (`90_validation_math/`)

### A.1 Mission
Audit every non-trivial mathematical claim, derivation, formula, and physical interpretation across all 5 producer folders. Flag errors, missing assumptions, and physically suspicious results.

### A.2 Inputs
Read-only access to:
- `01_theory/main.ipynb` and `01_theory/channel_reps.py`
- `02_ibm_experiment/main.ipynb` and `02_ibm_experiment/qpt_tools.py`
- `03_sdp_discrimination/main.ipynb` and `03_sdp_discrimination/sdp_tools.py`
- `04_quantum_combs/main.ipynb` and `04_quantum_combs/combs_tools.py`
- `05_interactive_widget/main.ipynb` and `05_interactive_widget/widget_core.py`

### A.3 Review Checklist
For each producer folder:

**Definitions & Conventions**
- Is the Choi matrix convention consistent with Section 0.5 ($C_\mathcal{E} = \sum_{ij} |i\rangle\langle j| \otimes \mathcal{E}(|i\rangle\langle j|)$)?
- Are partial trace conventions (over A vs over B) correctly applied?
- Are dimension labels ($d_A, d_B$, $d_{\text{in}}, d_{\text{out}}$) consistent within each notebook?

**Derivations & Proofs**
- Does the Choi-Jamiołkowski isomorphism proof in Agent-1 cover both directions?
- Is the SDP formulation in Agent-3 a correct restatement of Watrous's diamond norm SDP?
- Are the BLP and RHP non-Markovianity measures in Agent-4 stated correctly?
- Is the causality hierarchy for quantum combs (partial trace conditions) correctly written?

**Numerical Sanity Checks**
- Does Agent-1's round-trip conversion (Kraus → Choi → Kraus) pass to machine precision?
- Do Agent-3's SDP results match closed-form diamond norm for known cases (e.g., Pauli channels)?
- Does Agent-2's MLE reconstruction always return a valid CP/TP map?
- Do Agent-5's Bloch ellipsoid visualizations match expected shapes for standard channels (e.g., depolarizing → contracted sphere, amplitude damping → off-center ellipsoid)?

**Physical Plausibility**
- Are process fidelities in Agent-2 within $[0, 1]$ and decreasing with noise?
- Are discrimination probabilities in Agent-3 within $[1/2, 1]$?
- Do non-Markovianity measures in Agent-4 reduce to 0 for genuinely Markovian dynamics?

### A.4 Deliverable: `90_validation_math/MATH_REVIEW.md`
Structured report containing:
```
## Findings for Agent-1
### Critical (must fix)
- [ ] (description, location, suggested fix)
### Major (should fix)
- [ ] ...
### Minor (nice to fix)
- [ ] ...

## Findings for Agent-2
...
(repeat for all 5 agents)

## Summary
- Total critical issues: N
- Total major issues: N
- Total minor issues: N
- Overall mathematical soundness: [grade]
```

### A.5 Tools Allowed
- Run notebooks to verify numerical claims
- Write throwaway verification scripts in `90_validation_math/scratch/`
- Use SymPy or manual derivation for symbolic checks
- Cross-reference with Nielsen & Chuang, Watrous, Wilde

### A.6 Boundaries
- **Do not modify** any file in producer folders
- **Do not** rewrite producer code; only describe what should change
- If you find a likely bug, reproduce it in a minimal script under `scratch/` and reference it in the report

---

## Validator-B: Code Quality & Reproducibility (`91_validation_code/`)

### B.1 Mission
Audit code quality, correctness, performance, and reproducibility across all 5 producer folders. Run every notebook end-to-end on a clean environment and report anything that breaks, smells, or could be improved.

### B.2 Inputs
Read-only access to all 5 producer folders.

### B.3 Review Checklist

**Reproducibility**
- Does each `main.ipynb` execute top-to-bottom on a fresh kernel without errors?
- Is `requirements.txt` complete and version-pinned where critical?
- Are random seeds set as required by Section 0.5?
- Are any hardcoded paths or environment-specific assumptions present?

**Code Hygiene**
- Are all public functions type-hinted (per Section 0.5)?
- Are docstrings present in NumPy format?
- Are function names descriptive? Are there magic numbers without explanation?
- Are there obvious dead-code blocks or unused imports?

**Correctness Smells**
- Hermiticity checks: does code that produces Hermitian matrices verify $A = A^\dagger$ within tolerance?
- Numerical tolerance: are tolerances reasonable (e.g., `1e-9`, not `1e-3` for clean calculations)?
- Are eigendecomposition results sorted consistently (descending)?
- Are complex vs. real types handled correctly (no silent `dtype=float64` truncation of complex)?

**Performance & Scaling**
- Any obvious $O(n^4)$ or worse when $O(n^3)$ would suffice?
- Unnecessary recomputation inside loops?
- For Agent-5's widget: does it remain responsive on parameter changes?

**Testing**
- Do unit tests exist? Do they pass?
- Are edge cases (zero matrices, identity channels, max-mixed states) tested?

**Notebook Structure**
- Are notebooks readable as standalone documents (markdown narrative + code)?
- Are large outputs trimmed (no 1000-line printouts dumped)?
- Are plots labeled with titles, axis labels, and units?

### B.4 Execution Protocol
1. Create a fresh virtual environment
2. For each producer folder $i$:
   - `pip install -r 0i_*/requirements.txt`
   - Execute `0i_*/main.ipynb` via `jupyter nbconvert --execute`
   - Run `pytest 0i_*/test_*.py` if tests exist
   - Log every error, warning, deprecation
3. Save execution logs to `91_validation_code/execution_logs/`

### B.5 Deliverable: `91_validation_code/CODE_REVIEW.md`
```
## Execution Results
| Agent | Notebook runs? | Tests pass? | Warnings | Errors |
|-------|---------------|-------------|----------|--------|
| Agent-1 | ✅/❌ | ✅/❌/N/A | N | N |
| ... |

## Per-Agent Findings
### Agent-1
#### Blockers (notebook fails or wrong results)
- ...
#### Quality issues
- ...
#### Suggestions
- ...

(repeat for all 5)

## Cross-Cutting Observations
(patterns seen in multiple folders)
```

### B.6 Boundaries
- **Do not modify** producer code
- If a notebook fails, capture the full traceback in the report
- Suggested fixes should be brief code snippets, not full rewrites

---

## Validator-C: Cross-Folder Consistency (`92_validation_consistency/`)

### C.1 Mission
The 5 producers worked independently and likely diverged on notation, terminology, function naming, and style. Identify all inconsistencies that will cause friction when the work is integrated into a single report and presentation.

### C.2 Inputs
Read-only access to all 5 producer folders, plus this master specification document.

### C.3 Review Dimensions

**Mathematical Notation**
- Is the Choi matrix denoted consistently ($C$, $J$, $\Lambda$, $\rho_\mathcal{E}$ — which is used where)?
- Are channels denoted consistently ($\mathcal{E}$, $\Phi$, $\Lambda$, $\mathcal{N}$)?
- Are Kraus operators denoted consistently ($K_k$, $E_k$, $A_k$, $M_k$)?
- Is the maximally entangled state denoted consistently ($|\Omega\rangle$, $|\Phi^+\rangle$, $|\beta_{00}\rangle$)?
- Are bra-ket vs. matrix expressions used consistently?

**Terminology**
- "Channel" vs "map" vs "superoperator" — used interchangeably or carefully?
- "Process tomography" vs "channel tomography"
- "Diamond norm" vs "completely bounded trace norm"
- "Quantum comb" vs "process tensor" vs "higher-order map"
- Korean vs English term usage (if any appears in notebooks)

**Function & Variable Naming**
- For overlapping reimplementations (e.g., `kraus_to_choi`), are the signatures compatible?
- Are channel parameter names consistent (`p` for noise rate vs `gamma`, `lambda`, etc.)?
- Are dimension variables consistent (`d`, `dim`, `n`, `d_A`)?

**Visual Style**
- Are color palettes consistent across plots from different folders?
- Are plot styles (font sizes, dpi, figure sizes) coherent?
- Are Choi matrix heatmaps using the same colormap and orientation?

**Reference Standards**
- Are the same papers cited with consistent format?
- Are textbook references (Nielsen & Chuang, Watrous, Wilde) cited consistently?

**Document Voice**
- Are README files structured similarly?
- Is the level of mathematical formality similar across notebooks?

### C.4 Deliverable: `92_validation_consistency/CONSISTENCY_REVIEW.md`

```
## Notation Inconsistencies
| Concept | Agent-1 | Agent-2 | Agent-3 | Agent-4 | Agent-5 | Recommended |
|---------|---------|---------|---------|---------|---------|-------------|
| Choi matrix | C_E | J(Λ) | Choi | C | C | C |
| Channel | E | Λ | Φ | T | E | E |
| ... |

## Terminology Inconsistencies
- ...

## Function Signature Mismatches
- `kraus_to_choi` in Agent-1 takes `list[ndarray]`; in Agent-3 it takes `ndarray` of stacked operators — recommend Agent-1's form
- ...

## Visual Style Issues
- ...

## Recommended Standards (to be applied in revision round)
- Use `C` for Choi matrix
- Use `\mathcal{E}` for channel
- ...
```

Additionally, produce `92_validation_consistency/UNIFIED_GLOSSARY.md` — a single-page reference of recommended notation/terminology that revision-phase producers should adopt.

### C.5 Boundaries
- **Do not modify** producer code or notebooks
- Recommendations should be conservative: only flag inconsistencies that genuinely impede integration, not stylistic preferences

---

# Validator Coordination Notes

### Parallel Execution
All three validators run in parallel during Phase 2. They do not communicate with each other. Some overlap in findings is expected and acceptable — the user/orchestrator de-duplicates during the revision round.

### Validator Output Folder Structure
```
9X_validation_*/
├── MATH_REVIEW.md          (or CODE_REVIEW.md, CONSISTENCY_REVIEW.md)
├── README.md               (brief summary of findings)
├── scratch/                (verification scripts, execution logs)
└── (any supporting files)
```

### What Validators Do NOT Do
- Do not rewrite producer code
- Do not move or rename producer files
- Do not push opinions about scope or design choices made by producers
- Do not duplicate the producers' work

### What Happens After Validation
Phase 3 (revision) is driven by the user. The user reads all three validation reports, prioritizes issues (critical → major → minor), and either:
- Re-invokes the relevant producer agent with a specific fix list, or
- Manually applies small corrections

This loop may iterate, but typically one validation pass plus one revision pass is sufficient.

---

## Final Notes for All Agents

### Code Quality Bar (Producers)
- All public functions must have type hints and docstrings
- Unit tests are encouraged for numerical functions
- Notebooks must run top-to-bottom on a fresh kernel without errors
- Cite references inline (in markdown cells) for non-trivial formulas

### Independence Reminder (Producers)
You are working in **your own folder only** during Phase 1. Do not assume anything about the structure or contents of the other four producer folders. If a function you need overlaps with another agent's likely work, **reimplement it locally** with a clear name. Cross-folder consistency is the Validator-C's concern, not yours.

### Read-Only Discipline (Validators)
You have read access to all producer folders but **must not modify them**. Your sole output is a review report in your own validator folder. If you find a clear bug, document it precisely with file path, line number, and minimal reproduction — do not patch it.

### Output Folder Structure

**Producer folders:**
```
0X_subtask_name/
├── main.ipynb
├── README.md
├── requirements.txt
├── <module>.py
├── test_<module>.py        (optional but encouraged)
└── data/                   (if applicable)
```

**Validator folders:**
```
9X_validation_*/
├── <REVIEW_NAME>.md
├── README.md
├── scratch/                (verification scripts, execution logs)
└── (any supporting files)
```

### Working Style
- Be thorough. This is meant to be a high-quality course project.
- Prefer correctness and clarity over cleverness.
- When in doubt about a convention, follow Nielsen & Chuang's notation.

---

*End of specification. Producers should begin Phase 1 work in their designated folders. Validators should wait until all producers report completion, then begin Phase 2 in parallel.*
