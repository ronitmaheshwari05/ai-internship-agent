import re
from difflib import SequenceMatcher

# ============================================================
# MASTER SKILL GROUPS
# ============================================================

skill_groups = {

    # ========================================================
    # TECHNICAL SKILLS
    # ========================================================

    # Languages
    "python": ["python", "backend", "automation", "data", "ml"],
    "java": ["java", "spring", "backend", "android"],
    "c": ["c", "embedded", "systems"],
    "c++": ["c++", "cpp", "systems", "game", "engineer"],
    "c#": ["c#", ".net"],
    "javascript": ["javascript", "frontend", "web", "node"],
    "typescript": ["typescript", "frontend", "react"],
    "go": ["go", "golang", "backend", "microservices"],
    "rust": ["rust", "systems"],
    "php": ["php", "backend", "laravel"],
    "ruby": ["ruby", "rails"],
    "swift": ["swift", "ios"],
    "kotlin": ["kotlin", "android"],

    # Frontend
    "html": ["html", "frontend", "web"],
    "css": ["css", "frontend", "ui"],
    "react": ["react", "frontend", "ui"],
    "angular": ["angular", "frontend"],
    "vue": ["vue", "frontend"],
    "nextjs": ["nextjs", "react"],
    "tailwind": ["tailwind", "css"],
    "bootstrap": ["bootstrap", "frontend"],

    # Backend
    "nodejs": ["node", "nodejs", "backend", "api"],
    "express": ["express", "backend"],
    "django": ["django", "python", "backend"],
    "flask": ["flask", "python", "backend"],
    "fastapi": ["fastapi", "python", "api"],
    "spring": ["spring", "java", "backend"],

    # Databases
    "sql": ["sql", "database", "data"],
    "mysql": ["mysql", "database"],
    "postgresql": ["postgresql", "database"],
    "mongodb": ["mongodb", "nosql"],
    "sqlite": ["sqlite", "database"],
    "redis": ["redis", "cache"],

    # Data / Analytics
    "pandas": ["pandas", "data"],
    "numpy": ["numpy", "data"],
    "power bi": ["power bi", "analytics"],
    "tableau": ["tableau", "analytics"],
    "excel": ["excel", "analytics"],

    # AI / ML
    "machine learning": ["ml", "machine learning", "ai"],
    "deep learning": ["deep learning", "ai"],
    "tensorflow": ["tensorflow", "ml", "ai"],
    "pytorch": ["pytorch", "ml", "ai"],
    "keras": ["keras", "deep learning"],
    "scikit-learn": ["scikit", "machine learning"],
    "nlp": ["nlp", "language", "llm"],
    "computer vision": ["computer vision", "cv"],
    "rag": ["rag", "retrieval", "llm", "genai"],
    "llm": ["llm", "language model", "genai"],
    "genai": ["genai", "llm", "ai"],
    "hugging face": ["hugging face", "transformers"],

    # Cloud / DevOps
    "aws": ["aws", "cloud"],
    "azure": ["azure", "cloud"],
    "gcp": ["gcp", "cloud"],
    "docker": ["docker", "container"],
    "kubernetes": ["kubernetes", "k8s"],
    "linux": ["linux", "systems"],
    "git": ["git"],
    "github": ["github"],
    "ci/cd": ["deployment", "devops"],

    # Mobile
    "android": ["android", "mobile"],
    "ios": ["ios", "mobile"],
    "flutter": ["flutter", "mobile"],
    "react native": ["react native", "mobile"],

    # Security
    "cybersecurity": ["security", "cybersecurity"],
    "ethical hacking": ["security", "penetration testing"],

    # Core CS
    "dsa": ["dsa", "algorithms"],
    "dbms": ["dbms", "database"],
    "os": ["operating system"],
    "cn": ["networking", "computer networks"],
    "oop": ["oop", "object oriented"],

    # ========================================================
    # FINANCE
    # ========================================================

    "finance": ["finance", "financial", "investment", "banking"],
    "accounting": ["accounting", "accounts", "bookkeeping"],
    "investment banking": ["investment banking", "equity research"],
    "stock market": ["stock market", "trading", "equity"],
    "financial analysis": ["financial analysis", "valuation"],
    "taxation": ["tax", "gst", "income tax"],
    "auditing": ["audit", "auditing"],
    "fintech": ["fintech", "payments", "digital banking"],

    # ========================================================
    # HR
    # ========================================================

    "human resources": ["hr", "human resources", "recruitment"],
    "recruitment": ["recruiter", "talent acquisition", "hiring"],
    "payroll": ["payroll", "salary processing"],
    "training": ["training", "learning and development"],

    # ========================================================
    # MARKETING
    # ========================================================

    "marketing": ["marketing", "brand", "campaign"],
    "digital marketing": ["seo", "sem", "social media"],
    "content writing": ["content", "blog", "copywriting"],
    "seo": ["seo", "search engine optimization"],
    "branding": ["branding", "brand strategy"],
    "market research": ["market research", "consumer research"],

    # ========================================================
    # SALES
    # ========================================================

    "sales": ["sales", "business development"],
    "business development": ["bde", "client acquisition"],
    "inside sales": ["inside sales", "cold calling"],
    "customer success": ["customer success", "client support"],
    "crm": ["crm", "salesforce", "hubspot"],

    # ========================================================
    # RESEARCH
    # ========================================================

    "research": ["research", "analysis"],
    "research intern": ["research", "publication", "paper"],
    "scientific research": ["scientific", "lab research"],
    "policy research": ["policy analysis", "public policy"],

    # ========================================================
    # TEACHING / EDUCATION
    # ========================================================

    "teaching": ["teaching", "tutor", "mentor"],
    "teaching assistant": ["ta", "teaching assistant"],
    "education": ["education", "curriculum"],
    "online tutoring": ["online tutor", "edtech"],
    "subject matter expert": ["sme", "subject expert"],

    # ========================================================
    # DESIGN
    # ========================================================

    "graphic design": ["graphic design", "canva", "photoshop"],
    "ui/ux": ["ui", "ux", "figma", "wireframe"],
    "video editing": ["video editing", "premiere pro"],
    "animation": ["animation", "motion graphics"],

    # ========================================================
    # CONSULTING / MANAGEMENT
    # ========================================================

    "consulting": ["consulting", "strategy"],
    "management": ["management", "operations"],
    "project management": ["project management", "scrum"],
    "operations": ["operations", "process improvement"],

    # ========================================================
    # LAW
    # ========================================================

    "legal": ["legal", "law", "compliance"],
    "corporate law": ["corporate law", "contracts"],

    # ========================================================
    # HEALTHCARE
    # ========================================================

    "healthcare": ["healthcare", "medical"],
    "pharmacy": ["pharmacy", "drug"],
    "biotech": ["biotech", "biotechnology"],

    # ========================================================
    # MEDIA
    # ========================================================

    "journalism": ["journalism", "reporting"],
    "editing": ["editing", "proofreading"],
    "public relations": ["pr", "public relations"],

    # ========================================================
    # ENTREPRENEURSHIP
    # ========================================================

    "startup": ["startup", "founder", "entrepreneurship"],
    "product management": ["product management", "product manager"],

    # ========================================================
    # GENERAL
    # ========================================================

    "internship": ["intern", "internship"],
    "remote work": ["remote"],
    "hybrid work": ["hybrid"],
    "full time": ["full time"],
    "part time": ["part time"]
}

# ============================================================
# HELPER FUNCTIONS
# ============================================================

def clean_lines(output):

    return [
        line.strip()
        for line in output.split("\n")
        if line.strip()
    ]


def fuzzy_match(a, b, threshold=0.80):

    ratio = SequenceMatcher(None, a, b).ratio()
    return ratio >= threshold


# ============================================================
# FORMAT ACCURACY SCORE
# ============================================================

def format_accuracy_score(output):

    lines = clean_lines(output)

    if not lines:
        return 0

    total_score = 0

    required_fields = [
        "mode:",
        "compensation:",
        "stipend:",
        "duration:"
    ]

    for line in lines:

        score = 0
        lower_line = line.lower()

        # Line exists
        score += 20

        # Required fields
        for field in required_fields:
            if field in lower_line:
                score += 20

        total_score += min(score, 100)

    return round(total_score / len(lines), 2)


# ============================================================
# SKILL MATCH SCORE
# ============================================================

def skill_match_score(skills, output):

    skill_list = [
        s.strip().lower()
        for s in skills.split(",")
        if s.strip()
    ]

    lines = clean_lines(output)

    if not lines:
        return 0

    total_points = 0
    max_points = len(lines) * 2

    for line in lines:

        line_lower = line.lower()

        matched = False

        for skill in skill_list:

            related_words = skill_groups.get(skill, [skill])

            # Exact Match → +2
            if skill in line_lower:
                total_points += 2
                matched = True
                break

            # Related Keyword Match → +1
            for word in related_words:

                if word in line_lower:
                    total_points += 1
                    matched = True
                    break

                # Fuzzy Match
                words_in_line = line_lower.split()

                for token in words_in_line:

                    if fuzzy_match(word, token):
                        total_points += 1
                        matched = True
                        break

                if matched:
                    break

            if matched:
                break

    return round((total_points / max_points) * 100, 2)


# ============================================================
# LOCATION RELEVANCE SCORE
# ============================================================

def location_relevance_score(location, output):

    lines = clean_lines(output)

    if not lines:
        return 0

    location = location.lower().strip()

    matches = 0

    for line in lines:

        lower_line = line.lower()

        if location in lower_line:
            matches += 1

        elif "remote" in lower_line:
            matches += 0.75

        elif "hybrid" in lower_line:
            matches += 0.5

    return round((matches / len(lines)) * 100, 2)


# ============================================================
# DIVERSITY SCORE
# ============================================================

def diversity_score(output):

    lines = clean_lines(output)

    if not lines:
        return 0

    titles = []

    for line in lines:

        title = line.split("|")[0]

        title = re.sub(r"^\d+\.\s*", "", title)
        title = title.strip().lower()

        titles.append(title)

    unique_titles = len(set(titles))

    return round((unique_titles / len(titles)) * 100, 2)


# ============================================================
# RESPONSE COUNT SCORE
# ============================================================

def response_count_score(output):

    count = len(clean_lines(output))

    if count >= 5:
        return 100
    elif count == 4:
        return 80
    elif count == 3:
        return 60
    elif count == 2:
        return 40
    elif count == 1:
        return 20

    return 0


# ============================================================
# ROLE RELEVANCE SCORE
# ============================================================

def role_relevance_score(output):

    internship_roles = [

        # Tech
        "software engineer intern",
        "ml intern",
        "ai intern",
        "data science intern",
        "backend intern",
        "frontend intern",

        # Business
        "marketing intern",
        "finance intern",
        "hr intern",
        "sales intern",

        # Others
        "research intern",
        "teaching intern",
        "design intern",
        "consulting intern"
    ]

    lines = clean_lines(output)

    if not lines:
        return 0

    matches = 0

    for line in lines:

        lower_line = line.lower()

        for role in internship_roles:

            if role in lower_line:
                matches += 1
                break

    return round((matches / len(lines)) * 100, 2)


# ============================================================
# OVERALL SCORE
# ============================================================

def overall_score(skills, location, output):

    scores = {

        "Format Accuracy":
            format_accuracy_score(output),

        "Skill Match":
            skill_match_score(skills, output),

        "Location Relevance":
            location_relevance_score(location, output),

        "Diversity":
            diversity_score(output),

        "Response Count":
            response_count_score(output),

        "Role Relevance":
            role_relevance_score(output)
    }

    final_score = round(
        sum(scores.values()) / len(scores),
        2
    )

    scores["Final Score"] = final_score

    return scores


# ============================================================
# SAMPLE TEST
# ============================================================

if __name__ == "__main__":

    skills = """
    Python,
    Machine Learning,
    GenAI,
    Research,
    Marketing
    """

    location = "Jaipur"

    output = """
    1. ML Intern | Mode: Remote | Stipend: 25000 | Duration: 6 months
    2. Research Intern | Mode: Hybrid Jaipur | Compensation: 30000 | Duration: 3 months
    3. Digital Marketing Intern | Mode: Remote | Stipend: 15000 | Duration: 4 months
    4. Software Engineer Intern | Mode: Jaipur | Compensation: 40000 | Duration: 6 months
    5. Teaching Intern | Mode: Hybrid | Stipend: 12000 | Duration: 2 months
    """

    scores = overall_score(skills, location, output)

    print("\n========== EVALUATION SCORES ==========\n")

    for key, value in scores.items():
        print(f"{key}: {value}")