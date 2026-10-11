# RAG in Production: A Taxonomy of Failures and What CITE-RAG Actually Covers

Most RAG demos work. Most RAG systems in production fail silently.

Over the past few months I built [CITE-RAG](https://github.com/Pavan048/CITE-RAG) — a production-grade multi-hop retrieval system with inline citations. While building it, I ran into a pattern: every time I thought "this is basically done," I discovered another class of failure I hadn't accounted for.

I later mapped those experiences against research from Anthropic, Microsoft, NVIDIA, Google Cloud, OWASP, and a few arXiv RAG surveys. The full taxonomy runs to 12 categories. This note audits CITE-RAG against that taxonomy — not to claim completeness, but to be honest about what the system handles and what it intentionally leaves out.

---

## The 12 Categories

The full failure taxonomy covers:

1. Source data and knowledge management
2. Ingestion and document-processing failures
3. Chunking and indexing failures
4. Query understanding and routing
5. Retrieval failures
6. Evidence selection and context construction
7. Generation, hallucination, and citation
8. Multi-hop and reasoning failures
9. Security and adversarial inputs
10. Evaluation and testing
11. Production operations and observability
12. Multi-tenant and access control

---

## Coverage Audit

### 1. Source Data and Knowledge Management

| Failure Mode | CITE-RAG | Notes |
|---|---|---|
| Duplicate documents | ✅ Full | SHA-256 content-hash dedup in `app/api/documents.py` before any processing begins. Same bytes in a different filename are rejected. |
| Deleted-document persistence | ✅ Full | Hard delete propagates to Qdrant (by `doc_id` filter) and MongoDB atomically. |
| Missing provenance | ✅ Full | Every chunk stores `doc_id`, `page_number`, `section_title`, `content_type` in Qdrant payload. Used live at citation time. |
| Stale information / version confusion | ⚠️ Partial | Re-uploading a changed file creates a new document; old version isn't automatically evicted. Operator must delete manually. |
| Source authority / conflicting sources | ⚠️ Partial | Sufficiency check and reranker surface higher-scored chunks first. No explicit authority ranking or conflict detection. |
| Access restrictions (per-user) | ❌ Out of scope | Single-tenant design. No row-level security on Qdrant queries, no per-user document ACLs. |
| Delayed sync / connector failures | ❌ Out of scope | No automated connectors. Documents are pushed via API; freshness is the caller's responsibility. |

---

### 2. Ingestion and Document-Processing Failures

This is where I spent the most time during development. It shows.

| Failure Mode | CITE-RAG | Notes |
|---|---|---|
| Corrupted / unsupported files | ✅ Full | Magic-byte check (`%PDF-`), `pypdf` xref walk for page count. Files that fail either gate are rejected before queueing. |
| Parser crashes / per-page failures | ✅ Full | IBM Docling with `raises_on_error=False`. Per-page isolation: `page._backend is None or not page._backend.is_valid()` skips bad pages without killing the document. |
| OCR failures | ✅ Full | Docling OCR enabled by default. Handles scanned PDFs, low-resolution pages. |
| Table extraction | ✅ Full | Docling extracts tables as markdown. Multi-page and merged-cell handling is delegated to Docling's table model. |
| Figure / image extraction | ✅ Full | Figures cropped and captioned via BYOK LLM call (`caption_image()` in `parse.py`). |
| Header / footer contamination | ✅ Full | Docling structural parsing separates headers, footers, and body text. |
| Prompt injection in documents | ✅ Full | `sanitize_text()` in `chunk.py` redacts `"ignore all previous instructions"`, `"system:"`, and similar patterns via regex — runs before any LLM call. |
| BYOK key leakage in error logs | ✅ Full | `_redact(message, secret)` in `llm_client.py` strips API keys from all exceptions before propagation. Key passed per-call, never stored in client state. |
| Ingestion pipeline crash leaving stranded jobs | ✅ Full | `recover_stranded_jobs()` runs on startup. Jobs stranded mid-flight are hard-failed (not resumed) because the in-memory BYOK key is gone — honest failure rather than silent zombie. |
| Oversized documents causing OOM | ✅ Full | File streamed in 1MB chunks during upload; SHA-256 computed incrementally. Queue has bounded capacity; `put_nowait()` returns `503` under backpressure. |
| Silent parser truncation | ⚠️ Partial | Docling is trusted to extract everything it can. No post-parse completeness check comparing extracted page count to PDF page count. |
| Unicode / encoding problems | ⚠️ Partial | Delegated to Docling. Non-UTF-8 edge cases depend on Docling's handling. |
| Virus scanning | ⚠️ Skeleton | Code path exists (`virus_scan_enabled` in config), disabled by default. Not integrated with any scanner backend. |
| Multilingual documents | ⚠️ Partial | BGE-M3 is multilingual. Chunking and parsing handle Latin scripts well; RTL and mixed-script documents are not explicitly tested. |

---

### 3. Chunking and Indexing Failures

| Failure Mode | CITE-RAG | Notes |
|---|---|---|
| Chunk size / overlap misconfiguration | ✅ Configurable | `chunk_target_tokens=512`, `chunk_overlap_ratio=0.125`. Recursive splitting: paragraph → sentence → hard token slice. Greedy window merge to target size. |
| Boundary damage (definition split from explanation) | ✅ Full | Sentence-aware splitting before hard token slice. Paragraph-level grouping preserved by recursive strategy. |
| Heading separation | ✅ Full | Section title extracted from Docling structure and stored per-chunk as `section_title` metadata — not embedded in chunk text where it could be split away. |
| Deterministic / idempotent chunk IDs | ✅ Full | UUID5 deterministic IDs: `uuid5(NAMESPACE_URL, f"{doc_id}:{chunk_index}")`. Retry-safe; same document re-ingested produces same IDs, enabling clean upsert. |
| Table fragmentation | ⚠️ Partial | Tables extracted as single markdown string. If a table exceeds `chunk_target_tokens`, it will be split. No special table-preservation override. |
| Embedding model mismatch | ✅ Full | Single embedding service (BGE-M3) for both indexing and query time. No path where they could diverge. |
| Embedding drift on model change | ⚠️ Gap | No re-indexing trigger on model version change. If BGE-M3 is updated, old and new vectors coexist with no detection. |
| Sparse indexing errors | ✅ Full | BGE-M3 returns dense + sparse in one forward pass. No separate sparse pipeline that could desync. |
| Index inconsistency (partial write) | ✅ Full | Document status set to `ready` only after both Qdrant upsert AND MongoDB write succeed. Partial failures leave document in `processing` state. |

---

### 4. Query Understanding and Routing

| Failure Mode | CITE-RAG | Notes |
|---|---|---|
| Single vs. multi-hop misclassification | ✅ Full | `classify_plan_node` makes an explicit LLM call to classify intent before routing. Misclassification is possible but the decision is deliberate, not absent. |
| Wrong document routing | ✅ Full | `route_retrieve_node` embeds the current sub-question, runs summary-level vector search with a configurable similarity floor (`doc_routing_similarity_floor=0.35`). Caller can pin `file_ids` to skip routing entirely. |
| Missing query expansion | ⚠️ Partial | Multi-hop loop rewrites sub-queries across hops — functionally similar to expansion but tied to sufficiency failure, not proactive synonym expansion. |
| Ambiguous / underspecified queries | ⚠️ Partial | No clarification flow. System attempts retrieval; if evidence is insufficient after 4 hops, it returns a partial answer rather than hallucinating. |
| Conversation-context loss | ⚠️ Partial | Session state is maintained within a single request. Cross-session context resolution (e.g., "that document from yesterday") is not implemented. |
| Query routing to wrong collection | ✅ Full | Explicit `not_found` short-circuit on hop 1 when no document clears the routing floor — prevents unfiltered corpus-wide search on clearly out-of-scope queries. |
| Embedding service outage handling | ✅ Full | Hop 1 outage → `retrieval_unavailable` (honest service error, not "not found"). Later hop outage → contributes no evidence for that hop; loop continues with prior evidence. Distinction is deliberate and documented in `route_retrieve.py`. |

---

### 5. Retrieval Failures

| Failure Mode | CITE-RAG | Notes |
|---|---|---|
| Vector-only retrieval missing exact identifiers | ✅ Full | Hybrid search: BGE-M3 dense + sparse, fused in application code via RRF (`rrf_k=60`). Sparse leg handles exact-match terms, codes, identifiers. |
| Poor hybrid fusion | ✅ Full | RRF implemented in `route_retrieve_node`. Server-side Qdrant fusion is not used — application-level fusion gives consistent behavior regardless of Qdrant version. |
| Missing cross-hop deduplication | ✅ Full | `accumulate_node` is the only node allowed to write `evidence_pool`. Deduplication by `chunk_id` across all hops happens there, not in retrieval. |
| Hop count unbounded | ✅ Full | `hop_cap=4` enforced in `sufficiency_check_node`. Hop 4 sets `partial_answer` flag and exits — no wasted rewrite call on final hop. |
| Sufficiency check on wrong question | ✅ Full | LLM judges accumulated pool against the **original question**, not the current sub-question. Prevents the system from satisfying a sub-question and declaring victory. |
| Reranker unavailable | ✅ Full | Falls back to RRF order if cross-encoder is unreachable. Documented in `rerank_node`. |
| Hop 2+ routing per sub-question | ✅ Full | Each hop re-routes against `current_sub_question`, not the original query. Enables hop 2 to route to a different document than hop 1. |

---

### 6. Evidence Selection and Context Construction

| Failure Mode | CITE-RAG | Notes |
|---|---|---|
| Retrieving small chunks missing surrounding context | ✅ Full | `context_budget_node` implements small-to-large expansion: retrieved chunk IDs are swapped for their full parent sections before generation. |
| Context window overflow / uncontrolled token growth | ✅ Full | `context_token_budget=1800` tokens enforced. Lowest-ranked whole parent blocks dropped if over budget. Blocks are dropped whole, not truncated mid-sentence. |
| Shared parent block duplication | ✅ Full | When two chunks share a parent, the parent is included once. Backing chunk ID lists are merged. No repeated text in context. |
| No context → hallucinated answer | ✅ Full | `generate_cite_node` checks context. If empty, no LLM call is made. Honest "no information found" response instead. |

---

### 7. Generation, Hallucination, and Citation

| Failure Mode | CITE-RAG | Notes |
|---|---|---|
| Uncited or fabricated citations | ✅ Full | `generate_cite_node` enforces `[doc_id:page:chunk_id]` markers per sentence. Every marker is validated against the actual retrieved chunk catalog. Unmatched markers are stripped — not passed through. |
| Hallucinated answer from insufficient evidence | ✅ Full | Partial answer flag on hop cap exhaustion. Citation enforcement means unsupported claims lose their markers or aren't generated. |
| Key redaction in error propagation | ✅ Full | `_redact()` strips API keys before any exception surfaces to logs or API responses. |

---

### 8. Security and Adversarial Inputs

| Failure Mode | CITE-RAG | Notes |
|---|---|---|
| Prompt injection via document content | ✅ Full | `sanitize_text()` in `chunk.py` before any LLM call. |
| API key exposure in logs | ✅ Full | `_redact()` + per-call key passing, never stored in client object. |
| Malicious file uploads | ✅ Full | Magic byte check, page count validation, bounded upload stream. |
| Virus scanning | ⚠️ Skeleton | Flag exists, not wired. |
| Authorization-aware retrieval | ❌ Out of scope | No per-user filter on Qdrant queries. |
| Cross-tenant leakage | ❌ Out of scope | Single-tenant design. |
| OWASP LLM Top 10 — full coverage | ⚠️ Partial | Prompt injection addressed. Model denial-of-service partially addressed via queue backpressure. Others (insecure output handling, training data poisoning) not addressed. |

---

### 9. Evaluation and Testing

| Failure Mode | CITE-RAG | Notes |
|---|---|---|
| No eval harness | ⚠️ Skeleton | `app/eval/` exists with `golden_set/` subdirectory. `__init__.py` is empty. No RAGAS, no Opik integration, no automated regression pipeline. |
| No golden set | ⚠️ Skeleton | `golden_set/` folder present, currently empty. |
| Retrieval quality measurement | ❌ Gap | No recall@k, MRR, or NDCG measurement implemented. |
| Answer quality measurement | ❌ Gap | No faithfulness, answer relevance, or context precision scores. |

---

### 10. Production Operations and Observability

| Failure Mode | CITE-RAG | Notes |
|---|---|---|
| Startup recovery for crashed jobs | ✅ Full | `recover_stranded_jobs()` on service start. |
| Queue backpressure / overload handling | ✅ Full | `put_nowait()` → `503` when queue is full. Worker pool is bounded. |
| Service outage graceful degradation | ✅ Full | Embedding service down → honest error or hop skip. Reranker down → fallback to RRF. |
| Semantic caching | ✅ Full | In-process LRU cache keyed by dense embedding cosine similarity (`>= 0.97`), partitioned by `file_ids` scope, with TTL and automatic invalidation on document deletion (`app/services/semantic_cache.py`). |
| Cost & token tracking per request | ✅ Full | Token usage (prompt + completion) tracked per LLM call across LangGraph nodes, accumulated across multi-hop iterations with `operator.add` reducers, and exposed with USD cost estimation in `TokenSummary` (`app/retrieval/debug_trace.py`). |
| Per-hop node & execution tracing | ✅ Full | LangGraph execution stream trace recording exact path, sub-questions, retrieved chunks per hop, and raw prompt/response traces in `DebugInfo`. |
| Distributed tracing across external services | ⚠️ Partial | Node-level and hop-level tracing captured in `DebugInfo`; external OpenTelemetry/OTLP exporter not wired. |

---

## Summary

**What CITE-RAG covers well:**
- The entire ingestion hardening story — corrupt files, per-page parser isolation, prompt injection, BYOK key safety, backpressure, stranded job recovery, deduplication.
- The multi-hop retrieval loop — per-hop routing, cross-hop dedup, sufficiency checking against the original question, hop cap with honest partial answers.
- Citation integrity — per-sentence marker enforcement with catalog validation. No hallucinated citations pass through.
- Hybrid retrieval — dense + sparse, application-level RRF, reranker with fallback.
- Context construction — small-to-large expansion, token budgeting, no mid-block truncation, no duplicate parent sections.
- Semantic caching — scope-aware in-memory LRU cache with embedding similarity matching.
- Cost and execution observability — multi-hop token accumulation, per-node traces, and cost estimation.

**What CITE-RAG deliberately excludes:**
- Multi-tenant access control and per-user permission filtering. The system is single-tenant by design.
- Authorization-aware retrieval. No row-level security on Qdrant.

**What CITE-RAG has as gaps or skeletons:**
- Evaluation harness. The scaffolding is there (`app/eval/`); needs golden dataset and automated regression pipeline.
- External distributed tracing (OpenTelemetry/Opik exporter).
- Automatic re-indexing on model version change.
- Clarification flows for underspecified queries.

---

The implementation is at [github.com/Pavan048/CITE-RAG](https://github.com/Pavan048/CITE-RAG). Every coverage claim above maps to a specific file and function — none of this is aspirational.

The gaps are real. The eval harness and observability are the two I'd close first for anything going to production.
