"""
Stage 00 — first call.
Run from the repo root:  python stages/00_serve/first_call.py
"""
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from src.client import chat, ping


def main():
    print("Models currently served:")
    for m in ping().get("data", []):
        print("  -", m.get("id"))

    print("\nAsking the model a question...\n")
    resp = chat(
        messages=[
            {"role": "system", "content": "You are a concise assistant."},
            {"role": "user", "content": "In one sentence, what is Xinference?"},
        ],
        max_tokens=128,
    )
    print(resp.choices[0].message.content)


if __name__ == "__main__":
    main()
