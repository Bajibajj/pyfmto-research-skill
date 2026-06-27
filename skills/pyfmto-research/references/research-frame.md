# Research Frame

Use this reference when analyzing ideas, designing methods, improving algorithms, or writing conclusions for federated many-task optimization.

## Problem Setting

The target setting is federated many-task optimization with expensive black-box objectives. Each client owns a task, can evaluate the local objective only a very small number of times, and does not reveal local true evaluation pairs `(x,y)`.

The goal is to find small objective values under limited real evaluations while exploiting useful cross-task knowledge. The method should work when tasks are strongly similar, weakly related, or unrelated.

## Privacy Boundary

Never expose local true evaluation pairs `(x,y)`.

Allowed information can include model parameters, surrogate summaries, statistical summaries, rankings, task embeddings, similarity summaries, acquisition suggestions, candidate points, search directions, or other derived knowledge, as long as it does not reveal local true data pairs.

When a proposed transfer object may leak data pairs, stop and ask the user.

## Innovation Axes

Compare candidate ideas by innovation strength first, then feasibility.

Key axes:

- Task similarity: how to estimate similarity from scarce observations without sharing `(x,y)`.
- Transfer timing: when transfer should happen, such as early initialization, mid-run correction, late exploitation, or adaptive triggering.
- Transfer content: what knowledge is sent, such as surrogate parameters, task embeddings, acquisition hints, sampling directions, rankings, or uncertainty summaries.
- Transfer mechanism: how knowledge is aggregated, weighted, filtered, clustered, personalized, or rejected.
- Client usage: how a client turns received knowledge into candidate selection, surrogate priors, acquisition modification, trust weights, or restart decisions.
- Candidate-source attribution: which mechanism produced each true evaluation point and whether it helped or hurt.
- Diagnostic artifact evidence: transfer events, trust matrices, budget ledgers, surrogate health logs, and ablation switch registries that explain the mechanism.
- Heterogeneity robustness: how to avoid negative transfer when tasks are unrelated.
- Expensive evaluation efficiency: how each real evaluation improves search under `fe_max = 11 × dim`.
- Runtime/resource awareness: how much cost the method adds, whether GPU, batching, or vectorization can reduce it, and whether the cost is justified by objective gains.

## Default Analysis Template

For each proposed method, answer:

1. What private local information stays hidden?
2. What knowledge is transferred?
3. Why should this transferred knowledge be useful under scarce evaluations?
4. How is task similarity computed or inferred?
5. When does transfer happen and why then?
6. How does the client use received knowledge?
7. What prevents negative transfer?
8. Which source produced each true evaluation point, and how will that source be logged?
9. Which diagnostic artifacts will prove or disprove the mechanism?
10. Which baseline weakness does this address: IAFFBO, FMTBO, or FDEMD?
11. What ablation isolates the claimed contribution?
12. What runtime or resource cost is added, and can GPU, batching, vectorization, or a lighter surrogate reduce it without weakening the main objective gain?
