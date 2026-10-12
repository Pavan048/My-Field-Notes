# Hero 06 â€” Product quantization and ADC

```mermaid
flowchart LR
  X[Vector x in d dimensions] --> S[Split into m sub-vectors]
  S --> Q1[Subspace 1 codebook]
  S --> Q2[Subspace 2 codebook]
  S --> QN[Subspace m codebook]
  Q1 --> C[Compact code: m centroid IDs]
  Q2 --> C
  QN --> C
  Q[Query q] --> T[Per-subspace distance lookup tables]
  C -->|sum m table entries| D[Approximate distance]
```

**Figure 6.** Product quantization with asymmetric distance computation (ADC): the query remains full precision while database subvectors are represented by codebook IDs. Diagram is simplified; an implementation stores codebooks and codes separately.

**Takeaway:** PQ lowers vector storage and enables table-based scoring, at the cost of quantization error and training/index complexity.

**Sources:** [JÃ©gou, Douze & Schmid, Product Quantization (TPAMI 2011)](https://doi.org/10.1109/TPAMI.2010.57); [FAISS index overview](https://github.com/facebookresearch/faiss/wiki/Faiss-indexes).


