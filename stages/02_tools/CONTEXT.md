# Stage 02 — Tool calling (the agent loop)

## Goal
Make the model decide to call a function, execute it yourself, and feed the result
back. This is the core agent mechanic.

## What you do
Run `python stages/02_tools/tools.py` from the repo root. It defines two tools
(`check_pricing`, `book_demo`), asks the model questions that require them, and
completes the loop.

## The loop
1. Send the user message **plus tool definitions** (JSON schema).
2. The model returns a `tool_calls` finish reason with the chosen function + arguments.
3. **Your code** runs the actual function (Xinference does not execute it for you).
4. Append the tool result and call the model again for a natural-language answer.

## The point that connects to your earlier question
The tool definitions MUST be JSON schema at the model boundary — that's the
OpenAI-compatible function-calling spec, not a Xinference choice. Markdown (your ICM
folders) is the human-authored source; JSON schema is the compiled artifact the model
consumes. Same architecture you reasoned about: author in markdown, generate schema,
serve the call.

## What this teaches
- The split between **deciding** (the model / agent layer plans) and **acting** (your
  application executes). Xinference's agent-native serving + Xagent live on the
  deciding side.
- Why "autonomy" claims need a caveat: the platform emits the call; you own execution
  and guardrails.

## Interview line earned
"I've built a tool-calling loop on Xinference. The model emits the structured call,
my code executes it and returns the result, and the model composes the final answer.
The agent layer plans; the application acts. That distinction matters when a customer
asks how much the agent does on its own."
