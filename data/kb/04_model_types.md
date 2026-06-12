# Xinference: Model Types and How It Compares

Xinference serves more than chat models. It supports large language models, embedding
models, rerank models, multimodal models, speech recognition, image generation, and
code completion — a range of model types under one serving layer.

This breadth is the main difference from Ollama. Ollama is a simple, single-machine
tool focused on running LLMs locally, excellent on a laptop. Xinference covers the
same core job but adds a wider model-type range, cluster and distributed serving, and
a management UI. It is heavier and more enterprise-leaning — think of it as Ollama's
larger, more industrial counterpart.

Compared with vLLM, the relationship is different. vLLM is a high-throughput serving
engine optimized for raw speed in production. Xinference trades some peak throughput
for manageability and multi-model support, and it can use vLLM-style optimizations
underneath. The honest summary: Xinference wins on breadth and manageability, not on
being the single fastest engine.

The closest direct competitor in positioning is LocalAI, which offers a similar
OpenAI-compatible, self-hosted, multi-model drop-in replacement.
