# Graph Index Family: NSG, Vamana, SSG, CAGRA

> [!TIP]
> **TL;DR:** Graph ANN stores vector nodes plus selected neighbor edges and navigates the graph from entry points. HNSW adds random hierarchy; NSG seeks a sparse navigable graph; Vamana underlies DiskANN; CAGRA parallelizes construction/search for GPUs. Graph names are algorithms, not interchangeable product features.

## At a glance

| Family | Graph design / build idea | Main strength | Main trade-off | Primary source |
|---|---|---|---|---|
| HNSW | Layered proximity graph; incremental insertion | Strong in-memory recall/latency trade-off | Link memory and mutation/deletion handling | [HNSW](https://arxiv.org/abs/1603.09320) |
| NSG | Approximate monotonic relative-neighborhood graph; connectivity and spreading-out edges | Sparse navigable graph with low degree | Build pipeline and graph repair can be expensive | [PVLDB 2019](https://doi.org/10.14778/3303753.3303754) |
| Vamana / DiskANN | Robust pruned graph; SSD-oriented beam search | Disk-resident scale with controlled I/O | SSD reads and construction complexity | [NeurIPS 2019](https://proceedings.neurips.cc/paper/2019/hash/09853c7fb1d3f8ee67a61b6bf4a7f8e6-Abstract.html) |
| SSG | Satellite System Graph uses a navigable graph with geometric constraints | Strong graph-search point in research comparisons | Build/parameter behavior is data dependent | [paper](https://arxiv.org/abs/1907.06146) |
| CAGRA | GPU-parallel graph construction and search | High batch throughput and parallel build | GPU memory and deployment coupling | [ICDE 2024 paper](https://doi.org/10.1109/ICDE60146.2024.00323) |

**Figure 1.** Research-family distinctions; do not infer product support from a paper alone.  
**Takeaway:** Ask what graph is built, how it is searched, where it resides, and how it updates.

## Navigation picture

```mermaid
flowchart LR
  Q[Query] --> E[Entry point(s)]
  E --> G[Explore promising graph neighbors]
  G -->|closer candidate| G
  G -->|bounded candidate set| R[Return top-k]
  G -. disk design .-> SSD[(SSD neighbors / vectors)]
  G -. GPU design .-> GPU[Parallel frontier / distance kernels]
```

**Figure 2.** Common graph-search abstraction, simplified.  
**How to read this:** All graph families rely on navigable connectivity, but differ in graph construction and query scheduling. Disk methods optimize read count/locality; GPU methods expose parallel work; hierarchical methods use multiple scales.

**Takeaway:** Graph quality and hardware execution both determine retrieval cost.

## What differs

**TL;DR:** Graph algorithms encode different compromises between navigability, degree, build cost, and hardware locality.

- **NSG:** Fu et al. construct a graph approximating an MRNG, emphasizing connectivity, low average degree, short search paths, and compact index size. The paper reports Taobao e-commerce integration at billion-node scale; paper-reported results are workload-specific ([PVLDB paper](https://vldb.org/pvldb/vol12/p461-fu.pdf)).
- **Vamana:** DiskANN's graph construction applies robust pruning and supports beam-search traversal with SSD-resident adjacency/data. The original DiskANN paper evaluates a billion-point SIFT workload and reports its own hardware/data results; do not transfer them to another deployment without measurement ([NeurIPS paper](https://proceedings.neurips.cc/paper/2019/hash/09853c7fb1d3f8ee67a61b6bf4a7f8e6-Abstract.html)).
- **CAGRA:** Ootomo et al. develop a GPU-oriented graph build and search algorithm. NVIDIA cuVS documents CAGRA as a GPU index and exposes implementation-specific controls ([cuVS guide](https://docs.nvidia.com/cuvs/user-guide/)). Host-to-device memory and graph conversion matter operationally.
- **SSG:** A graph-family research baseline; use its paper and implementation to pin precise definitions rather than treating the name as a database index type.

| Axis | Questions to measure |
|---|---|
| Graph quality | Recall vs visited nodes / distance evaluations |
| Degree | Link memory, cache behavior, construction work |
| Build | Peak memory, parallelism, rebuild time, deterministic reproducibility |
| Hardware | RAM/SSD reads, GPU VRAM, host-device transfers, batch-size sensitivity |
| Freshness | Insert/delete path, tombstones, merge/rebuild requirements |
| Filters | Whether predicate changes traversal or only removes final candidates |

## Selection and failure modes

**TL;DR:** Select a graph by the serving hardware and lifecycle, not just the search-quality curve.

| Symptom | Check |
|---|---|
| Excellent recall but memory too high | Degree limits, IDs, raw vectors, replicas, alignment |
| Disk graph misses latency SLO | Random read count, beam width, SSD queue depth, cache hit rate |
| GPU throughput disappoints | Batch size, VRAM fit, transfer time, synchronization |
| New inserts lower recall | Incremental graph quality, update backlog, rebuild policy |
| Filter recall collapses | Eligibility-aware traversal, post-filter candidate starvation |

Benchmark each family against a flat exact baseline with the same data, filters, hardware, build budget, and query batch. Report recall@k, p95/p99, memory/VRAM, bytes read, build time, and update behavior. Graph implementations can have distinct APIs and guarantees even when they share a paper family name.

## SDE-1 checklist and interview Q&A

**TL;DR:** Make graph memory and traversal counters observable alongside recall and tail latency.

- Record implementation/version, degree parameters, build settings, seed, and corpus snapshot.
- Track visited nodes, distance computations, I/O per query, cache hit rate, and result count after filters.
- Test inserts/deletes and failure recovery; verify if graph state rebuilds from durable records.

**Basic — Why graph ANN?** It navigates selected local neighborhoods to avoid scoring the entire corpus; this trades graph storage/build work for fewer candidate evaluations.

**Deep — Why Vamana for SSD?** Its graph/search design is paired with beam-style traversal and disk access considerations; node layout, batching, and I/O behavior are integral to the system, not a property of any graph alone.

**Trap — Is CAGRA just HNSW on a GPU?** No. It is a GPU-oriented graph construction/search design with distinct parallelization and API behavior.

## References

- Fu et al., NSG, PVLDB 2019, [DOI](https://doi.org/10.14778/3303753.3303754).
- Subramanya et al., DiskANN, NeurIPS 2019, [paper](https://proceedings.neurips.cc/paper/2019/hash/09853c7fb1d3f8ee67a61b6bf4a7f8e6-Abstract.html).
- Ootomo et al., CAGRA, ICDE 2024, [DOI](https://doi.org/10.1109/ICDE60146.2024.00323); [cuVS docs](https://docs.nvidia.com/cuvs/user-guide/).
- [SSG paper](https://arxiv.org/abs/1907.06146); Malkov & Yashunin, [HNSW](https://arxiv.org/abs/1603.09320).

**Next:** [LSH and tree methods](05-lsh-and-tree-methods.md).  
**Related:** [HNSW](03-hnsw-deep-dive.md), [Disk-based ANN](06-disk-based-ann.md), [evaluation](../07-evaluation-benchmarking/01-metrics-recall-qps-latency.md).
