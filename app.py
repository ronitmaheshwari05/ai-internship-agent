import streamlit as st
import re
from src.agent.agent import get_internship_suggestions

# Page config
st.set_page_config(page_title="AI Internship Finder", layout="centered")

# Title
st.title("Internship Suggestion App")

# Inputs
skills = st.text_input("Enter your skills (comma-separated):")
location = st.text_input("Enter your preferred location:")

# Button
if st.button("Find Internships"):
    if skills and location:
        
        with st.spinner("Finding best internships for you... 🔍"):
            suggestions = get_internship_suggestions(skills, location)

        st.subheader("🔍 Suggested Internship Roles:")

        # Split response into lines
        roles = suggestions.split("\n")

        for role in roles:
            role = role.strip()

            if role:
                # Remove numbering like "1."
                role = re.sub(r"^\d+\.\s*", "", role)

                st.markdown(f"""
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
                """, unsafe_allow_html=True)

    else:
        st.error("Please enter both skills and location.")