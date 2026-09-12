# pyfmto-research-skill

A Codex skill for PyFMTO-based federated many-task optimization research.

It helps with research idea refinement, PyFMTO algorithm implementation, diagnosis-first algorithm improvement, experiment configuration, server-side screen runs, result analysis, and PyFMTO import/config debugging.

## Install

Clone this repository on the machine where Codex runs:

```bash
git clone git@github.com:Bajibajj/pyfmto-research-skill.git
mkdir -p "${CODEX_HOME:-$HOME/.codex}/skills"
ln -s /path/to/pyfmto-research-skill/skills/pyfmto-research "${CODEX_HOME:-$HOME/.codex}/skills/pyfmto-research"
```

Replace `/path/to/pyfmto-research-skill` with the actual clone path.

Restart Codex after linking the skill.

## Framework Usage References

The framework usage guidance is integrated by task so the agent reads the relevant operating rules before acting:

| Task | Reference |
| --- | --- |
| Setup, CLI, run/resume, result paths, completion checks | [Framework operations](skills/pyfmto-research/references/framework-operations.md) |
| YAML, aliases, budgets, own method in the last report column | [Experiment config](skills/pyfmto-research/references/experiment-config.md) |
| Algorithm/problem registration and evaluation recording | [PyFMTO workflow](skills/pyfmto-research/references/pyfmto-workflow.md) |
| Excel symbols, missing data, clipping, curves | [Result analysis](skills/pyfmto-research/references/result-analysis.md) |
| Effective client/server ports and screen runs | [Server orchestration](skills/pyfmto-research/references/server-experiment-orchestration.md) |

Copy and adapt [smoke.yaml](skills/pyfmto-research/assets/configs/smoke.yaml) or [new-method.template.yaml](skills/pyfmto-research/assets/configs/new-method.template.yaml) into the experiment project. The smoke example is a pipeline check; the new-method template needs an actual registered algorithm. Neither file is a measured performance result.

The operating rules are anchored to the audited upstream PyFMTO 0.3.4 code. The skill instructs the agent to check the actual installed version and local changes before applying them. It retains the existing research baselines, privacy boundaries, and diagnostic workflow.

Example requests:

```text
Use pyfmto-research to create configs for my method on 3D and 5D problems, with my method in the last Excel column. Do not run yet.
Use pyfmto-research to check whether this experiment can resume after I changed its parameters.
Use pyfmto-research to generate reports from existing results and verify the comparison target and symbol direction.
```

## Usage

Ask Codex to use `pyfmto-research` when working on PyFMTO research, for example:

```text
Use pyfmto-research to diagnose this PyFMTO experiment result.
Use pyfmto-research to improve algorithms/EVOFEDSURROGATE.
Use pyfmto-research to create repeat 3 configs for Arxiv2017 and Gecco2020.
```
