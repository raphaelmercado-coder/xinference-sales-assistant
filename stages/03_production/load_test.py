"""
Stage 03 — concurrency / auto-batching demo.
Run from the repo root:  python stages/03_production/load_test.py
"""
import sys, os, time, asyncio
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from dotenv import load_dotenv
from openai import AsyncOpenAI

load_dotenv()
ENDPOINT = os.getenv("XINFERENCE_ENDPOINT", "http://localhost:9997").rstrip("/")
LLM_MODEL = os.getenv("LLM_MODEL", "qwen2.5-instruct")


async def one_request(client, i):
    t0 = time.time()
    await client.chat.completions.create(
        model=LLM_MODEL,
        messages=[{"role": "user", "content": f"Write one short sentence about the number {i}."}],
        max_tokens=48,
    )
    return time.time() - t0


async def main(n=10):
    client = AsyncOpenAI(base_url=f"{ENDPOINT}/v1", api_key="not-needed")
    print(f"Firing {n} concurrent requests at {ENDPOINT} ...")
    t0 = time.time()
    latencies = await asyncio.gather(*[one_request(client, i) for i in range(n)])
    total = time.time() - t0
    serial = sum(latencies)
    print(f"\nWall-clock total : {total:.1f}s")
    print(f"Sum of latencies : {serial:.1f}s")
    print(f"Speedup vs serial: {serial / total:.1f}x")
    print("\nIf the speedup is well above 1x, the server is batching concurrent "
          "requests rather than handling them one at a time.")


if __name__ == "__main__":
    asyncio.run(main())
