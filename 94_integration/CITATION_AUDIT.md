# Citation Audit

## Extraction Summary

| Folder | Explicit references found | Context |
| --- | --- | --- |
| `01_theory` | Nielsen and Chuang; Watrous textbook; Wilde textbook | Channel representations, Choi matrices, Stinespring/natural forms, basic quantum-information background |
| `02_ibm_experiment` | [VERIFY] Qiskit Experiments; [VERIFY] qiskit-ibm-runtime / QiskitRuntimeService; [VERIFY] Qiskit Aer Simulator | Process-tomography workflow and optional IBM hardware/simulator path; no complete academic QPT citation found |
| `03_sdp_discrimination` | Watrous 2009; Watrous textbook | Diamond-norm SDP and quantum-channel discrimination |
| `04_quantum_combs` | Chiribella-D'Ariano-Perinotti 2008; Pollock et al. 2018; Breuer-Laine-Piilo 2009; Rivas-Huelga-Plenio 2010 | Quantum combs/process tensors and BLP/RHP non-Markovianity witnesses |
| `05_interactive_widget` | [VERIFY] NumPy; [VERIFY] Matplotlib; [VERIFY] ipywidgets | Widget dependencies and local visualization; no complete academic visualization citation found |

## References Appearing in Only One Folder

These are lower priority for cross-folder merging because they are currently single-folder citations.

- `nielsen2010quantum`: `01_theory`
- `wilde2017quantum`: `01_theory`
- `watrous2009semidefinite`: `03_sdp_discrimination`
- `chiribella2008quantum`: `04_quantum_combs`
- `pollock2018nonmarkovian`: `04_quantum_combs`
- `breuer2009measure`: `04_quantum_combs`
- `rivas2010entanglement`: `04_quantum_combs`
- `qiskitExperimentsVerify`: `02_ibm_experiment`
- `qiskitRuntimeVerify`: `02_ibm_experiment`
- `qiskitAerVerify`: `02_ibm_experiment`
- `numpyVerify`: `05_interactive_widget`
- `matplotlibVerify`: `05_interactive_widget`
- `ipywidgetsVerify`: `05_interactive_widget`

The only reference currently shared across producer folders is:

- `watrous2018theory`: `01_theory`, `03_sdp_discrimination`

## References Missing Key Information in the Project Inputs

The following entries are complete in `references.bib` because metadata was verified externally, but the original project citation text omitted important fields. This matters if the project wants citations to be self-contained in notebooks/READMEs.

- `nielsen2010quantum` [VERIFY original citation completeness]
  - Project text: “Nielsen and Chuang, Chapter 8.”
  - Missing in project input: full title, edition, publisher, year, ISBN.

- `watrous2018theory` [VERIFY original citation completeness]
  - Project text: “Watrous, Chapter 2” and “Watrous, The Theory of Quantum Information, Chapters 3 and 4.”
  - Missing in some project input: full title, publisher, year, DOI.

- `wilde2017quantum` [VERIFY original citation completeness]
  - Project text: “Wilde, Chapter 4.”
  - Missing in project input: full title, edition, publisher, year, DOI.

- `watrous2009semidefinite` [VERIFY original citation completeness]
  - Project text: “Watrous, Semidefinite programs for completely bounded norms (2009).”
  - Missing in project input: journal, volume, pages, DOI, arXiv ID.

- `chiribella2008quantum` [VERIFY original citation completeness]
  - Project text: “Chiribella, D'Ariano, and Perinotti, ‘Quantum circuit architecture’, 2008.”
  - Missing in project input: full first names, venue, volume, article number, DOI, arXiv ID.

- `pollock2018nonmarkovian` [VERIFY original citation completeness]
  - Project text: “Pollock et al., ‘Non-Markovian quantum processes: Complete framework and efficient characterization’, 2018.”
  - Missing in project input: full author list, venue, volume, article number, DOI, arXiv ID.

- `breuer2009measure` [VERIFY original citation completeness]
  - Project text: “Breuer, Laine, and Piilo, ‘Measure for the degree of non-Markovian behavior’, 2009.”
  - Missing in project input: full title, venue, volume, article number, DOI, arXiv ID.

- `rivas2010entanglement` [VERIFY original citation completeness]
  - Project text: “Rivas, Huelga, and Plenio, ‘Entanglement and Non-Markovianity of Quantum Evolutions’, 2010.”
  - Missing in project input: full first names, venue, volume, article number, DOI, arXiv ID.

## Software and Documentation Entries Needing Verification

These are intentionally incomplete in `references.bib`. The project mentions the software but does not cite a specific versioned documentation page, release paper, DOI, URL, or author list.

- `qiskitExperimentsVerify`
  - Missing: author/organization citation format, version, documentation URL or release paper, year.
  - Used in: `02_ibm_experiment`.

- `qiskitRuntimeVerify`
  - Missing: author/organization citation format, version, documentation URL, year.
  - Used in: `02_ibm_experiment`.

- `qiskitAerVerify`
  - Missing: author/organization citation format, version, documentation URL or release paper, year.
  - Used in: `02_ibm_experiment`.

- `numpyVerify`
  - Missing: citation choice, version, DOI or URL, year.
  - Used in: `05_interactive_widget`.

- `matplotlibVerify`
  - Missing: citation choice, version, DOI or URL, year.
  - Used in: `05_interactive_widget`.

- `ipywidgetsVerify`
  - Missing: citation choice, version, URL, year.
  - Used in: `05_interactive_widget`.

## Concepts Mentioned Without Full Source Citations

These concepts appear in the project, but their canonical references are not explicitly cited. They are not included in `references.bib` because the task requested no bibliography padding.

- Choi-Jamiołkowski isomorphism
- Stinespring representation/isometry
- Quantum process tomography / maximum-likelihood process tomography
- Entanglement-breaking channels
- Helstrom POVM
- Pauli transfer matrix / Bloch affine representation

## Suggested Additional References

The following are suggested additions only. They do not appear in `references.bib` because they were not explicitly cited in the project inputs.

- [SUGGESTION] Man-Duen Choi, “Completely positive linear maps on complex matrices,” *Linear Algebra and Its Applications*, 1975.
  - Why: canonical source for Choi positive semidefiniteness and complete positivity.

- [SUGGESTION] Andrzej Jamiołkowski, “Linear transformations which preserve trace and positive semidefiniteness of operators,” *Reports on Mathematical Physics*, 1972.
  - Why: canonical source for the Jamiołkowski correspondence.

- [SUGGESTION] W. Forrest Stinespring, “Positive functions on C*-algebras,” *Proceedings of the American Mathematical Society*, 1955.
  - Why: canonical source for the Stinespring dilation theorem.

- [SUGGESTION] Isaac L. Chuang and Michael A. Nielsen, “Prescription for experimental determination of the dynamics of a quantum black box,” *Journal of Modern Optics*, 1997.
  - Why: directly strengthens the Agent-2 process-tomography section.

- [SUGGESTION] Joseph F. Poyatos, J. Ignacio Cirac, and Peter Zoller, “Complete characterization of a quantum process: the two-bit quantum gate,” *Physical Review Letters*, 1997.
  - Why: classic quantum process tomography reference.

- [SUGGESTION] Mohseni, Rezakhani, and Lidar, “Quantum-process tomography: Resource analysis of different strategies,” *Physical Review A*, 2008.
  - Why: survey/resource-analysis reference for process tomography.

- [SUGGESTION] John Watrous, “Simpler semidefinite programs for completely bounded norms,” arXiv:1207.5726, 2012.
  - Why: useful follow-up for the diamond-norm SDP implementation, but the current project cites only the 2009 paper.

## Metadata Verification Sources Used

- Cambridge University Press pages for Nielsen-Chuang, Watrous, and Wilde textbooks.
- Theory of Computing and arXiv pages for Watrous 2009.
- APS/arXiv records for Chiribella-D'Ariano-Perinotti, Breuer-Laine-Piilo, and Rivas-Huelga-Plenio.
- APS/repository/arXiv records for Pollock et al. 2018.
