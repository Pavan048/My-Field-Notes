# Hero 07 â€” DiskANN memory and SSD path

```mermaid
flowchart LR
  Q[Query] --> B[Beam search controller]
  B -->|entry / candidate IDs| R[RAM-resident PQ codes and routing state]
  R -->|promising SSD node IDs| IO[Batch / coalesce reads]
  IO -->|graph neighborhoods and full vectors| SSD[(SSD-resident Vamana graph)]
  SSD -->|neighbors and exact distances| B
  B -->|top candidates| O[Results]
```

**Figure 7.** Conceptual DiskANN search split. Exact memory-resident structures, SSD layout, and read behavior depend on implementation and version; this is not a universal bill of materials.

**Takeaway:** Disk-based graph ANN spends memory on compact routing aids and uses SSD reads to expand promising candidates.

**Sources:** [Subramanya et al., DiskANN (NeurIPS 2019)](https://proceedings.neurips.cc/paper/2019/hash/09853c7fb1d3f8ee67a61b6bf4a7f8e6-Abstract.html); [Microsoft DiskANN repository](https://github.com/microsoft/DiskANN).


