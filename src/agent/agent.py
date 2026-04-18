import os
from dotenv import load_dotenv
from openai import OpenAI
from src.database.db import insert_search, get_recent_searches

# Load environment variables
load_dotenv()

# Initialize Mistral via OpenAI-compatible API
client = OpenAI(
    api_key=os.getenv("MISTRAL_API_KEY"),
    base_url="https://api.mistral.ai/v1"
)


def get_internship_suggestions(skills, location):

    #  Step 1: Fetch recent history (limit to avoid large prompt)
    history = get_recent_searches(limit=3)

    history_text = ""
    for h in history:
        history_text += f"Skills: {h.skills}, Location: {h.location}\n"

    #  Step 2: Build prompt
    prompt = f"""
    You are an AI internship assistant.

    Current User:
    Skills: {skills}
    Location: {location}

    Past Searches:
    {history_text}

    Suggest Exactly 5 internship roles for the user.

    Rules:
    - Only give role names with 1-line description
    - Do NOT include companies, tips, or extra text
    - Keep it short and clean
    - Focus only on India

    Format strictly like this:
    1. Role Name : Short Description
    2. Role Name : Short Description
    3. Role Name : Short Description
    4. Role Name : Short Description
    5. Role Name : Short Description
    """

    #  Step 3: Call LLM
    response = client.chat.completions.create(
        model="open-mistral-7b",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )

    output = response.choices[0].message.content

    #  step 4: clean response
    output = response.choices[0].message.content.strip()
    output = output.replace("**", "").strip()

     # Step 5: Store in database

    insert_search(skills, location, output)

    return output
