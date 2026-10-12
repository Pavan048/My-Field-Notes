# Hands-on Labs

> [!TIP] **TL;DR:** Labs must run, pin dependencies, show actual outputs, and report recall@10, QPS, and memory; no expected output may be presented as executed output. Planned labs are `todo`.

```mermaid
flowchart LR
  D[Public dataset] --> X[Exact baseline]
  D --> A[ANN implementation / system]
  X --> E[Recall@10]
  A --> E
  A --> P[QPS / latency / memory]
```

**Figure L1.** Minimum lab evidence flow.  
**Takeaway:** Reproducibility and measured results are part of the lab, not optional polish.

| Lab | Focus | Status |
|---|---|---|
| [Brute-force kNN](01-brute-force-knn/) | Exact baseline | todo |
| [IVF from scratch](02-ivf-from-scratch/) | Coarse quantization | todo |
| [Tiny HNSW](03-tiny-hnsw-from-scratch/) | Graph construction and search | todo |
| [PQ from scratch](04-pq-from-scratch/) | Quantization and ADC | todo |
| [FAISS sweep](05-faiss-sweep/) | Recall / QPS / memory | todo |
| [hnswlib parameter sweep](06-hnswlib-param-sweep/) | HNSW tuning | todo |
| [pgvector vs Qdrant](07-pgvector-vs-qdrant/) | Controlled system comparison | todo |
| [Filtered-search recall](08-filtered-search-recall/) | Selectivity effects | todo |

**Start here:** [Brute-force kNN](01-brute-force-knn/).


