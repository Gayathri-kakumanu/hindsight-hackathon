# Meeting Memory Agent

An AI agent that remembers every past interaction with a client — their
concerns, preferences, and promises made — using **Hindsight** as its
memory layer, so it can brief you before your next meeting instead of
starting from zero every time.

## How it works

```
User logs a meeting note  ──▶  Hindsight retain()  ──▶  stored in that
                                                          client's memory bank

User asks "prep me for my
meeting with John"        ──▶  Hindsight recall()  ──▶  relevant memories
                                       │
                                       ▼
                                 Groq LLM (grounded in those memories)
                                       │
                                       ▼
                              Personalized, specific answer
```

Each client gets their own isolated Hindsight **memory bank**, so John's
history never bleeds into Sara's.

## Setup (do this first, ~5 min)

### 1. Start Hindsight locally (Docker)

```bash
export OPENAI_API_KEY=sk-xxx   # Hindsight uses this internally for consolidation
docker run -it --pull always --name hindsight --restart unless-stopped \
  -p 8888:8888 -p 9999:9999 \
  -e HINDSIGHT_API_LLM_API_KEY=$OPENAI_API_KEY \
  vectorize/hindsight
```

The API is now live at `http://localhost:8888` (dashboard at `:9999`).

> No Docker / no time? Sign up for the free Hindsight Cloud instead at
> https://ui.hindsight.vectorize.io/signup and set `HINDSIGHT_URL` to the
> URL it gives you.

### 2. Install Python deps

```bash
cd meeting-memory-agent
pip install -r requirements.txt
```

### 3. Configure environment

```bash
cp .env.example .env
# then edit .env and add your GROQ_API_KEY (free at https://console.groq.com)
```

### 4. Seed realistic demo data

```bash
python seed_data.py
```

This creates 3 fake clients (John/Acme, Sara/Globex, Raj/Initech), each
with 2-3 prior "meetings" already stored in memory.

### 5. Run the app

```bash
python app.py
```

Open http://localhost:5000

## Demo flow (this is your wow moment)

1. Select **John (Acme Corp)** in the dropdown.
2. Ask: *"I have a meeting with John tomorrow, how should I prepare?"*
   → The agent recalls his security concerns, pricing pushback, and the
   unsent SOC 2 report — **before you've typed anything about him today.**
3. Log a new note: *"John finally agreed to the enterprise plan but wants
   a 90-day pilot first."*
4. Ask the same prep question again → the answer now includes the new
   commitment, layered on top of the old history.

That before/after — generic assistant vs. one that actually knows the
relationship — is the entire pitch.

## Project structure

```
meeting-memory-agent/
├── app.py            # Flask backend: retain/recall wiring + LLM call
├── seed_data.py       # Pre-loads 3 fake clients with meeting history
├── templates/
│   └── index.html     # Single-page chat UI
├── requirements.txt
├── .env.example
└── README.md
```

## What to say about Hindsight in your submission

- **Retain**: every meeting note and every agent answer is retained into
  a per-client memory bank (`hindsight.retain(...)`).
- **Recall**: before answering, the agent runs `hindsight.recall(...)`
  against that client's bank to pull only relevant facts (TEMPR retrieval
  — semantic + keyword + graph + temporal).
- **Isolation**: each client is its own memory bank, so context never
  leaks between clients — a real requirement for a multi-client tool.
