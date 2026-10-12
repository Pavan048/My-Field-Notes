# Hero 08 â€” Filtered ANN strategies

```mermaid
flowchart TB
  Q[Query + predicate] --> PRE[Pre-filter eligible set]
  PRE --> ANN1[ANN over eligible vectors]
  ANN1 --> R1[Filtered candidates]
  Q --> ANN2[ANN over all vectors]
  ANN2 --> POST[Post-filter candidates]
  POST --> R2[May return fewer than k / miss eligible neighbors]
  Q --> NATIVE[Filter-aware index or traversal]
  NATIVE --> R3[Predicate-aware candidate search]
```

**Figure 8.** Three common filtered-search patterns. â€œPre-filterâ€ may mean an exact scan over a selective subset or a filter-specific index; â€œnativeâ€ covers distinct algorithm families such as ACORN and Filtered-DiskANN.

**Takeaway:** Post-filtering can starve the result set; no strategy is best for every selectivity, metadata distribution, and index.

**Sources:** [ACORN (2024)](https://arxiv.org/abs/2403.04871); [Filtered-DiskANN (WWW 2023)](https://doi.org/10.1145/3543507.3583552).


