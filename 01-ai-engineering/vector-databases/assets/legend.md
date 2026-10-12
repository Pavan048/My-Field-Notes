# Diagram legend

Use these conventions across the vector-database notes. Mermaid class colors are optional because GitHub themes differ; labels and line styles carry the meaning.

| Shape / label | Meaning |
|---|---|
| Client / API | Caller-owned request boundary |
| Planner / coordinator | Routing, scheduling, query planning, or metadata decisions |
| Index / search | Candidate generation or approximate/exact scoring |
| WAL / durable log | Ordered mutation record used for recovery or replication |
| Segment / object storage | Persisted data/index files; immutable only where the system guarantees it |
| Solid arrow | Data or control flow explicitly described by the cited source |
| Dashed arrow | Optional, asynchronous, or version-specific path; label it explicitly |
| `growing` / `sealed` | Milvus-specific segment terms; do not generalize as universal vector DB terminology |
| `simplified` | Omits implementation details; caption must name the abstraction |

Every figure must have a number, descriptive caption, takeaway, and direct source links. Distinguish paper algorithms from a vendor's product architecture and cite versioned documentation when behavior is version-sensitive.


