# CLAUDE.md

Guidance for any AI agent working in this repo. Read this first.

## What this project is
A learning scaffold for the **Xinference** model-serving platform: a RAG +
tool-calling agent, built stage by stage. See `README.md` for the full picture.

## The one rule that matters most: this repo is CLIENT-ONLY
Models do **not** run here. They run on a **Google Colab GPU** (see
`notebooks/server.ipynb`). This repo holds only lightweight client code that talks to
that server over Xinference's OpenAI-compatible API.

- Do NOT `pip install xinference` locally or launch models on this machine.
- Do NOT suggest running a model on the user's Mac — the whole point is to keep
  inference off local RAM.
- All model calls go through `src/client.py`, which reads the endpoint from `.env`.

## Run convention
- Always run scripts from the **repo root** so `from src.client import ...` resolves.
- The endpoint and model names come from `.env` (copy `.env.example`). Never hardcode.
- Rerank uses Xinference's `/v1/rerank` endpoint, not the OpenAI spec — see
  `src/client.py`.

## Stage map (run in order)
| Stage | File | Teaches |
|---|---|---|
| `00_serve` | `stages/00_serve/first_call.py` | deploy + OpenAI-compatible API |
| `01_rag` | `stages/01_rag/rag.py` | multi-model serving + RAG |
| `02_tools` | `stages/02_tools/tools.py` | function calling / agent loop |
| `03_production` | `stages/03_production/load_test.py` | auto-batching / concurrency |

Each stage has a `CONTEXT.md` — read it before editing the stage.

## Gotchas
- Model names in `.env` must match Xinference's registry exactly, or launches fail.
- On a free Colab T4, the 7B LLM may OOM — drop to a smaller size in the notebook.
- These are environment/config issues, not code bugs; don't rewrite the code to
  "fix" them.
