# Hero 09 â€” Segment lifecycle

```mermaid
stateDiagram-v2
  [*] --> Growing: accept mutations
  Growing --> Sealed: flush / seal policy
  Sealed --> Indexed: build index artifact
  Indexed --> Merged: compaction publishes replacement
  Merged --> [*]: retire superseded segment after safe point
  Growing --> [*]: abort / recovery cleanup (implementation-specific)
  Sealed --> [*]: delete / retention cleanup (implementation-specific)
```

**Figure 9.** Simplified lifecycle using Milvus's growing/sealed vocabulary. Real segment states, compaction publication, and reclamation rules are product-specific; arrows are not a universal state machine.

**Takeaway:** Compaction creates replacement data/index views; safe retirement requires coordination with readers, snapshots, and recovery.

**Sources:** [Milvus data processing](https://milvus.io/docs/data_processing.md); [Milvus architecture](https://milvus.io/docs/architecture_overview.md).


