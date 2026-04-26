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

User Skills: {skills}
Preferred Location: {location}

Past Searches:
{history_text}

Task:
Suggest exactly 5 relevant internship opportunities based on the user's skills and preferred location.

IMPORTANT RULES:

1. Output exactly 5 lines only.
2. Each line must strictly follow this exact format:

Role Title at Company Name (Location) | Mode: Remote/Hybrid/Onsite | Compensation: Paid/Unpaid/Not Specified | Expected Stipend Range: ₹X-Y/month or Not Specified | Duration: 1 Month / 2 Months / 3 Months / 6 Months / Flexible

3. Do not skip any field.
4. Do not use bullet points, markdown, stars, explanations, headings, or extra text.
5. If any information is uncertain, write Not Specified.
6. Prioritize internships in the user's preferred location first.
7. If local opportunities are limited, include Remote or Hybrid roles.
8. Expected Stipend Range must be realistic and role-specific, based on common market standards.
9. Different internships should have different expected stipend ranges when appropriate.
10. Do not present stipend ranges as guaranteed official compensation.

Example Output:

1. Backend Developer Intern at Zoho (Pune) | Mode: Onsite | Compensation: Paid | Expected Stipend Range: ₹20k-30k/month | Duration: 6 Months
2. AI Research Intern at Infosys (Remote) | Mode: Remote | Compensation: Paid | Expected Stipend Range: ₹25k-40k/month | Duration: 3 Months
3. Data Analyst Intern at TCS (Mumbai) | Mode: Hybrid | Compensation: Paid | Expected Stipend Range: ₹15k-25k/month | Duration: 3 Months
4. Frontend Developer Intern at StartupHub (Bangalore) | Mode: Remote | Compensation: Paid | Expected Stipend Range: ₹10k-20k/month | Duration: Flexible
5. Machine Learning Intern at Wipro (Hyderabad) | Mode: Onsite | Compensation: Not Specified | Expected Stipend Range: Not Specified | Duration: 2 Months
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