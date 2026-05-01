import streamlit as st
import re
import urllib.parse
from src.agent.agent import get_internship_suggestions
from src.database.db import create_table, delete_search, get_recent_searches
from src.evaluation.evaluator import evaluate_response

# ------------------------------------------------
# Create DB Table
# ------------------------------------------------
create_table()

# ------------------------------------------------
# Page Config
# ------------------------------------------------
st.set_page_config(
    page_title="AI Internship Finder",
    page_icon="🎯",
    layout="centered"
)

# ------------------------------------------------
# Session State Defaults
# ------------------------------------------------
defaults = {
    "skills": "",
    "location": "",
    "saved_output": "",
    "selected_search_id": None,
    "mode_filter": "All",
    "pay_filter": "All"
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


# ------------------------------------------------
# Helper Functions
# ------------------------------------------------
def parse_role(role):
    role = re.sub(r"^\d+\.\s*", "", role.strip())
    parts = role.split("|")

    role_title = parts[0].strip()

    mode = "Not Specified"
    pay = "Not Specified"
    stipend = "Not Specified"
    duration = "Not Specified"

    if len(parts) > 1:
        mode = parts[1].replace("Mode:", "").strip()

    if len(parts) > 2:
        pay = parts[2].replace("Compensation:", "").strip()

    if len(parts) > 3:
        stipend = parts[3].replace("Expected Stipend Range:", "").strip()

    if len(parts) > 4:
        duration = parts[4].replace("Duration:", "").strip()

    return role_title, mode, pay, stipend, duration


def badge_color(mode):
    mode = mode.lower()

    if mode == "remote":
        return "#22c55e"
    if mode == "hybrid":
        return "#facc15"
    if mode == "onsite":
        return "#3b82f6"

    return "#9ca3af"


def display_roles(output):
    roles = output.split("\n")

    for role in roles:
        role = role.strip()
        if not role:
            continue

        role_title, mode, pay, stipend, duration = parse_role(role)

        # Filters
        if st.session_state.mode_filter != "All":
            if mode.lower() != st.session_state.mode_filter.lower():
                continue

        if st.session_state.pay_filter != "All":
            if pay.lower() != st.session_state.pay_filter.lower():
                continue

        mode_color = badge_color(mode)

        with st.container(border=True):

            st.markdown(f"### {role_title}")

            col1, col2 = st.columns([1, 1])

            with col1:
                st.markdown(
                    f"""
<span style="background:#1f2937;color:{mode_color};padding:6px 10px;border-radius:8px;font-size:13px;font-weight:600;">
{mode}
</span>
""",
                    unsafe_allow_html=True
                )

            with col2:
                st.markdown(
                    f"""
<span style="background:#1f2937;color:#22c55e;padding:6px 10px;border-radius:8px;font-size:13px;font-weight:600;">
{pay}
</span>
""",
                    unsafe_allow_html=True
                )

            st.markdown(f"💰 **{stipend}**")
            st.markdown(f"⏱ **{duration}**")

            # -------------------------------
            # NEW: Careers + Search Buttons
            # -------------------------------

            company_name = "Unknown"

            if " at " in role_title:
                company_part = role_title.split(" at ")[-1]
                company_name = company_part.split("(")[0].strip()

            company_query = urllib.parse.quote(company_name + " careers")
            role_query = urllib.parse.quote(role_title + " internship")

            st.markdown(
                f"[🏢 Open {company_name} Careers Page](https://www.google.com/search?q={company_query})"
            )

            st.write("")


def show_dashboard(skills, location, output):
    report = evaluate_response(skills, location, output)

    st.subheader("Evaluation Dashboard")

    c1, c2, c3 = st.columns(3)

    with c1:
        st.metric("Overall Score", f"{report['overall_score']}%")

    with c2:
        st.metric("Skill Match", f"{report['skill_match']}%")

    with c3:
        st.metric("Format Accuracy", f"{report['format_accuracy']}%")

    c4, c5, c6 = st.columns(3)

    with c4:
        st.metric("Location Match", f"{report['location_match']}%")

    with c5:
        st.metric("Diversity", f"{report['diversity_score']}%")

    with c6:
        st.metric("Response Count", f"{report['response_count']}%")

    st.progress(int(report["overall_score"]))


# ------------------------------------------------
# UI
# ------------------------------------------------
st.title("🎯 AI Internship Finder")

st.sidebar.title("Filters")

st.session_state.mode_filter = st.sidebar.selectbox(
    "Work Mode",
    ["All", "Remote", "Hybrid", "Onsite"]
)

st.session_state.pay_filter = st.sidebar.selectbox(
    "Compensation",
    ["All", "Paid", "Unpaid", "Not Specified"]
)

st.sidebar.divider()

# Sidebar history
st.sidebar.title("Recent Searches")

history = get_recent_searches(limit=5)

for item in history:

    st.sidebar.markdown(f"### 📍 {item['location']}")
    st.sidebar.caption(item["skills"])

    col1, col2 = st.sidebar.columns([3, 1])

    with col1:
        if st.button(f"Open {item['id']}", key=f"load_{item['id']}"):
            st.session_state.skills = item["skills"]
            st.session_state.location = item["location"]
            st.session_state.saved_output = item["response"]
            st.session_state.selected_search_id = item["id"]
            st.rerun()

    with col2:
        if st.button("🗑", key=f"delete_{item['id']}"):
            delete_search(item["id"])
            st.rerun()

# Inputs
skills = st.text_input("Enter your skills:", value=st.session_state.skills)
location = st.text_input("Enter location:", value=st.session_state.location)

# Show results
if st.session_state.saved_output:

    display_roles(st.session_state.saved_output)

    st.info("These are AI-generated suggestions. Visit official company careers pages to apply.")

    show_dashboard(skills, location, st.session_state.saved_output)

# Search button
if st.button("Find Internships"):

    suggestions, search_id = get_internship_suggestions(skills, location)

    st.session_state.saved_output = suggestions
    st.session_state.selected_search_id = search_id

    st.rerun()
