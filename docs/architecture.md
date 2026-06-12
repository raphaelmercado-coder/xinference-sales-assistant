# How this build works — in pictures

Three diagrams, in the order that makes the build click. Open this file in VS Code's
markdown **preview** (`Cmd+Shift+V`) — the diagrams render live. They also render on
GitHub.

---

## 1. The core idea: two machines, one API

The single most important thing to understand. Your laptop **never runs a model**. It
sends API requests to **Xinference**, which runs the models on a cloud GPU and sends
answers back.

```mermaid
flowchart LR
  subgraph LAPTOP["Your Laptop — this repo"]
    APP["stages/*.py<br/>(your app logic)"]
    CLIENT["src/client.py<br/>(OpenAI SDK)"]
    APP --> CLIENT
  end
  subgraph COLAB["Colab GPU"]
    XINF["XINFERENCE server<br/>(the product you're selling)"]
    LLM["qwen2.5-instruct<br/>LLM"]
    EMB["bge-base<br/>embeddings"]
    RER["bge-reranker<br/>rerank"]
    XINF --> LLM
    XINF --> EMB
    XINF --> RER
  end
  CLIENT -->|"OpenAI-compatible /v1 API<br/>over an ngrok tunnel"| XINF
```

**What it teaches:** Xinference *is* the server. It takes raw model files and turns them
into a callable API. One server is hosting three different model types at once — that
"multi-model serving" is a headline Xinference selling point. Your code is just a thin
client pointed at it.

---

## 2. RAG (Stage 01): how the three models cooperate

This is why Stage 01 answered accurately and *cited a source*, while Stage 00's bare LLM
just guessed. The embedder + reranker find the right documents; the LLM answers from
only those.

```mermaid
flowchart TD
  KB["data/kb/*.md<br/>(the knowledge base)"] --> EK["Embed every chunk<br/>(bge-base)"]
  Q["A question"] --> EQ["Embed the question<br/>(bge-base)"]
  EK --> RET["Retrieve top matches<br/>by cosine similarity<br/>(tiny math on your laptop)"]
  EQ --> RET
  RET --> RR["Rerank for precision<br/>(bge-reranker)"]
  RR --> GEN["LLM writes the answer<br/>from ONLY those chunks<br/>(qwen2.5) + cites the file"]
  GEN --> A["Grounded, cited answer"]
```

**What it teaches:** "RAG" = Retrieval-Augmented Generation. Instead of trusting the
LLM's memory, you *retrieve* relevant text first and make the LLM answer from it. All
three models are needed — and all three are served by the one Xinference instance.

---

## 3. Tool calling (Stage 02): the agent loop

How the assistant *does things* instead of just talking. The model decides which
function to call; **your code** runs it; the result goes back for a final answer.

```mermaid
sequenceDiagram
  participant U as User
  participant M as Model (via Xinference)
  participant App as Your code
  U->>M: "Book a demo for Raph on 2026-06-20" + tool definitions
  M-->>App: call book_demo(name=Raph, date=2026-06-20)
  Note over App: your app runs the real function<br/>(the model cannot run it itself)
  App-->>M: result — "Demo booked. Confirmation sent."
  M-->>U: "The demo is booked for Raph on June 20..."
```

**What it teaches:** the split between **deciding** (the model/agent plans) and
**acting** (your application executes). Xinference emits the structured call; you own
the execution and the guardrails. And when a question needs no tool ("capital of
France?"), the model just answers — it chooses.

---

## The arc in one line

`00 serve` → prove the API · `01 rag` → ground it in docs · `02 tools` → let it act ·
`03 scale` → test it under load. Each stage spotlights one Xinference capability.
