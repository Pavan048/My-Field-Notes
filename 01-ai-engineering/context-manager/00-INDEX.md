# Context Manager — Research & Learning Index

> **Scope:** How an AI application constructs, budgets, orders, supplies, observes, and manages the *active model context* for each invocation.
>
> **Status:** Active learning track · **Current checkpoint:** Foundations, assembly, tokenization and budgeting completed · **Next:** Context ordering and position effects.

---

## 1. Why this track exists

A model invocation can only use the information made available to it in that invocation (along with what is encoded in its parameters). In an agent application, the engineering problem is deciding **which information to include, in what representation, order, and budget**, then measuring whether the model used it correctly.

This track studies that problem from first principles through papers, source code, experiments and implementations.

### Working definition

**Context management** is the application- and inference-layer work of constructing and managing the information presented to a model for a particular invocation.

It includes:
- assembling instructions, user input, conversation, evidence, tool descriptions and relevant runtime data;
- selecting and ordering content under model/API limits;
- managing token budgets and context-window constraints;
- deciding what to omit, defer, summarize or retrieve;
- observing and evaluating the final model input and its outcomes.

This is a working definition for this notebook, not a claim that the field has one universally accepted definition.

---

## 2. Boundary: context management vs agent memory

These are **two related but distinct engineering tracks**. We will study them independently, then examine their interfaces later.

| Dimension | Context management | Agent memory |
|---|---|---|
| Primary question | What should the model receive now? | What information should the agent retain across time? |
| Main concern | Current invocation input | Persistence, updates, lifecycle and future reuse |
| Typical operations | Assemble, select, order, budget, serialize | Write, store, update, consolidate, forget, retrieve |
| Typical artifacts | Prompt/context payload, tool schemas, retrieved evidence | Memory records, event logs, profiles, knowledge stores |
| Evaluation | Context use, answer quality, token cost, latency | Recall, relevance, freshness, consistency, write quality |
| Relationship | May consume retrieved memory as an input source | May provide candidate information to context assembly |

**Important boundary rules**
1. A memory record is not automatically part of the model context. The application must select and inject it.
2. Retrieval is an operation that can supply candidates to context assembly; it is not synonymous with memory.
3. Context management can operate without persistent agent memory (for example, a stateless question-answering request).
4. Agent memory can exist outside the active context and may not be used in a given invocation.
5. We will not teach memory taxonomies or memory architectures inside this track, except where needed to describe an integration boundary.

Related future track: [Agent Memory](../agent-memory/00-INDEX.md).

---

## 3. Learning method

We will follow this cycle for each topic:

1. **Problem and first principles** — what breaks, and why?
2. **Mechanics** — what happens inside the application, API and model?
3. **Research** — read relevant papers and identify assumptions, methods, metrics and limitations.
4. **Systems study** — inspect real implementations and source code.
5. **Implementation** — build a small component or reproducible experiment.
6. **Evaluation** — measure quality, token use, latency, cost and failure modes.
7. **Field notes** — record conclusions, open questions and links.

We will distinguish paper findings, implementation observations, engineering hypotheses and rules of thumb. We will not adopt a framework-specific pattern as a principle without understanding the underlying problem.

---

## 4. Curriculum map

The sequence below is dependency-oriented. We will move forward only after understanding the current layer.

| ID | Module | Main questions | Status |
|---|---|---|---|
| CM-00 | Foundations and terminology | What is context? How does it differ from memory, retrieval and runtime state? | ✅ Completed |
| CM-01 | Context construction and assembly | Which sources contribute to a model invocation, and how are candidates selected? | ✅ Completed |
| CM-02 | Tokenization, budgets and context windows | What consumes tokens? How do input/output limits and safety margins work? | ✅ Completed |
| CM-03 | Context ordering and position effects | Does the location of evidence change whether it is used? What does Lost in the Middle show? | ▶ Next |
| CM-04 | Long-context behavior and utilization | What happens as context grows? How do distraction, interference and position interact? | Planned |
| CM-05 | Retrieval as context selection | How should candidates be found, ranked, filtered and fitted into a context? | Planned |
| CM-06 | Context relevance and selection policies | How do we decide what to include, exclude, defer or expand? | Planned |
| CM-07 | Tool context and progressive disclosure | How should tools and schemas be discovered and loaded without overwhelming the context? | Planned |
| CM-08 | Context compression and compaction | How can context be shortened while retaining task-relevant information? | Planned |
| CM-09 | Execution context and state handoff | What runtime information must be included for a model to continue a task? | Planned |
| CM-10 | Multi-agent context transfer | What should cross agent boundaries, and how should handoffs be represented? | Planned |
| CM-11 | Context observability and debugging | How do we inspect the exact input and diagnose context-related failures? | Planned |
| CM-12 | Context security and trust boundaries | How should untrusted content, prompt injection and tenant boundaries be handled? | Planned |
| CM-13 | Evaluation and benchmarks | How do we test context construction, evidence use and context degradation? | Planned |
| CM-14 | Production architecture and capstone | How do the components fit into a robust context manager? | Planned |

### Track completion criteria

The track is not complete when we have read the papers. It is complete when we can:
- explain the context construction lifecycle and its trade-offs;
- build a context manager with explicit policies and token budgets;
- trace and reproduce the exact input sent to a model;
- evaluate position, retrieval, compression and tool-loading strategies;
- identify context failures separately from model reasoning failures;
- explain security boundaries and production operational concerns.

---

## 5. Research reading list

The reading list is organized by the problem each work helps us understand. **Planned** means selected for study, not yet read or independently validated in this notebook.

### A. Context engineering and assembly

| Resource | Why it is on the list | Stage |
|---|---|---|
| [Anthropic — Effective context engineering for AI agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) | Practical framing for context construction, retrieval, tools and progressive disclosure | Planned |
| [Context Engineering Survey](https://arxiv.org/) | Broad research map; exact survey/version to be pinned before detailed review | Candidate — verify |

### B. Context length, position and utilization

| Resource | Why it is on the list | Stage |
|---|---|---|
| [Lost in the Middle: How Language Models Use Long Contexts](https://arxiv.org/abs/2307.03172) | Controlled study of how relevant information position affects long-context task performance | Selected — next |
| [LongBench](https://arxiv.org/abs/2308.14508) | Long-context evaluation across multiple task types | Planned |
| [RULER](https://arxiv.org/abs/2404.06654) | Evaluating long-context understanding beyond simple needle retrieval | Planned |

### C. Retrieval as context selection

| Resource | Why it is on the list | Stage |
|---|---|---|
| [Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks](https://arxiv.org/abs/2005.11401) | Foundational RAG formulation: retrieve evidence and condition generation on it | Planned |
| [Self-RAG](https://arxiv.org/abs/2310.11511) | Adaptive retrieval and self-reflective generation | Planned |
| [HyDE](https://arxiv.org/abs/2212.10496) | Query-side retrieval representation and its trade-offs | Planned |

### D. Compression and compact context representations

| Resource | Why it is on the list | Stage |
|---|---|---|
| [LLMLingua](https://arxiv.org/abs/2310.05736) | Coarse-to-fine prompt compression | Selected |
| [LongLLMLingua](https://aclanthology.org/2024.acl-long.91/) | Compression and question-aware context selection for long inputs | Selected |
| [LLMLingua-2](https://aclanthology.org/2024.findings-acl.57/) | Data-distillation-based prompt compression | Selected |
| [Selective Context](https://arxiv.org/abs/2310.06201) | Selecting informative text for context reduction | Planned |

### E. Tool context and progressive disclosure

| Resource | Why it is on the list | Stage |
|---|---|---|
| [Anthropic — Effective context engineering](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) | Tool definitions, retrieval and progressive disclosure guidance | Planned |
| [Model Context Protocol specification](https://modelcontextprotocol.io/specification/) | Protocol-level tool/resource context and discovery concepts | Planned |

### F. Evaluation and security

| Resource | Why it is on the list | Stage |
|---|---|---|
| [LongBench](https://arxiv.org/abs/2308.14508) | Long-context task evaluation | Planned |
| [RULER](https://arxiv.org/abs/2404.06654) | Synthetic and structured long-context evaluation | Planned |
| [OWASP Top 10 for LLM Applications](https://owasp.org/www-project-top-10-for-large-language-model-applications/) | Threat model for prompt injection and unsafe handling of untrusted context | Planned |

**Reading discipline:** before writing a paper summary, record its exact title, authors, publication venue/date, version, task setup, baselines, metrics, key results and limitations. A link in this index is a reading candidate, not evidence that we have verified every claim in the paper.

---

## 6. Systems and implementation study list

These are systems to inspect when the curriculum reaches the corresponding concept. We will inspect only the relevant components, not attempt to learn every repository end-to-end.

| System / project | What to inspect | Curriculum connection |
|---|---|---|
| [LangGraph](https://github.com/langchain-ai/langgraph) | State, message handling, reducers, checkpoint integration and execution flow | Assembly, execution context, handoff |
| [LlamaIndex](https://github.com/run-llama/llama_index) | Retrieval pipelines, node selection and context assembly | Retrieval and context selection |
| [Haystack](https://github.com/deepset-ai/haystack) | Pipeline-based retrieval and generation components | Retrieval and assembly |
| [Microsoft LLMLingua](https://github.com/microsoft/LLMLingua) | Compression implementation and evaluation | Compression |
| [vLLM](https://github.com/vllm-project/vllm) | Prompt handling, sequence scheduling and KV-cache-aware serving | Serving boundary; distinguish from application context policy |
| [SGLang](https://github.com/sgl-project/sglang) | Runtime execution and prefix/KV reuse mechanisms | Serving boundary |
| [Langfuse](https://github.com/langfuse/langfuse) | Traces, model-call inputs/outputs and observability | Debugging and evaluation |

A system's inclusion does not imply endorsement. We will verify current repository structure and version when we reach it.

---

## 7. Learning log — completed so far

### CM-00 — Foundations and terminology

**Question:** What information does an LLM have access to when generating an answer?

Learned:
- The application supplies the invocation's context; the model does not automatically inspect arbitrary databases, files or repositories.
- Context is the information supplied for the current invocation.
- Persistent memory is retained information that may become a source for a future context.
- Retrieval is the operation of finding/selecting candidate information.
- Execution state tracks workflow progress and information needed to continue.
- KV cache is an inference computation cache, not a user-memory store.

**Boundary we retain:** context, memory, retrieval, execution state and KV cache are different concepts.

### CM-01 — Context construction and assembly

**Question:** How does an application decide what to send to the model?

Learned a logical decomposition of context:
1. Instructions
2. Conversation history
3. Retrieved information / evidence
4. Tool definitions
5. Current request
6. Relevant execution data

Learned a conceptual assembly pipeline:

`Sources → Candidates → Filter / rank → Budget → Order → Serialize → Model input`

Additional concepts:
- Context assembly is not merely string concatenation.
- Progressive disclosure can avoid loading every tool schema or document at once.
- Stable and dynamic context have different change patterns; stable prefixes may be useful for cache reuse, subject to correctness and platform behavior.
- Observability requires knowing what actually entered the model, not just what the application intended to send.

### CM-02 — Tokenization, budgets and context windows

**Question:** How much information can an invocation contain?

Learned:
- Models consume tokenized input; token boundaries vary by tokenizer.
- BPE is a useful intuition for subword tokenization, not a universal description of every tokenizer.
- Context windows and API input/output limits must be accounted for separately according to the target API.
- Token allocation is a budget problem, not a fixed universal ratio.
- Input accounting can include message framing, tool schemas and multimodal payload accounting beyond plain text tokens.
- Production systems should use the target model/API's tokenizer and usage accounting.

Example budget calculation:

`32,768 total − 4,096 output reserve − 1,024 safety margin = 27,648 input tokens`

Overflow strategies introduced:
- truncation;
- sliding windows;
- summarization / compaction;
- retrieval-based selection;
- hierarchical loading.

Prototype implemented conceptually in the lesson: a Python `ContextBudgetManager` using `tiktoken` to count section tokens, compute a simple budget and report fit. It is a teaching prototype, not production-ready.

### CM-03 — Context ordering and position effects

**Question:** If the same relevant evidence appears at different positions in an otherwise equivalent context, does the model use it equally well?

Learned:
- Context presence does not guarantee context utilization.
- Self-attention lets token representations incorporate information from other positions, but attention is not equivalent to successful retrieval, comprehension or reasoning.
- Transformers incorporate positional information through architecture-dependent mechanisms such as positional embeddings or rotary positional embeddings (RoPE).
- Positional encoding and position-dependent task performance are different concepts.
- The *Lost in the Middle* study evaluated multi-document question answering and key-value retrieval while varying the location of relevant information.
- In many evaluated settings, performance followed a U-shaped pattern: stronger near the beginning and end, weaker in the middle.
- This is a reported pattern, not a universal ordering rule for every model, task or context length.

Practical implications introduced:
- Use clear document boundaries and source identifiers.
- Group related evidence and avoid unnecessary duplication.
- Treat context ordering as a design variable to evaluate, not a fixed recipe.
- Keep instructions and task requirements explicit.
- Preserve evidence provenance for inspection and citations.

**Primary paper:** [Lost in the Middle: How Language Models Use Long Contexts](https://arxiv.org/abs/2307.03172).

**Experiment designed:** EXP-03 — Position sensitivity benchmark. Keep the model, question, evidence, distractors, prompt construction and token length controlled; move the same evidence through beginning, quarter, middle, three-quarter and end positions. Measure answer accuracy, evidence identification, citation correctness, abstention, token count and latency. Use multiple questions and repeated trials.

**Limitations:** The paper does not establish that the end is always optimal, that every model has the same position curve, or that moving evidence fixes retrieval and reasoning failures.

### CM-04 — Long-context behavior and utilization

**Question:** Does a larger context window guarantee that a model can effectively use all the information supplied?

Learned:
- Context capacity, context utilization and task performance are different properties.
- Effective context length is task- and metric-dependent; it is not necessarily one universal number for a model.
- Long inputs can introduce distractor interference, information dilution and multi-hop reasoning challenges.
- Finding one fact is different from combining multiple facts across documents.
- A single benchmark score, especially from simple needle retrieval, can hide weaknesses on other long-context tasks.

Research studied:

**[LongBench — A Bilingual, Multitask Benchmark for Long Context Understanding](https://aclanthology.org/2024.acl-long.172/)**
- Broad evaluation across long-context tasks, including single-document QA, multi-document QA, summarization, few-shot learning, synthetic tasks and code completion.
- The lesson was to evaluate diverse task types rather than treat one retrieval task as a complete measure of long-context understanding.

**[RULER — What's the Real Context Size of Your Long-Context Language Models?](https://arxiv.org/abs/2404.06654)**
- Tests capabilities beyond a basic Needle-in-a-Haystack (NIAH) task.
- Introduces more demanding controlled tasks, including multi-needle retrieval, tracing and aggregation.
- Passing a simple needle retrieval test does not establish strong performance on complex long-context tasks.

Key distinction:
- **NIAH:** locate a planted fact among distractors.
- **Multi-hop:** connect evidence across multiple context locations.
- **Aggregation:** combine or compute over multiple pieces of evidence.
- **Long-document summarization:** retain and express important content across a longer source.

**Benchmark caveats:** LongBench offers broad dataset/task coverage; RULER offers controlled capability tests. Neither benchmark alone represents every production workload. Synthetic task success does not prove real-world agent competence.

**Experiment plan:** Evaluate single-fact retrieval, multi-fact retrieval, multi-document QA, multi-hop tracing, aggregation, summarization and codebase understanding over context lengths supported by the selected model. Record accuracy, evidence recall, citation correctness, abstention, input/output tokens, latency, cost and repeatability. Use controlled datasets and repeated trials; do not compare incomparable model/API configurations.

**Systems to inspect later:**
- [LongBench repository](https://github.com/THUDM/LongBench)
- [RULER repository](https://github.com/NVIDIA/RULER)

### Current checkpoint

- Completed: CM-00, CM-01, CM-02.
- Next lesson: CM-03 — Context ordering and position effects.
- No deep dive into agent-memory architectures has been counted as completed in this track.

---

## 8. Experiments and project backlog

We will turn concepts into reproducible experiments rather than rely only on reading.

| ID | Experiment / build | What it should teach | Status |
|---|---|---|---|
| EXP-01 | Tokenizer comparison notebook | Same text under different tokenizers | Planned |
| EXP-02 | Context budget allocator | Priority-based fitting under a hard token budget | Planned |
| EXP-03 | Position sensitivity benchmark | Same evidence at beginning, middle and end | Planned |
| EXP-04 | Retrieval-to-context pipeline | Candidate retrieval, ranking and context packing | Planned |
| EXP-05 | Tool schema progressive loader | Compact tool catalog → discovery → full schema | Planned |
| EXP-06 | Compression quality benchmark | Token reduction vs task accuracy/evidence retention | Planned |
| EXP-07 | Context trace viewer | Inspect exact serialized model input and token accounting | Planned |
| EXP-08 | Context manager capstone | Policies, budgets, ordering, observability and evaluation | Planned |

### Evaluation dimensions

Where applicable, experiments should record:
- task correctness / exact match;
- evidence recall and citation correctness;
- instruction compliance;
- abstention or uncertainty behavior;
- input and output token usage;
- latency and cost;
- repeatability / variance across trials;
- failure categories and examples.

We will define task-specific metrics rather than assume one score captures context quality.

---

## 9. Current design principles — hypotheses to test

These are working engineering principles, not universal guarantees:

1. **Measure the actual request.** Application-side character counts are not a substitute for target API token accounting.
2. **Make inclusion decisions explicit.** Record why each context item was selected.
3. **Treat ordering as a design variable.** Do not assume equal usefulness at every position.
4. **Use progressive disclosure for large tool/document inventories.** Load detail when it becomes relevant.
5. **Preserve provenance.** Keep source identifiers and boundaries so evidence can be inspected.
6. **Separate evidence from instructions.** Label untrusted retrieved content and define how it should be treated.
7. **Optimize for task utility, not maximum context fill.** More tokens do not automatically mean better answers.
8. **Evaluate end-to-end.** A retrieval or compression component must be tested in the full model task.

---

## 10. Open questions

We will keep unresolved questions here and close them with evidence or experiments.

- How does evidence position interact with context length, task type and model architecture?
- When does long-context input outperform retrieval, and when does it underperform?
- What is the right objective for context selection: relevance, coverage, diversity, recency, trust or a weighted combination?
- How can context packing preserve relationships between chunks, tables and multi-document evidence?
- How should tool schemas be summarized without hiding important constraints?
- How do we compare lossy compression with retrieval-based omission?
- How do we attribute a failure to missing context, bad ordering, retrieval, instruction conflict or model reasoning?
- What should be logged for reproducibility without leaking secrets or sensitive data?

---

## 11. Revision protocol

At the end of each major module, update this index:
- mark module status and date;
- add a concise explanation of what was learned and why;
- add papers actually read, with findings and limitations;
- add repositories/files actually inspected;
- record experiments, code, metrics and results;
- move unresolved questions forward;
- update the next lesson.

**Do not mark a paper, repository or experiment as completed merely because it appears in the plan.**

---

## 12. Next lesson

### CM-03 — Context ordering and position effects

We will investigate one controlled question:

> If the same relevant evidence is provided with the same task and the same distractors, does moving that evidence to a different position in the context change the model's ability to use it?

Study:
1. Positional information and attention at a conceptual level.
2. The *Lost in the Middle* paper's task setup and findings.
3. What the paper does and does not establish.
4. Practical context-ordering strategies and their limits.
5. A controlled position-sensitivity experiment.

Primary reading: [Lost in the Middle (Liu et al.)](https://arxiv.org/abs/2307.03172).

---

*Last updated: 2026-11-06*
