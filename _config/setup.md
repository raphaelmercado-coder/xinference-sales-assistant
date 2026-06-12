# Setup: wiring the two environments

This project splits across **Colab (serving)** and **your Mac (client)**. Here's how
to connect them.

## A. Serving side (Google Colab)

1. Upload `notebooks/server.ipynb` to https://colab.research.google.com (or open it
   from GitHub).
2. **Runtime -> Change runtime type -> GPU** (a free T4 is enough).
3. Run the cells top to bottom. They:
   - install `xinference[all]`
   - start the Xinference server on port 9997
   - launch three models: an LLM (`qwen2.5-instruct`), an embedding model
     (`bge-base-en-v1.5`), and a reranker (`bge-reranker-base`)
   - run a quick chat to confirm it's alive

Leave the notebook running. Colab free tiers idle out after a while; if it dies,
re-run the cells.

## B. Two ways to run the client

### Option 1 — everything inside the notebook (simplest, zero networking)
Paste the stage code into notebook cells and run there. The endpoint stays
`http://localhost:9997`. Good for first contact with the API.

### Option 2 — client on your Mac, server on Colab (the realistic setup)
You need to expose the Colab server to the internet with a tunnel.

1. Make a free account at https://ngrok.com and copy your authtoken.
2. In the notebook, run the **optional ngrok cell**, pasting your authtoken.
3. It prints a public URL like `https://abcd-1234.ngrok-free.app`.
4. On your Mac: `cp .env.example .env`, then set
   `XINFERENCE_ENDPOINT=https://abcd-1234.ngrok-free.app` (no trailing slash).
5. `pip install -r requirements.txt`
6. Run any stage: `python stages/00_serve/first_call.py`

This is the version worth doing once, because "client here, inference there, talking
over the OpenAI-compatible API" is the exact architecture you'd pitch to a customer.

## C. Sanity check

From your Mac (Option 2) or a notebook cell (Option 1):

```python
from src.client import ping
print(ping())   # should list qwen2.5-instruct, bge-base-en-v1.5, bge-reranker-base
```

## Notes

- Model names in `.env` must match exactly what the notebook launches.
- If a model fails to launch on the free T4 (out of memory), drop the LLM to a
  smaller size in the notebook (e.g. `qwen2.5-instruct` at 1.5B or 3B instead of 7B).
- Run stages from the repo root so `from src.client import ...` resolves.
