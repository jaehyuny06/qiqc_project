# Choi Representation of Quantum Channels

## Overview

This course project studies the Choi representation of quantum channels from
several complementary angles: mathematical foundations, process tomography,
semidefinite programming, non-Markovian dynamics, and interactive
visualization. The central idea is that a quantum channel can be represented as
a single matrix, its Choi matrix, and that this matrix makes important channel
properties visible through ordinary linear algebra.

The project is written for readers who know the basics of quantum information
but are new to this particular implementation. Each sub-project is a narrative
notebook with supporting Python utilities, tests, and reproducible examples.
The notebooks can be read independently, but together they show how the same
Choi convention connects theory, numerical experiments, hardware-facing
tomography workflows, operational channel discrimination, and multi-time
quantum processes.

Across the repository, the shared convention is the unnormalized Choi matrix

```text
C_E = sum_ij |i><j|_A tensor E(|i><j|)_B
```

where the input system is first and the output system is second. With this
convention, trace preservation is checked as `Tr_B(C_E) = I_A`.

## Project Structure

```text
.
├── 01_theory/
│   ├── main.ipynb
│   ├── README.md
│   ├── channel_reps.py
│   └── test_channel_reps.py
│
├── 02_ibm_experiment/
│   ├── main.ipynb
│   ├── README.md
│   ├── qpt_tools.py
│   ├── test_qpt_tools.py
│   └── data/
│
├── 03_sdp_discrimination/
│   ├── main.ipynb
│   ├── README.md
│   ├── sdp_tools.py
│   └── test_sdp_tools.py
│
├── 04_quantum_combs/
│   ├── main.ipynb
│   ├── README.md
│   ├── combs_tools.py
│   ├── non_markovian_dynamics.py
│   └── test_combs_tools.py
│
├── 05_interactive_widget/
│   ├── main.ipynb
│   ├── README.md
│   ├── channel_utils.py
│   ├── widget_core.py
│   ├── test_widget_core.py
│   └── figures/
│
├── choi_common/
│   ├── README.md
│   ├── representations.py
│   ├── channels.py
│   ├── validation.py
│   ├── metrics.py
│   ├── visualization.py
│   ├── utils.py
│   └── tests/
│
├── 94_integration/
│   ├── REFERENCES.md
│   ├── references.bib
│   ├── CITATION_AUDIT.md
│   ├── DUPLICATION_ANALYSIS.md
│   ├── LIBRARY_STRUCTURE.md
│   ├── MIGRATION_PLAN.md
│   └── MIGRATION_LOG.md
│
└── pyproject.toml
```

Folder summaries:

- `01_theory/`: theoretical foundations and representation conversions among
  Kraus, Choi, Stinespring, and natural/Liouville forms.
- `02_ibm_experiment/`: offline-reproducible quantum process tomography
  workflow, with optional IBM Quantum hardware submission notes.
- `03_sdp_discrimination/`: channel discrimination using the diamond norm and
  Watrous-style semidefinite programs.
- `04_quantum_combs/`: multi-time processes, finite-memory quantum combs, and
  non-Markovianity witnesses.
- `05_interactive_widget/`: local ipywidgets dashboard for visualizing qubit
  Choi matrices and Bloch-sphere channel action.
- `choi_common/`: shared utilities extracted from duplicated producer-folder
  implementations.
- `94_integration/`: integration reports, migration notes, and consolidated
  bibliography.

## Key Results

- The project verifies numerically that complete positivity is equivalent to
  Choi positive semidefiniteness, and trace preservation is equivalent to
  `Tr_B(C_E) = I_A`.
- Kraus, Choi, Stinespring, and natural representations can be converted
  consistently, with the numerical Choi rank matching the minimum number of
  Kraus operators.
- The process-tomography workflow reconstructs noisy stand-ins for `X`, `H`,
  and `CNOT`, then compares linear inversion, CPTP projection, fidelity, and
  diamond-distance diagnostics.
- Equal-prior channel discrimination is connected to the diamond norm through
  `p_success = 1/2 + 1/4 ||E_0 - E_1||_diamond`, and the examples show a strict
  ancilla-assisted advantage.
- Multi-time examples show that a channel family can be valid at each time
  while still failing CP-divisibility, and that a reused environment can
  produce a non-factorizing quantum comb.

## Sub-Topics

### 1. Theoretical Foundations

The theory notebook introduces the shared Choi convention and implements the
core finite-dimensional channel representations. It demonstrates standard
channels such as identity, bit flip, phase flip, depolarizing, amplitude
damping, and phase damping channels, then checks CP, TP, Choi rank, and
round-trip consistency between representations. Start here if you want the
mathematical baseline used everywhere else.

- Notebook: [01_theory/main.ipynb](01_theory/main.ipynb)
- Folder README: [01_theory/README.md](01_theory/README.md)

### 2. IBM Quantum Process Tomography

The process-tomography notebook builds a reproducible offline QPT workflow for
the `X`, `H`, and `CNOT` gates. By default, it simulates deterministic noisy
channels and reconstructs Choi matrices without requiring IBM credentials or
queue time. It also documents how to submit equivalent tomography circuits to
IBM Quantum hardware when an account and backend are available.

- Notebook: [02_ibm_experiment/main.ipynb](02_ibm_experiment/main.ipynb)
- Folder README: [02_ibm_experiment/README.md](02_ibm_experiment/README.md)

### 3. SDP Channel Discrimination

The discrimination notebook studies how well two quantum channels can be told
apart using the diamond norm. It implements the SDP, compares results with
closed-form qubit examples, extracts optimal states and measurements, and
shows how entanglement with an ancilla can improve the success probability.
This sub-topic is the most operational: it turns Choi matrices into a concrete
decision problem.

- Notebook: [03_sdp_discrimination/main.ipynb](03_sdp_discrimination/main.ipynb)
- Folder README: [03_sdp_discrimination/README.md](03_sdp_discrimination/README.md)

### 4. Non-Markovian Dynamics and Quantum Combs

The quantum-combs notebook extends the Choi viewpoint from one channel to
multi-time processes. It includes toy dephasing models, BLP trace-distance
revival estimates, RHP-style CP-divisibility witnesses, and a collision model
where memory appears because the environment is reused. This section is useful
for seeing why a sequence of valid one-time channels may not describe the full
history of an open quantum system.

- Notebook: [04_quantum_combs/main.ipynb](04_quantum_combs/main.ipynb)
- Folder README: [04_quantum_combs/README.md](04_quantum_combs/README.md)

### 5. Interactive Choi Widget

The widget notebook provides a local dashboard for qubit channels. It displays
the Choi matrix, eigenvalues, CP/TP indicators, Kraus information, and Bloch
deformation for supported channel families. Some modes intentionally allow
non-CP parameter choices so the Choi-positivity condition can be seen directly.

- Notebook: [05_interactive_widget/main.ipynb](05_interactive_widget/main.ipynb)
- Folder README: [05_interactive_widget/README.md](05_interactive_widget/README.md)

## Installation

### 1. Python Version

Use Python 3.10 or newer. The shared package declares:

```text
requires-python = ">=3.10"
```

The notebooks were validated with recent NumPy, SciPy, Matplotlib, CVXPY,
Jupyter, and Qiskit-related packages as pinned in the subfolder
`requirements.txt` files.

### 2. Create and Activate a Virtual Environment

From the project root:

```bash
python -m venv .venv
```

On macOS or Linux:

```bash
source .venv/bin/activate
```

On Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Then upgrade packaging tools:

```bash
python -m pip install --upgrade pip setuptools wheel
```

### 3. Install the Shared Library

Install the local `choi_common` package in editable mode:

```bash
python -m pip install -e .
```

This makes imports such as the following available from any subfolder:

```python
from choi_common.representations import kraus_to_choi
from choi_common.validation import is_cp, is_tp
```

### 4. Install Subfolder Dependencies

For a focused run, install the requirements for the folder you plan to execute:

```bash
python -m pip install -r 01_theory/requirements.txt
python -m pip install -r 02_ibm_experiment/requirements.txt
python -m pip install -r 03_sdp_discrimination/requirements.txt
python -m pip install -r 04_quantum_combs/requirements.txt
python -m pip install -r 05_interactive_widget/requirements.txt
```

If dependency conflicts appear, create separate virtual environments for the
IBM/Qiskit workflow and the lighter theory/widget workflows. The
`02_ibm_experiment` folder has the heaviest dependency set because it includes
Qiskit, Qiskit Aer, Qiskit Experiments, and IBM Runtime packages.

### 5. IBM Quantum Token Setup

The default project notebooks do not require IBM credentials. Only the optional
hardware submission path in `02_ibm_experiment` needs IBM Quantum access.

For current account setup, follow IBM's documentation for
`QiskitRuntimeService.save_account`:

- IBM Runtime service API:
  <https://quantum.cloud.ibm.com/docs/api/qiskit-ibm-runtime/qiskit_ibm_runtime.QiskitRuntimeService>
- IBM guide for saving credentials:
  <https://qiskit.qotlabs.org/docs/guides/save-credentials>

A typical setup pattern is:

```python
from qiskit_ibm_runtime import QiskitRuntimeService

QiskitRuntimeService.save_account(
    token="<YOUR_IBM_QUANTUM_TOKEN>",
    channel="ibm_quantum_platform",
    overwrite=True,
)
```

Do not commit tokens, account files, or raw private credentials to this
repository.

### 6. Optional MOSEK License for SDP

The SDP code can run with open-source solvers such as SCS or CLARABEL, but it
will prefer MOSEK when MOSEK is installed and licensed. MOSEK is optional.

Install and configure MOSEK only if you want faster or more robust SDP solves:

- MOSEK documentation: <https://docs.mosek.com/>

Without MOSEK, small educational examples should still run with the fallback
solvers used by CVXPY.

## Running the Project

### Recommended Reading Order

1. `01_theory/main.ipynb`: learn the shared convention and representation
   conversions.
2. `05_interactive_widget/main.ipynb`: build visual intuition for qubit Choi
   matrices and Bloch-sphere action.
3. `02_ibm_experiment/main.ipynb`: see how Choi matrices are reconstructed from
   process-tomography data.
4. `03_sdp_discrimination/main.ipynb`: use Choi matrices in an operational
   channel-discrimination problem.
5. `04_quantum_combs/main.ipynb`: extend the representation to multi-time
   memory processes.

### Launch a Notebook

From the project root:

```bash
jupyter notebook
```

Then open the desired `main.ipynb` file in the browser.

You can also execute a notebook non-interactively:

```bash
jupyter nbconvert --to notebook --execute 01_theory/main.ipynb --output executed_main.ipynb
```

For Windows PowerShell, the same command form works:

```powershell
jupyter nbconvert --to notebook --execute 01_theory/main.ipynb --output executed_main.ipynb
```

### Run the Tests

Run a folder's tests from the project root:

```bash
python -m pytest 01_theory -q
python -m pytest 02_ibm_experiment -q
python -m pytest 03_sdp_discrimination -q
python -m pytest 04_quantum_combs -q
python -m pytest 05_interactive_widget -q
python -m pytest choi_common/tests -q
```

Or run all available tests:

```bash
python -m pytest -q
```

### Launch the Interactive Widget

Install the widget requirements, then open the notebook:

```bash
python -m pip install -r 05_interactive_widget/requirements.txt
jupyter notebook 05_interactive_widget/main.ipynb
```

The widget is fully local. It does not need IBM Quantum access or network
connectivity once dependencies are installed.

## Reproducing Results

Several notebooks set `np.random.seed(42)` near the top to make plots and
sample data stable. The process-tomography workflow is offline-reproducible by
default: it uses deterministic simulated noisy channels rather than submitting
jobs to live IBM hardware.

Hardware-backed IBM Quantum results are not expected to reproduce exactly.
Queue time, backend calibration, shot noise, and device availability can all
change between runs. Treat the included sample data as deterministic examples,
not as hardware claims.

Expected runtime depends most strongly on SDP size and solver availability.
The theory, widget, and small comb examples should run quickly on a laptop.
The SDP and QPT notebooks may take longer when solving conic programs,
especially without MOSEK or when larger tensor-power examples are enabled.

For reproducible local reports:

```bash
jupyter nbconvert --to notebook --execute 01_theory/main.ipynb --output executed_main.ipynb
jupyter nbconvert --to notebook --execute 02_ibm_experiment/main.ipynb --output executed_main.ipynb
jupyter nbconvert --to notebook --execute 03_sdp_discrimination/main.ipynb --output executed_main.ipynb
jupyter nbconvert --to notebook --execute 04_quantum_combs/main.ipynb --output executed_main.ipynb
jupyter nbconvert --to notebook --execute 05_interactive_widget/main.ipynb --output executed_main.ipynb
```

If a notebook writes `executed_main.ipynb`, keep that generated output out of
final source-control commits unless the course deliverable explicitly asks for
executed notebooks.

## Team and Contributions

TODO: Replace these placeholders with the final team member names and actual
contribution statements.

| Team Member | Contribution |
| --- | --- |
| TODO: Team member 1 | Theoretical foundations and representation conversions |
| TODO: Team member 2 | IBM Quantum process tomography workflow |
| TODO: Team member 3 | SDP channel discrimination and diamond-norm examples |
| TODO: Team member 4 | Non-Markovian dynamics and quantum combs |
| TODO: Team member 5 | Interactive Choi visualization widget |

Additional integration work:

- TODO: Shared-library extraction and migration reviewer.
- TODO: Bibliography and reference consolidation reviewer.
- TODO: Final report/editorial reviewer.

## References

The consolidated bibliography is maintained in:

- [94_integration/REFERENCES.md](94_integration/REFERENCES.md)
- [94_integration/references.bib](94_integration/references.bib)
- [94_integration/CITATION_AUDIT.md](94_integration/CITATION_AUDIT.md)

Key references used across the project include:

- Michael A. Nielsen and Isaac L. Chuang, *Quantum Computation and Quantum
  Information*, Cambridge University Press, 2010.
- John Watrous, *The Theory of Quantum Information*, Cambridge University
  Press, 2018.
- Mark M. Wilde, *Quantum Information Theory*, Cambridge University Press,
  2017.
- John Watrous, "Semidefinite Programs for Completely Bounded Norms," *Theory
  of Computing*, 2009.
- Giulio Chiribella, Giacomo Mauro D'Ariano, and Paolo Perinotti, "Quantum
  Circuit Architecture," *Physical Review Letters*, 2008.
- Felix A. Pollock, Cesar Rodriguez-Rosario, Thomas Frauenheim, Mauro
  Paternostro, and Kavan Modi, "Non-Markovian Quantum Processes: Complete
  Framework and Efficient Characterization," *Physical Review A*, 2018.

## Acknowledgments

TODO: Add course name, term, instructor, teaching assistants, institution, and
any required academic-integrity statement.

TODO: Add an AI tool usage disclosure if required by course policy. Suggested
starting point:

```text
Parts of the project integration, code review, documentation drafting, and
reference consolidation were assisted by AI tools. The team reviewed and
validated the final code, notebooks, results, and written explanations.
```

TODO: Add any credits for external libraries, IBM Quantum access, solver
licenses, or institutional computing resources.

## License

TODO: Choose and add a final license before public release.

Suggested option for course-project code:

```text
MIT License
```

If the project includes course-restricted material, unpublished results, or
third-party assets with separate terms, confirm the appropriate license with
the instructor before publishing.
