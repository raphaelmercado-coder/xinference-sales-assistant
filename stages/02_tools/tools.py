"""
Stage 02 — tool calling.
Run from the repo root:  python stages/02_tools/tools.py
"""
import sys, os, json
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from src.client import chat


# --- the actual functions (your application code) ---
def check_pricing(edition: str) -> str:
    table = {
        "community": "Community Edition: free, open-source, self-hosted.",
        "enterprise": "Enterprise: custom pricing; adds SLA, support, advanced ops. Contact sales.",
    }
    return table.get(edition.lower(), f"Unknown edition: {edition}")


def book_demo(name: str, date: str) -> str:
    return f"Demo booked for {name} on {date}. Confirmation email sent."


REGISTRY = {"check_pricing": check_pricing, "book_demo": book_demo}

# --- tool definitions the model sees (JSON schema, OpenAI-compatible) ---
TOOLS = [
    {"type": "function", "function": {
        "name": "check_pricing",
        "description": "Look up pricing for a Xinference edition.",
        "parameters": {"type": "object", "properties": {
            "edition": {"type": "string", "enum": ["community", "enterprise"]}},
            "required": ["edition"]}}},
    {"type": "function", "function": {
        "name": "book_demo",
        "description": "Book a product demo for a prospect.",
        "parameters": {"type": "object", "properties": {
            "name": {"type": "string"},
            "date": {"type": "string", "description": "YYYY-MM-DD"}},
            "required": ["name", "date"]}}},
]


def run(user_msg: str) -> str:
    messages = [{"role": "user", "content": user_msg}]
    first = chat(messages=messages, tools=TOOLS, tool_choice="auto", max_tokens=256)
    msg = first.choices[0].message

    if not msg.tool_calls:
        return msg.content  # model chose to just answer

    # echo the assistant's tool-call message back into the history
    messages.append({
        "role": "assistant",
        "content": msg.content or "",
        "tool_calls": [tc.model_dump() for tc in msg.tool_calls],
    })

    # execute each call (this is YOUR code, not the model's)
    for tc in msg.tool_calls:
        fn = REGISTRY[tc.function.name]
        args = json.loads(tc.function.arguments)
        result = fn(**args)
        print(f"  [tool] {tc.function.name}({args}) -> {result}")
        messages.append({"role": "tool", "tool_call_id": tc.id, "content": str(result)})

    final = chat(messages=messages, max_tokens=256)
    return final.choices[0].message.content


if __name__ == "__main__":
    for q in [
        "How much does the enterprise edition cost?",
        "Book a demo for Raph on 2026-06-20.",
        "What's the capital of France?",  # no tool needed; model should just answer
    ]:
        print("USER:", q)
        print("BOT :", run(q))
        print("-" * 60)
