"""
Run once before the demo to pre-load 3 fake clients with a few meetings'
worth of history each. This is what makes the "wow" moment work -
the agent should already know things before you ever type into the UI.

Usage:
    python seed_data.py
"""
import os
from dotenv import load_dotenv
from hindsight_client import Hindsight

load_dotenv()

hindsight = Hindsight(
    base_url=os.getenv("HINDSIGHT_URL", "http://localhost:8888"),
    api_key=os.getenv("HINDSIGHT_API_KEY"),  # required for Hindsight Cloud; unused for local Docker
)

SEED = {
    "acme-john": {
        "name": "John (Acme Corp)",
        "mission": (
            "I track my colleague's relationship with John at Acme Corp: his "
            "concerns, preferences, promises made to him, and what was "
            "discussed in each meeting, so I can brief my colleague before "
            "the next meeting."
        ),
        "notes": [
            "Meeting 1 (6 weeks ago): John raised concerns about data security "
            "and asked detailed questions about our compliance certifications.",
            "Meeting 2 (4 weeks ago): John said the enterprise pricing tier "
            "felt too expensive compared to competitor X. He asked for a "
            "discount or a smaller starter tier.",
            "Meeting 3 (2 weeks ago): John asked specifically about SSO "
            "support and SOC 2 compliance. We promised to send him the SOC 2 "
            "report by end of week - this was not yet sent.",
        ],
    },
    "globex-sara": {
        "name": "Sara (Globex)",
        "mission": (
            "I track my colleague's relationship with Sara at Globex: her "
            "concerns, preferences, promises made to her, and what was "
            "discussed in each meeting, so I can brief my colleague before "
            "the next meeting."
        ),
        "notes": [
            "Meeting 1 (3 weeks ago): Sara is very focused on onboarding "
            "speed for her team - she has 40 people who need to be live "
            "within 2 weeks of signing.",
            "Meeting 2 (1 week ago): Sara loved the dashboard demo and asked "
            "for a custom analytics export feature. We promised to check "
            "with the product team and follow up.",
        ],
    },
    "initech-raj": {
        "name": "Raj (Initech)",
        "mission": (
            "I track my colleague's relationship with Raj at Initech: his "
            "concerns, preferences, promises made to him, and what was "
            "discussed in each meeting, so I can brief my colleague before "
            "the next meeting."
        ),
        "notes": [
            "Meeting 1 (5 weeks ago): Raj is the technical decision maker, "
            "very detail-oriented, wants API documentation and rate limit "
            "details before committing to anything.",
            "Meeting 2 (2 weeks ago): Raj tested the API and found the "
            "rate limits too low for his use case. He asked whether higher "
            "limits are available on a custom plan.",
        ],
    },
}


def main():
    for bank_id, info in SEED.items():
        print(f"Creating bank: {bank_id} ({info['name']})")
        try:
            hindsight.banks.create(
                bank_id=bank_id, name=info["name"], mission=info["mission"]
            )
        except Exception as e:
            print(f"  (bank may already exist: {e})")

        for note in info["notes"]:
            print(f"  Retaining: {note[:60]}...")
            hindsight.retain(bank_id=bank_id, content=note, context="meeting note")

    print("\nDone. Seeded 3 clients with realistic meeting history.")


if __name__ == "__main__":
    main()
