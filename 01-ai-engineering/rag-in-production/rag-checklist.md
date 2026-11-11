# RAG Production Checklist

> Fill this out for each RAG project. Check off items as implemented and tested.
> Based on: 12-category RAG failure taxonomy from [rag-deep-dive.md](rag-deep-dive.md)

**Project**: _______________  
**Date Started**: _______________  
**Vector DB**: _______________  
**Embedding Model**: _______________  
**LLM**: _______________  
**Team**: _______________

---

## Phase 1: Source Data & Document Management

- [ ] Content deduplication strategy defined (hash-based SHA-256 on raw bytes, or semantic similarity threshold)
- [ ] Deduplication enforced at API boundary before ingestion begins
- [ ] Delete propagation tested end-to-end: vector DB → metadata store → semantic cache
- [ ] Hard delete confirmed (not soft-delete flag) with cascade to all derived records
- [ ] Provenance fields defined per chunk: `doc_id`, `page_number`, `section_title`, `ingested_at`, `source_url`
- [ ] Version replacement flow tested: old version vectors deleted before new version indexed
- [ ] Document version tracked in metadata; queries can filter by version if needed
- [ ] Source authority scoring defined (or explicitly decided as not needed for this use case)
- [ ] Access control per document defined: which users / tenants can access which docs
- [ ] Authority conflict resolution strategy documented (reranking? explicit precedence rules?)

**Notes**: _____

---

## Phase 2: Ingestion & Parsing

- [ ] Parser chosen and justified for each file type in scope (PDF, DOCX, HTML, XLSX, PPTX, etc.)
- [ ] Per-page / per-section error isolation implemented: one bad page does not kill full batch
- [ ] Partial success response returned: failed pages listed, successful pages indexed
- [ ] OCR strategy defined for scanned documents (Tesseract, Azure Document Intelligence, etc.)
- [ ] Scanned PDFs routed to separate OCR pipeline, not text-extraction pipeline
- [ ] Table extraction validated: tables extracted as markdown, not fragmented prose
- [ ] Table row boundary splitting: header row duplicated on every slice of a split table
- [ ] Figure / image strategy chosen: caption-only, skip entirely, or vision-describe
- [ ] Page count cross-check: extracted page count validated against PDF metadata `page_count`
- [ ] Silent truncation detection: alert if extracted content is significantly shorter than expected
- [ ] Prompt injection sanitization implemented and runs before any LLM call in ingestion
- [ ] Injection sanitization tested with known patterns: `IGNORE ALL PREVIOUS`, `<system>`, `you are now`
- [ ] Upload size limits enforced at API boundary (per-file and per-request)
- [ ] Backpressure enforced at ingestion queue: large uploads don't starve other tenants
- [ ] API keys and credentials redacted from all error logs and exception traces

**Notes**: _____

---

## Phase 3: Chunking & Embedding

- [ ] Chunking strategy chosen and documented: recursive, semantic, fixed-size, or hybrid
- [ ] Chunk size validated on a representative sample of actual production documents
- [ ] Different chunk sizes configured per content type (prose vs. code vs. tables)
- [ ] Sentence-boundary awareness implemented: no splits mid-sentence
- [ ] Fallback hierarchy defined: paragraph → sentence → hard token slice (with overlap)
- [ ] Overlap between chunks configured and tuned (typical: 10-20% of chunk size in tokens)
- [ ] Chunk IDs are deterministic: `UUID5(namespace, f"{doc_id}:{chunk_index}")` or equivalent
- [ ] Deterministic IDs verified: re-ingesting same document produces same chunk IDs
- [ ] Embedding model chosen, pinned, and version tracked in chunk metadata
- [ ] Embedding model is identical for index time and query time (desync is a silent failure)
- [ ] Sparse + dense strategy chosen: hybrid (BGE-M3), dense-only, or dense + separate BM25
- [ ] Embedding drift detection plan in place: what happens when model is updated?
- [ ] Re-embedding plan documented for model migration (full re-index required)

**Notes**: _____

---

## Phase 4: Index & Storage

- [ ] Vector DB chosen with explicit justification (Qdrant, Weaviate, Pinecone, pgvector, etc.)
- [ ] Index type chosen with parameter tuning documented: HNSW (`m`, `ef_construction`) / IVF / flat
- [ ] Payload / metadata schema defined in vector DB (fields stored alongside vectors)
- [ ] Hard filter fields indexed as payload indexes: `tenant_id`, `user_id`, `doc_type`, `doc_id`
- [ ] WAL / durability settings reviewed and set appropriately for data criticality
- [ ] Replication strategy defined for high availability (replica count, consistency level)
- [ ] Segment compaction strategy configured: aggressive enough to reclaim deleted vector space
- [ ] mmap vs. RAM-only decision documented and justified (mmap for large indexes, RAM for latency-critical)
- [ ] Backup and restore procedure tested (not just defined — actually tested)
- [ ] Index size projected at 1x, 10x, 100x expected corpus size

**Notes**: _____

---

## Phase 5: Retrieval

- [ ] Retrieval mode chosen and justified: dense-only / sparse-only / hybrid
- [ ] If hybrid: fusion weights (`α`) tuned on validation set with ground-truth relevance labels
- [ ] Filter strategy chosen per query type: pre-filter / post-filter / in-graph filtering
- [ ] Pre-filter recall tested: small candidate sets after filtering don't collapse recall
- [ ] Multi-query retrieval implemented for decomposed / multi-hop queries
- [ ] Query rewriting implemented and tested against vocabulary mismatch cases
- [ ] Recall@K measured on held-out ground truth dataset (not just anecdotally checked)
- [ ] MRR@K measured in addition to Recall@K
- [ ] Cross-tenant isolation explicitly tested: attempt to retrieve another tenant's documents; confirm failure
- [ ] Re-ranker evaluated: MRR measured with and without re-ranker on your domain before adding it
- [ ] Retrieval latency benchmarked at p50 / p95 / p99 under expected load

**Notes**: _____

---

## Phase 6: Evidence Selection & Context Assembly

- [ ] Top-K limit set and validated: not so large it fills context, not so small it misses evidence
- [ ] MMR (Maximal Marginal Relevance) or equivalent diversity mechanism implemented
- [ ] Token budget allocation defined per context section (instructions / evidence / query / output)
- [ ] Instructions budget is reserved first and never truncated by evidence overflow
- [ ] Evidence truncation strategy documented: which chunks get dropped when over budget?
- [ ] Evidence coverage check implemented: not just relevance, but are answer-critical entities present?
- [ ] Context ordering validated: highest-scored evidence at start AND end (lost-in-the-middle mitigation)
- [ ] Authorization hard-filter confirmed at retrieval layer, not post-hoc in evidence selection
- [ ] Context payload logged per request for debugging and offline eval
- [ ] Metadata included with each chunk in context (doc title, page, date) for citation generation

**Notes**: _____

---

## Phase 7: Generation & Citation

- [ ] System prompt tested for instruction persistence across short and long contexts
- [ ] Critical instructions duplicated: at start of system prompt AND immediately before the question
- [ ] Citation grounding check implemented: every `[N]` citation verified to exist in context
- [ ] Quoted text in citations fuzzy-matched against actual chunk content
- [ ] Citation fabrication tested: ask for citations to documents not in context; confirm rejection
- [ ] Hallucination rate measured on eval set with known ground truth
- [ ] Abstention behavior explicitly tested: query with no supporting evidence → model must refuse
- [ ] Abstention instruction in system prompt ("If you cannot find the answer in the documents, say so")
- [ ] Sufficiency check implemented for multi-hop queries (optional for simple single-hop)
- [ ] Sufficiency loop capped at hard maximum iterations (e.g., 2) to prevent infinite loops
- [ ] Output length limits enforced: max tokens set appropriate to use case
- [ ] Generation model and version logged per request

**Notes**: _____

---

## Phase 8: Evaluation

- [ ] Ground truth QA dataset built with ≥ 100 examples per domain / document type
- [ ] Ground truth includes: query, expected answer, source chunk IDs, expected citations
- [ ] Retrieval eval: Recall@K measured (K = your production top-K)
- [ ] Retrieval eval: Precision@K measured
- [ ] Retrieval eval: MRR@K measured
- [ ] Generation eval: answer accuracy vs. ground truth
- [ ] Generation eval: citation accuracy (% citations that are correct and verifiable)
- [ ] Generation eval: abstention rate on no-evidence queries (should be ~100%)
- [ ] Adversarial test set built: missing information, conflicting documents, injection attempts
- [ ] Adversarial injection test: documents with injection patterns don't hijack generation
- [ ] End-to-end latency benchmarked: p50, p95, p99 under realistic query load
- [ ] Cost per query estimated: retrieval inference + LLM tokens (input + output)
- [ ] Eval suite runs in CI/CD pipeline on every model or prompt change

**Notes**: _____

---

## Phase 9: Production Operations

- [ ] Request-level structured logging implemented: query, chunks, context tokens, latency breakdown
- [ ] Unique `request_id` on every request for trace correlation
- [ ] Recall@K sampled in production (5% of traffic) and computed against random held-out queries
- [ ] Recall@K production alert wired: notify on-call when recall drops below threshold
- [ ] Citation verification failure rate alerted: notify on-call when failure rate > threshold
- [ ] Sufficiency loop frequency alerted: notify when >N% of queries require >1 iteration
- [ ] Semantic cache implemented for high-volume FAQ-style queries (saves LLM cost)
- [ ] Cache hit rate monitored and cache TTL tuned
- [ ] Backpressure and rate limiting enforced per tenant at ingestion and query
- [ ] Startup job recovery: on-restart, stranded ingestion jobs detected and resumed or failed explicitly
- [ ] Embedding model migration runbook written: re-index plan, cutover strategy, rollback plan
- [ ] Runbook: what to do when recall drops (checklist of investigation steps)
- [ ] Runbook: what to do when citation failures spike
- [ ] Ingestion queue depth monitored and alerted
- [ ] p99 latency alert wired to on-call

**Notes**: _____

---

## Phase 10: Security

- [ ] Prompt injection sanitization in ingestion pipeline (before any LLM call during parsing/chunking)
- [ ] Prompt injection sanitization at query time (before rewriting, before generation)
- [ ] Sanitization tested with known injection patterns; regression test suite exists
- [ ] Cross-tenant retrieval explicitly tested: confirmed that tenant A cannot retrieve tenant B's data
- [ ] Tenant isolation implemented as hard pre-filter at vector DB, not as post-filter or guidance
- [ ] PII handling policy defined: what PII can appear in chunks? In logs?
- [ ] PII in logs redacted or masked before shipping to log aggregation
- [ ] Hard delete cascade tested end-to-end: delete request → Qdrant delete → MongoDB purge → cache invalidate
- [ ] GDPR / CCPA deletion SLA defined and tested (how long does full deletion take?)
- [ ] Encryption keys (BYOK) never logged: redacted from all error paths and exception traces
- [ ] Context overflow attack tested: adversarially long inputs don't evict system instructions
- [ ] Input token limits enforced at API boundary before hitting the LLM

**Notes**: _____

---

## Completion Summary

| Phase | Status | Owner | Last Verified |
|---|---|---|---|
| Phase 1: Source Data & Document Management | ⬜ Not Started | | |
| Phase 2: Ingestion & Parsing | ⬜ Not Started | | |
| Phase 3: Chunking & Embedding | ⬜ Not Started | | |
| Phase 4: Index & Storage | ⬜ Not Started | | |
| Phase 5: Retrieval | ⬜ Not Started | | |
| Phase 6: Evidence Selection & Context Assembly | ⬜ Not Started | | |
| Phase 7: Generation & Citation | ⬜ Not Started | | |
| Phase 8: Evaluation | ⬜ Not Started | | |
| Phase 9: Production Operations | ⬜ Not Started | | |
| Phase 10: Security | ⬜ Not Started | | |

> **Status legend**: ⬜ Not Started → 🔄 In Progress → ✅ Complete → ⚠️ Needs Review
