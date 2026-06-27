# Candidate Source Logging

Use this reference when implementing or analyzing PyFMTO algorithms that choose real evaluation points from multiple sources.

## Contents

- Core Question
- Privacy Boundary
- Minimum Fields
- Two-Stage Record
- Source Type Vocabulary
- Where To Log
- Example Record
- Negative Transfer Analysis
- Implementation Checklist

## Core Question

Every true evaluation must answer:

Which mechanism produced this evaluated point?

The answer must separate local search, transferred knowledge, server aggregation, random exploration, elite reuse, mutation, crossover, restart, and fallback behavior. Without this provenance, a result can show that performance improved or degraded, but cannot explain whether the mechanism caused positive transfer, negative transfer, or ordinary local progress.

## Privacy Boundary

Do not expose local true evaluation pairs `(x,y)` across clients.

Candidate-source logs should track provenance without joining a private local point and its true value in a shared place. Use local-only logs for private details and shared-safe summaries for server or cross-client analysis.

If a log would reveal another client's true evaluated `(x,y)` pair, remove the raw value, replace it with a candidate id or summary, or ask the user before continuing.

## Minimum Fields

Log one record when a candidate is selected for true evaluation, and optionally another record after the local result is known.

Minimum provenance fields:

- `eval_id`: stable id for this true evaluation.
- `client_id`: client or task that evaluates the point.
- `round_id` or `iter_id`: communication or optimization stage.
- `fe_index`: local true evaluation count after initialization.
- `stage`: initialization, early, middle, late, or restart.
- `source_type`: controlled source label.
- `source_owner`: local, server, cluster id, or source client id when safe.
- `source_detail`: short method detail, such as acquisition name or mutation rule.
- `parent_candidate_ids`: optional ids used to generate the point.
- `transfer_id`: id of the transferred package or server message, if any.
- `similarity`, `trust`, or `weight`: values used to accept or rank transferred knowledge.
- `selection_reason`: why this point was selected for real evaluation.
- `privacy_scope`: local_only, server_safe, or shared_safe.
- `outcome_summary`: improved, tied, worsened, failed, or unknown; avoid raw private y in shared logs.

## Two-Stage Record

Use a two-stage record when possible:

- `pre_eval`: created before the expensive objective call; contains provenance, source, trust, selection reason, and privacy scope.
- `post_eval`: created after the local result is known; contains only privacy-safe outcome summary in shared logs.

Raw `y` may appear only in `local_only` logs. Shared or server-safe logs should use `outcome_summary`, rank change, or normalized improvement category instead.

Do not write a shared record that joins a raw local `x` with its raw local `y`.

## Source Type Vocabulary

Use stable source labels so reports can count them across algorithms and variants.

Recommended labels:

- `init_random`: initialization sample.
- `random`: random exploration after initialization.
- `local_surrogate`: local surrogate proposes the point.
- `local_acquisition`: local acquisition function selects the point.
- `local_elite`: local elite archive reuses or refines a strong candidate.
- `local_evolution`: local evolutionary operator creates the point.
- `mutation`: mutation from one or more parents.
- `crossover`: crossover or recombination from parents.
- `transferred_candidate`: candidate directly suggested by transferred knowledge.
- `transferred_model`: candidate produced by a transferred model, prior, kernel, or hyperparameter summary.
- `server_aggregate`: server aggregation produces the point or ranking.
- `cluster_aggregate`: task cluster or neighborhood aggregation produces the point.
- `similarity_neighbor`: related task or neighbor guides the point.
- `restart`: restart or diversity recovery source.
- `fallback`: emergency source after fitting, transfer, or candidate generation fails.

If a project needs a new label, add it to the project-level notes and keep the old labels stable.

## Where To Log

Use three layers when possible:

- Client local provenance log: may include private local details needed for debugging, but must remain local.
- Server-safe summary log: source counts, transfer ids, trust values, accepted or rejected knowledge, and outcome summaries.
- Report-level aggregation: per-client and per-stage counts by `source_type`, plus weak-client and negative-transfer summaries.

Do not rely only on free-form text. Prefer structured records such as key-value rows, CSV rows, JSON lines, or table-like logger output that can be parsed later.

## Example Record

```text
eval_id=c03-r08-fe21, client_id=c03, round_id=8, fe_index=21, stage=middle, source_type=transferred_candidate, source_owner=server, transfer_id=srv-r08-msg02, similarity=0.72, trust=0.55, selection_reason=top_trusted_transfer_after_local_filter, privacy_scope=server_safe, outcome_summary=improved
```

This record explains the mechanism without exposing a raw local true `(x,y)` pair.

## Negative Transfer Analysis

Candidate-source logs should make these questions answerable:

- Which clients receive transferred or server-generated candidates?
- Which source types dominate weak clients versus strong clients?
- Does a client worsen after accepting transferred knowledge from low-similarity tasks?
- Does high trust actually correlate with improved outcomes?
- Does late transfer help exploitation or inject harmful candidates?
- Does disabling transfer reduce bad `transferred_candidate`, `transferred_model`, `server_aggregate`, or `cluster_aggregate` outcomes?
- Are improvements actually from local search rather than the proposed transfer module?

For paper conclusions, report both objective evidence and mechanism evidence. A transfer method is more convincing when improved clients show source logs consistent with the claimed transfer mechanism.

## Implementation Checklist

When editing an algorithm:

1. Assign an `eval_id` before each true evaluation.
2. Record the candidate source before calling the expensive objective.
3. Attach transfer, similarity, trust, parent, and selection metadata when available.
4. After the evaluation, record only a privacy-safe outcome summary in shared logs.
5. Count source types by client, stage, and repeat in reports or analysis scripts.
6. Treat unknown or missing source labels as a bug in diagnostic runs.
