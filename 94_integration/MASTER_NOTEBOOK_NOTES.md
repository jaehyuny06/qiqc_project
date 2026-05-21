# Master Notebook Notes

## Current Status

`00_master.ipynb` has been expanded from a lightweight draft into a more
complete Korean guided overview for beginner readers.

The notebook now removes the explicit `DRAFT` and `USER WILL REVISE` markers
from the narrative. It explains what each Agent/sub-topic contributed, why the
topic matters, how the code example should be interpreted, and how the five
parts connect through the shared Choi representation.

## What Was Expanded

| Section | Update |
| --- | --- |
| Title and Overview | Rewritten as a project-level overview explaining the role of all five Agents. |
| Introduction | Expanded with beginner-friendly explanations of quantum channels, CP, TP, and the shared Choi convention. |
| Foundations | Added detailed explanation of Kraus, Choi, Stinespring, and natural/Liouville representations. |
| Process Tomography | Clarified how reconstructed Choi matrices serve as diagnostics and why the master notebook uses saved offline data. |
| SDP Discrimination | Added operational interpretation of diamond norm, equal-prior discrimination, and the SDP input. |
| Quantum Combs | Expanded the bridge from single-step Choi matrices to multi-time processes with memory. |
| Interactive Widget | Added explanation of what the widget helps the reader see and how it supports intuition for the other sections. |
| Synthesis | Rewritten as a full narrative bridge connecting Agent-1 through Agent-5. |
| Conclusion | Expanded with accomplishments, limitations, and future directions. |
| References | Kept links to the consolidated bibliography and clarified why each key reference matters. |

## Validation

The notebook was executed successfully after the narrative expansion:

```bash
jupyter nbconvert --to notebook --execute --inplace 00_master.ipynb
```

Observed result:

- Execution completed successfully.
- Runtime was approximately 12 seconds in the current local environment.
- No hardware access was required.
- The SDP cell remained guarded against local solver failures.
- Korean text was preserved as UTF-8.
- No `???` mojibake runs were detected.
- No Unicode replacement character was detected.
- No explicit `DRAFT` or `USER WILL REVISE` markers remain in `00_master.ipynb`.

## Honest Remaining Gaps

- The process-tomography section remains hardware-ready rather than a confirmed
  live-hardware result. It uses saved offline-simulated data for reproducible
  execution.
- The SDP example is intentionally small and pedagogical. A stronger final
  research narrative could compute a diamond distance directly from Agent-2's
  reconstructed Choi matrix.
- The comb section connects conceptually to single-step Choi matrices, but it
  is not data-driven from the tomography output.
- The widget is qubit-focused and does not directly visualize two-qubit CNOT
  tomography or full quantum combs.

## Suggested Human Polish

- Add the final course title, team names, and instructor information if this
  notebook will be submitted.
- Decide whether to call Agent-2's section "Process Tomography on Real
  Hardware" or "Hardware-Ready Process Tomography" depending on the final
  hardware status.
- Add a single custom schematic showing the flow:
  `representations -> tomography -> discrimination -> combs -> widget`.
- If the final report includes live IBM data, replace the saved simulated
  example or add a short comparison cell.

