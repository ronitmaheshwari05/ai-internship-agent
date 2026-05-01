import streamlit as st
import re
import urllib.parse
import time
from dotenv import load_dotenv

from src.agent.agent import get_internship_suggestions
from src.database.db import (
    delete_search,
    get_recent_searches,
    create_table
)
from src.evaluation.evaluator import evaluate_response

# -------------------------------
# Load ENV
# -------------------------------
load_dotenv()

# -------------------------------
# INIT DB
# -------------------------------
create_table()

# -------------------------------
# Page Config
# -------------------------------
st.set_page_config(
    page_title="AI Internship Finder",
    page_icon="🎯",
    layout="centered"
)

# -------------------------------
# SESSION DEFAULTS
# -------------------------------
defaults = {
    "skills": "",
    "location": "",
    "saved_output": "",
    "mode_filter": "All",
    "pay_filter": "All",
    "selected_id": None,
    "history": [],
    "last_refresh": time.time()
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value

# -------------------------------
# AUTO REFRESH (EVERY 5 SEC)
# -------------------------------
if time.time() - st.session_state.last_refresh > 5:
    st.session_state.history = get_recent_searches(limit=5)
    st.session_state.last_refresh = time.time()

# First load
if not st.session_state.history:
    st.session_state.history = get_recent_searches(limit=5)

# -------------------------------
# ENTER KEY FIX
# -------------------------------
st.markdown("""
<script>
document.addEventListener('keydown', function(e) {
  if (e.key === 'Enter') {
    const inputs = Array.from(document.querySelectorAll('input[type="text"]'));
    const active = document.activeElement;
    const idx = inputs.indexOf(active);

    if (idx !== -1) {
      e.preventDefault();
      if (idx < inputs.length - 1) {
        inputs[idx + 1].focus();
      }
    }
  }
});
</script>
""", unsafe_allow_html=True)

# -------------------------------
# HELPERS
# -------------------------------
def parse_role(role):
    role = re.sub(r"^\d+\.\s*", "", role.strip())
    parts = role.split("|")

    role_title = parts[0].strip()
    mode = parts[1].replace("Mode:", "").strip() if len(parts) > 1 else "Not Specified"
    pay = parts[2].replace("Compensation:", "").strip() if len(parts) > 2 else "Not Specified"
    stipend = parts[3].replace("Expected Stipend Range:", "").strip() if len(parts) > 3 else "Not Specified"
    duration = parts[4].replace("Duration:", "").strip() if len(parts) > 4 else "Not Specified"

    return role_title, mode, pay, stipend, duration


def badge_color(mode):
    return {
        "remote": "#22c55e",
        "hybrid": "#facc15",
        "onsite": "#3b82f6"
    }.get(mode.lower(), "#9ca3af")


def display_roles(output):
    for role in output.split("\n"):
        if not role.strip():
            continue

        role_title, mode, pay, stipend, duration = parse_role(role)

        if st.session_state.mode_filter != "All" and mode.lower() != st.session_state.mode_filter.lower():
            continue

        if st.session_state.pay_filter != "All" and pay.lower() != st.session_state.pay_filter.lower():
            continue

        with st.container(border=True):
            st.markdown(f"### {role_title}")

            col1, col2 = st.columns(2)
            col1.markdown(f"<span style='color:{badge_color(mode)}'>{mode}</span>", unsafe_allow_html=True)
            col2.markdown(f"<span style='color:#22c55e'>{pay}</span>", unsafe_allow_html=True)

            st.markdown(f"💰 **{stipend}**")
            st.markdown(f"⏱ **{duration}**")

            company_name = "Unknown"
            if " at " in role_title:
                company_name = role_title.split(" at ")[-1].split("(")[0].strip()

            query = urllib.parse.quote(company_name + " careers")

            st.link_button(
                f"🏢 Open {company_name} Careers",
                f"https://www.google.com/search?q={query}"
            )


def show_dashboard(skills, location, output):
    report = evaluate_response(skills, location, output)

    st.subheader("Evaluation Dashboard")

    c1, c2, c3 = st.columns(3)
    c1.metric("Overall", f"{report['overall_score']}%")
    c2.metric("Skill Match", f"{report['skill_match']}%")
    c3.metric("Format", f"{report['format_accuracy']}%")

    c4, c5, c6 = st.columns(3)
    c4.metric("Location", f"{report['location_match']}%")
    c5.metric("Diversity", f"{report['diversity_score']}%")
    c6.metric("Count", f"{report['response_count']}%")

    st.progress(int(report["overall_score"]))


# -------------------------------
# UI
# -------------------------------
st.title("🎯 AI Internship Finder")

# Sidebar Filters
st.sidebar.title("Filters")

st.session_state.mode_filter = st.sidebar.selectbox(
    "Work Mode", ["All", "Remote", "Hybrid", "Onsite"]
)

st.session_state.pay_filter = st.sidebar.selectbox(
    "Compensation", ["All", "Paid", "Unpaid", "Not Specified"]
)

st.sidebar.divider()

# -------------------------------
# SIDEBAR HISTORY
# -------------------------------
st.sidebar.title("Recent Searches")

history = st.session_state.history

if not history:
    st.sidebar.write("No searches yet")
else:
    for idx, item in enumerate(history, start=1):

        st.sidebar.markdown(f"### #{idx} 📍 {item['location']}")
        st.sidebar.caption(item["skills"])

        col1, col2 = st.sidebar.columns([3, 1])

        if col1.button(f"Open {idx}", key=f"open_{item['id']}"):
            st.session_state.skills = item["skills"]
            st.session_state.location = item["location"]
            st.session_state.saved_output = item["response"]
            st.session_state.selected_id = item["id"]

        if col2.button("🗑", key=f"delete_{item['id']}"):
            delete_search(item["id"])

            st.session_state.history = [
                h for h in st.session_state.history if h["id"] != item["id"]
            ]

            # 🔥 immediate UI update
            st.rerun()

# -------------------------------
# INPUTS
# -------------------------------
skills = st.text_input("Enter your skills:", value=st.session_state.skills)
location = st.text_input("Enter location:", value=st.session_state.location)

# -------------------------------
# SEARCH (NO FLICKER)
# -------------------------------
if st.button("Find Internships"):

    if not skills.strip() or not location.strip():
        st.warning("Please enter both fields")

    else:
        with st.spinner("Finding internships..."):
            suggestions, search_id = get_internship_suggestions(skills, location)

        st.session_state.skills = skills
        st.session_state.location = location
        st.session_state.saved_output = suggestions
        st.session_state.selected_id = search_id

        st.session_state.history = get_recent_searches(limit=5)

# -------------------------------
# RESULTS
# -------------------------------
if st.session_state.saved_output:

    st.subheader("Previous Search Result")

    if st.button("Delete"):
        if st.session_state.selected_id:
            delete_search(st.session_state.selected_id)

        st.session_state.saved_output = ""
        st.session_state.selected_id = None
        st.session_state.history = get_recent_searches(limit=5)

        # 🔥 refresh UI
        st.rerun()

    display_roles(st.session_state.saved_output)

    st.info("These are AI-generated suggestions. Visit company careers pages to apply.")

    show_dashboard(
        st.session_state.skills,
        st.session_state.location,
        st.session_state.saved_output
    )
