# Stage 03 — Production signals: auto-batching & concurrency

## Goal
See the throughput story firsthand by firing many requests at once and observing that
total time is far less than the sum of individual times — evidence the server is
batching concurrent requests.

## What you do
Run `python stages/03_production/load_test.py` from the repo root. It sends N
concurrent chat requests with the async OpenAI client and reports timing.

## What to look for
If `total_time` is much smaller than `sum(individual_latencies)`, the server handled
them in parallel rather than one-by-one. That's Xinference's **auto-batching**:
multiple concurrent requests are automatically grouped to improve throughput.

## What this teaches
- The difference between "it answers" (Stage 00) and "it serves under load" — the
  thing that actually matters for production and is the operations manager's concern.
- Why a managed/enterprise tier exists: throughput, distributed inference across
  workers, shared KV cache across replicas. Free tools can answer; production serving
  is about concurrency and reliability.

## Interview line earned
"I load-tested an Xinference deployment and watched auto-batching collapse concurrent
requests into far less wall-clock time than serial. That's the throughput layer that
separates a demo from production serving — and it's exactly what an ops owner cares
about when they ask 'will this hold up under real traffic?'"

## Stretch
- Try the ngrok tunnel (see `_config/setup.md`) so the client on your Mac hits the
  Colab server — the real client/server split you'd pitch.
- Bump N and watch how latency scales.
