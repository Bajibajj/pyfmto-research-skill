# Algorithm Improvement Protocol

Use this reference before modifying an existing PyFMTO algorithm for stronger performance.

## Principle

Improve from evidence, not from intuition alone.

Performance is the primary scientific target. Wall-clock time and implementation cost are secondary constraints: measure them, log them, and keep switches for expensive components, but do not reject a clearly stronger method only because it is slower.

Do not expose local true evaluation pairs `(x,y)`. Any server-side or cross-client knowledge must be a privacy-preserving summary, model, ranking, embedding, hyperparameter statistic, candidate suggestion, or other non-raw artifact.

## Mandatory Diagnosis Before Coding

Before changing an algorithm, choose the smallest diagnostic artifact set that can explain the current failure mode or hypothesis. Then inspect the relevant run artifacts:

- config values, especially budget, initialization, algorithm parameters, reporter comparisons, and ports;
- `loglevel: DEBUG` logs;
- `snapshot: true` snapshots;
- `verbose: true` console or file outputs;
- final reports, convergence curves, Excel tables, and per-client traces;
- candidate-source provenance when true evaluation origin matters;
- true-evaluation budget ledgers when comparing expensive black-box runs;
- ablation switch registry for modules that changed;
- transfer-event logs only when transfer is part of the hypothesis;
- similarity or trust matrix snapshots only when trust, similarity, clustering, or personalization is part of the hypothesis;
- surrogate model health logs only when model fit, uncertainty, or candidate quality may explain the result;
- weak-client behavior, not only average rank or final aggregate counts.

If logs are not detailed enough, first run a diagnostic repeat 1 experiment with `verbose: true`, `snapshot: true`, `loglevel: DEBUG`, candidate-source logging, and the selected diagnostic artifacts before designing a nontrivial change.

## Diagnosis Angles

Read the run as a system, not as a single score.

Check these angles:

- optimization stage: initialization, early exploration, middle transfer, late exploitation;
- candidate source: every true evaluation should be traceable to local surrogate, transferred suggestion, server aggregation, elite archive, random exploration, mutation, crossover, restart, fallback, or Bayesian acquisition;
- transfer timing: whether transfer starts too early, too late, too often, or after trust has collapsed;
- transfer content: whether the method sends useful structure or noisy summaries;
- task similarity: whether similarity separates related and unrelated clients under very few evaluations;
- trust matrix: whether high-trust pairs are actually related and stable across stages;
- transfer event: whether knowledge was sent, accepted, rejected, ignored, or used as intended;
- negative transfer: whether unrelated tasks receive harmful knowledge and which candidate sources caused the worsening;
- budget ledger: whether every client stays within `fe_max = 300` and whether duplicate evaluations waste budget;
- client usage: whether clients actually exploit received knowledge or ignore it;
- heterogeneity: whether gains come from easy clients while hard clients stagnate;
- surrogate health: fit failure, overconfidence, poor calibration, kernel instability, or expensive retraining;
- evolutionary behavior: diversity loss, premature convergence, mutation scale, elite pressure, and search-direction reuse;
- federated behavior: aggregation bias, stale knowledge, client imbalance, communication frequency, and privacy boundary;
- Bayesian behavior: acquisition balance, uncertainty quality, batch scoring, and exploration under `fe_max = 300`.

Summarize the failure mode in one or two sentences before proposing a change.

## Literature And Method Intake

When a stronger method may require new ideas, check recent and effective work in the relevant direction before implementation. Relevant directions include evolutionary computation, federated learning, multi-task learning, federated optimization, Bayesian optimization, surrogate-assisted optimization, transfer learning, meta-learning, and task-similarity estimation.

Do not import a modern method by name only. For each candidate idea, judge:

- Does it respect the `(x,y)` privacy boundary?
- Can it work with very few true evaluations?
- Does it fit `fe_max = 300`, including initialization?
- Does it handle heterogeneous or unrelated clients?
- Does it reduce or detect negative transfer?
- Can PyFMTO implement it cleanly without breaking discovery/config/reporting?
- Can expensive pieces be isolated behind switches for ablation?
- Is GPU or batched computation useful for this component?

Prefer ideas that create a clean paper story: clear failure mode, clear mechanism, clear ablation, and clear diagnostic signal.

## Change Proposal Template

Before coding an improvement, write a compact proposal with:

1. Diagnostic artifact set: which artifacts are selected and why.
2. Diagnosis evidence: which logs, snapshots, matrices, budget ledgers, surrogate health records, curves, or tables show the problem.
3. Failure mode: what is going wrong and for which clients or stages.
4. Hypothesis: why the proposed change should improve final objective values.
5. Mechanism: what changes in transfer timing, transfer content, similarity, client usage, surrogate, or search behavior.
6. Privacy check: what crosses the client-server boundary and why it is safe.
7. Ablation: the smallest switch that can remove the new component.
8. Expected signal: what should change in the selected artifacts, curves, and `+/-/≈` tables.
9. Cost note: extra CPU/GPU/memory/disk cost and whether it needs a fallback.

## Implementation Rules

Keep improvements traceable:

- Add parameters that can disable the new component.
- Log candidate-source provenance for every true evaluation in diagnostic runs.
- Log transfer source, selected clients, similarity/trust values, candidate source, and client usage when relevant.
- Keep only the transfer-event, trust-matrix, budget-ledger, surrogate-health, and ablation-switch artifacts that the method or claim depends on.
- Keep PyFMTO discovery names, config keys, report paths, and imports stable.
- Avoid stacking several untested ideas in one variant.
- Run smoke, pilot, diagnosis, repeat 3 performance test, ablation, and failure-client analysis before promoting a variant.
