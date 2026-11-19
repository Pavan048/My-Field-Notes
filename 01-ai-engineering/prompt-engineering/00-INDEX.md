# Prompt Engineering — Level 3 · Foundations

> **One index + one complete technical blog.** Learn to make LLM instructions clear, testable, economical and reliable. Context engineering—the broader selection, retrieval and management of relevant context—is a later, separate topic.

[**Read the complete Prompt Engineering deep dive →**](prompt-engineering-deep-dive.md)

## Roadmap

**Phase:** 1 · Foundations  
**Level:** 3 · Prompt Engineering  
**Interview weight:** 5/10 — essential basic competence, usually not a headline differentiator  
**On-the-job weight:** 8/10 — repeated daily in AI engineering  
**Level allocation:** 11 of 286 sessions (4%)  
**Cumulative allocation:** 67 of 286 sessions (23%)  
**Prerequisite:** Level 2 · Working with LLM APIs (Orchestration)  
**Accelerated option:** 7-day version in 100 Days of AI Engineering (as supplied in the roadmap).

| Module | Sessions | Deep-dive chapter | Deliverable |
|---|---:|---|---|
| M3.1 Anatomy of a prompt | 1 | [1](prompt-engineering-deep-dive.md#module-1--anatomy-of-a-prompt-m31) | A correctly scoped prompt contract |
| M3.2 Zero-shot & few-shot | 2 | [2](prompt-engineering-deep-dive.md#module-2--zero-shot-and-few-shot-prompting-m32) | A good example set and no-example baseline |
| M3.3 Reasoning & decomposition | 1 | [3](prompt-engineering-deep-dive.md#module-3--reasoning-and-decomposition-m33) | A workflow for complex tasks |
| M3.4 System prompt design | 2 | [4](prompt-engineering-deep-dive.md#module-4--system-prompt-design-m34) | A maintainable instruction hierarchy |
| M3.5 Controlling output | 1 | [5](prompt-engineering-deep-dive.md#module-5--controlling-output-m35) | Strict structured result + validator |
| M3.6 Prompt reliability & debugging | 2 | [6](prompt-engineering-deep-dive.md#module-6--prompt-reliability-and-debugging-m36) | Failure taxonomy and regression suite |
| M3.7 Versioning, cost & caching | 1 | [7](prompt-engineering-deep-dive.md#module-7--prompt-versioning-cost-and-caching-m37) | Prompt experiment ledger + caching policy |
| M3.8 Prompt injection basics | 1 | [8](prompt-engineering-deep-dive.md#module-8--prompt-injection-basics-m38) | Tested trust boundary |
| M3.9 Optimize a Real Prompt (capstone) | Capstone | [9](prompt-engineering-deep-dive.md#module-9--capstone-optimize-a-real-prompt) | Before/after prompts and measurable checks |

**Roadmap note:** the first eight modules total 11 listed sessions. The capstone has no separate session allocation in the supplied roadmap, so the 11-session total is left unchanged.

## Technique selector — not every pattern belongs in every prompt

| Situation | First technique | Pitfall to avoid |
|---|---|---|
| Clear task with strong model | Zero-shot | Overengineering |
| Repeated extraction/classification ambiguity | Few-shot with edge cases | Pattern/label leakage |
| Complex multi-part task | Decomposition, checkpoints, tools | Excessive verbose reasoning |
| Exact data format needed | API-native structured output + validation | “Return JSON” as sole guarantee |
| Domain-specific assistant | Stable developer/system contract | Contradictory or overlong instructions |
| Hallucinations on missing facts | Explicit evidence/abstention rubric + eval | Claiming prompts guarantee correctness |
| High latency or cost | Shorten stable prompts, test caching | Removing essential constraints |
| Untrusted documents | Separate data from instructions and enforce backend ACL | Treating delimiters as security |

## The operating mental model

~~~mermaid
flowchart LR
 GOAL["User's actual task"] --> SPEC["Define success and failure"]
 SPEC --> PROMPT["Instructions + examples + output contract"]
 PROMPT --> RUN["Run pinned model"]
 RUN --> CHECK["Check facts, format, safety, cost"]
 CHECK --> FAIL{"Pass release gates?"}
 FAIL -->|No| DEBUG["Diagnose + revise one thing"]
 DEBUG --> PROMPT
 FAIL -->|Yes| VERSION["Version and monitor"]
~~~

## Sources

- [OpenAI prompt engineering](https://developers.openai.com/api/docs/guides/prompt-engineering)
- [OpenAI reasoning best practices](https://developers.openai.com/api/docs/guides/reasoning-best-practices)
- [Anthropic Claude prompting best practices](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices)
- [Google prompt design strategies](https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/prompts/prompt-design-strategies)
- [OWASP prompt-injection prevention](https://cheatsheetseries.owasp.org/cheatsheets/LLM_Prompt_Injection_Prevention_Cheat_Sheet.html)

*Original engineering synthesis. Last updated: 2026-11-19. This is a learning roadmap, not a claim of course completion.*
