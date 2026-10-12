# Hero 11 â€” Index selection decision tree

```mermaid
flowchart TD
  S[Start: characterize scale, updates, filters, latency, RAM] --> E{Can exact scan meet SLO and cost?}
  E -->|yes| FLAT[Flat / exact baseline]
  E -->|no| M{Must most index state fit in RAM?}
  M -->|yes| U{High update rate or frequent rebuilds?}
  U -->|yes| IVF[Evaluate IVF or update-friendly design]
  U -->|no| GRAPH[Evaluate HNSW / graph ANN]
  M -->|no| DISK[Evaluate DiskANN / disk-based ANN]
  FLAT --> F{Strong metadata filters?}
  IVF --> F
  GRAPH --> F
  DISK --> F
  F -->|yes| FILTER[Benchmark filter-aware and exact-subset paths]
  F -->|no| BENCH[Benchmark recall, p95/p99, QPS, build, and total memory]
  FILTER --> BENCH
```

**Figure 11.** A starting decision tree, not a product recommendation. Every branch ends in workload-specific measurement; index names alone do not determine behavior.

**Takeaway:** Choose from workload constraints and measured Pareto curves, then validate failure and update behavior.

**Sources:** [FAISS indexes](https://github.com/facebookresearch/faiss/wiki/Faiss-indexes); [ANN-Benchmarks](https://ann-benchmarks.com/); [DiskANN paper](https://proceedings.neurips.cc/paper/2019/hash/09853c7fb1d3f8ee67a61b6bf4a7f8e6-Abstract.html).


