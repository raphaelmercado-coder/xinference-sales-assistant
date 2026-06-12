# Xinference: Agents and Scaling

Xinference offers agent-native serving by integrating with Xagent, enabling dynamic
planning, tool use, and autonomous multi-step reasoning rather than static pipelines.
Xagent is an enterprise agent platform for building and running agents with planning,
memory, and tool use.

Tool use follows the OpenAI-compatible function-calling pattern. When the model
decides to use a tool, the response carries a tool_calls finish reason with the chosen
function and arguments. Xinference does not execute the function itself — the developer
runs it using the model's output and returns the result. The model plans; the
application acts.

For throughput and reliability, Xinference automatically batches multiple concurrent
requests together, which significantly improves throughput under load. It supports
distributed inference across workers and a shared KV cache across multiple replicas to
make serving more efficient at scale.

These production features — auto-batching, distributed inference, shared KV cache — are
the parts that matter once a deployment moves past a single user and has to hold up
under real concurrent traffic.
