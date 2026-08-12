# Demo Video Script (~2.5 min)

**0:00–0:20 — The problem**
"Every time I open ChatGPT before a client meeting, it knows nothing about
that client. I have to re-explain everything — their concerns, what I
promised them, what we last talked about. That's the problem I'm solving:
an agent with real memory."

**0:20–0:50 — Show the seeded history**
Select "John (Acme Corp)" in the dropdown. Ask:
*"I have a meeting with John tomorrow, how should I prepare?"*
Let the answer render on screen — point out it's referencing security
concerns, pricing pushback, and the unsent SOC 2 report, none of which you
typed today. "This is all from meetings that happened weeks ago — the
agent remembered them using Hindsight."

**0:50–1:10 — Explain the mechanism (screen: architecture diagram or code)**
"Every meeting note gets stored with Hindsight's retain() call, into a
memory bank that belongs only to that client. When I ask a question, the
agent calls recall() to pull back just the relevant facts, then hands
those to the LLM to write a grounded, specific answer — not a generic
one."

**1:10–1:40 — Show the before/after live**
Log a brand new note: *"John finally agreed to the enterprise plan but
wants a 90-day pilot first."*
Ask the same prep question again. Show the new fact now appears alongside
the old history. "The agent didn't just add one fact — it's building a
running picture of the relationship."

**1:40–2:10 — Why this matters (real-world impact)**
"This isn't a toy. Anyone with recurring client relationships — sales,
consulting, account management, even therapists or teachers — needs an
assistant that remembers people, not just facts."

**2:10–2:30 — Close**
"Built with Flask, Groq, and Hindsight for memory. Repo link and live
demo are in the description."
