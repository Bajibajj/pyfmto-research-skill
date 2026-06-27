# Server Experiment Orchestration

Use this reference when running PyFMTO experiments on a server with screen sessions.

## Contents

- Defaults
- Resource Preflight
- Adaptive Parallelism
- CPU/GPU Complementary Scheduling
- Screen Naming
- Logs
- Port Handling
- Launch Pattern
- Monitoring
- Batch Interpretation

## Defaults

Use conda environment `fmto` unless the user specifies another environment.

Use `out/_logs/` for screen output logs.

Use `repeat: 3` for performance testing after smoke and pilot pass. Use repeat 1 for quick pilot signals. Use repeat 5 or 10 only after repeat 3 evidence supports a stronger claim.

## Resource Preflight

Do not assume the server capacity. Check resources before launching a batch:

```bash
screen -ls
nproc
free -h
df -h .
nvidia-smi
```

If `nvidia-smi` is unavailable, treat the machine as CPU-only unless the project clearly provides another accelerator path.

## Adaptive Parallelism

Choose the number of parallel screen runs from the current machine state:

1. Count active screen sessions and avoid relaunching duplicates.
2. Estimate whether the target algorithms are CPU-heavy, GPU-heavy, or mixed.
3. Check available CPU cores, memory, disk, and GPU memory/utilization.
4. Start conservatively on an unfamiliar server, then expand after logs and load look healthy.
5. Reduce parallelism when verbose logs, snapshots, diagnostic artifacts, or large reports create disk pressure.

For CPU-heavy PyFMTO experiments, run several in parallel only when CPU and memory are clearly available. Do not use a fixed global number across all servers.

For GPU-heavy experiments, prefer one heavy GPU task per GPU unless GPU memory and utilization are both low.

## CPU/GPU Complementary Scheduling

When a batch contains both CPU-heavy and GPU-heavy algorithms, prefer mixed scheduling so CPU and GPU resources are used together.

Good pattern:

- Run one GPU-heavy experiment if the GPU is available.
- Run one or more CPU-heavy experiments alongside it if CPU, memory, and disk are healthy.
- Keep monitoring `nvidia-smi`, CPU load, memory, and logs.
- If the GPU task also consumes many CPU threads, reduce CPU-only parallel runs.

Avoid launching only CPU-heavy runs while the GPU is idle when a GPU-ready experiment is waiting. Also avoid launching only GPU-heavy runs when CPU-only ablations can run safely in parallel.

The goal is maximum useful throughput, not maximum session count.

## Screen Naming

Keep screen names short and readable:

```text
<alg>_<problem>_<tag>
<alg>_<ablation>_<problem>_<tag>
<alg>_report_<problem>
```

Examples:

```text
newalg_arxiv_r3
newalg_no_transfer_arxiv_r3
newalg_gpu_gecco_r3
newalg_report_arxiv
```

Use lowercase screen session names even if the PyFMTO algorithm alias is uppercase.

## Logs

Write screen output logs to `out/_logs/`.

Use one log per screen session, such as `out/_logs/newalg_arxiv_r3.log`.

Write structured diagnostic artifacts to `out/_diagnostics/<run_id>/<algorithm>/<problem>/<repeat_id>/` when the algorithm supports them. Keep screen logs and diagnostic artifacts separate.

## Port Handling

Port ranges are not fixed.

Before launching parallel PyFMTO runs:

1. Inspect each config and ensure `launcher.port` values are unique.
2. Follow the project's existing port convention if one exists.
3. If no convention exists, choose unused-looking ports dynamically.
4. When possible, check active processes or use a small Python socket probe before finalizing ports.
5. If a run fails with connection or bind errors, treat port conflict as a first suspect.

## Launch Pattern

Typical screen command shape:

```bash
screen -dmS newalg_arxiv_r3 bash -lc 'cd <project-root> && conda activate fmto && pyfmto run -c configs/run_NEWALG_arxiv_r3.yaml > out/_logs/newalg_arxiv_r3.log 2>&1'
```

Use report screens after run screens finish unless the report reads already completed result directories.

## Monitoring

While a batch runs, periodically check:

- `screen -ls` for live sessions.
- log tails for import errors, port conflicts, stalled aggregation, or failed reports.
- `nvidia-smi` for GPU memory and utilization when GPU code is enabled.
- CPU load and memory if many CPU-heavy runs are active.
- disk usage if many verbose snapshots or diagnostic artifacts are active.

If disk is low, reduce snapshots, disable unnecessary verbose outputs, or move old outputs before launching more repeat runs.

## Batch Interpretation

After parallel runs finish, compare main and ablation results together.

A module is useful when removing it worsens final values, convergence behavior, stability, or weak-client behavior. A module is suspicious when removing it improves results, or when it sharply reduces runtime without hurting objective quality.
