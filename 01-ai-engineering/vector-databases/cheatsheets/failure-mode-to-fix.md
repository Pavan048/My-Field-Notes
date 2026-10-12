# Failure mode to first diagnostic

> **TL;DR:** Change the layer that explains the symptom; do not reflexively increase ANN search breadth.

```mermaid
flowchart TD
 Recall drop --> Check[metric / model / corpus / filters]
 Latency spike --> Trace[queue / shard / cache / I/O]
 Underfilled results --> Selectivity[eligible count / oversampling]
 Stale results --> Pipeline[ingestion lag / replica freshness]
```

**Figure 1: Simplified conceptual view of this topic.**

**Takeaway:** Follow the arrows to see where the method spends work and where the main trade-off enters.

### How to read this

- Follow arrows in the direction data or decisions move.
- The labels name the main components; they do not promise a specific implementation.
- Use the table and field notes below to connect the picture to measurements.

**Visual takeaway:** The diagram shows the main data or decision path; labels are conceptual, not performance guarantees.

## Field notes

| Symptom | First check | Candidate action |
|---|---|---|
| Recall falls | model, metric, corpus snapshot, filtered ground truth | restore semantics, then tune search |
| p99 rises | queueing, page faults, shard tail, compaction | isolate hot path and resource contention |
| Fewer than k rows | eligible-set size and postfilter attrition | adapt plan / oversample / filtered index |
| Stale data | write checkpoints, segment visibility, replica lag | repair pipeline and freshness contract |

## Sources

[ANN-Benchmarks](https://ann-benchmarks.com/) · [Big ANN benchmarks](https://big-ann-benchmarks.com/). Product behavior and defaults can vary by release; pin the version used in any benchmark.

**Next:** [Master index](../00-INDEX.md) · [Glossary](../99-glossary.md).
