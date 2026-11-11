<p align="center">
  <img src="https://capsule-render.vercel.app/api?type=waving&color=0:080a0f,35:0f172a,70:1e293b,100:0369a1&height=220&section=header&text=MY%20FIELD%20NOTES&fontSize=42&fontColor=ffffff&desc=Personal%20Engineering%20Archive%20%E2%80%A2%20AI%20Engineering%20%E2%80%A2%20Systems%20Internals&descFontSize=16&descAlignY=68&animation=fadeIn" alt="My Field Notes Banner" width="100%" />
</p>

<p align="center">
  <a href="https://github.com/Pavan048/My-Field-Notes"><img src="https://img.shields.io/badge/Status-Living_Archive-10B981?style=flat-square" alt="Status Living Archive" /></a>
  &nbsp;
  <a href="#-topics"><img src="https://img.shields.io/badge/Focus-AI_Engineering_%7C_Internals-0284C7?style=flat-square" alt="Focus" /></a>
  &nbsp;
  <a href="https://linkedin.com/in/sajjaraopavankrishna"><img src="https://img.shields.io/badge/Author-Pavan_Krishna-6366F1?style=flat-square" alt="Author Pavan Krishna" /></a>
</p>

---

### 📖 About This Archive

This repository is my **personal technical field notebook and reference library for production AI systems**.

Rather than high-level tutorials or surface-level API usage, this space is dedicated to **first-principles systems internals, mathematical trade-offs, and failure modes**:

- 🔬 **Evidence-Backed**: Every core concept is grounded in published literature (arXiv, IEEE, NeurIPS) and real production implementations.
- 📐 **Depth Over Breadth**: Designed for senior and staff engineers who want to understand the mechanical internals of models, indexes, and memory layers.
- 📊 **Visual-First**: Structured with Mermaid sequence diagrams, state machines, and architecture pipelines before prose.

---

### 🗂️ Knowledge Taxonomy

Each domain is organized as a dedicated folder containing a fast-lookup **`00-INDEX.md`** and an in-depth, blog-style technical deep dive:

```text
My-Field-Notes/
└── 01-ai-engineering/
    ├── vector-databases/         # Embeddings, ANN graphs (HNSW), quantization, storage engines
    ├── context-engineering/      # Context stack, token budgets, position effects, compression
    ├── agent-memory/             # Cognitive memory taxonomy, lifecycles, temporal graphs
    └── rag-in-production/        # 12-category failure taxonomy, hybrid retrieval, production checklist
```

---

### 📑 Topics

#### 🗃️ 1. [Vector Databases](01-ai-engineering/vector-databases/00-INDEX.md)
*Storage engines, metric spaces, and high-dimensional ANN algorithms.*

- [x] **[Vector Database Internals](01-ai-engineering/vector-databases/vector-databases.md)**: Metric spaces, Curse of Dimensionality, HNSW layer skip-lists, IVF-PQ Voronoi quantization, DiskANN SSD beam search, LSM segment architecture, and filtered search recall cliffs.

#### 🧠 2. [Context Engineering](01-ai-engineering/context-engineering/00-INDEX.md)
*Constructing, budgeting, ordering, and securing the active model context.*

- [x] **[Context Engineering Deep Dive](01-ai-engineering/context-engineering/context-engineering.md)**: The 6-layer context stack, token budgeting arithmetic, position effects (*Lost in the Middle*), long-context utilization pitfalls (RULER / LongBench), progressive disclosure, and prompt injection defense.

#### 💾 3. [Agent Memory](01-ai-engineering/agent-memory/00-INDEX.md)
*Information lifecycle, state persistence, and retrieval across sessions.*

- [x] **[Agent Memory Architectures](01-ai-engineering/agent-memory/agent-memory.md)**: Episodic vs. semantic vs. procedural memory, write-path deduplication, contradiction resolution, temporal knowledge graphs (Graphiti / Zep), Letta (MemGPT), and evaluation harnesses (LongMemEval).

#### 🔍 4. [RAG in Production](01-ai-engineering/rag-in-production/00-INDEX.md)
*Multi-hop retrieval pipelines, grounding, and operational resilience.*

- [x] **[RAG Failure Taxonomy & CITE-RAG Architecture](01-ai-engineering/rag-in-production/rag-deep-dive.md)**: 12 categories of production RAG failures, dense+sparse hybrid retrieval (BGE-M3), iterative sufficiency checks, and citation grounding.
- [x] **[RAG Production Checklist](01-ai-engineering/rag-in-production/rag-checklist.md)**: 10-phase production deployment readiness checklist for teams building enterprise RAG systems.

---

### 📬 Connect

- **Author**: Sajjarao Pavan Krishna
- **Role**: AI Engineer @ Exto (Bengaluru, India)
- **LinkedIn**: [linkedin.com/in/sajjaraopavankrishna](https://linkedin.com/in/sajjaraopavankrishna)
- **Email**: [pavankrishna048@gmail.com](mailto:pavankrishna048@gmail.com)
