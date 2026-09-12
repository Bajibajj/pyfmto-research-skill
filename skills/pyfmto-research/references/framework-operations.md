# Framework Operations

Use for environment setup, CLI preflight, running, resuming, reporting, and operational debugging. Read only the sections relevant to the user's request; scientific design remains in the existing research references.

## Contents

- Version and environment
- Working directory and CLI
- Run and completion evidence
- Resume and changed variants
- Result locations and report collisions
- Failure handling and source anchors

## Version And Environment

The concrete behavior here and in the configuration/workflow/result references was audited on 2026-09-11 against:
- PyFMTO 0.3.4, commit `a00c30b7d355f9c80a4eadab7d2799236df774c6`.
- Upstream FMTO, commit `dc07321e71ab8b22250b3742baa6bce52adeff47`.

Treat these as an evidence baseline, not a mandate to downgrade or overwrite an installed framework. Check the actual environment first; if it differs or is locally modified, inspect the relevant installed implementation before applying its config/discovery/port/report behavior. When that cannot be checked, label instructions unverified for that environment.

From the confirmed experiment project and selected environment:

```bash
python -c "import sys, pyfmto; print(sys.executable); print(pyfmto.__version__); print(pyfmto.__file__)"
python -m pip show pyfmto
python -m pip check
git rev-parse HEAD
pyfmto -h
```

Match the CLI executable to the selected Python environment; use the shell's command lookup if PATH is ambiguous. Record a dirty checkout as well as its commit when relevant. PyFMTO is the installed framework; FMTO supplies algorithms, problems, data, and experiment YAML. The skill repository itself is neither the framework nor the experiment workspace.

For a new environment, the upstream documented starting point is Python 3.10. Reuse the user's specified environment when appropriate. Install the project requirements plus the selected algorithms' requirements, for example:

```bash
python -m pip install -r requirements.txt
python -m pip install -r algorithms/BO/requirements.txt
python -m pip install -r algorithms/ADDFBO/requirements.txt
```

These two algorithm dependencies support the bundled smoke asset only; they do not replace the user's research baseline choices. Record the actual resolved package versions for reproducibility. Installation, syntax validation, discovery, and completed optimization are distinct validation levels.

## Working Directory And CLI

Run from the experiment project root unless deliberately using additional sources. In the audited CLI, `-c` selects a config file without changing the working directory. Relative results paths resolve from the working directory, not the YAML directory. `launcher.sources` contains roots whose children include `algorithms/` and `problems/`; the current directory is added automatically. Do not point it only at the algorithms subdirectory.

After copying/adapting a config to the project, replace placeholders below with real discovered names and a real config path:

```bash
pyfmto list algorithms -c <config.yaml>
pyfmto list problems -c <config.yaml>
pyfmto show algorithms.<ALG> -c <config.yaml>
pyfmto show problems.<PROBLEM> -c <config.yaml>
pyfmto list reports -c <config.yaml>
pyfmto show reports.excel -c <config.yaml>
```

Current show syntax is group-qualified. Names come from registered wrapper classes and are case-sensitive, e.g. `Arxiv2017`, not necessarily the lowercase package directory. See [pyfmto-workflow.md](pyfmto-workflow.md) for registrations and exactly-once evaluation recording.

The audited `show` loads a registered component's defaults; it does not resolve YAML aliases or display merged overrides. For an alias such as `BO_LIGHT` with `base: BO`, query `algorithms.BO`, then inspect the alias config and resolved parameters or run snapshot separately. The same distinction applies to problem aliases and report-format defaults.

Confirm the selected components are available and the effective constructor parameters match the intended aliases. Failures in unselected optional packages need not trigger unrelated installations or code changes. A directory listing from `inspect_fmto_project.py` does not prove runtime availability.

## Run And Completion Evidence

For an authorized experiment, read [experiment-config.md](experiment-config.md), prepare a separate small smoke config, and establish the output root before launching. The [smoke asset](../assets/configs/smoke.yaml) checks the pipeline; its two repeats and tiny budget are not performance evidence. Apply the user's experiment protocol for pilots and formal runs.

```bash
pyfmto run -c <config.yaml>
pyfmto report -c <config.yaml>
```

Run and report are separate operations. For config-only requests, produce and validate the config without launching optimization. For report-only requests, use existing results; changing report formats, style, or comparison order does not require new FE.

The audited Launcher creates a server subprocess and runs clients in threads; separate run jobs share the default `localhost:18510`. Before concurrent jobs, follow [server-experiment-orchestration.md](server-experiment-orchestration.md) and verify effective client/server port isolation. Merely adding `launcher.port` does not provide it.

A successful shell exit or created screen is insufficient. Check experiment summary/issues, errors in logs, actual completed result files, repeat counts, client IDs, record lengths, and FE ledgers. Before claiming a report succeeded, verify that the intended target and all comparison members actually loaded and that the expected output exists; report generation can log errors or omit missing algorithms.

Return a concise execution receipt:
- Project root, interpreter/framework version, project revision or recorded local changes, and config path.
- Commands actually executed; dispatch/session/job identifiers when applicable.
- Intended algorithms/problems, budgets, repeat count, comparison target, and resolved result root.
- Actual completed repeats and expected versus loaded report members; raw-result, log, and report paths.
- Validation level and remaining failures, without calling syntax checks or synthetic tests completed optimization.

Keep receipts and experiment data in the project/output location authorized by the user, never in this reusable skill. Reuse existing authorization; changing scope, compute budget, or deployment destination requires checking that scope, not mechanically asking again.

## Resume And Changed Variants

In the audited implementation, each normal completion saves one result. The next repeat ID is the number of matching files plus one; repeat is the desired total, not the number to append.

- With two existing completed repeats, setting repeat to five ordinarily adds three.
- Lowering repeat does not remove old files; the reporter loads all matching files, not only the configured repeat count.
- An interrupted repeat has no optimizer checkpoint to resume; completed repeats can be reused, while unfinished work generally restarts.
- Check continuous numbering before resuming. Deleting a middle `RepXX` file does not request targeted repair and can cause a later repeat number to be reused.
- Before reusing results, match the full experimental identity: code, algorithm parameters, problem definition, FE, NPD, seeds, and initialization protocol. Paths do not encode every one of these.
- A changed algorithm or protocol needs a fresh result root or correctly isolated alias. Preserve comparable baseline results deliberately; do not assume they remain compatible merely because a file exists.

Use [variant-management.md](variant-management.md) for project-specific provenance. Existing snapshots under the same day's snapshot path are reused; algorithm-package snapshots are not complete backups of problem code, cross-package dependencies, or the environment.

## Result Locations And Report Collisions

In the audited implementation the raw layout is:

```text
<results>/<algorithm-or-alias>/<problem-name>_<task-count>T_<dim>D/NPD<npd>/
  FEi<fe_init>_FEm<fe_max>_Seed<seed>_Rep01.msgpack
```

Actual verbose problem names and prefixes depend on resolved parameters. Inspect the produced paths; do not reconstruct them from old README examples such as `Run <id>.msgpack`. For the smoke asset, one expected example is `out/smoke_pyfmto/BO/Tetci2019_10T_3D/NPD1/FEi11_FEm14_Seed123_Rep01.msgpack`.

Reports use `<reporter.results>/<report-generation-date>/<last-loaded-algorithm>/<verbose-problem>/NPD<npd>.xlsx`. Reporter results is both its input root and output root; it is not a separate report-only destination option. The date is when reporting runs, not necessarily when optimization ran.

The report filename omits full comparison membership and FE/seed prefixes. Groups or configs with the same result root, date, target, verbose problem, and NPD can overwrite each other even with different baseline lists or FE/seed selections. Combine compatible comparison groups, or generate and preserve separately named report copies before the next export. Never combine incompatible experiment settings to avoid a naming collision.

Framework logs normally live at `out/logs/pyfmto.log` under the working directory. Enabled verbose run logs live beneath the corresponding result directory; screen stdout/stderr and structured research diagnostics follow the existing project conventions.

## Failure Handling And Source Anchors

| Observation | Next check |
| --- | --- |
| Component unavailable | Selected environment, dependency traceback, registration wrapper, case, source root, relative imports |
| No work appears to run | Component summary, existing matched files, repeat count, and initialization versus total FE |
| FE stalls or exceeds budget | Exactly-once result recording and batch size; reconcile actual objective calls |
| Connection/bind failure | Server traceback, current listener, actual endpoint wiring; do not retry with an unused YAML key |
| Missing final algorithm column | Result identity/coverage and `Unavailable data`; do not silently switch targets |
| NaN tests, negative or near-zero values | Raw records and preprocessing; follow [result-analysis.md](result-analysis.md) |
| Excel permission/interface error | Whether the file is open; pandas compatibility with `Styler.map` (introduced in 2.1); actual dependency versions |

Pinned sources for rechecking behavior:
- [CLI](https://github.com/Xiaoxu-Zhang/pyfmto/blob/a00c30b7d355f9c80a4eadab7d2799236df774c6/src/pyfmto/utilities/cli.py), [config and filenames](https://github.com/Xiaoxu-Zhang/pyfmto/blob/a00c30b7d355f9c80a4eadab7d2799236df774c6/src/pyfmto/experiment/config.py), [Launcher](https://github.com/Xiaoxu-Zhang/pyfmto/blob/a00c30b7d355f9c80a4eadab7d2799236df774c6/src/pyfmto/experiment/launcher.py).
- [Discovery](https://github.com/Xiaoxu-Zhang/pyfmto/blob/a00c30b7d355f9c80a4eadab7d2799236df774c6/src/pyfmto/utilities/loaders.py), [DEMO registration](https://github.com/Xiaoxu-Zhang/fmto/blob/dc07321e71ab8b22250b3742baa6bce52adeff47/algorithms/DEMO/__init__.py), [problem registration](https://github.com/Xiaoxu-Zhang/fmto/blob/dc07321e71ab8b22250b3742baa6bce52adeff47/problems/arxiv2017/__init__.py).
- [Reporter](https://github.com/Xiaoxu-Zhang/pyfmto/blob/a00c30b7d355f9c80a4eadab7d2799236df774c6/src/pyfmto/experiment/reporter.py), [statistics and report paths](https://github.com/Xiaoxu-Zhang/pyfmto/blob/a00c30b7d355f9c80a4eadab7d2799236df774c6/src/pyfmto/experiment/utils.py), [FE and random control](https://github.com/Xiaoxu-Zhang/pyfmto/blob/a00c30b7d355f9c80a4eadab7d2799236df774c6/src/pyfmto/problem/problem.py).
- [Client endpoints](https://github.com/Xiaoxu-Zhang/pyfmto/blob/a00c30b7d355f9c80a4eadab7d2799236df774c6/src/pyfmto/framework/client.py), [Server endpoints](https://github.com/Xiaoxu-Zhang/pyfmto/blob/a00c30b7d355f9c80a4eadab7d2799236df774c6/src/pyfmto/framework/server.py).
