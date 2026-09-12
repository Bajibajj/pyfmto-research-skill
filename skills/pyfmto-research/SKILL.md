---
name: pyfmto-research
description: Federated many-task optimization research and PyFMTO implementation workflows. Use when Codex helps with FMTO, expensive black-box optimization, privacy-preserving multi-task transfer, task similarity, heterogeneous clients, evolutionary computation, federated learning, multi-task learning, federated optimization, Bayesian optimization, surrogate-assisted optimization, diagnosis-first algorithm improvement, candidate-source logging, transfer-event logging, similarity/trust matrix snapshots, evaluation budget ledgers, surrogate health diagnostics, ablation switch registries, runtime/GPU-aware algorithm design, new PyFMTO algorithms/problems, experiment configs, screen-based server experiments, pyfmto run/report workflows, result analysis, paper-style conclusions, or debugging PyFMTO loading/import/config failures.
---

# PyFMTO Research

Use this skill as a full-cycle assistant for federated many-task optimization research on PyFMTO projects. Prioritize the user's research constraints over generic optimization advice, and ask when a scientific or privacy assumption is unclear.

## Core Priorities

1. Support the full loop: idea → method → PyFMTO implementation → config → run → report → result interpretation.
2. Make algorithm improvement diagnosis-first: inspect DEBUG logs, snapshots, verbose traces, curves, reports, weak-client behavior, and candidate-source provenance before changing code.
3. Require every true evaluation point to have a traceable source: local search, transfer, server aggregation, random, elite, mutation, crossover, restart, or fallback.
4. Select the minimal necessary diagnostic artifact set before enabling logs or loading detailed references.
5. Preserve mechanism-level diagnostics when relevant: transfer events, similarity/trust matrices, true-evaluation budget ledgers, surrogate health logs, and ablation switch registries.
6. Optimize for final objective quality, innovation strength, and scientific evidence first; treat wall-clock time as a measured secondary constraint.
7. Preserve the privacy boundary: never expose local true evaluation pairs `(x,y)`.
8. Treat innovation strength as the main criterion when comparing possible method directions.
9. Consider wall-clock cost, parallelism, and GPU feasibility when designing algorithms, but do not make low runtime the first priority unless the user says so.
10. Prefer PyFMTO conventions and existing project templates over invented structure.

## Decision Flow

1. Classify the request: research idea, algorithm implementation, algorithm improvement, problem implementation, experiment config/run, result analysis, or PyFMTO debug.
2. Load only the reference files needed for that class of task. For config/run/resume/report/debug, first read `references/framework-operations.md`; it supplies the version check, working-directory rules, and completion evidence.
3. For algorithm improvement, read `references/algorithm-improvement-protocol.md` before proposing code changes.
4. Inspect the local PyFMTO project before editing or running anything.
5. State the intended change or experiment plan and wait for approval before coding when requirements are not fully specified.
6. Implement with relative imports, explicit public exports, and PyFMTO-compatible config names.
7. Validate availability with PyFMTO list/show commands when possible.
8. For authorized experiments, record the resolved config, runtime version, results, and completion evidence described in `references/framework-operations.md`. Config-only and report-only requests do not authorize new optimization runs.

## Reference Navigation

Read these files only when needed:

- `references/research-frame.md`: Use for idea analysis, method design, innovation comparison, task similarity, transfer timing/content/usage, privacy, and heterogeneity.
- `references/pyfmto-workflow.md`: Use for implementing or modifying algorithms/problems and debugging PyFMTO discovery/import/config issues.
- `references/repo-map.md`: Use when working inside this repository or when locating templates, algorithms, problems, configs, and outputs.
- `references/framework-operations.md`: Use before setup, run, resume, report, or operational debugging; verify the installed framework and project before applying version-specific instructions.
- `references/experiment-config.md`: Use when creating or editing experiment YAML files, baseline comparisons, budgets, report formats, and detailed run settings. It links copyable config assets.
- `references/result-analysis.md`: Use when interpreting Excel/console/curve reports, `+/-/≈` counts, convergence plots, and paper-style claims.
- `references/domain-map.md`: Use when connecting FMTO with evolutionary computation, federated learning, multi-task learning, federated optimization, Bayesian optimization, and surrogate-assisted optimization.
- `references/method-design-rubric.md`: Use when judging a new algorithm idea or improvement by innovation, privacy, objective quality, runtime cost, GPU potential, and ablation value.
- `references/algorithm-improvement-protocol.md`: Use before modifying an existing algorithm; diagnose DEBUG logs, snapshots, verbose traces, curves, tables, and weak-client behavior before coding.
- `references/candidate-source-logging.md`: Use when implementing or analyzing real evaluation provenance; every evaluated point should record whether it came from local search, transfer, server aggregation, random, elite, mutation, crossover, restart, or fallback.
- `references/diagnostic-artifact-standards.md`: Use when defining transfer-event logs, similarity/trust matrix snapshots, true-evaluation budget ledgers, surrogate health logs, and ablation switch registries.
- `references/experiment-protocol.md`: Use when planning smoke, pilot, repeat, ablation, report, failure-client analysis, and claim-check stages.
- `references/server-experiment-orchestration.md`: Use when running multiple experiments on the server with conda `fmto`, screen, ports, logs, CPU/GPU checks, and repeat defaults.
- `references/variant-management.md`: Use when managing algorithm variants; keep project-specific variant ledgers inside the project, not inside this reusable skill.

## Research Defaults

Frame FMTO methods around these questions:

- Before improving an algorithm, what do DEBUG logs, snapshots, verbose outputs, curves, tables, candidate-source logs, and weak-client traces show?
- For each true evaluation point, was it produced by local search, transfer, server aggregation, random exploration, elite reuse, mutation, crossover, restart, or fallback?
- Which transfer events, similarity/trust snapshots, budget ledger entries, surrogate health logs, and ablation switches explain the mechanism?
- How is task similarity estimated under very few evaluations?
- When should transfer happen: early, middle, late, or adaptively?
- What is transferred: model parameters, surrogate priors, kernel/hyperparameter summaries, sampling suggestions, rankings, task embeddings, search directions, or statistics?
- How does a client use received knowledge without exposing local true `(x,y)` pairs?
- How does the method avoid negative transfer under task heterogeneity?
- What is the innovation compared with IAFFBO, FMTBO, and FDEMD?
- Does the method improve final objective values, stability, convergence, or weak-client behavior; and what runtime cost should be recorded?

## Experiment Defaults

Use these defaults unless the user overrides them:

- Main baselines: `FDEMD`, `FMTBO`, `IAFFBO`.
- When evaluating the user's new method, put that method last in each `reporter.comparisons` group so it is the final algorithm column and comparison target. Put `IAFFBO` last only when the user explicitly selects it as the target; preserve an explicitly requested order.
- Main problems: `Arxiv2017`, `Gecco2020`, and the CEC problem package available through PyFMTO discovery.
- Use `npd: 1` for the default IID setting; these benchmarks already contain task heterogeneity.
- Use total true evaluation budget `fe_max: 300`; this total includes initialization evaluations.
- Use detailed experiment settings: `verbose: true`, `snapshot: true`, `loglevel: DEBUG`.
- For algorithm improvement, keep detailed diagnostics until the failure mode and the gain mechanism are clear.
- Track candidate-source provenance for each true evaluation in diagnostic runs.
- Choose a diagnostic level and artifact output path before long diagnostic runs.
- Enable only the selected diagnostic artifacts needed for the current hypothesis; avoid turning on every log and snapshot by default.
- Use `repeat: 3` as the default performance-test setting before promoting a variant to larger repeat counts.
- Before screen-based parallel runs, inspect the current server and choose concurrency from CPU, GPU, memory, disk, active screens, and algorithm cost.
- When CPU-heavy and GPU-heavy experiments are both waiting, prefer mixed CPU/GPU scheduling so both resource types are used effectively.

## PyFMTO Practices

For code changes:

- Use the project's current templates before creating new architecture.
- Use relative imports inside algorithm/problem packages.
- For the audited 0.3.4 interface, register `AlgorithmData` and `ProblemData` subclasses in package `__init__.py`; verify the installed interface before adapting a different version.
- Keep algorithm names and problem names aligned with PyFMTO discovery names, including case.
- Check availability with `pyfmto list algorithms`, `pyfmto list problems`, and `pyfmto show algorithms.<ALG>` / `pyfmto show problems.<PROBLEM>`, passing the same `-c` config.
- Record each true evaluation exactly once; isolate changed code/parameters from old results, and verify report coverage before interpreting the final algorithm column.
- Do not edit generated results or snapshots unless the user explicitly asks.

For unclear research choices:

- Ask the user rather than inventing hidden assumptions.
- Separate confirmed facts, implementation choices, and hypotheses.
- Prefer small pilot experiments before large runs.

## Optional Script

Use `scripts/inspect_fmto_project.py` to summarize a PyFMTO project before deeper work. It is intentionally lightweight and does not replace PyFMTO CLI validation.
