# Recall, QPS, and latency metrics

> **TL;DR:** Report quality and speed together: recall@k against exact ground truth, throughput under stated concurrency, and latency percentiles.

```mermaid
flowchart LR
 Dataset --> GT[exact top-k]
 Dataset --> ANN[approximate top-k]
 GT --> R[recall@k]
 ANN --> R
 Load --> P[p50 / p95 / p99 + QPS]
 R --> Gate[quality + SLO gate]
 P --> Gate
```

**Figure 1: Simplified conceptual view of this topic.**

**Takeaway:** Follow the arrows to see where the method spends work and where the main trade-off enters.

### How to read this

- Follow arrows in the direction data or decisions move.
- The labels name the main components; they do not promise a specific implementation.
- Use the table and field notes below to connect the picture to measurements.

**Visual takeaway:** The diagram shows the main data or decision path; labels are conceptual, not performance guarantees.

## Field notes

Recall@k is overlap between approximate and exact result sets divided by k; for fewer than k returned IDs, keep k in the denominator. QPS depends on concurrency and queueing, so never compare single-query latency with saturated throughput. Include warm-up, failures, result count, filters, hardware, and confidence across query cohorts.

## Sources

[ANN-Benchmarks](https://ann-benchmarks.com/) · [Big ANN benchmarks](https://big-ann-benchmarks.com/). Product behavior and defaults can vary by release; pin the version used in any benchmark.

**Next:** [Master index](../00-INDEX.md) · [Glossary](../99-glossary.md).
