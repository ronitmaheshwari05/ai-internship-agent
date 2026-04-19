import streamlit as st
import re
from src.agent.agent import get_internship_suggestions
from src.database.db import create_table, delete_search, get_recent_searches

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

    main = parts[0].strip()

    mode = "Not Specified"
    pay = "Not Specified"

    if len(parts) > 1:
        mode = parts[1].replace("Mode:", "").strip()

    if len(parts) > 2:
        pay = parts[2].replace("Compensation:", "").strip()

    return main, mode, pay


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

        main, mode, pay = parse_role(role)

        # Filters
        if st.session_state.mode_filter != "All":
            if mode.lower() != st.session_state.mode_filter.lower():
                continue

        if st.session_state.pay_filter != "All":
            if pay.lower() != st.session_state.pay_filter.lower():
                continue

        mode_color = badge_color(mode)

        with st.container(border=True):

            st.markdown(
                f"### {main}"
            )

            col1, col2, col3 = st.columns([1,1,5])

            with col1:
                st.markdown(
                    f"""
<span style="
background:#1f2937;
color:{mode_color};
padding:6px 10px;
border-radius:8px;
font-size:13px;
font-weight:600;">
{mode}
</span>
""",
                    unsafe_allow_html=True
                )

            with col2:
                st.markdown(
                    """
<span style="
background:#1f2937;
color:#22c55e;
padding:6px 10px;
border-radius:8px;
font-size:13px;
font-weight:600;">
Paid
</span>
""",
                    unsafe_allow_html=True
                )

            st.write("")

# ------------------------------------------------
# Title
# ------------------------------------------------
st.title("🎯 AI Internship Finder")


# ------------------------------------------------
# Sidebar Filters
# ------------------------------------------------
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


# ------------------------------------------------
# Sidebar History
# ------------------------------------------------
st.sidebar.title("Recent Searches")

history = get_recent_searches(limit=5)

for item in history:

    st.sidebar.markdown(f"### 📍 {item.location}")
    st.sidebar.caption(item.skills)

    col1, col2 = st.sidebar.columns([3, 1])

    with col1:
        if st.button(
            f"Open {item.id}",
            key=f"load_{item.id}",
            use_container_width=True
        ):
            st.session_state.skills = item.skills
            st.session_state.location = item.location
            st.session_state.saved_output = item.response
            st.session_state.selected_search_id = item.id
            st.rerun()

    with col2:
        if st.button(
            "🗑",
            key=f"delete_{item.id}",
            use_container_width=True
        ):
            delete_search(item.id)

            if st.session_state.selected_search_id == item.id:
                st.session_state.saved_output = ""
                st.session_state.selected_search_id = None

            st.rerun()

    st.sidebar.divider()


# ------------------------------------------------
# Inputs
# ------------------------------------------------
skills = st.text_input(
    "Enter your skills (comma-separated):",
    value=st.session_state.skills
)

location = st.text_input(
    "Enter your preferred location:",
    value=st.session_state.location
)


# ------------------------------------------------
# Show Previous Result
# ------------------------------------------------
show_previous = bool(st.session_state.saved_output)

if show_previous:

    col1, col2 = st.columns([4, 1])

    with col1:
        st.subheader("Previous Search Result")

    with col2:
        if st.button("Delete", key="delete_result"):

            if st.session_state.selected_search_id:
                delete_search(st.session_state.selected_search_id)

            st.session_state.saved_output = ""
            st.session_state.selected_search_id = None
            st.rerun()

    display_roles(st.session_state.saved_output)


# ------------------------------------------------
# Search Button
# ------------------------------------------------
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

    if st.button("Find Internships", use_container_width=True):

        with st.spinner("Finding best internships for you..."):

            suggestions, search_id = get_internship_suggestions(
                skills,
                location
            )

        st.session_state.skills = skills
        st.session_state.location = location
        st.session_state.saved_output = suggestions
        st.session_state.selected_search_id = search_id

        st.rerun()
