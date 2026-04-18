import streamlit as st
import re
from src.agent.agent import get_internship_suggestions
from src.database.db import create_table, get_recent_searches


# Create DB Table
create_table()

# Page Config
st.set_page_config(page_title="AI Internship Finder", layout="centered")


# Session State Defaults
if "skills" not in st.session_state:
    st.session_state.skills = ""

if "location" not in st.session_state:
    st.session_state.location = ""

if "saved_output" not in st.session_state:
    st.session_state.saved_output = ""


# Helper Function
def display_roles(output):
    roles = output.split("\n")

    for role in roles:
        role = role.strip()

        if role:
            role = re.sub(r"^\d+\.\s*", "", role)

            st.markdown(
                f"""
                <div style="
                    padding:15px;
                    margin-bottom:12px;
                    border-radius:12px;
                    background-color:#111827;
                    border:1px solid #2d3748;
                    font-size:16px;
                ">
                    {role}
                </div>
                """,
                unsafe_allow_html=True
            )


# Title
st.title("Internship Suggestion App")


# Sidebar History
st.sidebar.title("Recent Searches")

history = get_recent_searches(limit=5)

for item in history:
    st.sidebar.markdown(f"### 📍 {item.location}")
    st.sidebar.caption(item.skills)

    if st.sidebar.button(
        f"Open Search {item.id}",
        key=f"load_{item.id}"
    ):
        st.session_state.skills = item.skills
        st.session_state.location = item.location
        st.session_state.saved_output = item.response

    st.sidebar.divider()


# Inputs
skills = st.text_input(
    "Enter your skills (comma-separated):",
    value=st.session_state.skills
)

location = st.text_input(
    "Enter your preferred location:",
    value=st.session_state.location
)


# Show Previous Result
show_previous = bool(st.session_state.saved_output)

if show_previous:
    st.subheader("Previous Search Result:")
    display_roles(st.session_state.saved_output)


# Show Button ONLY if editing/new search
show_button = (
    (skills.strip() and location.strip())
    and
    (
        skills != st.session_state.skills
        or location != st.session_state.location
        or not show_previous
    )
)

if show_button:

    if st.button("Find Internships"):

        with st.spinner("Finding best internships for you... "):
            suggestions = get_internship_suggestions(skills, location)

        st.session_state.skills = skills
        st.session_state.location = location
        st.session_state.saved_output = suggestions

        st.rerun()