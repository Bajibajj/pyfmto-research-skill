# PyFMTO Workflow

Use this reference when implementing or modifying PyFMTO algorithms/problems, or when debugging discovery, import, and config failures.

## Before Editing

1. Inspect the target project structure.
2. Read local `README.md`, `CONVENTIONS.md`, `config.yaml`, and relevant algorithm/problem templates if present.
3. Check existing names with `pyfmto list algorithms` and `pyfmto list problems` when the environment is available.
4. Ask the user when the requested method design leaves a research assumption unclear.

## New Algorithm Workflow

1. Copy or mirror the local algorithm template, usually `algorithms/DEMO`.
2. Implement a `Client` subclass and a `Server` subclass when the method has communication or aggregation.
3. Put shared package/action/data classes in a utility module inside the algorithm package.
4. Use relative imports inside the algorithm package.
5. Export the algorithm through `algorithms/<ALG>/__init__.py` by subclassing `AlgorithmData`.
6. Document configurable hyperparameters in class docstrings so `pyfmto show <ALG>` can expose them.
7. Validate with `pyfmto list algorithms` and `pyfmto show <ALG>`.

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

1. Copy or mirror `problems/demo` when the project provides it.
2. Implement `SingleTaskProblem` classes for individual tasks when needed.
3. Implement a `MultiTaskProblem` subclass for the benchmark family.
4. Export the public problem class in `problems/<problem>/__init__.py`.
5. Keep default parameters in docstrings so `pyfmto show <problem>` can expose them.
6. Validate with `pyfmto list problems` and `pyfmto show <problem>`.

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

1. Read the failure message from the `msg` column.
2. Check missing dependencies before changing code.
3. Check package `__init__.py` exports.
4. Check whether a subclass of `Client`, `Server`, `AlgorithmData`, or `MultiTaskProblem` is discoverable.
5. Check relative imports and filename/package name mismatches.
6. Run `pyfmto show <name>` after fixing discovery.

For config failures:

1. Confirm launcher algorithm/problem names match PyFMTO discovery names.
2. Confirm aliased entries use `base` correctly.
3. Confirm problem budgets satisfy `fe_max > fe_init` when the problem requires it.
4. Confirm reporter `comparisons` are lists and include at least two algorithms for table/curve reports.
