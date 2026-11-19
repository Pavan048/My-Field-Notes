# Python + RAG Ingestion — Last-Minute Revision (2–4 min)

## Python execution
- **Python:** High-level, dynamically typed language; supports multiple threads/processes.
- **CPython:** Standard Python implementation, mostly C.
- **Execution:** `app.py` → CPython **compiles** to **bytecode** → CPython VM **interprets** it → CPU executes interpreter machine code.
- **Compiled:** Code translated to another form. **Interpreted:** An interpreter executes instructions. Bytecode is **not** native CPU code.

## OS + concurrency
- **Process:** Running program with its own virtual memory/resources; processes don't automatically share Python objects.
- **Thread:** Execution unit within a process; threads share process memory, each has its own call stack.
- **Stack:** Function-call/execution state. **Heap:** Python objects (lists, dicts, etc.) generally live here.
- **GIL:** In traditional CPython, one thread executes Python bytecode per interpreter at a time; I/O can overlap.
- **Concurrency:** Tasks progress over overlapping time. **Parallelism:** Tasks run simultaneously.
- **Threads:** Useful for blocking I/O. **Asyncio:** Event loop switches between coroutines when they `await` nonblocking I/O. **Multiprocessing:** CPU-bound parallelism with separate memory.
- **4 cores ≠ 4-thread limit.** Worker count is configured and benchmarked; too many CPU workers waste RAM and cause contention.
- **Bounded concurrency:** Caps in-flight operations. **Rate limit:** Caps calls/tokens in a time window.

## Flask / FastAPI
- **Flask:** Lightweight Python web framework; typically WSGI/synchronous. Run in production with Gunicorn (or another WSGI server).
- **FastAPI:** ASGI framework with typed validation and async support; served by **Uvicorn**.
- **Framework:** Defines routes and logic. **Server:** Accepts connections and runs the app.
- `uvicorn main:app --workers 2` = two API worker processes.

## RAG ingestion — FastAPI + Celery + Redis + MongoDB
- **Flow:** Upload → FastAPI validates/authenticates → save PDF + MongoDB `PENDING` job → enqueue Celery task via Redis → return `202 + job_id` → worker extracts/OCRs, cleans, chunks, embeds, stores → MongoDB `COMPLETED/FAILED`.
- **Redis:** Broker carrying job messages (send a file reference/job ID, **not** the entire PDF).
- **Celery:** Executes queued background tasks. Default **prefork** worker pool uses child processes.
- **MongoDB:** Job status + tenant/document metadata; vectors only if configured.
- **Why queue?** API stays responsive; bursts are buffered; processing scales/retries independently.
- **CPU-heavy pure-Python parsing:** Processes. **Remote embeddings/DB I/O:** Async/threads where supported, with concurrency caps.
- **Example:** Four execution slots run ~four tasks concurrently; remaining jobs wait or may be prefetched.

## Production risks → fixes
- **Duplicate uploads/retries:** Hash, idempotency, stable chunk IDs, upserts.
- **Worker crashes / huge PDFs:** Retry/recovery settings, page-wise processing, memory caps.
- **Embedding 429/timeouts:** Batching, bounded concurrency, exponential backoff.
- **Partial writes:** Versioning/cleanup; expose document for retrieval only when complete.
- **Queue publish/Redis failures:** Persistence, reconciliation or outbox.
- **MongoDB overload / tenant floods:** Bulk writes, indexes, connection limits, quotas.
- **Monitor:** Job status, error rate, queue depth, throughput, memory, latency.

**20-second interview answer:** “FastAPI validates documents and creates MongoDB job records. Celery publishes tasks through Redis, and background workers extract, chunk, embed and store results, then update status. A queue protects API responsiveness during upload bursts. We design for retries, duplicates, rate limits, memory spikes and partial failures, and tune workers using CPU/RAM and throughput.”

*Distinguish safeguards you built from those you would propose.*
