# Disk-based ANN

> **TL;DR:** SSD-backed graph and partition indexes reduce RAM pressure, but random I/O, caching, and build/update paths become first-class design limits.

```mermaid
flowchart LR
 Q[query] --> R[RAM entry points/cache]
 R --> I[SSD reads: adjacency + vectors]
 I --> T[top-k candidates]
 T --> X[exact rerank]
```

**Figure 1: Simplified conceptual view of this topic.**

**Takeaway:** Follow the arrows to see where the method spends work and where the main trade-off enters.

### How to read this

- Follow arrows in the direction data or decisions move.
- The labels name the main components; they do not promise a specific implementation.
- Use the table and field notes below to connect the picture to measurements.

**Visual takeaway:** The diagram shows the main data or decision path; labels are conceptual, not performance guarantees.

## Field notes

DiskANN uses a navigable graph designed around SSD access; SPANN combines posting lists and an in-memory routing structure; FreshDiskANN and SPFresh address updates with different graph/partition maintenance strategies. Measure I/O per query, cache hit rate, queue depth, and tail latency. Storage locality can matter more than raw distance arithmetic.

## Sources

[DiskANN paper](https://proceedings.neurips.cc/paper/2019/hash/09853c7fb1d3f8ee67a61b6bf4a7f8e6-Abstract.html) · [Filtered-DiskANN](https://doi.org/10.1145/3543507.3583552). Product behavior and defaults can vary by release; pin the version used in any benchmark.

**Next:** [Master index](../00-INDEX.md) · [Glossary](../99-glossary.md).
