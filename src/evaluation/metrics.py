import re

# ------------------------------------------------
# Format Accuracy Score
# ------------------------------------------------
def format_accuracy_score(output):

    lines = [line.strip() for line in output.split("\n") if line.strip()]

    if not lines:
        return 0

    total_score = 0

    for line in lines:

        score = 0
        lower_line = line.lower()

        if line:
            score += 20

        if "mode:" in lower_line:
            score += 20

        if "compensation:" in lower_line:
            score += 20

        if "stipend:" in lower_line:
            score += 20

        if "duration:" in lower_line:
            score += 20

        total_score += score

    return round(total_score / len(lines), 2)


# ------------------------------------------------
# Skill Match Score
# ------------------------------------------------
def skill_match_score(skills, output):

    skill_groups = {

        # Languages
        "python": ["python", "backend", "automation", "data", "ml"],
        "java": ["java", "spring", "backend", "android"],
        "c": ["c", "embedded", "systems"],
        "c++": ["c++", "systems", "game", "engineer"],
        "c#": ["c#", ".net"],
        "javascript": ["javascript", "frontend", "web", "node"],
        "typescript": ["typescript", "frontend", "react"],
        "go": ["go", "backend", "microservices"],
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
        "oop": ["oop", "object oriented"]
    }

    skill_list = [
        s.strip().lower()
        for s in skills.split(",")
        if s.strip()
    ]

    lines = [line.lower() for line in output.split("\n") if line.strip()]

    if not lines:
        return 0

    matches = 0

    for line in lines:

        found = False

        for skill in skill_list:

            related_words = skill_groups.get(skill, [skill])

            for word in related_words:

                if word in line:
                    found = True
                    break

            if found:
                matches += 1
                break

    return round((matches / len(lines)) * 100, 2)


# ------------------------------------------------
# Location Relevance Score
# ------------------------------------------------
def location_relevance_score(location, output):

    lines = [line.lower() for line in output.split("\n") if line.strip()]

    if not lines:
        return 0

    location = location.lower().strip()
    matches = 0

    for line in lines:

        if location in line:
            matches += 1

        elif "remote" in line or "hybrid" in line:
            matches += 0.5

    return round((matches / len(lines)) * 100, 2)


# ------------------------------------------------
# Diversity Score
# ------------------------------------------------
def diversity_score(output):

    lines = [line.strip() for line in output.split("\n") if line.strip()]

    if not lines:
        return 0

    titles = []

    for line in lines:

        title = line.split("|")[0]
        title = re.sub(r"^\d+\.\s*", "", title).strip().lower()

        titles.append(title)

    unique_titles = len(set(titles))

    return round((unique_titles / len(titles)) * 100, 2)


# ------------------------------------------------
# Response Count Score
# ------------------------------------------------
def response_count_score(output):

    lines = [line.strip() for line in output.split("\n") if line.strip()]

    count = len(lines)

    if count == 5:
        return 100
    if count == 4:
        return 80
    if count == 3:
        return 60
    if count == 2:
        return 40
    if count == 1:
        return 20

    return 0