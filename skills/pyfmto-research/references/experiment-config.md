# Experiment Config

Use this reference when creating or editing PyFMTO experiment YAML files. Apply the installed-version check in [framework-operations.md](framework-operations.md) before using the audited 0.3.4 behavior below.

## Default Baselines

Use these baselines unless the user overrides them:

```yaml
launcher:
  algorithms: [FDEMD, FMTBO, IAFFBO]
```

When evaluating the user's new method, use it as the last algorithm in each report group. Keep the run order aligned for readability; an explicitly requested comparison target or order takes precedence:

```yaml
launcher:
  algorithms: [FDEMD, FMTBO, IAFFBO, NEWALG]
```

## Configuration Contract

| Section | Purpose |
| --- | --- |
| `launcher.algorithms` / `launcher.problems` | Actual run lists; defining parameters elsewhere does not schedule a component |
| Top-level `algorithms` | Algorithm aliases and `client` / `server` kwargs; optional `base` selects a registered algorithm |
| Top-level `problems` | Problem aliases and scalar dimension/FE/NPD/seed settings; optional `base` selects a registered problem |
| `reporter.comparisons` | List of algorithm lists, determining column order and comparison target |
| `reporter.results` / `reporter.problems` | Default to launcher values when omitted |
| `reporter.params.<format>` | Format-specific arguments; they do not alter optimization budgets |

If comparisons are omitted, the launcher algorithm list becomes one report group. Moving the top-level algorithm parameter block to the end of YAML does not change column order. Use explicit comparisons when a target column matters.

Keep YAML keys unique and use spaces, not tabs. Unknown keys are not proof of supported behavior: inspect the receiving constructor or CLI schema. In particular, `packages` records package versions in snapshots; it does not install dependencies.

## Default Problems

Prioritize:

- `Arxiv2017`
- `Gecco2020`
- CEC problems from `problems/cec2022`, after confirming the PyFMTO discovery name

Always verify problem names with `pyfmto list problems` when possible.

## Budget Defaults

Default true evaluation budget:

- `fe_max = 300`
- The total budget includes initialization evaluations.
- Keep `npd: 1` for the default IID setting.
- Treat benchmark task diversity as the main source of heterogeneity unless the user requests non-IID partitioning.

Set `fe_max: 300` explicitly for each problem, independent of `dim`, unless the user specifies another budget. This is the research default, not a change to the installed framework's fallback. Keep `fe_init < fe_max`; tiny smoke checks may use a smaller budget.

Use scalar `dim`, `npd`, and `seed` in the audited version. Its config path does not expand list values into runs; use explicit problem aliases or separate configs for multiple settings, with a numeric budget per alias. Example fragment:

```yaml
problems:
  Arxiv3D:
    base: Arxiv2017
    dim: 3
    fe_init: 15
    fe_max: 300
  Arxiv5D:
    base: Arxiv2017
    dim: 5
    fe_init: 25
    fe_max: 300
```

Add both aliases to `launcher.problems`. Different seed aliases also remain separate problem groups in standard reports; they are not automatically pooled across seeds.

NPD is partitions per dimension, not client count. It controls initialization partitions; subsequent search restrictions depend on the algorithm. `weak` temporarily seeds NumPy for partitioning; `strong` includes initialization sampling in that scope; quote `random_ctrl: 'no'` to avoid YAML boolean parsing. Neither setting proves all random generators or concurrent execution are reproducible. The audited Launcher does not use `launcher.seed` to assign repeat seeds.

## Detailed Run Settings

Use detailed settings for research runs:

```yaml
launcher:
  save: true
  loglevel: DEBUG
  snapshot: true
  verbose: true
```

Use `repeat: 3` as the default performance-test setting after smoke and pilot pass. Increase the budget or repeat count only within the user's authorized scope; retain earlier authorization instead of asking again. Repeat count alone never establishes a stronger claim.

Before long diagnostic runs, choose a diagnostic level and output root. Prefer:

```text
out/_diagnostics/<run_id>/<algorithm>/<problem>/<repeat_id>/
```

Keep screen stdout and stderr logs in `out/_logs/`.

If the algorithm provides diagnostic switches, enable only the diagnostics required by the selected diagnostic level and current hypothesis. Choose from candidate-source logging, transfer-event logging, similarity/trust matrix snapshots, true-evaluation budget ledgers, surrogate health logs, and ablation switch registry output. Do not hardcode key names; follow the local algorithm config style.

## Reporter Defaults

Use reports that support both inspection and paper writing:

```yaml
reporter:
  formats: [console, excel, curve]
  comparisons:
    - [FDEMD, FMTBO, IAFFBO, NEWALG]
  params:
    curve:
      on_log_scale: true
      merge: true
      suffix: '.jpg'
    excel:
      pvalue: 0.05
```

PyFMTO treats the last loaded algorithm in each group as the comparison target. Put `NEWALG` last when the user wants their own method in the final Excel algorithm column; keep IAFFBO last only for an explicitly IAFFBO-centered comparison.

Before reporting, check that all intended algorithms have matching, complete results. Missing target data can silently change the target. Report paths can also collide across groups with the same target/problem/NPD on the same day: combine compatible groups or export and preserve each report separately. See [framework-operations.md](framework-operations.md) for file matching and [result-analysis.md](result-analysis.md) for symbol direction, clipping, and log-transform semantics.

The existing research default uses log-transformed curves. Check the objective domain and log10-before-statistics semantics; use `on_log_scale: false` when original-scale output is requested. This switch does not disable the reporter's value clipping.

## Run Commands

Typical commands:

```bash
pyfmto list algorithms -c <config.yaml>
pyfmto list problems -c <config.yaml>
pyfmto show algorithms.<ALG> -c <config.yaml>
pyfmto show problems.<PROBLEM> -c <config.yaml>
pyfmto run -c <config.yaml>
pyfmto report -c <config.yaml>
```

Before long runs, prefer a tiny pilot config that validates loading, budgets, logging, and output paths.

## Copyable Config Assets

- [smoke.yaml](../assets/configs/smoke.yaml): upstream BO/ADDFBO pipeline check, with deliberately tiny FE and two repeats. These tutorial algorithms do not replace the research baseline defaults.
- [new-method.template.yaml](../assets/configs/new-method.template.yaml): FDEMD/FMTBO/IAFFBO plus the user's method in the final report column. Replace `NEWALG` with its verified registration or a configured alias, then set the project-specific budget, output root, and constructor parameters.

Copy an asset into the target project's config directory before adapting it; do not run from the skill directory or save experiment results there. Read [framework-operations.md](framework-operations.md) for the run/report receipt and resume checks.
