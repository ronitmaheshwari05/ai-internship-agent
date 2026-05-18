import os

from groq import Groq
from dotenv import load_dotenv

from jinja2 import (
    Environment,
    FileSystemLoader
)

from src.features.resume_builder.pdf_generator import generate_pdf

# =====================================================
# LOAD ENV
# =====================================================
load_dotenv()

# =====================================================
# GROQ CLIENT
# =====================================================
client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

# =====================================================
# TEMPLATE ENGINE
# =====================================================
env = Environment(
    loader=FileSystemLoader(
        "src/features/resume_builder/templates"
    )
)

# =====================================================
# TEMPLATE MAP
# =====================================================
template_map = {

    "Modern Blue": "modern.html",

    "Minimal ATS": "minimal.html",

    "Overleaf Style": "overleaf.html",

    "Corporate Professional": "modern.html"
}

# =====================================================
# GENERATE RESUME HTML
# =====================================================
def generate_resume_html(

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
    achievements,
    template_style
):

    selected_template = template_map.get(
        template_style,
        "modern.html"
    )

    template = env.get_template(
        selected_template
    )

    html_content = template.render(

        name=name,

        email=email,

        phone=phone,

        linkedin=linkedin,

        github=github,

        location=location,

        education=education,

        skills=skills,

        experience=experience,

        projects=projects,

        certifications=certifications,

        achievements=achievements
    )

    return html_content

# =====================================================
# GENERATE RESUME PDF
# =====================================================
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
    achievements,
    template_style
):

    # =====================================================
    # AI PROMPT
    # =====================================================
    prompt = f"""
You are an expert ATS resume writer.

Create a professional ATS-friendly resume.

ONLY use information provided by the user.

Do NOT:
- create fake experience
- create fake projects
- create fake companies
- create fake achievements

Improve wording professionally.

Keep formatting:
- concise
- modern
- professional

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
"""

    # =====================================================
    # GROQ API CALL
    # =====================================================
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

    # =====================================================
    # AI OUTPUT
    # =====================================================
    ai_resume = response.choices[0].message.content

    # =====================================================
    # TEMPLATE
    # =====================================================
    selected_template = template_map.get(
        template_style,
        "modern.html"
    )

    template = env.get_template(
        selected_template
    )

    # =====================================================
    # HTML RENDERING
    # =====================================================
    html_content = template.render(

        name=name,

        email=email,

        phone=phone,

        linkedin=linkedin,

        github=github,

        location=location,

        education=education,

        skills=skills,

        experience=experience,

        projects=projects,

        certifications=certifications,

        achievements=achievements,

        ai_resume=ai_resume
    )

    # =====================================================
    # OUTPUT PATH
    # =====================================================
    output_dir = "generated_resumes"

    os.makedirs(
        output_dir,
        exist_ok=True
    )

    safe_name = (
        name
        .replace(" ", "_")
        .lower()
    )

    output_path = (
        f"{output_dir}/{safe_name}_resume.pdf"
    )

    # =====================================================
    # GENERATE PDF
    # =====================================================
    generate_pdf(
        html_content,
        output_path
    )

    # =====================================================
    # RETURN PDF PATH
    # =====================================================
    return output_path