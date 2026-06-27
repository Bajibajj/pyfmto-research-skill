# Variant Management

Use this reference when managing algorithm variants in a PyFMTO research project.

## Scope Rule

Keep this skill generic. Do not store project-specific algorithm results, variant rankings, or experiment conclusions inside the skill.

For each project, keep variant records in the project itself. Before creating a new variant, look for project-level notes such as:

- `experiments/*variant*.md`
- `notes/*variant*.md`
- `docs/*experiment*.md`
- `out/*analysis*.md`
- user-specified experiment notes

If no project-level ledger exists, ask before creating one.

## Recommended Ledger Fields

A project-level variant ledger should record:

- Variant name.
- Parent algorithm or baseline.
- Hypothesis being tested.
- Method change in one or two sentences.
- Config file path.
- Result directory or report path.
- Problem, dimension, NPD, budget, seed, and repeat count.
- Comparison group and reference algorithm.
- `+/-/≈` summary when available.
- Strong clients and weak clients.
- Selected diagnostic artifact set and reason.
- Candidate-source summary by stage and client when available.
- Transfer-event summary and similarity/trust snapshot notes.
- Budget ledger status and any violation.
- Surrogate health warnings or fallback usage.
- Ablation switches and run tags.
- Runtime, GPU usage, and resource-cost notes.
- Diagnostic clues from verbose logs.
- Decision: keep, merge, rerun, ablate, pause, or discard.

Do not treat repeat 1 results as final claims. Mark them as screening signals.

## Before Creating A Variant

1. Inspect existing project-level ledgers and reports.
2. Identify the closest previous variant.
3. State what is new and what hypothesis it isolates.
4. Decide the minimum ablation needed to test it.
5. Reuse existing config naming patterns when possible.
6. Keep aliases clear and short.
7. Add logging only for signals needed to analyze the hypothesis.

## After Running A Variant

1. Record where the config and results are stored.
2. Summarize performance against the intended reference algorithm.
3. Note runtime and resource costs as secondary evidence.
4. Record which diagnostic artifacts were selected and why.
5. Summarize which candidate sources helped or hurt when provenance logs exist.
6. Summarize transfer events, trust snapshots, budget ledger status, surrogate health warnings, and active ablation switches when available.
7. Identify weak clients or failure modes.
8. Decide whether to keep, merge, rerun with repeat 3, or discard.
9. Update only the project-level ledger, never this skill.
