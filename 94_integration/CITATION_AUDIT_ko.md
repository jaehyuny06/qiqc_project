# Citation Audit 한국어판

## 추출 요약

| Folder | 발견된 reference | 사용 맥락 |
| --- | --- | --- |
| `01_theory` | Nielsen and Chuang; Watrous textbook; Wilde textbook | Channel representation, Choi matrix, Stinespring/natural form |
| `02_ibm_experiment` | `[VERIFY]` Qiskit Experiments; qiskit-ibm-runtime; Qiskit Aer | QPT workflow와 optional IBM hardware/simulator path |
| `03_sdp_discrimination` | Watrous 2009; Watrous textbook | Diamond-norm SDP와 channel discrimination |
| `04_quantum_combs` | Chiribella et al. 2008; Pollock et al. 2018; Breuer-Laine-Piilo 2009; Rivas-Huelga-Plenio 2010 | Quantum comb/process tensor, BLP/RHP witness |
| `05_interactive_widget` | `[VERIFY]` NumPy; Matplotlib; ipywidgets | Widget dependency와 visualization |

## 한 폴더에만 등장하는 참고문헌

대부분의 reference는 한 folder에만 등장한다. Cross-folder로 공유되는 완전 reference는 현재 `watrous2018theory`뿐이며, `01_theory`와 `03_sdp_discrimination`에서 모두 사용된다.

## 원 입력에서 정보가 부족했던 항목

다음 항목들은 `references.bib`에서는 외부 metadata 확인으로 완성했지만, project input 자체에는 정보가 부족했다.

- `nielsen2010quantum`: title, edition, publisher, year, ISBN 부족.
- `watrous2018theory`: 일부 input에서 publisher, year, DOI 부족.
- `wilde2017quantum`: title, edition, publisher, year, DOI 부족.
- `watrous2009semidefinite`: journal, volume, pages, DOI, arXiv ID 부족.
- `chiribella2008quantum`: full author names, venue, volume, article number, DOI, arXiv ID 부족.
- `pollock2018nonmarkovian`: full author list, venue, volume, article number, DOI, arXiv ID 부족.
- `breuer2009measure`: full title, venue, volume, article number, DOI, arXiv ID 부족.
- `rivas2010entanglement`: full author names, venue, volume, article number, DOI, arXiv ID 부족.

## Software/Documentation 확인 필요

다음 항목은 project에서 언급되었지만 정확히 어떤 citation을 쓸지 결정해야 한다.

- Qiskit Experiments
- qiskit-ibm-runtime / QiskitRuntimeService
- Qiskit Aer Simulator
- NumPy
- Matplotlib
- ipywidgets

## Project에 개념은 등장하지만 완전 source citation이 없는 항목

- Choi-Jamiołkowski isomorphism
- Stinespring representation/isometry
- Quantum process tomography / maximum-likelihood process tomography
- Entanglement-breaking channels
- Helstrom POVM
- Pauli transfer matrix / Bloch affine representation

## Suggested Additional References

Bibliography에 무조건 넣은 것은 아니지만, final report를 강화하려면 다음 고전 reference를 추가하는 것이 좋다.

- Man-Duen Choi, "Completely positive linear maps on complex matrices," 1975.
- Andrzej Jamiołkowski, "Linear transformations which preserve trace and positive semidefiniteness of operators," 1972.
- W. Forrest Stinespring, "Positive functions on C*-algebras," 1955.
- Isaac L. Chuang and Michael A. Nielsen, "Prescription for experimental determination of the dynamics of a quantum black box," 1997.
- Joseph F. Poyatos, J. Ignacio Cirac, and Peter Zoller, "Complete characterization of a quantum process: the two-bit quantum gate," 1997.
- Mohseni, Rezakhani, and Lidar, "Quantum-process tomography: Resource analysis of different strategies," 2008.
- John Watrous, "Simpler semidefinite programs for completely bounded norms," 2012.
