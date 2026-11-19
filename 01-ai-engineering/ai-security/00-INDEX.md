# AI Security — Level 8 / Evaluation & Trust

> One navigation index and one substantial, readable technical blog. **The design goal is an AI system that remains safe even when a model makes a bad decision or reads malicious content.**

[**Read the complete AI Security engineering blog**](ai-security-deep-dive.md)

## Roadmap details

- **Phase 4:** Evaluation & Trust.
- **Interview weight:** 5/10 — usually prompt injection, RAG leakage or least-privilege tools; expect deeper questions in security-sensitive AI platform roles.
- **On-the-job weight:** 7/10 — a single authorization failure or unauthorized action can be serious.
- **Supplied roadmap progress:** Level 8 is 15 of 286 sessions (5%); cumulative through level 8 is 161 of 286 (56%). These are roadmap allocations, not a claim you completed them.
- **Prerequisite:** Level 7 · LLM Evaluations.

| Module | Sessions | Blog chapter | What you'll learn |
|---|---:|---|---|
| M8.1 AI threat model | 1 | [Module 1](ai-security-deep-dive.md#module-1-ai-threat-model-m81) | Assets, actors, boundaries and impact |
| M8.2 Prompt injection & data exfiltration | 3 | [Module 2](ai-security-deep-dive.md#module-2-prompt-injection-and-data-exfiltration-m82) | Direct/indirect injection, exfiltration, mitigations |
| M8.3 Jailbreaks, guardrails & moderation | 2 | [Module 3](ai-security-deep-dive.md#module-3-jailbreaks-guardrails-and-moderation-m83) | Filter limits and layered controls |
| M8.4 Agent & tool security | 2 | [Module 4](ai-security-deep-dive.md#module-4-agent-and-tool-security-m84) | Least privilege, approvals and sandboxing |
| M8.5 RAG & knowledge security | 1 | [Module 5](ai-security-deep-dive.md#module-5-rag-and-knowledge-security-m85) | ACLs, document poisoning, provenance |
| M8.6 Data privacy, PII & secrets | 2 | [Module 6](ai-security-deep-dive.md#module-6-data-privacy-pii-and-secrets-m86) | Data minimization, logging, secret handling |
| M8.7 Red teaming | 2 | [Module 7](ai-security-deep-dive.md#module-7-red-teaming-ai-systems-m87) | Controlled attacks, scoring, incident triage |
| M8.8 Responsible AI & governance | 1 | [Module 8](ai-security-deep-dive.md#module-8-responsible-ai-and-governance-m88) | Ownership, documentation, oversight |
| M8.9 Capstone | 1 | [Module 9](ai-security-deep-dive.md#module-9-capstone-red-team-and-secure-an-agentic-rag-app-m89) | Build and test a secure local agentic RAG workflow |

**Total: 15 roadmap sessions across 9 modules.**

## One architecture to remember

~~~mermaid
flowchart LR
 A["User + authenticated identity"] --> B["Backend authorization"]
 B --> C["Tenant-scoped retrieval"]
 C --> D["LLM (untrusted decision maker)"]
 D --> E["Proposed tool call"]
 E --> F{"Server policy + user approval"}
 F -->|Deny| G["No action + safe audit"]
 F -->|Permit| H["Scoped execution"]
~~~

**Interview-first reading:** Modules **1 → 2 → 4 → 5 → 9**, then **3 → 6 → 7 → 8**. The main blog contains diagrams, worked attacks, comparisons, policy code, regression tests and interview answers.

## Primary sources

- [OWASP 2026 LLM Top 10](https://genai.owasp.org/resource/owasp-genai-llm-top-10-2026/)
- [OWASP 2026 Agentic Applications Top 10](https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/)
- [OWASP Prompt Injection Prevention](https://cheatsheetseries.owasp.org/cheatsheets/LLM_Prompt_Injection_Prevention_Cheat_Sheet.html)
- [OWASP AI Agent Security](https://cheatsheetseries.owasp.org/cheatsheets/AI_Agent_Security_Cheat_Sheet.html)
- [OWASP RAG Security](https://cheatsheetseries.owasp.org/cheatsheets/RAG_Security_Cheat_Sheet.html)
- [NIST Generative AI Risk Management Profile](https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-generative-artificial-intelligence)

*Original explanatory guide. Updated 2026-11-19. Guidance evolves; confirm standards and legal requirements for each deployment.*
