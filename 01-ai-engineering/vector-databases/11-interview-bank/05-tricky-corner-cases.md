# Tricky corner cases

> **TL;DR:** Most retrieval bugs are semantic mismatches or denominator mistakes, not mysterious ANN behavior.

```mermaid
flowchart LR
 Zero vectors --> Metric edge case
 Duplicate IDs --> Dedup before top-k
 Ties --> Stable tie policy
 Filtered set < k --> Explicit underfill
 Mixed models --> Route by version
```

**Visual takeaway:** The diagram shows the main data or decision path; labels are conceptual, not performance guarantees.

## At a glance

| Question | Practical answer |
|---|---|
| What to measure | Quality against an exact or judged baseline, latency percentiles, resource use |
| Main trade-off | Search work and representation cost versus recall, freshness, and complexity |
| First diagnostic | Hold the data, metric, filters, and query set fixed; change one variable |

## Field notes

Cosine is undefined for a zero vector unless the system defines a convention. Duplicate records can consume multiple top-k slots. Ties require deterministic policy for reproducible tests. Recall denominator should remain k even when approximate output is short. Empty filtered sets are valid. Never compare scores across incompatible embedding models as if they shared one geometry.

## Sources

[ANN survey](https://arxiv.org/abs/1806.09823) · [FAISS paper](https://arxiv.org/abs/1702.08734). Product behavior and defaults can vary by release; pin the version used in any benchmark.

**Next:** [Master index](../00-INDEX.md) · [Glossary](../99-glossary.md).
