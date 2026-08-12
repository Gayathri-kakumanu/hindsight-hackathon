import os
from flask import Flask, request, jsonify, render_template
from hindsight_client import Hindsight
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# --- Hindsight: memory layer ---
hindsight = Hindsight(
    base_url=os.getenv("HINDSIGHT_URL", "http://localhost:8888"),
    api_key=os.getenv("HINDSIGHT_API_KEY"),  # required for Hindsight Cloud; unused for local Docker
)

# --- LLM: Groq (OpenAI-compatible endpoint) ---
llm = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1",
)
LLM_MODEL = os.getenv("LLM_MODEL", "openai/gpt-oss-120b")

# Each "client" gets its own isolated Hindsight memory bank.
CLIENTS = {
    "acme-john": "John (Acme Corp)",
    "globex-sara": "Sara (Globex)",
    "initech-raj": "Raj (Initech)",
}

_ensured_banks = set()


def ensure_bank(bank_id, name):
    """Create the memory bank once per process if it doesn't already exist."""
    if bank_id in _ensured_banks:
        return
    try:
        hindsight.banks.create(
            bank_id=bank_id,
            name=name,
            mission=(
                f"I track my colleague's relationship with {name}: their concerns, "
                "stated preferences, promises made to them, and what was discussed "
                "in each meeting, so I can brief my colleague before the next meeting."
            ),
        )
    except Exception:
        pass  # bank already exists - fine
    _ensured_banks.add(bank_id)


@app.route("/")
def home():
    return render_template("index.html", clients=CLIENTS)


@app.route("/api/log", methods=["POST"])
def log_note():
    """RETAIN: store a raw meeting note into that client's memory bank."""
    data = request.json
    bank_id = data["bank_id"]
    note = data["note"]
    ensure_bank(bank_id, CLIENTS.get(bank_id, bank_id))

    hindsight.retain(bank_id=bank_id, content=note, context="meeting note")
    return jsonify({"status": "stored"})


@app.route("/api/ask", methods=["POST"])
def ask():
    """RECALL + LLM: pull relevant memory, ground the LLM's answer in it."""
    data = request.json
    bank_id = data["bank_id"]
    question = data["question"]
    ensure_bank(bank_id, CLIENTS.get(bank_id, bank_id))

    recalled = hindsight.recall(bank_id=bank_id, query=question, max_tokens=2048)
    memory_lines = [r.text for r in recalled.results]
    memory_text = "\n".join(f"- {m}" for m in memory_lines) or "No prior memory for this client yet."

    prompt = f"""You are a personal meeting-prep assistant for a salesperson.
Use the MEMORY below (real facts from past meetings with this client) to answer
the QUESTION. Be specific: name concerns, promises made, and preferences from
memory. If memory is empty, say plainly this is the first interaction with
this client instead of inventing anything.

MEMORY:
{memory_text}

QUESTION: {question}

ANSWER:"""

    completion = llm.chat.completions.create(
        model=LLM_MODEL,
        messages=[{"role": "user", "content": prompt}],
    )
    answer = completion.choices[0].message.content

    # Retain this Q&A itself so the agent's own past answers become memory too.
    hindsight.retain(
        bank_id=bank_id,
        content=f"User asked: {question}. Agent answered: {answer}",
        context="agent interaction",
    )

    return jsonify({"answer": answer, "memories_used": memory_lines})


if __name__ == "__main__":
    app.run(debug=True, port=5000)
