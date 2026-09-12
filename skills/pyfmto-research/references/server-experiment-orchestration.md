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

Apply the version check in [framework-operations.md](framework-operations.md). In upstream 0.3.4, both client and server default to `localhost:18510`; `launcher.port` is not a supported wiring mechanism. Different screen sessions or different unused YAML port numbers do not isolate listeners.

Before parallel launches:

1. Inspect the actual launcher, Client/Server constructors, and `set_addr` calls. Identify the parameters the project really routes to both endpoints.
2. If a custom version supports per-run ports, give each job a distinct port, check existing listeners, and verify the effective client/server pair in a small run. A free-port probe alone does not prove the config takes effect.
3. If the project has no supported port isolation, run serially. Do not add a cosmetic `launcher.port` key or silently modify the framework to enable parallelism.
4. Use separate result roots for different protocol/code versions, even when ports are isolated. Check active sessions and result completion before relaunching.
5. If a run fails with connection or bind errors, inspect the listener and server startup traceback before retrying.

## Launch Pattern

Typical screen command shape:

```bash
screen -dmS newalg_arxiv_r3 bash -lc 'cd <project-root> && mkdir -p out/_logs && conda run --no-capture-output -n fmto pyfmto run -c configs/run_NEWALG_arxiv_r3.yaml > out/_logs/newalg_arxiv_r3.log 2>&1'
```

Replace `<project-root>` and the config path with verified paths before executing. Verify `conda run` works in this shell, or use the project's already validated shell initialization and interpreter. A created screen session is dispatch evidence, not proof the experiment succeeded.

Use report screens after run screens finish unless the report reads already completed result directories. Apply the run receipt and report-coverage checks in [framework-operations.md](framework-operations.md).

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
