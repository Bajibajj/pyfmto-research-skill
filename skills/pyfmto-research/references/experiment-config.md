# Experiment Config

Use this reference when creating or editing PyFMTO experiment YAML files.

## Default Baselines

Use these baselines unless the user overrides them:

```yaml
launcher:
  algorithms: [FDEMD, FMTBO, IAFFBO]
```

When a new method is evaluated, put it before the baselines and keep `IAFFBO` last when it is the reference algorithm:

```yaml
launcher:
  algorithms: [NEWALG, FDEMD, FMTBO, IAFFBO]
```

## Default Problems

Prioritize:

- `Arxiv2017`
- `Gecco2020`
- CEC problems from `problems/cec2022`, after confirming the PyFMTO discovery name

Always verify problem names with `pyfmto list problems` when possible.

## Budget Defaults

Default true evaluation budget:

- `fe_max = 11 × dim`
- The total budget includes initialization evaluations.
- Keep `npd: 1` for the default IID setting.
- Treat benchmark task diversity as the main source of heterogeneity unless the user requests non-IID partitioning.

If `dim` is a single integer, compute `fe_max` directly. For example, `dim: 3` means `fe_max: 33`.

If `dim` is a list, either write explicit problem aliases or ask the user how to represent per-dimension budgets. Do not silently create an invalid YAML structure.

## Detailed Run Settings

Use detailed settings for research runs:

```yaml
launcher:
  save: true
  loglevel: DEBUG
  snapshot: true
  verbose: true
```

Use `repeat: 3` as the default performance-test setting after smoke and pilot pass. Ask before launching repeat 5 or repeat 10 because those are stronger-claim runs and cost more wall-clock time.

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
    - [NEWALG, FDEMD, FMTBO, IAFFBO]
  params:
    curve:
      on_log_scale: true
      merge: true
      suffix: '.jpg'
    excel:
      pvalue: 0.05
```

PyFMTO treats the last algorithm in each `comparisons` list as the reference algorithm for `+/-/≈` table suffixes. Put `IAFFBO` last only when the user wants IAFFBO as the reference.

## Run Commands

Typical commands:

```bash
pyfmto list algorithms
pyfmto list problems
pyfmto show <name>
pyfmto run -c <config.yaml>
pyfmto report -c <config.yaml>
```

Before long runs, prefer a tiny pilot config that validates loading, budgets, logging, and output paths.
