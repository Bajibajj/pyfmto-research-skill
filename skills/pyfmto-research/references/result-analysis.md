# Result Analysis

Use this reference when interpreting PyFMTO reports, comparing algorithms, reading convergence curves, or drafting paper-style conclusions. The operational details below describe the audited 0.3.4 implementation; confirm the installed version using [framework-operations.md](framework-operations.md).

## Result Coverage Before Claims

1. Record intended and actually loaded comparison members; inspect `Available data`, `Unavailable data`, and table headers. Missing algorithms are skipped by the current reporter, so missing target data can change the last column and target. Do not present this as the requested comparison.
2. Match result roots, aliases, dimensions, FE/NPD/seed prefixes, client IDs, and actual repeat counts. Reporter loads all matching files, not a subset capped by launcher.repeat.
3. Check raw records for incomplete, unequal-length, non-finite, or mixed-protocol data before summarizing. Preserve the raw files; do not invent missing runs or silently discard failures.
4. If the user requested only analysis or report generation, report missing data rather than starting new optimization to fill it.

## PyFMTO `+/-/≈` Rule

PyFMTO's table generator compares each available algorithm against the last successfully loaded algorithm in that `comparisons` group. Verify full coverage before treating it as the requested target.

For a comparison list such as:

```yaml
comparisons:
  - [FDEMD, FMTBO, IAFFBO, NEWALG]
```

`NEWALG` is the comparison target and final algorithm column. `FDEMD`, `FMTBO`, and `IAFFBO` are compared against it. If the user explicitly chooses IAFFBO as the target, put IAFFBO last and state that target instead.

The suffix is attached to the compared algorithm's mean value:

- `+`: the compared algorithm is significantly better than the reference algorithm.
- `-`: the compared algorithm is significantly worse than the reference algorithm.
- `≈`: no detected significant difference from the reference algorithm; this does not establish equivalence.

The objective is minimized, so a smaller mean optimum is better.

## Statistical Test

PyFMTO uses an independent samples t-test on the best optimum lists from repeated runs.

Default `pvalue` is `0.05` unless configured otherwise. The current `scipy.stats.ttest_ind` call uses its defaults; it is not automatically a paired test or a multiple-comparison correction. Treat the suffix rules as meaningful only when the test result is finite and its assumptions are appropriate. Tiny samples or constant data can yield NaN, for which the current branch can produce a misleading `+` or `-`; report this limitation instead of claiming significance.

Decision logic:

1. If test p value is greater than configured `pvalue`, mark `≈`.
2. Otherwise, if compared mean is larger than reference mean, mark `-`.
3. Otherwise, mark `+`.

When explaining results, state the reference algorithm explicitly. Do not say “the method is +” without saying what it is compared against.

## Table Interpretation

For each client/task:

- Read mean best optimum values row by row.
- Interpret suffixes relative to the last algorithm in the comparison group.
- Use the summary row `+/-/≈` as each compared column's task counts against the target, not as the target method's own win/loss/tie counts; the target's summary cell is blank.
- Treat highlighted cells as best observed means, but still discuss statistical suffixes separately.

The Excel sheet is `Global`; its first column is `Clients`. Cells are formatted mean final best-so-far values across repeats, including initialization, with suffixes on compared columns. They are not a cross-client global mean or a built-in mean-plus-standard-deviation table. Map task IDs explicitly rather than treating row position as the task ID.

The current preprocessing clips every best-so-far value below `1e-20` to `1e-20`, including negative objectives; this affects Excel even with log plotting disabled. Compare against original `.msgpack` values when negative or near-zero values matter. Do not claim the exported mean is always the raw mean.

If repeat count is too small, state that statistical conclusions are weak. For example, `1.00e+01-` in a baseline column means that baseline lost to the target under a valid test, not that the target lost.

## Curve Analysis

When analyzing convergence curves, discuss:

- Early phase: whether transfer helps before enough local samples exist.
- Middle phase: whether the method accelerates improvement or avoids stagnation.
- Late phase: whether it reaches a better final optimum.
- Stability: the audited shading is standard error, not standard deviation or a confidence interval; inspect repeated-run variability separately.
- Negative transfer: whether unrelated tasks degrade performance after receiving knowledge.
- Candidate-source attribution: which source types produced improvements or failures at each stage.

Use log-transformed curves when appropriate for the objective domain and state the transformation. The audited reporter computes mean and standard error after log10 transformation, not log10 of the original mean. Its x-axis indexes saved evaluation records (including initialization by default), although labeled `Iteration`; do not equate it with communication rounds for batch algorithms.

The final algorithm is drawn in red. Violin reports show only that algorithm's initial versus subsequent decision-coordinate samples, not every algorithm's final fitness distribution. Set `merge: false` for separate figures or vector output such as `.svg`/`.pdf`; merging may clean the individual-image directory.

## Mechanism Evidence

When explaining why a method works or fails, inspect the selected artifacts first. Add more artifacts only when the mechanism remains ambiguous.

Possible evidence includes:

- transfer-event logs: whether knowledge was sent, accepted, rejected, ignored, or used;
- similarity/trust snapshots: whether high-trust neighbors look plausible;
- true-evaluation budget ledgers: whether each client stayed within budget;
- surrogate health logs: whether model failure explains poor candidates;
- ablation switch registry: whether the intended module was actually enabled or disabled;
- candidate-source logs: whether gains came from the claimed mechanism or from local search.

Do not claim a mechanism from final objective values alone.

## Paper-Style Claim Template

When drafting conclusions, separate evidence from interpretation:

1. State the setting: problem, dimension, budget, NPD, repeat count, baselines, and reference algorithm.
2. Report table evidence: final mean, `+/-/≈` counts, and where improvements are concentrated.
3. Report curve evidence: convergence behavior, final plateau, and stability.
4. Explain why the method helps in FMTO terms: similarity estimation, trust matrix behavior, transfer timing, transferred knowledge, candidate-source attribution, client usage, surrogate health, or heterogeneity handling.
5. Mention limitations: weak tasks, small repeat count, unstable clients, unknown candidate sources, missing transfer events, missing trust snapshots, budget ledger issues, surrogate health warnings, or possible negative transfer.
6. Suggest next ablations.
