# DiskANN paper note

> **TL;DR:** DiskANN shows graph ANN can operate with a large SSD-resident index while using RAM for routing and caching.

```mermaid
flowchart LR
 Q --> R[RAM-resident entry/cache]
 R --> G[SSD graph neighborhood reads]
 G --> V[vector distance evaluations]
 V --> K[top-k]
```

**Figure 1: Simplified conceptual view of this topic.**

**Takeaway:** Follow the arrows to see where the method spends work and where the main trade-off enters.

### How to read this

- Follow arrows in the direction data or decisions move.
- The labels name the main components; they do not promise a specific implementation.
- Use the table and field notes below to connect the picture to measurements.

**Visual takeaway:** The diagram shows the main data or decision path; labels are conceptual, not performance guarantees.

## Field notes

The work co-designs graph construction and search for SSD access, reporting billion-scale experiments in its evaluated setup. Reproduce results only with matching hardware, data, and settings. For deployment, measure bytes/read, cache behavior, build cost, and tail latency, and include an update strategy rather than assuming static-index results transfer.

## Sources

[DiskANN paper](https://proceedings.neurips.cc/paper/2019/hash/09853c7fb1d3f8ee67a61b6bf4a7f8e6-Abstract.html) · [Filtered-DiskANN](https://doi.org/10.1145/3543507.3583552). Product behavior and defaults can vary by release; pin the version used in any benchmark.

**Next:** [Master index](../../00-INDEX.md) · [Glossary](../../99-glossary.md).
