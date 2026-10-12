# Query Processing

> [!TIP] **TL;DR:** Real retrieval queries combine a vector objective with predicates, ranking signals, and often reranking; candidate-generation quality must be evaluated under the full query. Planned notes are `todo`.

```mermaid
flowchart LR
  Q[Query + predicates] --> C[Candidate generation]
  C --> F[Filter / fuse signals]
  F --> R[Rerank]
  R --> K[Final top-k]
```

**Figure QP1.** Simplified query pipeline.  
**Takeaway:** The most relevant index benchmark may not predict the full pipeline's quality or latency.

| File | Focus | Status |
|---|---|---|
| [Filtered and hybrid search](01-filtered-and-hybrid-search.md) | Predicate-aware retrieval | todo |
| [BM25, dense, sparse](02-hybrid-bm25-dense-sparse.md) | Lexical/vector fusion | todo |
| [Reranking and multivector](03-reranking-and-multivector.md) | Late interaction and rerankers | todo |
| [Query planning](04-query-planning-and-cost-model.md) | Selectivity and cost model | todo |

**Start here:** [Filtered and hybrid search](01-filtered-and-hybrid-search.md).


