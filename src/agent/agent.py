import os
from dotenv import load_dotenv
from openai import OpenAI
from src.database.db import (
    insert_search,
    get_recent_searches,
    get_cached_search
)

# -------------------------------
# Load Environment Variables
# -------------------------------
load_dotenv()

# -------------------------------
# Initialize Mistral Client
# -------------------------------
client = OpenAI(
    api_key=os.getenv("MISTRAL_API_KEY"),
    base_url="https://api.mistral.ai/v1"
)


# -------------------------------
# Main Function
# -------------------------------
def get_internship_suggestions(skills, location):

    # -------------------------------
    # Step 1: Check Cache First
    # -------------------------------
    cached = get_cached_search(skills, location)

    if cached:
        return cached.response, cached.id

    # -------------------------------
    # Step 2: Load Recent Searches
    # -------------------------------
    history = get_recent_searches(limit=3)

    history_text = ""

    for h in history:
        history_text += f"Skills: {h.skills}, Location: {h.location}\n"

    # -------------------------------
    # Step 3: Build Prompt
    # -------------------------------
    prompt = f"""
You are an AI internship recommendation assistant.

Current User:
Skills: {skills}
Preferred Location: {location}

Past Searches:
{history_text}

Task:
Suggest exactly 5 relevant internship opportunities based on the user's skills and preferred location.

Rules:
1. Prioritize internships in the user's preferred location.
2. If suitable local roles are limited, include Remote or Hybrid opportunities.
3. Suggestions may include global companies, but relevance to user skills is mandatory.
4. Keep results short, clean, and professional.
5. Do NOT use markdown symbols, bold text, bullets, or extra commentary.
6. Mention whether the internship is Paid, Unpaid, or Not Specified.
7. Mention work mode as Remote, Onsite, or Hybrid.

Format strictly like this:

1. Internship Title at Company Name (Location) | Mode: Remote/Onsite/Hybrid | Compensation: Paid/Unpaid/Not Specified
2. Internship Title at Company Name (Location) | Mode: Remote/Onsite/Hybrid | Compensation: Paid/Unpaid/Not Specified
3. Internship Title at Company Name (Location) | Mode: Remote/Onsite/Hybrid | Compensation: Paid/Unpaid/Not Specified
4. Internship Title at Company Name (Location) | Mode: Remote/Onsite/Hybrid | Compensation: Paid/Unpaid/Not Specified
5. Internship Title at Company Name (Location) | Mode: Remote/Onsite/Hybrid | Compensation: Paid/Unpaid/Not Specified
"""

    # -------------------------------
    # Step 4: Call Mistral API
    # -------------------------------
    response = client.chat.completions.create(
        model="open-mistral-7b",
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0.3
    )

    # -------------------------------
    # Step 5: Clean Output
    # -------------------------------
    output = response.choices[0].message.content.strip()

    output = output.replace("**", "")
    output = output.replace("*", "")
    output = output.strip()

    # -------------------------------
    # Step 6: Save to Database
    # -------------------------------
    search_id = insert_search(skills, location, output)

    return output, search_id