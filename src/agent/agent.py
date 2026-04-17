import os
from dotenv import load_dotenv
from openai import OpenAI

# Load env variables
load_dotenv()

# Initialize client (Mistral via OpenAI-compatible API)
client = OpenAI(
    api_key=os.getenv("MISTRAL_API_KEY"),
    base_url="https://api.mistral.ai/v1"
)

def get_internship_suggestions(skills, location):
    prompt = f"""
    Suggest Exactly 5 internship roles for a student  with skiils: {skills}
    preferred location: {location}.
    Focus only in India.

    Rules:
    -only gives role names with 1-line description of the role.
    -Do Not include companies, tips, explanations, or extra text
    -Keep it short and clean

    Format strictly like this:
    1. Role Name : Short Description
    2. Role Name : Short Description
    3. Role Name : Short Description
    4. Role Name : Short Description
    5. Role Name : Short Description
    """

    response = client.chat.completions.create(
        model="mistral-small",
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0.3
    )

    return response.choices[0].message.content
