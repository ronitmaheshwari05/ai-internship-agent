import os
from dotenv import load_dotenv
from openai import OpenAI
from src.database.db import (
    insert_search,
    get_recent_searches,
    get_cached_search
)

load_dotenv()

client = OpenAI(
    api_key=os.getenv("MISTRAL_API_KEY"),
    base_url="https://api.mistral.ai/v1"
)


def get_internship_suggestions(skills, location):

    # -------------------------------
    # Cache
    # -------------------------------
    cached = get_cached_search(skills, location)

    if cached:
        # ⚠️ IMPORTANT: still save it as new history
        try:
            new_id = insert_search(skills, location, cached["response"])
        except:
            new_id = cached["id"]

        return cached["response"], new_id

    # -------------------------------
    # History
    # -------------------------------
    history = get_recent_searches(limit=3)

    history_text = ""
    for h in history:
        history_text += f"Skills: {h['skills']}, Location: {h['location']}\n"

    # -------------------------------
    # Prompt
    # -------------------------------
    prompt = f"""
You are an AI internship assistant.

Skills: {skills}
Location: {location}

Past:
{history_text}

Give 5 internships in format:
Role at Company (Location) | Mode: Remote/Hybrid/Onsite | Compensation: Paid/Unpaid | Expected Stipend Range: ₹X-Y/month | Duration: X Months

No extra text.
"""

    # -------------------------------
    # AI Call
    # -------------------------------
    try:
        response = client.chat.completions.create(
            model="mistral-small-latest",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2
        )

        output = response.choices[0].message.content.strip()

    except:
        output = "Error generating results."

    # -------------------------------
    # Save
    # -------------------------------
    try:
        search_id = insert_search(skills, location, output)
    except:
        search_id = None

    return output, search_id