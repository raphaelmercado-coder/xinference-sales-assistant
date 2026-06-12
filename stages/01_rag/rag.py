"""
Stage 01 — RAG over the Xinference docs in data/kb/.
Run from the repo root:  python stages/01_rag/rag.py

Pipeline: embed KB -> cosine retrieve -> rerank -> generate grounded answer.
"""
import sys, os, glob
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

import numpy as np
from src.client import embed, rerank, chat

KB_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "data", "kb")


def load_chunks(path=KB_DIR):
    chunks = []
    for fp in sorted(glob.glob(os.path.join(path, "*.md"))):
        text = open(fp, encoding="utf-8").read()
        for para in (p.strip() for p in text.split("\n\n")):
            if len(para) > 40:  # skip headers / tiny fragments
                chunks.append({"source": os.path.basename(fp), "text": para})
    return chunks


def cosine(a, b):
    a, b = np.array(a), np.array(b)
    return float(a @ b / (np.linalg.norm(a) * np.linalg.norm(b) + 1e-9))


def build_index(chunks):
    vecs = embed([c["text"] for c in chunks])
    for c, v in zip(chunks, vecs):
        c["vec"] = v
    return chunks


def retrieve(query, index, k=8, top_n=3):
    qv = embed([query])[0]
    prelim = sorted(index, key=lambda c: cosine(qv, c["vec"]), reverse=True)[:k]
    rr = rerank(query, [c["text"] for c in prelim], top_n=top_n)
    return [prelim[item["index"]] for item in rr["results"]]


def answer(query, index):
    ctx = retrieve(query, index)
    context = "\n\n".join(f"[{c['source']}] {c['text']}" for c in ctx)
    resp = chat(messages=[
        {"role": "system", "content":
            "Answer using ONLY the provided context. Cite the source file in brackets. "
            "If the answer is not in the context, say you don't know."},
        {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {query}"},
    ], max_tokens=400)
    return resp.choices[0].message.content


if __name__ == "__main__":
    print("Indexing knowledge base...")
    index = build_index(load_chunks())
    print(f"Indexed {len(index)} chunks.\n")

    for q in [
        "What is the difference between Xinference and Ollama?",
        "How does Xinference handle many requests at once?",
        "What model types can Xinference serve?",
    ]:
        print("Q:", q)
        print(answer(q, index))
        print("-" * 60)
