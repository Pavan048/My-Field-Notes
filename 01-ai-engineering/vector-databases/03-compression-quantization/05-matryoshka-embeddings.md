# Matryoshka embeddings

> **TL;DR:** Matryoshka training makes prefixes of an embedding useful, enabling dimension-versus-quality trade-offs without a separate model per dimension.

```mermaid
flowchart LR
 E[trained full embedding] --> P1[prefix d1: cheap shortlist]
 E --> P2[prefix d2: stronger retrieval]
 P1 --> R[retrieve candidates]
 R --> P2[rerank with longer prefix]
```

**Figure 1: Simplified conceptual view of this topic.**

**Takeaway:** Follow the arrows to see where the method spends work and where the main trade-off enters.

### How to read this

- Follow arrows in the direction data or decisions move.
- The labels name the main components; they do not promise a specific implementation.
- Use the table and field notes below to connect the picture to measurements.

**Visual takeaway:** The diagram shows the main data or decision path; labels are conceptual, not performance guarantees.

## Field notes

Truncation is meaningful only for embeddings trained with a compatible objective; slicing a conventional embedding can degrade quality unpredictably. Store the largest needed representation or regenerate shorter vectors from the model. Benchmark each prefix on task relevance, index footprint, and serving latency. Matryoshka dimensions compose naturally with quantization but their errors interact.

## Sources

[Matryoshka Representation Learning](https://arxiv.org/abs/2205.13147) · [Sentence Transformers Matryoshka](https://sbert.net/examples/sentence_transformer/training/matryoshka/README.html). Product behavior and defaults can vary by release; pin the version used in any benchmark.

**Next:** [Master index](../00-INDEX.md) · [Glossary](../99-glossary.md).
