<p align="center">
  <img src="https://capsule-render.vercel.app/api?type=waving&color=0:080a0f,35:0f172a,70:1e293b,100:0369a1&height=220&section=header&text=MY%20FIELD%20NOTES&fontSize=42&fontColor=ffffff&desc=Personal%20Engineering%20Archive%20%E2%80%A2%20AI%20Engineering%20%E2%80%A2%20System%20Design%20%E2%80%A2%20DevOps%20%E2%80%A2%20Teardowns&descFontSize=16&descAlignY=68&animation=fadeIn" alt="My Field Notes Banner" width="100%" />
</p>

<p align="center">
  <a href="https://github.com/Pavan048/My-Field-Notes"><img src="https://img.shields.io/badge/Status-Living_Archive-10B981?style=flat-square" alt="Status Living Archive" /></a>
  &nbsp;
  <a href="#-knowledge-taxonomy"><img src="https://img.shields.io/badge/Focus-AI_Engineering_%7C_System_Design_%7C_DevOps-0284C7?style=flat-square" alt="Focus" /></a>
  &nbsp;
  <a href="https://linkedin.com/in/sajjaraopavankrishna"><img src="https://img.shields.io/badge/Author-Pavan_Krishna-6366F1?style=flat-square" alt="Author Pavan Krishna" /></a>
</p>

---

### 📖 About This Archive

This repository is my **personal technical field notebook and evergreen reference library**. 

Instead of treating software engineering as syntax memorization or surface-level tutorials, this space is dedicated to **investigative engineering** and **first-principles understanding**:

- 🔬 **Open-Source Teardowns**: Dissecting emerging startups and production frameworks (agent memory, coding harnesses, vector databases) to analyze how they actually work under the hood.
- 🏛️ **System Design & Distributed Systems**: Analyzing High-Level (HLD) and Low-Level (LLD) architectures, data modeling, concurrency bottlenecks, and failure modes.
- 🤖 **AI Engineering**: Deep dives into multi-agent orchestration, multi-hop RAG pipelines, cognitive memory layers, evaluation harnesses, and token economics.
- ⚙️ **DevOps & Infrastructure**: Practical production notes on Kubernetes, Docker optimization, CI/CD promotion workflows, and Linux internals.
- 💡 **Everyday Learnings (TIL)**: Short, sharp captures of subtle bugs, edge cases, and architectural trade-offs encountered in the wild.

---

### 🗂️ Knowledge Taxonomy

```text
My-Field-Notes/
├── 01-ai-engineering/          # Multi-agent graphs, RAG architectures, memory, evals
├── 02-system-design/
│   ├── hld/                    # High-Level Design (distributed systems, caching, queues)
│   └── lld/                    # Low-Level Design (patterns, concurrency, data structures)
├── 03-devops-and-infra/        # Kubernetes, Docker, CI/CD, Linux, networking, observability
├── 04-opensource-teardowns/    # Deep architectural dissections of open-source projects
├── 05-til/                     # Quick, bite-sized "Today I Learned" insights
└── templates/                  # Standardized templates for writing structured notes
```

---

### 📑 Topic Directory

#### 🤖 1. AI Engineering & Cognitive Systems
*Deep dives into production LLM architectures, agentic orchestration, and retrieval.*

- [x] **Agentic RAG vs. Naive RAG**: When single-pass retrieval breaks and why multi-hop loops are necessary.
- [ ] **Hierarchical Context Management**: Small-to-large chunk expansion and context budgeting.
- [ ] **Two-Tier Cognitive Memory**: Designing session caching (Redis) + episodic recall (Qdrant) for self-improving agents.
- [ ] **Evaluation Harnesses & Guardrails**: Measuring relevance, accuracy, and hallucination with Opik.

#### 🏛️ 2. System Design & Distributed Architectures
*High-Level & Low-Level Design patterns, trade-offs, and scalability bottlenecks.*

- [ ] **HLD: Distributed Rate Limiter** — Sliding Window Counter vs. Token Bucket with Redis Cluster failover.
- [ ] **HLD: Real-Time Event-Driven Notification Engine** — Fan-out patterns with Kafka and consumer groups.
- [ ] **LLD: Concurrent Connection Pool** — Thread safety, semaphores, and graceful connection lifecycle management.
- [ ] **Database Partitioning & Sharding** — Range vs. Hash sharding and rebalancing strategies.

#### ⚙️ 3. DevOps, Cloud & Infrastructure
*Hard-won lessons from the infrastructure trenches.*

- [ ] **Zero-Downtime Deployments** — Blue/Green vs. Rolling updates and database migration locks.
- [ ] **Kubernetes Ingress Controllers** — Traffic routing, SSL termination, and Service mesh comparisons.
- [ ] **Docker Multi-Stage Build Optimization** — Slashing image footprint and container attack surface.
- [ ] **Linux Observability Primitives** — Understanding `top`, `vmstat`, `strace`, and eBPF.

#### 🔬 4. Open-Source Teardowns
*Reverse-engineering real-world startups and open-source tools to see what's hype vs. reality.*

- [ ] **Open-Source Agent Memory Breakdown**: A structural comparison of Mem0, Letta (MemGPT), and Zep.
- [ ] **Autonomous Coding Agent Harnesses**: Sandboxing, execution sandpits, and evaluation loops (SWE-bench / e2b).
- [ ] **Vector Database Internals**: HNSW indexing vs. Inverted File (IVF) graph traversals in Qdrant.

#### 💡 5. Today I Learned (TIL)
*Atomic, single-concept notes and debugging gotchas.*

- [ ] Python asyncio event loop blocking traps and background worker lifespans.
- [ ] PostgreSQL connection pool exhaustion during peak bursts.
- [ ] Handling SSE token buffering across reverse proxies (Nginx / Cloudflare).

---

### 📐 Standard Note Structure

Every technical deep dive in this repository follows a disciplined 5-part engineering framework:

1. **The Core Engineering Challenge**: What problem are we solving, and under what scale/latency constraints?
2. **Architecture & Data Flow**: Clear, labeled Mermaid diagrams illustrating component interactions.
3. **Under the Hood & Implementation**: Key data structures, algorithms, and pseudo-code.
4. **Trade-off Analysis (*Why X and not Y?*)**: An honest comparison matrix of alternative approaches.
5. **Failure Modes & Production Reality**: What happens when dependencies crash, network splits occur, or budgets overflow?

---

### 📬 Connect

- **Author**: Sajjarao Pavan Krishna
- **Role**: AI Engineer (SDE 1) @ Exto (Bengaluru, India)
- **LinkedIn**: [linkedin.com/in/sajjaraopavankrishna](https://linkedin.com/in/sajjaraopavankrishna)
- **Email**: [pavankrishna048@gmail.com](mailto:pavankrishna048@gmail.com)
