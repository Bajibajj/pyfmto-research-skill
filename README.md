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

## Usage

Ask Codex to use `pyfmto-research` when working on PyFMTO research, for example:

```text
Use pyfmto-research to diagnose this PyFMTO experiment result.
Use pyfmto-research to improve algorithms/EVOFEDSURROGATE.
Use pyfmto-research to create repeat 3 configs for Arxiv2017 and Gecco2020.
```
