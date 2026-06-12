# Xinference Sales Assistant

> **In one breath:** a small AI assistant that answers questions from a set of docs and
> can call functions (e.g. look up pricing, book a demo). The AI models run on a **free
> cloud GPU** (Google Colab); this repo is the lightweight code on your laptop that
> talks to them over a standard API. **Status: works end-to-end** — see
> [`docs/demo-run.md`](docs/demo-run.md) for a real captured run.

A hands-on learning project: a RAG + tool-calling agent served entirely on
**Xinference**, built to learn the platform end-to-end (and double as technical-
homework practice for an AI Technical Sales Engineer role).

## The one thing to understand first: this project lives in two places

| Where | What runs there | RAM cost on your Mac |
|---|---|---|
| **Colab (GPU)** | Xinference + the models (LLM, embedding, reranker) | none |
| **VSCode (your Mac)** | This repo: the client app, RAG logic, tool defs, notes | trivial |

The heavy lifting (inference) happens on a free Colab GPU. Your machine only runs
lightweight client code that talks to Colab over Xinference's OpenAI-compatible API.
That mirrors exactly what the platform sells: **app on your infra, inference on a
server elsewhere.**

## Stages (ICM-style)

Each stage is a self-contained step with its own `CONTEXT.md` that records what it
teaches you and the interview line you earn by finishing it.

| Stage | Teaches | Run |
|---|---|---|
| `00_serve` | Deploy a model, swap GPT in one line | `python stages/00_serve/first_call.py` |
| `01_rag` | Multi-model serving (LLM + embed + rerank), RAG | `python stages/01_rag/rag.py` |
| `02_tools` | Function calling / the agent loop | `python stages/02_tools/tools.py` |
| `03_production` | Auto-batching, concurrency, tunnels | `python stages/03_production/load_test.py` |

## Quick start

1. **Serve the models** — open `notebooks/server.ipynb` in Google Colab, set the
   runtime to GPU, run all cells. It boots Xinference and launches three models.
   (Optionally start the ngrok tunnel cell to reach it from your Mac.)
2. **Wire the client** — copy `.env.example` to `.env` and set
   `XINFERENCE_ENDPOINT` to your Colab/ngrok URL (or `http://localhost:9997` if you
   run everything inside the notebook).
3. **Install local deps** — `pip install -r requirements.txt`
4. **Walk the stages** — run them in order. Read each `CONTEXT.md` first.

See `_config/setup.md` for the full wiring details.

## Why this project

Every stage maps to a capability a hiring manager will probe, and the whole arc is
POC-shaped: scope -> configure -> prove. By the end you can speak to deployment, the
OpenAI-compatible API, multi-model serving, embeddings/rerank, tool calling, and
auto-batching from direct experience — not theory.
