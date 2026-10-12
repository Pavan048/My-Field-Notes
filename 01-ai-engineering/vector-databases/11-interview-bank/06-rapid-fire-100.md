# Rapid-fire retrieval questions

> **TL;DR:** Use these prompts for spaced review; answer with a definition plus one operational consequence.

```mermaid
flowchart LR
 Define --> Explain
 Explain --> Measure
 Measure --> Tradeoff
 Tradeoff --> Validate
```

**Visual takeaway:** The diagram shows the main data or decision path; labels are conceptual, not performance guarantees.

## At a glance

| Question | Practical answer |
|---|---|
| What to measure | Quality against an exact or judged baseline, latency percentiles, resource use |
| Main trade-off | Search work and representation cost versus recall, freshness, and complexity |
| First diagnostic | Hold the data, metric, filters, and query set fixed; change one variable |

## Field notes

**1–10:** Define embedding, cosine, inner product, L2, normalization, anisotropy, hubness, kNN, ANN, recall@k. **11–20:** Explain IVF, nlist, nprobe, HNSW, M, efConstruction, efSearch, PQ, ADC, OPQ. **21–30:** Compare Flat/IVF/HNSW/DiskANN; describe mmap, page cache, WAL, tombstone, compaction, shard fan-out, global top-k, prefilter, postfilter, hybrid fusion. **31–40:** Define p99, QPS, candidate recall, reranking, freshness lag, idempotency, model migration, tenant isolation, filtered ground truth, rollback gate. For each, add a workload example and a measurement.

## Sources

[ANN survey](https://arxiv.org/abs/1806.09823) · [FAISS paper](https://arxiv.org/abs/1702.08734). Product behavior and defaults can vary by release; pin the version used in any benchmark.

**Next:** [Master index](../00-INDEX.md) · [Glossary](../99-glossary.md).
