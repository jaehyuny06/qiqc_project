# Unified References

This bibliography consolidates references explicitly appearing in the five producer READMEs and notebooks. Metadata for complete entries was verified against publisher or arXiv records; incomplete software/documentation mentions are retained with `[VERIFY]` tags instead of invented fields.

## Textbooks

1. Michael A. Nielsen and Isaac L. Chuang. *Quantum Computation and Quantum Information*. 10th Anniversary Edition. Cambridge University Press, 2010. ISBN 9781107002173.
   - BibTeX key: `nielsen2010quantum`
   - Used by: `01_theory`
   - Context: Chapter 8 is cited for quantum channels, Kraus operators, Choi matrices, and representation conversions.

2. John Watrous. *The Theory of Quantum Information*. Cambridge University Press, 2018. DOI: `10.1017/9781316848142`.
   - BibTeX key: `watrous2018theory`
   - Used by: `01_theory`, `03_sdp_discrimination`
   - Context: Agent 1 cites Chapter 2 for basic quantum-information notions; Agent 3 cites Chapters 3 and 4 for state/channel distances and channel theory.

3. Mark M. Wilde. *Quantum Information Theory*. 2nd edition. Cambridge University Press, 2017. DOI: `10.1017/9781316809976`.
   - BibTeX key: `wilde2017quantum`
   - Used by: `01_theory`
   - Context: Chapter 4 is cited for quantum-information/channel background.

## Foundational Papers

No complete foundational-paper citation appears in the project inputs for the original Choi, Jamiołkowski, or Stinespring papers. The concepts appear in `01_theory/main.ipynb`, but the source metadata is not cited there. See [CITATION_AUDIT.md](CITATION_AUDIT.md) for suggested additions.

## Process Tomography

No complete academic process-tomography citation appears in the project inputs. `02_ibm_experiment` discusses quantum process tomography, linear inversion, MLE/CPTP projection, and Qiskit Experiments, but it does not cite a specific paper or documentation URL. See the `[VERIFY]` software/documentation entries and audit notes below.

## Channel Discrimination and SDP

1. John Watrous. “Semidefinite Programs for Completely Bounded Norms.” *Theory of Computing* 5(11):217-238, 2009. DOI: `10.4086/toc.2009.v005a011`. arXiv: `0901.4709`.
   - BibTeX key: `watrous2009semidefinite`
   - Used by: `03_sdp_discrimination`
   - Context: Primary reference for the diamond-norm semidefinite program used in binary quantum-channel discrimination.

2. John Watrous. *The Theory of Quantum Information*. Cambridge University Press, 2018. DOI: `10.1017/9781316848142`.
   - BibTeX key: `watrous2018theory`
   - Used by: `01_theory`, `03_sdp_discrimination`
   - Context: Textbook support for the diamond norm, state/channel distances, and unital channels.

## Non-Markovian Dynamics and Quantum Combs

1. Giulio Chiribella, Giacomo Mauro D'Ariano, and Paolo Perinotti. “Quantum Circuit Architecture.” *Physical Review Letters* 101:060401, 2008. DOI: `10.1103/PhysRevLett.101.060401`. arXiv: `0712.1325`.
   - BibTeX key: `chiribella2008quantum`
   - Used by: `04_quantum_combs`
   - Context: Quantum-comb formalism and multi-slot circuit/process representation.

2. Felix A. Pollock, César Rodríguez-Rosario, Thomas Frauenheim, Mauro Paternostro, and Kavan Modi. “Non-Markovian Quantum Processes: Complete Framework and Efficient Characterization.” *Physical Review A* 97(1):012127, 2018. DOI: `10.1103/PhysRevA.97.012127`. arXiv: `1512.00589`.
   - BibTeX key: `pollock2018nonmarkovian`
   - Used by: `04_quantum_combs`
   - Context: Process-tensor framework for multi-time non-Markovian quantum processes.

3. Heinz-Peter Breuer, Elsi-Mari Laine, and Jyrki Piilo. “Measure for the Degree of Non-Markovian Behavior of Quantum Processes in Open Systems.” *Physical Review Letters* 103:210401, 2009. DOI: `10.1103/PhysRevLett.103.210401`. arXiv: `0908.0238`.
   - BibTeX key: `breuer2009measure`
   - Used by: `04_quantum_combs`
   - Context: BLP trace-distance-revival witness used for information-backflow demonstrations.

4. Ángel Rivas, Susana F. Huelga, and Martin B. Plenio. “Entanglement and Non-Markovianity of Quantum Evolutions.” *Physical Review Letters* 105:050403, 2010. DOI: `10.1103/PhysRevLett.105.050403`. arXiv: `0911.4270`.
   - BibTeX key: `rivas2010entanglement`
   - Used by: `04_quantum_combs`
   - Context: RHP CP-divisibility witness used for non-Markovian dynamics.

## Software and Documentation

These software/documentation references appear as project dependencies or workflow mentions, but the inputs do not provide complete citation metadata. They are included with `[VERIFY]` tags so the user can decide whether to cite versioned documentation pages, release papers, or omit them from the final bibliography.

1. [VERIFY] *Qiskit Experiments*.
   - BibTeX key: `qiskitExperimentsVerify`
   - Used by: `02_ibm_experiment`
   - Context: Optional process-tomography submission path.

2. [VERIFY] *qiskit-ibm-runtime / QiskitRuntimeService*.
   - BibTeX key: `qiskitRuntimeVerify`
   - Used by: `02_ibm_experiment`
   - Context: Optional IBM Quantum hardware account/backend workflow.

3. [VERIFY] *Qiskit Aer Simulator*.
   - BibTeX key: `qiskitAerVerify`
   - Used by: `02_ibm_experiment`
   - Context: Suggested simulator fallback for realistic offline runs.

4. [VERIFY] *NumPy*.
   - BibTeX key: `numpyVerify`
   - Used by: `05_interactive_widget`
   - Context: Local numerical computation dependency.

5. [VERIFY] *Matplotlib*.
   - BibTeX key: `matplotlibVerify`
   - Used by: `05_interactive_widget`
   - Context: Choi heatmaps, Bloch deformation plots, and static dashboard preview.

6. [VERIFY] *ipywidgets*.
   - BibTeX key: `ipywidgetsVerify`
   - Used by: `05_interactive_widget`
   - Context: Interactive dashboard controls.
