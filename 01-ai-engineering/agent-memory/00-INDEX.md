# Agent Memory — Separate Learning Track

> This folder is intentionally separate from `context-manager/`. Context management and agent memory are related, but they answer different engineering questions.

## Scope

**Agent memory** studies how an agent retains, updates, organizes, retrieves, consolidates and forgets information across turns, tasks and sessions.

Primary questions:
- What information should be persisted?
- How should memories be represented and stored?
- How are memories updated, invalidated, consolidated or forgotten?
- How should memories be retrieved and ranked for a future task?
- How do we evaluate memory quality, freshness, consistency and safety?

## Boundary with context management

| Context management | Agent memory |
|---|---|
| What should the model receive now? | What should the agent retain for later? |
| Constructs an invocation's input | Manages information over time |
| Selects, orders and budgets context | Writes, updates, consolidates and retrieves memories |
| Can consume memory as one input source | Can supply candidates to context assembly |

A stored memory is not automatically present in a model invocation. A context can also be assembled without any persistent agent-memory system.

## Planned curriculum

This track will be developed independently after the context-manager foundations are stable.

| ID | Module | Status |
|---|---|---|
| AM-00 | Memory problem, terminology and boundaries | Planned |
| AM-01 | Memory representations and schemas | Planned |
| AM-02 | Episodic and semantic memory architectures | Planned |
| AM-03 | Procedural and prospective memory | Planned |
| AM-04 | Memory write policies and extraction | Planned |
| AM-05 | Retrieval, ranking and relevance | Planned |
| AM-06 | Updates, contradictions, freshness and forgetting | Planned |
| AM-07 | Consolidation and memory lifecycle | Planned |
| AM-08 | Memory evaluation and benchmarks | Planned |
| AM-09 | Security, privacy, isolation and memory integrity | Planned |
| AM-10 | Open-source systems and implementation capstone | Planned |

## Initial research candidates

These references are candidates for future study. They are not marked as read or validated here.

| Resource | Intended study |
|---|---|
| [MemGPT](https://arxiv.org/abs/2310.08560) | Memory hierarchy and virtual context management |
| [A-MEM](https://arxiv.org/abs/2502.12110) | Agentic memory construction and linking |
| [Mem0](https://github.com/mem0ai/mem0) | Practical memory platform and implementation |
| [Graphiti](https://github.com/getzep/graphiti) | Temporal knowledge graph for agent memory |
| [LongMemEval](https://arxiv.org/abs/2410.10813) | Long-term conversational memory evaluation |
| [MemoryAgentBench](https://arxiv.org/abs/2507.05257) | Benchmarking agent memory capabilities |

We will verify each paper's exact metadata, version, methods and findings when beginning this track.

## Study protocol

For every system or paper, capture:
1. Memory problem and assumptions.
2. Representation and storage model.
3. Write/update/delete lifecycle.
4. Retrieval and ranking process.
5. Evaluation tasks and metrics.
6. Failure modes, limitations and security implications.
7. What we can reproduce or build.

## Status

- Track created as a separate conceptual boundary.
- No agent-memory module is counted as completed yet.
- Next step for this track: begin AM-00 when we intentionally switch from context management to memory.

*Last updated: 2026-11-06*
