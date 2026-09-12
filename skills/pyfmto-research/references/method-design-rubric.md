# Method Design Rubric

Use this reference when judging a new algorithm idea, improving an existing algorithm, or choosing among variants.

## Required Questions

For every method proposal, answer these before coding:

1. What minimal diagnostic artifact set is needed for this proposal?
2. What diagnosis evidence from DEBUG logs, snapshots, verbose outputs, selected artifacts, curves, tables, or weak-client traces motivates the change?
3. What hypothesis does the method test?
4. What is the strongest novelty compared with IAFFBO, FMTBO, and FDEMD?
5. What private local information remains hidden?
6. What is transferred, when is it transferred, and how is it used by the client?
7. How does the method estimate or avoid task similarity?
8. How does it suppress negative transfer?
9. Why should the change improve final objective values, stability, convergence, or weak-client behavior?
10. What runtime cost should be measured and recorded?
11. Can any part use GPU or vectorized/batched computation?
12. What ablation proves the contribution?

## Quality Criteria

Prefer methods that:

- Improve final objective values under `fe_max = 300`.
- Improve stability, convergence behavior, or weak-client outcomes when aggregate gains are close.
- Record wall-clock time and justify extra cost when performance gains are meaningful.
- Use privacy-preserving summaries instead of true `(x,y)` pairs.
- Produce interpretable logs for transfer source, timing, trust, and client usage.
- Record candidate-source provenance for true evaluation points, including privacy-safe outcome summaries.
- Keep selected transfer-event, similarity/trust matrix, budget-ledger, surrogate-health, and ablation-switch artifacts when the method uses those mechanisms.
- Have one or two clear ablation switches.
- Fail gracefully on unrelated tasks.

## Runtime Cost Checklist

Runtime is secondary to objective quality and scientific evidence, but it must be measured. Before adding a complex component, estimate:

- Training cost per client per iteration.
- Candidate-pool size and scoring cost.
- Server aggregation cost.
- Communication and synchronization overhead.
- Extra disk cost from verbose logs and snapshots.
- Whether repeat experiments remain practical.

If a component improves quality but increases time heavily, do not reject it automatically. Require a switch to disable it, an ablation to justify it, and a note explaining the performance-cost tradeoff.

## Latest Method Checklist

When performance improvement needs new ideas, review recent and effective methods from evolutionary computation, federated learning, multi-task learning, federated optimization, Bayesian optimization, surrogate-assisted optimization, transfer learning, meta-learning, and task similarity.

Before adopting an idea, check:

- It does not leak true `(x,y)` pairs.
- It can work under very few evaluations and `fe_max = 300`.
- It handles task heterogeneity and has a negative-transfer defense.
- It creates a clear ablation and a clear log signal.
- It can fit PyFMTO discovery, config, run, report, and snapshot workflows.
- It can use GPU or batching when naturally suitable, without forcing GPU where the workload is CPU-bound.

## GPU Checklist

Prefer GPU when the workload has large batched tensor operations, neural surrogates, deep kernels, large candidate scoring batches, or GPU-supported models.

Be cautious when using DACE, scikit-learn Gaussian processes, small-dimensional local optimization, or frequent Python process synchronization. These are often CPU-bound.

When adding GPU code:

- Keep CPU fallback.
- Avoid moving tiny arrays repeatedly between CPU and GPU.
- Log whether GPU was used.
- Compare wall-clock time against the CPU version.
- Design experiments so GPU-heavy variants can run alongside CPU-heavy ablations when server resources allow.

## Promotion Rule

Do not promote a variant to the main line from one lucky run.

Suggested ladder:

1. Smoke passes without loading/import/config failure.
2. Pilot repeat 1 shows a plausible signal.
3. Detailed diagnosis explains the likely gain or failure mode.
4. Performance test repeat 3 improves or ties key baselines and records runtime cost.
5. Selected diagnostic artifacts are complete enough to explain the claimed mechanism.
6. Ablation identifies which component caused the gain.
7. Failure-client analysis explains remaining weak tasks.
8. Only then consider repeat 5 or repeat 10 for stronger claims.

If runtime worsens sharply, the result can still continue only when the objective gain is strong, the mechanism is interpretable, and the expensive component is ablated or switchable.
