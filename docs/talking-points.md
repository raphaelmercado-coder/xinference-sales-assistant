# Talking Points — AI Technical Sales Engineer

A cheat sheet to speak to this build cold. The arc is POC-shaped: **scope → configure
→ prove.** Each stage maps to a capability a hiring manager will probe, and I've *done*
each one against a live server — not read about it.

## The 30-second pitch
> "I stood up an open model-serving platform (Xinference) on a GPU, then built a
> client-side RAG + tool-calling agent against it over the OpenAI-compatible API. The
> models run on the server; my app runs anywhere and talks to it with a one-line
> base_url change. That's the exact pattern a customer would deploy: app on their
> infra, inference managed elsewhere."

## The architecture in one breath
- **Server (Colab GPU):** Xinference serves an LLM, an embedding model, and a reranker
  — three model types, one platform, one API surface.
- **Client (my Mac):** standard OpenAI Python SDK, `base_url` pointed at the server.
- **Link:** ngrok tunnel — proves the client/server split, not just localhost.

---

## Stage-by-stage: what it proves + the line I earn

### 00 — Serve a model, swap GPT in one line
**Proves:** Xinference exposes an OpenAI-compatible endpoint at `{endpoint}/v1`;
existing OpenAI code works unchanged except `base_url`.
> "The drop-in replacement is real — you point base_url at your own server and existing
> code just works. For a customer already on the OpenAI SDK, migration is a config
> change, not a rewrite."

### 01 — Multi-model serving + RAG
**Proves:** LLM + embedding model + reranker all served by **one** Xinference instance,
composed into a retrieval pipeline that answers from a knowledge base with citations.
> "I built a RAG pipeline where the LLM, the embedding model, and the reranker were all
> served by one Xinference instance. That breadth is the separation from single-purpose
> tools — you stand up the whole retrieval stack on one platform instead of stitching
> three services together."

**Differentiator to name:** Ollama is LLM-focused; serving embeddings + rerankers from
the same layer is the concrete thing it doesn't do.

### 02 — Tool calling (the agent loop)
**Proves:** the model emits a structured tool call; my code executes it; the model
composes the final answer. It also correctly *declined* to call a tool for a
general-knowledge question.
> "The model emits the structured call, my code executes it and returns the result, and
> the model composes the final answer. The agent layer plans; the application acts.
> That distinction matters when a customer asks how much the agent does on its own."

**Honesty hook:** autonomy claims need a caveat — the platform emits the call; you own
execution and guardrails.

### 03 — Production signals: concurrency / auto-batching
**Proves:** the async client/server throughput pattern; the *concept* that a production
serving layer batches concurrent work.
> "The throughput layer is what separates a demo from production serving — it's exactly
> what an ops owner cares about when they ask 'will this hold up under real traffic?'"

**Be straight about the measurement:** on a free T4 + Transformers engine + free ngrok
tunnel, you won't see dramatic batching numbers. The real auto-batching story is
**vLLM on a larger GPU**. Knowing *why* — and not overselling a weak benchmark — is
itself a sales-engineer signal.

---

## Bonus talking point: the dependency-debugging war story
Getting the server up surfaced a real-world platform issue worth telling:
- Colab shipped **transformers 5.x**, which broke the build two ways: LLM generation
  (`'DynamicCache' object is not subscriptable`) and the embedder (`peft` importing the
  removed `HybridCache`).
- Fix: pin **transformers 4.56.0** (the highest 4.x — satisfies vLLM's floor, keeps the
  old cache API) and drop the unused **peft**. One coherent version set, both bugs gone.

**Why it lands in an interview:** SEs spend their lives in customer environments where
versions don't line up. "I read the actual tracebacks, found the version conflict, and
pinned a set the whole stack agreed on" is the exact muscle the job needs.

---

## Capabilities I can now speak to from direct experience
Deployment · OpenAI-compatible API & drop-in migration · multi-model serving ·
embeddings + rerank in a RAG stack · function calling / agent loop · async concurrency
& the auto-batching throughput story · real dependency troubleshooting in a GPU env.
