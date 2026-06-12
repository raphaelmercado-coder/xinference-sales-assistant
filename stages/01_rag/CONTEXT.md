# Stage 01 — Multi-model serving + RAG

## Goal
Serve three model types from one platform (LLM + embedding + reranker) and use them
together to answer questions grounded in a knowledge base — Xinference's own docs,
stored in `data/kb/`.

## What you do
1. The notebook already launched the embedding and rerank models.
2. Run `python stages/01_rag/rag.py` from the repo root.
3. It chunks the KB, embeds it, retrieves + reranks for a query, and answers from
   only the retrieved context.

## The pipeline
- **Embed** every KB chunk (Xinference embedding model).
- **Retrieve** the top-k chunks by cosine similarity to the query.
- **Rerank** those with the reranker for precision (Xinference rerank endpoint).
- **Generate** an answer from the reranked context (the LLM).

All three models run on the same Colab GPU under one Xinference server. The vector
math is trivial and runs locally — no RAM strain.

## What this teaches
- Xinference serves LLMs, embeddings, and rerankers from **one** layer. This is the
  concrete thing Ollama does not do — it's LLM-focused. The multi-model breadth is a
  real differentiator you can now demonstrate.
- A production RAG stack needs all three; here it's three `launch` calls, not three
  separate services to wire up.

## Interview line earned
"I built a RAG pipeline where the LLM, the embedding model, and the reranker were all
served by one Xinference instance. That breadth is the separation from single-purpose
tools — you stand up the whole retrieval stack on one platform instead of stitching
three services together."
