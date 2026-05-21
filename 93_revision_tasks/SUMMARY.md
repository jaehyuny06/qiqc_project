# Revision Task Summary

## Scope

This coordination pass read the Phase 2 validation outputs and converted them into producer-specific, actionable revision lists. No producer files were modified. The task files are:

- `AGENT_1_TASKS.md`
- `AGENT_2_TASKS.md`
- `AGENT_3_TASKS.md`
- `AGENT_4_TASKS.md`
- `AGENT_5_TASKS.md`

## Task Counts

| Producer | Folder | Critical | Major | Minor | Total | Estimated Complexity |
|----------|--------|----------|-------|-------|-------|----------------------|
| Agent-1 | `01_theory/` | 0 | 2 | 5 | 7 | Medium |
| Agent-2 | `02_ibm_experiment/` | 0 | 5 | 4 | 9 | High |
| Agent-3 | `03_sdp_discrimination/` | 0 | 1 | 6 | 7 | Low-Medium |
| Agent-4 | `04_quantum_combs/` | 0 | 4 | 4 | 8 | High |
| Agent-5 | `05_interactive_widget/` | 0 | 1 | 5 | 6 | Low-Medium |
| **Total** |  | **0** | **13** | **24** | **37** |  |

## Recommended Order of Execution

1. **Agent-2 first**: It has the most important deliverable gap. The diamond-distance proxy must be replaced or supplemented by a true SDP diamond norm before final integration can make quantitative claims about tomography results.
2. **Agent-4 second**: The comb causality hierarchy issue affects the conceptual correctness of the non-Markovian/comb section. Fixing this early will clarify whether related text and function names need broader changes.
3. **Agent-3 third**: It is mathematically sound and should be revised mainly to become the stable SDP/API reference that Agent-2 can mirror.
4. **Agent-1 fourth**: Its foundations are sound, but conversion coverage and notation cleanup should be completed before final report integration.
5. **Agent-5 fifth**: The widget is already functioning; its revisions are mostly labeling, API wrapping, and reproducibility polish.

## De-duplication Decisions

- Agent-2's `diamond_distance_proxy` was flagged by Validator-A, Validator-B, and Validator-C. It was merged into one Major task because all findings refer to the same underlying gap: a proxy is not the required diamond norm SDP.
- Agent-4's `comb_partial_trace_check` was flagged by Validator-A and Validator-B. It was merged into one Major task because both reports identify the same issue: the function checks only a global TP trace condition, not the full comb causality hierarchy.
- Dependency pinning was raised by Validator-B for every folder and reinforced by Validator-C's project-wide standards. It is listed separately for every producer because each folder has its own `requirements.txt`.
- Choi helper naming and argument-order mismatches were raised by Validator-C. They are included as producer-specific tasks where the local API differs from `UNIFIED_GLOSSARY.md`.
- Visual palette and heatmap issues were treated as minor unless they affect a producer's main deliverable. Validators did not flag any plot as mathematically wrong.

## Conflicts or Ambiguities

- No direct contradictions were found between validators.
- Some Validator-C recommendations are integration standards rather than local correctness bugs. These were prioritized as Major only when a function signature or argument order could plausibly break integration, and as Minor for notation, plot style, or document voice cleanup.
- Agent-4's RHP implementation was not deemed wrong by validators; it is a grid-based witness. The revision task is to label and explain it precisely, not to replace it with a full continuous RHP implementation.
- Agent-5 intentionally allows non-CP maps for teaching. The task is not to remove that feature, but to avoid labeling non-physical overlaps as process fidelities.

## Global Revision Standards

All agents should consult `92_validation_consistency/UNIFIED_GLOSSARY.md` during revision:

- Use unnormalized Choi matrices.
- Use input-first tensor order `A \otimes B`.
- Use `C_\mathcal{E}` for channel Choi matrices and `C_\Phi` for channel differences.
- Use `T` for quantum comb/process tensor Choi operators.
- Use `Tr_B(C_\mathcal{E})=I_A` for trace preservation.
- Prefer `d_in` and `d_out` in code.
- Prefer `apply_choi_channel(choi, rho, d_in=None, d_out=None)` for Choi-form channel application.
- Reserve "diamond norm" for SDP or analytic exact values; call heuristic quantities "proxies".
- Use `RdBu_r` for signed real/imaginary Choi heatmaps and `viridis` for magnitudes.
