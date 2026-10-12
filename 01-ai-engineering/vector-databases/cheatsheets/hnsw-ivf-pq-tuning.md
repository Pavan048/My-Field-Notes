# HNSW / IVF / PQ tuning

> **TL;DR:** Increase search effort to recover recall, then measure added latency and memory on the same query cohort.

```mermaid
flowchart TD
 Recall low --> HNSW[Raise efSearch]
 Recall low --> IVF[Raise nprobe]
 Memory high --> PQ[More compact codes]
 Change --> Eval[recheck recall + p99 + bytes]
```

**Figure 1: Simplified conceptual view of this topic.**

**Takeaway:** Follow the arrows to see where the method spends work and where the main trade-off enters.

### How to read this

- Follow arrows in the direction data or decisions move.
- The labels name the main components; they do not promise a specific implementation.
- Use the table and field notes below to connect the picture to measurements.

**Visual takeaway:** The diagram shows the main data or decision path; labels are conceptual, not performance guarantees.

## Field notes

| Method | Build knobs | Query knob | First cost to watch |
|---|---|---|---|
| HNSW | M, efConstruction | efSearch | graph memory and p99 |
| IVF | nlist, training sample | nprobe | training and scanned vectors |
| PQ | subspaces, bits, rotation | candidate depth | quantization recall loss |

## Sources

[FAISS paper](https://arxiv.org/abs/1702.08734) · [FAISS index guide](https://github.com/facebookresearch/faiss/wiki/Faiss-indexes). Product behavior and defaults can vary by release; pin the version used in any benchmark.

**Next:** [Master index](../00-INDEX.md) · [Glossary](../99-glossary.md).
