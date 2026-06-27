# Diagnostic Artifact Standards

Use this reference when designing, implementing, running, or analyzing PyFMTO algorithms where mechanism-level evidence matters.

## Contents

- Artifact Selection Policy
- Diagnostic Levels
- Output Path Convention
- Transfer Event Log
- Similarity And Trust Matrix Snapshot
- True Evaluation Budget Ledger
- Surrogate Model Health Log
- Ablation Switch Registry

## Principle

A diagnostic run should explain why a result changed, not only whether it changed.

For expensive federated many-task optimization, keep these artifacts whenever feasible:

- Transfer event log.
- Task similarity or trust matrix snapshot.
- True evaluation budget ledger.
- Surrogate model health log.
- Ablation switch registry.

These artifacts complement candidate-source logging. Candidate-source logs explain where evaluated points came from. The artifacts here explain why transfer happened, whom the method trusted, whether the budget was respected, whether the surrogate was healthy, and which modules were active.

Keep the privacy boundary: do not share local true `(x,y)` pairs across clients.

## Artifact Selection Policy

Do not enable or load every diagnostic artifact by default. Choose the smallest set that can answer the current hypothesis or failure mode.

Default lightweight set:

- Candidate-source provenance for true evaluation points.
- True-evaluation budget ledger when budgets are being compared or enforced.
- Ablation switch registry for any changed module.

Add artifacts only when relevant:

- Add transfer-event logs when the method sends, receives, filters, or uses transferred knowledge.
- Add similarity or trust matrix snapshots when the method uses task similarity, trust, neighborhoods, clustering, or personalization.
- Add surrogate health logs when candidate quality, uncertainty, model fitting, or surrogate choice may explain the result.
- Add all major artifacts only for ambiguous failures, final repeat 3 mechanism evidence, or paper claims that depend on the full causal story.

Before running or analyzing an experiment, state the selected artifact set and why. Missing irrelevant artifacts should not block analysis. Missing relevant artifacts should weaken or block mechanism claims.

## Diagnostic Levels

Use diagnostic levels to avoid enabling every artifact by habit.

Level 1: Provenance

- Candidate-source log.
- True-evaluation budget ledger.
- Ablation switch registry for changed modules.

Level 2: Transfer Diagnosis

- Level 1 artifacts.
- Transfer-event log.
- Similarity or trust matrix snapshot when applicable.

Level 3: Surrogate And Paper Audit

- Level 2 artifacts.
- Surrogate health log.
- Full weak-client mechanism analysis.
- Runtime and cost summary.

Default to Level 1 for new variants, smoke-adjacent pilots, and basic performance tests. Use Level 2 when transfer, trust, similarity, clustering, neighborhoods, or personalization are part of the hypothesis. Use Level 3 when surrogate behavior, ambiguous failures, repeat 3 promotion, or paper claims need a deeper audit.

## Output Path Convention

Keep diagnostic artifacts separate from screen output logs.

Default artifact root:

```text
out/_diagnostics/<run_id>/<algorithm>/<problem>/<repeat_id>/
```

Use a short `run_id` that matches the config or output naming when possible. For dimensions, NPD settings, or ablation tags, include them in `run_id`, `problem`, or an adjacent metadata file instead of changing field meanings.

Recommended artifact names:

- `candidate_sources.jsonl` or `candidate_sources.csv`.
- `transfer_events.jsonl`.
- `similarity_trust_snapshots.npz`, `similarity_trust_snapshots.jsonl`, or one file per snapshot.
- `budget_ledger.csv`.
- `surrogate_health.jsonl`.
- `ablation_switches.yaml` or `ablation_switches.json`.
- `runtime_cost_summary.json` or `runtime_cost_summary.csv`.
- `weak_client_mechanism.md` for Level 3 analysis notes.

Use `out/_logs/` for screen stdout and stderr logs. Do not mix large diagnostic artifacts into screen logs unless the local project already has a stronger convention.

## Transfer Event Log

Record one event whenever transfer knowledge is created, sent, accepted, rejected, transformed, or used for candidate selection.

Minimum fields:

- `event_id`: stable id for the transfer event.
- `round_id` or `iter_id`: communication or optimization stage.
- `source_client` or `source_group`: origin of the knowledge, using safe ids.
- `target_client`: receiver of the knowledge.
- `transfer_type`: candidate, model_summary, surrogate_prior, kernel_param, ranking, task_embedding, search_direction, trust_weight, acquisition_hint, or statistic.
- `transfer_payload_id`: id of the transferred object, not raw private `(x,y)`.
- `similarity`, `trust`, or `weight`: values that justified the transfer.
- `decision`: sent, accepted, rejected, clipped, delayed, ignored, or used.
- `usage_mode`: candidate_pool, surrogate_prior, acquisition_bias, mutation_direction, restart_seed, elite_filter, or fallback.
- `privacy_scope`: local_only, server_safe, or shared_safe.
- `outcome_summary`: improved, tied, worsened, failed, unused, or unknown.

Use this log to connect transfer timing and transfer content to candidate-source outcomes and negative-transfer analysis.

## Similarity And Trust Matrix Snapshot

For heterogeneous tasks, save a task-to-task similarity or trust matrix at important rounds.

Snapshot when:

- transfer begins;
- trust or similarity is recomputed;
- clustering or neighbor selection changes;
- a client accepts or rejects transferred knowledge;
- before and after major adaptive schedule changes.

Minimum fields:

- `snapshot_id`, `round_id`, and `stage`.
- `client_order`: stable order of rows and columns.
- `matrix_type`: similarity, trust, weight, distance, or cluster_membership.
- `matrix_values`: N × N values or a sparse equivalent.
- `normalization`: how values are scaled.
- `diagonal_policy`: self value, ignored, or masked.
- `top_neighbors`: selected neighbors per client.
- `rejected_neighbors`: blocked or down-weighted neighbors when available.
- `reason`: periodic, transfer_trigger, cluster_update, failure_analysis, or ablation.

In analysis, inspect whether high-trust pairs are actually related and whether weak clients trusted harmful sources.

## True Evaluation Budget Ledger

In expensive black-box runs, every true evaluation must be accountable.

Keep a per-client ledger with:

- `client_id`, `problem`, `dim`, `repeat_id`, and `seed`.
- `fe_max`: total allowed true evaluations, normally `11 × dim`.
- `fe_init`: initialization evaluations.
- `fe_used`: current true evaluations used.
- `remaining_fe`: remaining true evaluations.
- `eval_id`: id matching candidate-source logs.
- `eval_stage`: initialization, early, middle, late, restart, or fallback.
- `source_type`: link to candidate-source provenance.
- `is_duplicate`: whether the point duplicates a previous local evaluation.
- `budget_status`: within_budget, exhausted, blocked, or violation.

Treat a budget violation as a serious experiment validity problem. Do not compare a variant against baselines until the budget ledger is clean.

## Surrogate Model Health Log

Record surrogate health so failures are not wrongly blamed on transfer.

Minimum fields:

- `client_id`, `round_id`, `stage`, and `model_type`.
- `n_train`: number of local or allowed training samples.
- `dim`: search dimension.
- `fit_status`: success, warning, failed, fallback, or skipped.
- `fit_time` and `predict_time` when available.
- `condition_flag`: stable, ill_conditioned, singular, overfit, underfit, or unknown.
- `uncertainty_summary`: min, median, max, or calibrated/unreliable flag.
- `prediction_error_proxy`: cross-validation error, leave-one-out error, ranking consistency, or unavailable.
- `hyperparameter_summary`: safe kernel, length-scale, regularization, or model parameter summary.
- `fallback_used`: true or false.
- `health_action`: continue, regularize, refit, switch_model, trust_down, or fallback.

For GP, KRG, RBFN, SVR, or neural surrogates, log enough to distinguish model pathology from bad transfer.

## Ablation Switch Registry

Maintain a registry for every configurable research module.

Recommended fields:

- `switch_name`: exact config key or code parameter.
- `module`: similarity, trust, candidate_filter, uncertainty_gate, server_clustering, elite_archive, gpu_scoring, fallback, transfer_schedule, or surrogate_health.
- `default_value`: default setting for the main method.
- `ablation_value`: value used to disable or weaken the module.
- `ablation_name`: short run tag, such as no_similarity or no_trust.
- `hypothesis`: what the module is expected to improve.
- `expected_signal`: what should change in logs, curves, matrices, or tables.
- `dependencies`: switches that must stay fixed for a fair test.
- `privacy_effect`: whether the switch changes shared information.
- `cost_effect`: expected CPU, GPU, memory, disk, or communication cost.
- `status`: planned, implemented, tested, promoted, paused, or discarded.

Do not promote a module that cannot be disabled or isolated in an ablation.
