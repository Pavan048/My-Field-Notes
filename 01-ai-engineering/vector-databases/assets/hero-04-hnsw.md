# Hero 04 â€” HNSW layered search

```mermaid
flowchart TB
  subgraph L2[Upper sparse layer]
    A((entry)) --> B((near query region))
  end
  subgraph L1[Intermediate layer]
    C((entry)) --> D((closer)) --> E((closer still))
  end
  subgraph L0[Base layer: all points]
    F((entry)) --> G((candidate)) --> H((candidate)) --> I((nearest region))
    G --- J((neighbor))
    H --- K((neighbor))
  end
  A -. greedy descent .-> C
  B -. efSearch expansion .-> D
  E -. greedy descent .-> G
  I -. maintain candidate / result heaps .-> K
```

**Figure 4.** Simplified HNSW traversal across nested proximity graphs. The pictured edges are illustrative, not a particular graph instance; HNSW searches upper layers greedily and performs a broader best-first search on layer 0.

**Takeaway:** Upper layers provide long-range navigation; the base layer spends the query's search budget refining candidates.

**Sources:** [Malkov & Yashunin, HNSW (2016; journal version 2018)](https://arxiv.org/abs/1603.09320).


