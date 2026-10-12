# Foundations

> [!TIP] **TL;DR:** Define the representation and distance semantics, then formalize the nearest-neighbor objective before selecting an index. These notes are planned and remain `todo`.

```mermaid
flowchart LR
  E[Embedding space] --> M[Metric and score]
  M --> K[Exact kNN objective]
  K --> D[Database / library choice]
```

**Figure F1.** Foundation dependency.  
**Takeaway:** Index behavior cannot repair a mismatch between the model's geometry and the retrieval score.

| File | Focus | Status |
|---|---|---|
| [Embeddings and similarity](01-embeddings-and-similarity.md) | Embeddings, cosine/dot/L2, normalization, geometry | todo |
| [Nearest-neighbor problem](02-nearest-neighbor-problem.md) | Exact cost, ANN, recall@k | todo |
| [Vector DB vs traditional DB](03-vector-db-vs-traditional-db.md) | Database, extension, engine, library categories | todo |

**Start here:** [Embeddings and similarity](01-embeddings-and-similarity.md).


