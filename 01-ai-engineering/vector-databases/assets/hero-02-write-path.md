# Hero 02 â€” Write path and segment lifecycle

```mermaid
sequenceDiagram
  participant C as Client
  participant A as Access / streaming service
  participant W as WAL
  participant G as Growing buffer / segment
  participant D as Background data worker
  participant O as Object storage
  C->>A: insert / update / delete
  A->>W: append mutation
  W-->>A: durable acknowledgement (system-specific)
  A->>G: apply mutation for serving
  G->>D: flush / seal when policy is met
  D->>O: persist segment and build index artifacts
  O-->>D: artifact locations / metadata
  D-->>A: publish sealed searchable version
```

**Figure 2.** Simplified WAL-to-segment path, using Milvus terminology. Exact acknowledgement and publication semantics depend on product/version and consistency settings.

**Takeaway:** Durability, freshness, and index readiness are distinct milestones; never infer one from another without checking the system contract.

**Sources:** [Milvus data processing](https://milvus.io/docs/data_processing.md); [Milvus architecture](https://milvus.io/docs/architecture_overview.md).


