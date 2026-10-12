# Hero 03 â€” Read path: local and distributed

```mermaid
flowchart LR
  Q[Query vector + predicate] --> R[Route to partitions / shards]
  R --> S1[Shard 1 search]
  R --> S2[Shard 2 search]
  R --> Sn[Shard n search]
  S1 -->|local top-k candidates| M[Merge candidates]
  S2 -->|local top-k candidates| M
  Sn -->|local top-k candidates| M
  M -->|global top-k| X[Optional exact rerank]
  X --> O[Return IDs, scores, payload]
  S1 -.->|read index / vectors| D[(Memory, SSD, or remote storage)]
```

**Figure 3.** Simplified distributed top-k retrieval. A local top-k merge is exact only under compatible scoring and candidate coverage assumptions; ANN candidate generation can already omit true neighbors.

**Takeaway:** Sharding requires local candidate generation plus global reduction; filtering and reranking placement changes both recall and cost.

**Sources:** [Milvus architecture](https://milvus.io/docs/architecture_overview.md); [FAISS paper](https://arxiv.org/abs/1702.08734).


