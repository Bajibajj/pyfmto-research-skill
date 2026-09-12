# Repository Map

Use this reference when locating structure in any PyFMTO project.

## Scope Rule

Keep this file generic. Do not store a specific project's algorithm names, problem names, result rankings, or absolute root path here.

When entering a project, inspect the local files first and build the project map from that repository.

## Common PyFMTO Project Structure

Typical files and directories:

- `README.md`: project usage, CLI commands, and experiment notes.
- `CONVENTIONS.md`: project-specific PyFMTO coding rules when present.
- `requirements.txt`: Python dependencies.
- `config.yaml`: default or full experiment config.
- `minimal.yaml`: minimal runnable config when present.
- `configs/`: additional run/report configs.
- `algorithms/`: local algorithm packages.
- `problems/`: local problem packages.
- `out/`: run outputs, snapshots, logs, and reports.
- `latex/`, `paper/`, or `docs/`: paper-related material; edit only when requested.

## Discovery Workflow

1. List the project root.
2. Inspect `algorithms/` and `problems/` directories if present.
3. Read project-level `README.md` and `CONVENTIONS.md` when they exist.
4. Find templates such as `algorithms/DEMO` or `problems/demo`, but do not assume they always exist.
5. Use `pyfmto list algorithms` and `pyfmto list problems` to confirm discovery names.
6. Use `pyfmto show algorithms.<ALG>` or `pyfmto show problems.<PROBLEM>` with the selected `-c` config before writing final configs. Check the installed version and working directory using [framework-operations.md](framework-operations.md).

## Algorithm Template Signals

A PyFMTO algorithm package usually contains:

- an `__init__.py` exporting an `AlgorithmData` subclass;
- a `Client` subclass;
- a concrete `Server` subclass (required by the audited 0.3.4 availability check even without knowledge transfer);
- optional utility modules for package/action/data classes;
- docstrings exposing configurable parameters.

Prefer local templates when available. If no template exists, inspect the closest working algorithm package before adding a new one.

## Problem Template Signals

A PyFMTO problem package usually contains:

- an `__init__.py` exporting a `ProblemData` wrapper whose `problem` attribute binds the MultiTaskProblem class in the audited 0.3.4 interface;
- `SingleTaskProblem` subclasses for task-level objectives when needed;
- a `MultiTaskProblem` subclass for the task family;
- default parameters in docstrings;
- relative imports for shared benchmark functions.

For CEC or benchmark-family experiments, always confirm the PyFMTO discovery name because folder names and config names may differ.

## Project-Specific Notes

Project-specific experiment memory belongs in the project, not in this skill.

Look for or create project-level files such as `experiments/*.md`, `notes/*.md`, or `out/*analysis*.md` only after asking the user when the location is unclear.
