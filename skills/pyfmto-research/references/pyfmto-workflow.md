# PyFMTO Workflow

Use this reference when implementing or modifying PyFMTO algorithms/problems, or when debugging discovery, import, and config failures.

## Before Editing

1. Inspect the target project structure.
2. Read local `README.md`, `CONVENTIONS.md`, `config.yaml`, and relevant algorithm/problem templates if present. Apply the version check in [framework-operations.md](framework-operations.md); installed source and working registrations resolve stale template/README differences.
3. Check existing names with `pyfmto list algorithms` and `pyfmto list problems` when the environment is available.
4. Ask the user when the requested method design leaves a research assumption unclear.

## New Algorithm Workflow

1. Copy or mirror the local algorithm template, usually `algorithms/DEMO`.
2. For the audited 0.3.4 interface, bind both a concrete `Client` subclass and a concrete `Server` subclass; the availability check requires both, even when the method has no knowledge transfer.
3. Put shared package/action/data classes in a utility module inside the algorithm package.
4. Use relative imports inside the algorithm package.
5. Export the algorithm through `algorithms/<ALG>/__init__.py` by subclassing `AlgorithmData`.
6. Document configurable hyperparameters as YAML in Client/Server class docstrings, read them from constructor kwargs, and use them in the implementation. YAML values alone do not implement a feature.
7. Validate with `pyfmto list algorithms -c <config.yaml>` and `pyfmto show algorithms.<ALG> -c <config.yaml>`. The registered wrapper class name, not just the directory name, is the config name.

For a copied DEMO package named `MyAlgorithm`, a minimal registration is:

```python
from pyfmto.framework import AlgorithmData
from .demo_client import DemoClient
from .demo_server import DemoServer

class MyAlgorithm(AlgorithmData):
    client = DemoClient
    server = DemoServer
```

A renamed copy still has DEMO behavior until its mechanism is implemented. Keep constructor parameters under the matching `algorithms.<name>.client` or `.server` config section.

## Algorithm Improvement Workflow

1. Identify the baseline being modified: IAFFBO, FMTBO, FDEMD, or another local algorithm.
2. Preserve the baseline behavior unless the requested change explicitly replaces it.
3. Isolate the innovation in a small module or method when possible.
4. Add config parameters for ablations instead of hardcoding research choices.
5. Keep privacy constraints explicit: no local true `(x,y)` pairs should be sent.
6. Add candidate-source provenance logging before each true evaluation in diagnostic runs.
7. Add transfer-event logging when the method creates, sends, filters, accepts, rejects, or uses transferred knowledge.
8. Save similarity or trust matrix snapshots when the method uses trust, similarity, clustering, neighborhoods, or personalization.
9. Maintain a true-evaluation budget ledger for expensive black-box experiments and any baseline comparison under strict `fe_max`.
10. Add surrogate model health logging when surrogate fitting, uncertainty, or candidate quality may explain the result.
11. Add config switches for changed research modules and expensive modules, then record them in an ablation switch registry.
12. Write selected diagnostic artifacts under the diagnostic output path; keep screen stdout and stderr logs in `out/_logs/`.

## New Problem Workflow

1. Inspect a working local problem registration. The audited upstream `problems/demo` uses an older export pattern; use `problems/arxiv2017/__init__.py` to check the current interface.
2. Implement `SingleTaskProblem` classes for individual tasks when needed.
3. Implement a `MultiTaskProblem` subclass; pass FE/NPD kwargs into each task, assign stable unique IDs with `set_id`, and declare unknown optima with `set_x_global(None)`.
4. In the audited interface, export a `ProblemData` subclass with `problem = YourMultiTaskProblem` from `problems/<problem>/__init__.py`.
5. Keep default parameters in the problem class docstring and verify supported dimensions.
6. Validate with `pyfmto list problems -c <config.yaml>` and `pyfmto show problems.<PROBLEM> -c <config.yaml>`; names are case-sensitive.

## Evaluation Accounting

Remaining FE is `fe_max - solutions.size` in the audited framework. Choose one recording path:

- Automatic: set `self.problem.auto_update_solutions = True`, then evaluate; do not append again.
- Manual: leave automatic updates disabled, evaluate, then call `self.solutions.append(x, y)` exactly once.

Use the plural `solutions` interface. Missing records can stall termination; duplicate records consume the recorded budget twice. Limit each batch to remaining FE and reconcile the ledger with actual objective calls, including any evaluations performed outside the optimizer. Predictions and candidate proposals are not true FE.

## Import Rules

Use relative imports inside algorithm/problem packages.

Good examples:

```python
from .demo_utils import Actions
from ..BO.bo_utils import ThompsonSampling
from ..benchmarks import Ackley
```

Avoid absolute imports that hardcode the top-level project package.

## Debug Checklist

For `pyfmto list algorithms` or `pyfmto list problems` failures:

1. Read the CLI's actual availability and diagnostic fields: `available`/`issues` in the audited version, rather than assuming the older `pass`/`msg` column names.
2. Check missing dependencies before changing code.
3. Check package `__init__.py` exports.
4. Check `AlgorithmData` / `ProblemData` wrapper discovery and the concrete classes bound by each wrapper; merely exporting Client/Server/MultiTaskProblem classes is insufficient in the audited version.
5. Check relative imports and filename/package name mismatches.
6. Run the corresponding `pyfmto show algorithms.<ALG>` or `pyfmto show problems.<PROBLEM>` with the same `-c` config after fixing discovery.

For config failures:

1. Confirm launcher algorithm/problem names match PyFMTO discovery names.
2. Confirm aliased entries use `base` correctly.
3. Confirm problem budgets satisfy `fe_max > fe_init` when the problem requires it.
4. Confirm reporter `comparisons` are lists and include at least two algorithms for table/curve reports.
