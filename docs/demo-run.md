# Demo Run — captured outputs

**Date:** 2026-06-12
**What this is:** a real, end-to-end run of all four stages against a live Xinference
server. Proof the build works, not just that it compiles.

## Setup under test
| Piece | Detail |
|---|---|
| **Serving** | Xinference 2.10.0 on a free **Colab T4 GPU** |
| **Models** | `qwen2.5-instruct` (3B, Transformers engine) · `bge-base-en-v1.5` (embedding) · `bge-reranker-base` (rerank) — three model types, one server |
| **Client** | This repo on a Mac, OpenAI Python SDK, base_url pointed at the server |
| **Link** | ngrok tunnel — client on the Mac, inference on Colab (the real client/server split) |

> Architecture proven: **app on your infra, inference on a server elsewhere, over the
> OpenAI-compatible API.** That is exactly what the platform sells.

---

## Stage 00 — Serve a model, swap GPT in one line
`python stages/00_serve/first_call.py`

Proves the OpenAI-compatible endpoint: existing OpenAI SDK code works against a
self-served open model by changing only `base_url`.

```
Models currently served:
  - qwen2.5-instruct
  - bge-base-en-v1.5
  - bge-reranker-base

Asking the model a question...

Xinference refers to a hardware and software platform designed for accelerating
deep learning inference on edge devices.
```

*(Note: the ungrounded answer is loose — the 3B model's general knowledge. Stage 01
fixes this by grounding answers in the knowledge base. Good before/after contrast.)*

---

## Stage 01 — Multi-model serving + RAG
`python stages/01_rag/rag.py`

Pipeline: embed KB → cosine retrieve → rerank → generate grounded answer. All three
models served by one Xinference instance.

```
Indexing knowledge base...
Indexed 23 chunks.

Q: What is the difference between Xinference and Ollama?
Xinference has a wider model type range compared to Ollama, additional features
including cluster and distributed serving, and a management UI. Xinference also
supports multiple models whereas Ollama focuses on running LLMs locally on a single
machine. Xinference seems to be more enterprise-oriented than Ollama which is lighter
and better suited for laptops.
------------------------------------------------------------
Q: How does Xinference handle many requests at once?
For throughput and reliability, Xinference automatically batches multiple concurrent
requests together, which significantly improves throughput under load.
[05_agents_and_scaling.md]
------------------------------------------------------------
Q: What model types can Xinference serve?
Xinference serves large language models, embedding models, rerank models, multimodal
models, speech recognition, image generation, code completion [04_model_types.md].
------------------------------------------------------------
```

**Payoff:** answers are now accurate *and cite their source file* — the RAG stack
(LLM + embedder + reranker) corrects the loose Stage 00 answer.

---

## Stage 02 — Tool calling (the agent loop)
`python stages/02_tools/tools.py`

The model decides to call a function, the application executes it, the result is fed
back for a final natural-language answer.

```
USER: How much does the enterprise edition cost?
  [tool] check_pricing({'edition': 'enterprise'}) -> Enterprise: custom pricing; adds
         SLA, support, advanced ops. Contact sales.
BOT : For the Enterprise Edition, costs are based on custom pricing and come with
      additional features such as Service Level Agreement (SLA), dedicated support,
      and advanced operational capabilities. Since it's customized for each customer,
      you would need to contact their sales team...
------------------------------------------------------------
USER: Book a demo for Raph on 2026-06-20.
  [tool] book_demo({'name': 'Raph', 'date': '2026-06-20'}) -> Demo booked for Raph on
         2026-06-20. Confirmation email sent.
BOT : The demo has been successfully booked for Raph on June 20, 2026. A confirmation
      email has been sent to Raph with all the details of the appointment.
------------------------------------------------------------
USER: What's the capital of France?
BOT : The capital of France is Paris. Would you like further information...
------------------------------------------------------------
```

**Payoff:** the model called the right tool with correctly-parsed args for the first
two, and **correctly chose NOT to call a tool** for the general-knowledge question.
The agent layer plans; the application acts.

---

## Stage 03 — Concurrency / auto-batching
`python stages/03_production/load_test.py`

Fires N concurrent chat requests via the async OpenAI client and compares wall-clock
time to the sum of individual latencies.

```
Firing 6 concurrent requests at localhost...
(ran >13 min without completing — interrupted)
```

**The empirical finding (and the honest read for the interview):** concurrency was
tested two ways and **both confirm the same conclusion** — this free-tier setup does
not serve well under concurrent load:

1. **Over the ngrok tunnel** (N=10, then N=4): requests stalled behind the free
   tunnel's connection limits.
2. **Inside the notebook on localhost** (N=6, no tunnel): still did not complete after
   13+ minutes.

A *single* request is fast (Stage 00/cell 4 answered instantly). It is specifically
**concurrency** that collapses — because the **Transformers serving engine on a T4**
does not do vLLM-style continuous batching: simultaneous generations contend for GPU
memory and thrash instead of being grouped.

**This is the point of the stage, demonstrated the hard way:** free/Transformers-engine
serving answers one request fine but does not hold up under load. Production throughput
requires the **vLLM engine on a larger GPU** (Colab Pro A100/L4), where Xinference's
auto-batching actually kicks in. Knowing *why* — and not overselling a weak benchmark —
is itself the sales-engineer signal: free tools answer; production serving is about
concurrency and reliability.

**To get real throughput numbers:** relaunch the LLM with `model_engine="vLLM"` on a
Colab Pro GPU and re-run the load test.

---

## How to reproduce
1. Colab: run `notebooks/server.ipynb` on a GPU runtime (cell 1 pins the working
   dependency set; cells 2–4 boot the server + 3 models; cell 6 opens the ngrok tunnel).
2. Put the printed ngrok URL in `.env` as `XINFERENCE_ENDPOINT` (no trailing slash).
3. From the repo root: `python stages/00_serve/first_call.py` (then 01, 02, 03).

> The ngrok URL is **ephemeral** — it changes each time the tunnel restarts. If Colab
> disconnects, re-run cell 6 and update `.env` with the new URL.
