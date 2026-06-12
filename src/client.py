"""
Shared client for talking to Xinference's OpenAI-compatible API.

Xinference exposes an OpenAI-compatible server at {endpoint}/v1, so the standard
`openai` SDK works by simply changing base_url. That single-line swap IS the
platform's headline value prop — this file is where you experience it.

Rerank is NOT part of the OpenAI spec, so it uses Xinference's own /v1/rerank
endpoint via a plain HTTP POST.
"""
import os
import requests
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

ENDPOINT = os.getenv("XINFERENCE_ENDPOINT", "http://localhost:9997").rstrip("/")
LLM_MODEL = os.getenv("LLM_MODEL", "qwen2.5-instruct")
EMBED_MODEL = os.getenv("EMBED_MODEL", "bge-base-en-v1.5")
RERANK_MODEL = os.getenv("RERANK_MODEL", "bge-reranker-base")


def get_client() -> OpenAI:
    # api_key is required by the SDK but unused by Xinference; any string works.
    return OpenAI(base_url=f"{ENDPOINT}/v1", api_key="not-needed")


def chat(messages, model=None, **kwargs):
    """Chat completion. Pass tools=/tool_choice= through kwargs for function calling."""
    return get_client().chat.completions.create(
        model=model or LLM_MODEL, messages=messages, **kwargs
    )


def embed(texts, model=None):
    """Return a list of embedding vectors for a list of strings."""
    if isinstance(texts, str):
        texts = [texts]
    resp = get_client().embeddings.create(model=model or EMBED_MODEL, input=texts)
    return [d.embedding for d in resp.data]


def rerank(query, documents, model=None, top_n=None):
    """Rerank documents against a query. Returns Xinference's rerank JSON:
    {"results": [{"index": int, "relevance_score": float}, ...]}"""
    payload = {"model": model or RERANK_MODEL, "query": query, "documents": documents}
    if top_n:
        payload["top_n"] = top_n
    r = requests.post(f"{ENDPOINT}/v1/rerank", json=payload, timeout=120)
    r.raise_for_status()
    return r.json()


def ping():
    """Sanity check: list the models currently served."""
    r = requests.get(f"{ENDPOINT}/v1/models", timeout=30)
    r.raise_for_status()
    return r.json()
