import re


def calculate_ats_score(
    resume_text,
    target_role
):

    role_keywords = {

        "AI/ML Intern": [
            "python",
            "machine learning",
            "tensorflow",
            "pytorch",
            "deep learning",
            "data analysis",
            "sql"
        ],

        "Software Engineering Intern": [
            "python",
            "java",
            "c++",
            "dsa",
            "algorithms",
            "git",
            "api"
        ],

        "Data Science Intern": [
            "python",
            "pandas",
            "numpy",
            "sql",
            "visualization",
            "statistics"
        ],

        "Finance Intern": [
            "excel",
            "financial analysis",
            "valuation",
            "accounting",
            "forecasting"
        ],

        "Marketing Intern": [
            "seo",
            "social media",
            "branding",
            "analytics",
            "marketing"
        ]
    }

    keywords = role_keywords.get(
        target_role,
        []
    )

    resume_lower = resume_text.lower()

    matched = []

    missing = []

    for keyword in keywords:

        if keyword in resume_lower:
            matched.append(keyword)

        else:
            missing.append(keyword)

    # =====================================================
    # SCORE
    # =====================================================
    if len(keywords) == 0:

        score = 50

    else:

        score = int(
            (len(matched) / len(keywords)) * 100
        )

    # =====================================================
    # BONUS
    # =====================================================
    if len(resume_text) > 1000:
        score += 5

    score = min(score, 100)

    return {

        "score": score,

        "matched": matched,

        "missing": missing
    }