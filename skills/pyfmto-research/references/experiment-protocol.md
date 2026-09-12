# Experiment Protocol

Use this reference when planning experiments after an algorithm change.

## Contents

- Stage 1: Smoke
- Stage 2: Pilot
- Stage 3: Diagnosis Before Improvement
- Stage 4: Parallel Ablation Batch
- Stage 5: Performance Test
- Stage 6: Report
- Stage 7: Failure-Client Analysis
- Stage 8: Claim Check

## Stage 1: Smoke

Goal: prove the algorithm can load and finish a tiny run.

Use a small problem, low dimension, low budget, `snapshot: false`, and `verbose: true`.

Check:

- `pyfmto list algorithms` passes.
- `pyfmto show algorithms.<ALG> -c <config.yaml>` exposes expected parameters.
- One tiny `pyfmto run` finishes.
- No import, port, logging, or shape errors appear.

## Stage 2: Pilot

Goal: detect whether the idea has any signal.

Use the main target problem with repeat 1, detailed logs, and normal budget. Do not claim significance from this stage.

Default target for this project: Arxiv2017, Gecco2020, and CEC after discovery-name confirmation.

## Stage 3: Diagnosis Before Improvement

Goal: understand why the algorithm succeeds or fails before changing it.

Use `verbose: true`, `snapshot: true`, and `loglevel: DEBUG` unless disk pressure makes this impossible.

Before inspecting everything, select a diagnostic level and the minimal artifact set required by the current hypothesis. Record the artifact output path, then inspect the relevant items:

- final objective values and `+/-/≈` comparison tables;
- convergence curves by stage: initialization, early exploration, middle transfer, late exploitation;
- per-client behavior, especially weak or unrelated clients;
- task-similarity, trust, transfer timing, transfer source, and client usage traces when available;
- transfer-event logs when transfer behavior is under diagnosis;
- similarity or trust matrix snapshots when trust, similarity, clustering, or personalization is under diagnosis;
- candidate-source provenance when real evaluation origin matters;
- true-evaluation budget ledger when budget validity or duplicate evaluations matter;
- surrogate health logs when model fitting, uncertainty, or candidate quality may explain the result;
- ablation switch registry for active or changed modules;
- negative-transfer signs where received knowledge worsens a client;
- unknown or missing candidate-source labels, which weaken mechanism analysis;
- runtime, GPU usage, memory, disk, and logging cost as secondary evidence.

Write a short diagnosis before proposing code changes: failure mode, affected clients, likely mechanism, and expected log signal after the fix.

## Stage 4: Parallel Ablation Batch

Goal: identify which module causes gains or failures.

After the main variant is ready, build the batch from the ablation switch registry:

- `main`: full algorithm.
- `no_transfer`: disable server transfer.
- `no_similarity`: disable task-similarity personalization.
- `no_local` or `no_elite`: remove local exploitation or elite candidate source.
- `fixed_schedule`: disable adaptive schedules such as kappa or trust decay.
- `cost_light`: reduce expensive candidate generation or model fitting for cost ablation.

Run them in parallel only after resource and effective client/server port isolation checks in [server-experiment-orchestration.md](server-experiment-orchestration.md) pass; the upstream default port is shared.

## Stage 5: Performance Test

Default performance-test repeat is `3`.

Use `repeat: 3` before deciding whether a variant deserves larger repeat counts. Keep `verbose: true`, `snapshot: true`, `loglevel: DEBUG`, and the artifacts required by the selected diagnostic level unless disk pressure is high.

## Stage 6: Report

Generate console, Excel, and curve reports.

When evaluating the user's method, put it last so it becomes the final algorithm column and comparison target:

```yaml
comparisons:
  - [FDEMD, FMTBO, IAFFBO, NEWALG]
```

For ablations against the full method, put the full method last. Use IAFFBO last only when the user selects it as the target. Before interpreting a report, follow the data-coverage and symbol checks in [result-analysis.md](result-analysis.md); missing target data must not be treated as a valid comparison.

## Stage 7: Failure-Client Analysis

Do not only report aggregate wins.

For weak clients, inspect:

- objective scale and whether log transform was active;
- selected candidate sources and their outcome summaries;
- transfer mode, transfer event decision, and trust value;
- similarity or trust neighbors selected for that client;
- early, middle, and late convergence;
- whether local, elite, server, or random candidates caused improvements;
- whether surrogate health degraded before the weak-client failure;
- whether the task appears unrelated to the transferred knowledge.

## Stage 8: Claim Check

Map results to claims conservatively:

- Main method beats baselines: assess matched budgets, repeated-run variability, per-client regressions, and valid statistics. Repeat 3 is a screening default, not sufficient evidence by itself.
- Similarity module helps: supported only if `no_similarity` drops while other settings stay controlled.
- Transfer module helps: supported only if `no_transfer` drops or convergence slows and transfer-event logs show the module was actually used.
- Trust or similarity module helps: supported only if trust snapshots show plausible neighbors and the controlled ablation drops.
- Budget validity: required before comparing methods; budget ledger violations invalidate the run.
- Surrogate failure explanation: required when weak clients fail after model-health warnings.
- Runtime advantage: supported only if wall-clock logs show lower or comparable runtime.
- Expensive-but-strong method: supported only if objective gains are stable, the mechanism is interpretable, and the expensive component has an ablation or switch.
- Robust heterogeneity: supported only if weak or unrelated clients do not collapse.

If evidence is mixed, write a narrower claim and plan the next ablation.
