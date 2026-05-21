# 통합 참고문헌

이 문서는 다섯 producer README와 notebook에 실제로 등장한 참고문헌을 통합한 것이다. 완전한 entry는 publisher, DOI, arXiv record 등을 통해 metadata를 확인했고, 입력 파일에 완전한 citation 정보가 없는 software/documentation 항목은 `[VERIFY]`로 표시했다.

## Textbooks

1. Michael A. Nielsen and Isaac L. Chuang. *Quantum Computation and Quantum Information*. 10th Anniversary Edition. Cambridge University Press, 2010. ISBN 9781107002173.
   - BibTeX key: `nielsen2010quantum`
   - 사용 folder: `01_theory`
   - 맥락: quantum channel, Kraus operator, Choi matrix, representation conversion.

2. John Watrous. *The Theory of Quantum Information*. Cambridge University Press, 2018. DOI: `10.1017/9781316848142`.
   - BibTeX key: `watrous2018theory`
   - 사용 folder: `01_theory`, `03_sdp_discrimination`
   - 맥락: channel theory, state/channel distance, diamond norm.

3. Mark M. Wilde. *Quantum Information Theory*. 2nd edition. Cambridge University Press, 2017. DOI: `10.1017/9781316809976`.
   - BibTeX key: `wilde2017quantum`
   - 사용 folder: `01_theory`
   - 맥락: quantum information/channel background.

## Foundational Papers

원 project input에는 Choi, Jamiołkowski, Stinespring 원 논문의 완전 citation이 들어 있지 않았다. 따라서 bibliography에는 넣지 않고, `CITATION_AUDIT_ko.md`의 suggested additions에 정리했다.

## Process Tomography

`02_ibm_experiment`는 process tomography, linear inversion, MLE/CPTP projection, Qiskit Experiments를 설명하지만 완전한 academic QPT citation은 제공하지 않았다. 관련 software/documentation 항목은 `[VERIFY]`로 유지한다.

## Channel Discrimination and SDP

1. John Watrous. "Semidefinite Programs for Completely Bounded Norms." *Theory of Computing* 5(11):217-238, 2009. DOI: `10.4086/toc.2009.v005a011`. arXiv: `0901.4709`.
   - BibTeX key: `watrous2009semidefinite`
   - 사용 folder: `03_sdp_discrimination`
   - 맥락: diamond norm SDP와 binary quantum-channel discrimination.

## Non-Markovian Dynamics and Quantum Combs

1. Giulio Chiribella, Giacomo Mauro D'Ariano, and Paolo Perinotti. "Quantum Circuit Architecture." *Physical Review Letters* 101:060401, 2008. DOI: `10.1103/PhysRevLett.101.060401`. arXiv: `0712.1325`.
   - BibTeX key: `chiribella2008quantum`

2. Felix A. Pollock, Cesar Rodriguez-Rosario, Thomas Frauenheim, Mauro Paternostro, and Kavan Modi. "Non-Markovian Quantum Processes: Complete Framework and Efficient Characterization." *Physical Review A* 97(1):012127, 2018. DOI: `10.1103/PhysRevA.97.012127`. arXiv: `1512.00589`.
   - BibTeX key: `pollock2018nonmarkovian`

3. Heinz-Peter Breuer, Elsi-Mari Laine, and Jyrki Piilo. "Measure for the Degree of Non-Markovian Behavior of Quantum Processes in Open Systems." *Physical Review Letters* 103:210401, 2009. DOI: `10.1103/PhysRevLett.103.210401`. arXiv: `0908.0238`.
   - BibTeX key: `breuer2009measure`

4. Ángel Rivas, Susana F. Huelga, and Martin B. Plenio. "Entanglement and Non-Markovianity of Quantum Evolutions." *Physical Review Letters* 105:050403, 2010. DOI: `10.1103/PhysRevLett.105.050403`. arXiv: `0911.4270`.
   - BibTeX key: `rivas2010entanglement`

## Software and Documentation

다음 항목은 project dependency 또는 workflow mention으로 등장하지만, 입력 파일에 versioned documentation page, release paper, DOI, URL, author list가 완전히 제공되지 않았다.

- `[VERIFY]` Qiskit Experiments: `qiskitExperimentsVerify`
- `[VERIFY]` qiskit-ibm-runtime / QiskitRuntimeService: `qiskitRuntimeVerify`
- `[VERIFY]` Qiskit Aer Simulator: `qiskitAerVerify`
- `[VERIFY]` NumPy: `numpyVerify`
- `[VERIFY]` Matplotlib: `matplotlibVerify`
- `[VERIFY]` ipywidgets: `ipywidgetsVerify`
