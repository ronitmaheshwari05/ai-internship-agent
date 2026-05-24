import streamlit as st
import urllib.parse
from dotenv import load_dotenv

from src.agent.agent import get_internship_suggestions

from src.features.auth.auth import (
    signup,
    login
)

from src.features.resume_builder.builder import (
    generate_resume,
    generate_resume_html
)

from src.features.resume_builder.ats_score import (
    calculate_ats_score
)

from src.database.db import (
    get_recent_searches,
    delete_search,
    create_table,
    insert_search,
    get_cached_search
)

from src.evaluation.evaluator import evaluate_response

# =====================================================
# LOAD ENV + DB
# =====================================================
load_dotenv()
create_table()

# =====================================================
# PAGE CONFIG
# =====================================================
st.set_page_config(
    page_title="AI Internship Finder Agent",
    page_icon="🎯",
    layout="wide"
)

# =====================================================
# SESSION STATE
# =====================================================
if "skills" not in st.session_state:
    st.session_state.skills = ""

if "location" not in st.session_state:
    st.session_state.location = ""

if "ai_output" not in st.session_state:
    st.session_state.ai_output = ""

if "user" not in st.session_state:
    st.session_state.user = None

if "uid" not in st.session_state:
    st.session_state.uid = None

# =====================================================
# AUTHENTICATION
# =====================================================

st.sidebar.title("🔐 Authentication")

# =====================================================
# LOGGED IN USER
# =====================================================

if st.session_state.user:

    st.sidebar.success(
        f"Logged in as {st.session_state.user}"
    )

    if st.sidebar.button("Logout"):

        st.session_state.user = None
        st.session_state.uid = None

        st.rerun()

# =====================================================
# LOGIN / SIGNUP
# =====================================================

else:

    auth_mode = st.sidebar.selectbox(
        "Choose Mode",
        ["Login", "Signup"]
    )

    auth_email = st.sidebar.text_input(
        "Email"
    )

    auth_password = st.sidebar.text_input(
        "Password",
        type="password"
    )

    # =====================================================
    # SIGNUP
    # =====================================================

    if auth_mode == "Signup":

        if st.sidebar.button(
            "Create Account"
        ):

            result = signup(
                auth_email,
                auth_password
            )

            if isinstance(result, dict):

                st.sidebar.success(
                    "Account Created Successfully!"
                )

            else:

                st.sidebar.error(result)

    # =====================================================
    # LOGIN
    # =====================================================

    if auth_mode == "Login":

        if st.sidebar.button("Login"):

            result = login(
                auth_email,
                auth_password
            )

            if isinstance(result, dict):

                st.session_state.user = auth_email

                st.session_state.uid = result[
                    "localId"
                ]

                st.sidebar.success(
                    "Login Successful!"
                )

                st.rerun()

            else:

                st.sidebar.error(
                    "Invalid email or password"
                )

# =====================================================
# BLOCK APP IF NOT LOGGED IN
# =====================================================

if not st.session_state.user:

    st.warning(
        "Please login to access the AI Internship Finder Agent"
    )

    st.stop()

# =====================================================
# COLOR FUNCTIONS
# =====================================================
def get_mode_color(mode):

    mode = mode.lower()

    if mode == "remote":
        return "#22c55e"

    elif mode == "hybrid":
        return "#facc15"

    elif mode == "onsite":
        return "#3b82f6"

    return "#9ca3af"


def get_pay_color(pay):

    if pay.lower() == "paid":
        return "#1e3a8a"

    return "#9ca3af"

# =====================================================
# TITLE
# =====================================================
st.title("AI Internship Finder Agent")

st.caption(
    "AI Internship Recommendations + ATS Resume Builder"
)

# =====================================================
# INTERNSHIP FINDER
# =====================================================
st.header("AI Internship Suggestions")

# =====================================================
# INPUTS
# =====================================================
skills = st.text_input(
    "Enter your skills (comma separated):",
    value=st.session_state.skills
)

location = st.text_input(
    "Enter location:",
    value=st.session_state.location
)

mode_filter = st.selectbox(
    "Work Mode",
    ["All", "Remote", "Hybrid", "Onsite"]
)

# =====================================================
# SEARCH BUTTON
# =====================================================
if st.button("Find Internships"):

    if not skills.strip() or not location.strip():

        st.warning("Please enter both fields")

    else:

        skills_clean = skills.strip().lower()
        location_clean = location.strip().lower()

        st.session_state.skills = skills_clean
        st.session_state.location = location_clean

        cached = get_cached_search(
            skills_clean,
            location_clean
        )

        # =====================================================
        # CACHE
        # =====================================================
        if cached:

            st.session_state.ai_output = cached["response"]

        # =====================================================
        # API CALL
        # =====================================================
        else:

            with st.spinner(
                "Finding internships..."
            ):

                ai_output, _ = get_internship_suggestions(
                    skills_clean,
                    location_clean
                )

            st.session_state.ai_output = ai_output

            insert_search(
                skills_clean,
                location_clean,
                ai_output
            )

# =====================================================
# DEFAULT MESSAGE
# =====================================================
if not st.session_state.ai_output:

    st.info(
        "Enter skills and location to get internship suggestions"
    )

# =====================================================
# SHOW INTERNSHIPS
# =====================================================
if st.session_state.ai_output:

    st.subheader("Suggested Internships")

    shown = 0

    for role in st.session_state.ai_output.split("\n"):

        if not role.strip():
            continue

        parts = role.split("|")

        title = parts[0].strip()

        mode = (
            parts[1]
            .replace("Mode:", "")
            .strip()
            if len(parts) > 1
            else "N/A"
        )

        pay = (
            parts[2]
            .replace("Compensation:", "")
            .strip()
            if len(parts) > 2
            else "N/A"
        )

        stipend = (
            parts[3]
            .replace("Expected Stipend Range:", "")
            .strip()
            if len(parts) > 3
            else ""
        )

        duration = (
            parts[4]
            .replace("Duration:", "")
            .strip()
            if len(parts) > 4
            else ""
        )

        # =====================================================
        # FILTER
        # =====================================================
        if (
            mode_filter != "All"
            and mode.lower() != mode_filter.lower()
        ):
            continue

        shown += 1

        # =====================================================
        # CARD
        # =====================================================
        with st.container(border=True):

            st.markdown(f"### {title}")

            st.divider()

            col1, col2 = st.columns(2)

            # MODE
            col1.markdown(
                f"""
                <span style='
                    color:{get_mode_color(mode)};
                    font-weight:700;
                '>
                    {mode}
                </span>
                """,
                unsafe_allow_html=True
            )

            # PAY
            col2.markdown(
                f"""
                <span style='
                    color:{get_pay_color(pay)};
                    font-weight:700;
                '>
                    {pay}
                </span>
                """,
                unsafe_allow_html=True
            )

            # STIPEND
            if stipend:

                st.write(
                    f"Expected Stipend Range: {stipend}"
                )

            # DURATION
            if duration:

                st.write(
                    f"Duration: {duration}"
                )

            # CAREERS LINK
            company = (
                title.split(" at ")[-1]
                if " at " in title
                else "Company"
            )

            query = urllib.parse.quote(
                company + " careers"
            )

            st.link_button(
                "Careers Page",
                f"https://www.google.com/search?q={query}"
            )

    # =====================================================
    # NO RESULTS
    # =====================================================
    if shown == 0:

        st.warning(
            "No internships found for selected work mode"
        )

    # =====================================================
    # DISCLAIMER
    # =====================================================
    st.info(
        "These are AI-generated internship suggestions. "
        "Please visit official company career pages "
        "for accurate and latest openings."
    )

    # =====================================================
    # EVALUATION DASHBOARD
    # =====================================================
    report = evaluate_response(
        st.session_state.skills,
        st.session_state.location,
        st.session_state.ai_output
    )

    st.subheader("Evaluation Dashboard")

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Overall",
        f"{report['overall_score']}%"
    )

    col2.metric(
        "Skill Match",
        f"{report['skill_match']}%"
    )

    col3.metric(
        "Format",
        f"{report['format_accuracy']}%"
    )

    col4, col5, col6 = st.columns(3)

    col4.metric(
        "Location",
        f"{report['location_match']}%"
    )

    col5.metric(
        "Diversity",
        f"{report['diversity_score']}%"
    )

    col6.metric(
        "Count",
        f"{report['response_count']}%"
    )

    st.progress(
        int(report["overall_score"])
    )

# =====================================================
# RESUME BUILDER
# =====================================================
st.divider()

st.header("AI Resume Builder")

st.info(
    "Create ATS-friendly professional resumes "
    "with AI-powered resume generation."
)

# =====================================================
# PERSONAL INFORMATION
# =====================================================
st.subheader("Personal Information")

col1, col2 = st.columns(2)

with col1:

    name = st.text_input("Full Name")

    email = st.text_input("Email")

    phone = st.text_input("Phone Number")

with col2:

    resume_location = st.text_input("Location")

    linkedin = st.text_input("LinkedIn Profile")

    github = st.text_input("GitHub / Portfolio")

# =====================================================
# TARGET ROLE
# =====================================================
target_role = st.selectbox(
    "Target Internship Role",
    [
        "AI/ML Intern",
        "Software Engineering Intern",
        "Data Science Intern",
        "Backend Developer Intern",
        "Frontend Developer Intern",
        "Cloud Intern",
        "Cybersecurity Intern",
        "Finance Intern",
        "Marketing Intern",
        "HR Intern",
        "Business Analyst Intern"
    ]
)

# =====================================================
# EDUCATION
# =====================================================
education = st.text_area(
    "Education"
)

# =====================================================
# SKILLS
# =====================================================
resume_skills = st.text_area(
    "Skills"
)

# =====================================================
# EXPERIENCE
# =====================================================
experience = st.text_area(
    "Experience"
)

# =====================================================
# PROJECTS
# =====================================================
projects = st.text_area(
    "Projects"
)

# =====================================================
# CERTIFICATIONS
# =====================================================
certifications = st.text_area(
    "Certifications"
)

# =====================================================
# ACHIEVEMENTS
# =====================================================
achievements = st.text_area(
    "Achievements"
)

# =====================================================
# TEMPLATE SELECTION
# =====================================================
template_style = st.selectbox(
    "Resume Template",
    [
        "Modern Blue",
        "Minimal ATS",
        "Corporate Professional",
        "Overleaf Style"
    ]
)

# =====================================================
# LIVE PREVIEW
# =====================================================
st.subheader("Live Resume Preview")

preview_html = generate_resume_html(

    name=name,

    email=email,

    phone=phone,

    linkedin=linkedin,

    github=github,

    location=resume_location,

    education=education,

    skills=resume_skills,

    experience=experience,

    projects=projects,

    certifications=certifications,

    achievements=achievements,

    template_style=template_style
)

st.components.v1.html(
    preview_html,
    height=900,
    scrolling=True
)

# =====================================================
# GENERATE RESUME BUTTON
# =====================================================
if st.button("Generate Resume PDF"):

    if not name or not email:

        st.warning(
            "Please fill required fields"
        )

    else:

        with st.spinner(
            "Generating Professional Resume..."
        ):

            pdf_path = generate_resume(

                name=name,

                email=email,

                phone=phone,

                linkedin=linkedin,

                github=github,

                location=resume_location,

                education=education,

                skills=resume_skills,

                experience=experience,

                projects=projects,

                certifications=certifications,

                achievements=achievements,

                template_style=template_style
            )

        st.success(
            "Resume generated successfully!"
        )

        with open(pdf_path, "rb") as pdf_file:

            st.download_button(
                label="Download Resume PDF",
                data=pdf_file,
                file_name=f"{name}_resume.pdf",
                mime="application/pdf"
            )

        ats = calculate_ats_score(

            resume_text=
            resume_skills
            + " "
            + experience
            + " "
            + projects,

            target_role=target_role
        )

        st.subheader("ATS Resume Score")

        st.metric(
            "ATS Score",
            f"{ats['score']}%"
        )

        if ats["matched"]:

            st.success(
                "Matched Keywords: "
                + ", ".join(ats["matched"])
            )

        if ats["missing"]:

            st.warning(
                "Missing Keywords: "
                + ", ".join(ats["missing"])
            )

# =====================================================
# SIDEBAR HISTORY
# =====================================================
st.sidebar.title("Recent Searches")

history = get_recent_searches(limit=10)

unique = {}

for item in history:

    key = (
        item["skills"],
        item["location"]
    )

    if key not in unique:

        unique[key] = item

clean_history = list(unique.values())[:5]

if not clean_history:

    st.sidebar.write("No searches yet")

else:

    for item in clean_history:

        st.sidebar.markdown(
            f"Location: {item['location']}"
        )

        st.sidebar.caption(
            item["skills"]
        )

        col1, col2 = st.sidebar.columns([2, 1])

        if col1.button(
            "Open",
            key=f"open_{item['id']}"
        ):

            st.session_state.skills = item["skills"]

            st.session_state.location = item["location"]

            st.session_state.ai_output = item["response"]

        if col2.button(
            "Delete",
            key=f"delete_{item['id']}"
        ):

            delete_search(item["id"])

            st.rerun()

        st.sidebar.divider()