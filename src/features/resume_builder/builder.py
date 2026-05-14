import os

from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

def generate_resume(
    name,
    email,
    phone,
    linkedin,
    github,
    location,
    education,
    skills,
    experience,
    projects,
    certifications,
    achievements
):

    prompt = f"""
You are an expert ATS resume writer.

Create a professional one-page resume.

ONLY use information provided by the user.
Do NOT create fake experience,
fake projects,
or fake achievements.

Candidate Information:

Name: {name}
Email: {email}
Phone: {phone}
LinkedIn: {linkedin}
GitHub: {github}
Location: {location}

Education:
{education}

Skills:
{skills}

Experience:
{experience}

Projects:
{projects}

Certifications:
{certifications}

Achievements:
{achievements}

Instructions:

- Make resume ATS friendly
- Keep formatting professional
- Use markdown formatting
- Use concise bullet points
- Keep resume clean and modern
- Omit empty sections
- Include ALL skill categories exactly as provided
- Do not invent information
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.7,
        max_tokens=2000
    )

    return response.choices[0].message.content