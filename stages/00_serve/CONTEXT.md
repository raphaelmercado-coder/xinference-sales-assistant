# Stage 00 — Serve a model, swap GPT in one line

## Goal
Prove you can deploy an open model on Xinference and call it through the standard
OpenAI SDK by changing only the base URL.

## What you do
1. Models are already launched by the notebook.
2. Run `python stages/00_serve/first_call.py` from the repo root.
3. Watch a reply come back from a model you are serving yourself.

## What this teaches
- Xinference exposes an **OpenAI-compatible** endpoint at `{endpoint}/v1`.
- Your existing OpenAI code works against it unchanged except for `base_url`.
- This is the literal "swap GPT for any LLM by changing a single line" claim — now
  something you've done, not read about.

## Interview line earned
"I've run open models through Xinference's OpenAI-compatible API. The drop-in
replacement is real — you point base_url at your own server and existing code just
works. For a customer already on the OpenAI SDK, migration is a config change, not a
rewrite."
