# Domain Map

Use this reference when connecting a method idea to related research areas.

## Core Intersection

The target area combines federated many-task optimization, expensive black-box optimization, surrogate-assisted search, privacy-preserving knowledge transfer, and heterogeneous tasks.

A strong method should not be explained from only one field. Map each idea to the relevant fields below, then identify the real novelty.

## Evolutionary Computation View

Ask:

- What is the population or candidate pool?
- How are crossover, mutation, selection, and elitism used?
- Does diversity prevent premature convergence?
- Does local exploitation appear too early or too late?
- Are generated candidates evaluated by real objectives or surrogate scores?

Useful concepts: elite archive, diversity pressure, adaptive mutation, restart, niching, multi-source offspring, surrogate-assisted evolutionary optimization.

## Federated Learning View

Ask:

- What can each client send without exposing true `(x,y)` pairs?
- What does the server aggregate or personalize?
- How many communication rounds are needed?
- Is the method robust to client heterogeneity?
- Does the server send global knowledge, clustered knowledge, or client-specific knowledge?

Useful concepts: personalization, secure aggregation mindset, communication efficiency, client drift, partial participation, privacy-preserving summaries.

## Multi-Task Learning View

Ask:

- Which tasks are similar, weakly related, or unrelated?
- Is task similarity static or changing during optimization?
- Does the method learn shared structure or only exchange candidates?
- How is negative transfer detected and suppressed?
- Can task groups or neighborhoods be updated online?

Useful concepts: task embedding, task clustering, shared representation, personalized transfer, relatedness estimation, negative transfer.

## Federated Optimization View

Ask:

- Is the difficulty from data heterogeneity, task heterogeneity, or both?
- Does local progress conflict with global transfer?
- Does synchronization help or slow down search?
- Should aggregation be global, weighted, clustered, or client-specific?
- What is the communication and synchronization overhead?

Useful concepts: non-IID clients, local-global tradeoff, robust aggregation, asynchronous versus synchronous rounds, system heterogeneity.

## Bayesian Optimization View

Ask:

- What surrogate model is used and how stable is it under very few samples?
- What acquisition function controls exploration and exploitation?
- How is uncertainty calibrated when objectives have very different scales?
- Does transfer change the surrogate prior, acquisition, candidate pool, or trust weights?
- Does each real evaluation provide enough information gain?

Useful concepts: Gaussian process, kernel/hyperparameter transfer, acquisition scheduling, lower confidence bound, expected improvement, batch candidate scoring.

## Runtime And GPU View

Solution quality is the first performance target. Runtime and resource cost are secondary evidence that must be recorded and explained.

Ask:

- Which part dominates runtime: surrogate training, candidate scoring, evolutionary generation, communication, logging, or reporting?
- Can candidate scoring be vectorized or batched?
- Can GPU accelerate model fitting or candidate evaluation without large transfer overhead?
- If the algorithm wins objective value but costs much more time, what ablation or switch explains that tradeoff?
- Does the method scale with number of clients, dimension, and repeat count?

Prefer GPU when it naturally fits large batched work or GPU-supported models. Do not force GPU when the algorithm is dominated by CPU-only libraries, small matrices, process synchronization, or disk logging.
