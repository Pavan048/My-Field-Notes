# Hero 01 â€” Vector database architecture

```mermaid
flowchart LR
  C[Client / SDK] -->|query or mutation| A[API / access layer]
  A -->|validated request| P[Planner / router]
  P -->|target shards and segments| I[ANN index / exact scorer]
  I -->|candidate IDs and scores| F[Filter / rerank / top-k]
  F -->|results| A
  I -->|index and vector reads| S[Local memory / SSD]
  S -->|cache miss or durable artifact| O[(Object storage)]
  A -.->|metadata / health| M[(Metadata and control plane)]
```

**Figure 1.** Simplified component map for a vector-search service; boundaries and storage paths vary by product. This is a conceptual map, not an assertion that every product has a separate planner or object store.

**Takeaway:** Retrieval combines request routing, candidate generation, filtering/ranking, and data access; these may be co-located or distributed.

**Sources:** [Milvus architecture documentation](https://milvus.io/docs/architecture_overview.md); [Milvus: A Purpose-Built Vector Data Management System (SIGMOD 2021)](https://doi.org/10.1145/3448016.3457550).


