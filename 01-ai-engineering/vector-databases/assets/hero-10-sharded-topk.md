# Hero 10 â€” Sharded scatter-gather top-k

```mermaid
sequenceDiagram
  participant P as Query planner / proxy
  participant A as Shard A
  participant B as Shard B
  participant C as Shard C
  P->>A: query vector, filter, local k'
  P->>B: query vector, filter, local k'
  P->>C: query vector, filter, local k'
  A-->>P: candidate IDs + scores
  B-->>P: candidate IDs + scores
  C-->>P: candidate IDs + scores
  P->>P: deduplicate and reduce to global top-k
```

**Figure 10.** Simplified scatter-gather query. Local `k'` and global top-k correctness depend on score comparability, filters, duplicates, and whether local ANN search is approximate.

**Takeaway:** Global top-k is a merge problem; increasing shard fan-out can raise tail latency and candidate volume.

**Sources:** [Milvus architecture](https://milvus.io/docs/architecture_overview.md); [FAISS paper](https://arxiv.org/abs/1702.08734).


