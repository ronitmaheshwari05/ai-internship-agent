<div align="center">

# 🎓 AI Internship Finder Agent

**An AI-powered agent that helps students discover relevant internship opportunities based on their skills and preferred location.**

[![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.x-FF4B4B?style=flat-square&logo=streamlit&logoColor=white)](https://streamlit.io)
[![Mistral AI](https://img.shields.io/badge/Mistral-AI-F97316?style=flat-square)](https://mistral.ai)
[![GSSoC 2026](https://img.shields.io/badge/GSSoC-2026-6366F1?style=flat-square)](https://gssoc.girlscript.tech)
[![License: MIT](https://img.shields.io/badge/License-MIT-22C55E?style=flat-square)](LICENSE)

*Built as part of the **AI Agents for India** track under [GirlScript Summer of Code 2026](https://gssoc.girlscript.tech)*

</div>

---

## 📌 Table of Contents

- [Overview](#-overview)
- [Problem Statement](#-problem-statement)
- [Solution](#-solution)
- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [System Workflow](#-system-workflow)
- [Getting Started](#-getting-started)
- [Project Structure](#-project-structure)
- [Roadmap](#-roadmap)
- [Contributing](#-contributing)
- [Author](#-author)

---

## 🧠 Overview

Finding the right internship is hard — especially when you're a student with limited time and specific skills. **AI Internship Finder Agent** cuts through the noise by using a large language model to generate **personalized, context-aware internship role suggestions** in seconds. Just enter your skills and location, and let the agent do the rest.

---

## ❗ Problem Statement

Students consistently face three core challenges in internship discovery:

| Challenge | Impact |
|-----------|--------|
| Sifting through irrelevant listings | Wastes hours of research time |
| No skill-based filtering | Mismatched applications, lower success rates |
| Slow, generic suggestions | Discourages proactive job seeking |

---

## ✅ Solution

This agent takes a **simple 2-input approach** and turns it into intelligent, actionable output:

1. **Input** — User provides their skills and preferred location
2. **Process** — A Mistral LLM interprets the query with an optimized prompt
3. **Output** — Structured, relevant internship role suggestions rendered in a clean UI

No sign-ups. No job board scraping. Just instant AI-driven personalization.

---

## ✨ Features

### Phase 1 (Completed ✅)

- 🔍 **Skill-based suggestions** — Tailored roles based on what you know
- 📍 **Location-aware filtering** — Relevant opportunities for your city or region
- 🤖 **Mistral LLM integration** — Fast, accurate role recommendations
- 🖥️ **Streamlit UI** — Clean, responsive, card-based result display
- ⚡ **Optimized prompting** — Structured output with minimal hallucination

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|------------|
| Language | Python 3.8+ |
| Frontend | Streamlit |
| AI Model | Mistral API |
| Config | python-dotenv |

---

## 🔄 System Workflow

```
User Input (Skills + Location)
        │
        ▼
  Prompt Builder
        │
        ▼
  Mistral LLM API
        │
        ▼
  Response Parser
        │
        ▼
  Streamlit Card UI  ──►  User sees internship suggestions
```

> Full flowchart available at [`docs/flowcharts/flowchart.png`](docs/flowcharts/flowchart.png)

---

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or above
- A valid [Mistral API key](https://console.mistral.ai/)

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/ai-internship-finder.git
cd ai-internship-finder
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment

Create a `.env` file in the root directory:

```env
MISTRAL_API_KEY=your_api_key_here
```



### 4. Run the App

```bash
streamlit run app.py
```

Open your browser at `http://localhost:8501` and start exploring internships!

---

## 📁 Project Structure

## 📁 Project Structure

```text
AI-INTERNSHIP-AGENT/
├── app.py                     # Main Streamlit application
├── config.py                  # Configuration settings
├── requirements.txt
├── README.md
├── .env                       # Environment variables (ignored)
├── .env.example               # Sample environment config
├── .gitignore
├── venv/                      # Virtual environment (ignored)
├── .venv/                     # Virtual environment (ignored)

├── data/
│   ├── raw/                   # Raw data (future use)
│   └── processed/             # Processed data (future use)

├── docs/
│   └── flowcharts/
│       ├── flowchart.png
│       └── FlowchartFeatures.png

├── logs/                      # Application logs

├── src/
│   ├── agent/
│   │   ├── agent.py           # Core AI agent logic
│   │   └── prompts.py         # Prompt templates
│
│   ├── database/
│   │   ├── db.py              # Database connection & queries (Phase 2)
│   │   └── models.py          # Data models
│
│   ├── evaluation/
│   │   ├── evaluator.py       # Evaluation logic
│   │   └── metrics.py         # Performance metrics
│
│   ├── features/
│   │   ├── auth/
│   │   │   └── auth.py        # Authentication module (planned)
│   │   ├── internship/
│   │   │   ├── fetcher.py     # Internship fetching logic
│   │   │   └── filters.py     # Filtering logic
│   │   └── resume_builder/
│   │       └── builder.py     # Resume builder module (planned)
│
│   └── utils/
│       └── helpers.py         # Utility functions

├── tests/
│   └── test_agent.py          # Unit tests
```
---

## 🗺️ Roadmap

| Phase | Feature | Status |
|-------|---------|--------|
| 1 | Core AI agent + Streamlit UI | ✅ Done |
| 2 | Search history with database integration | 🔜 Upcoming |
| 2 | Response caching & regeneration | 🔜 Upcoming |
| 3 | Agent evaluation metrics dashboard | 🔜 Upcoming |
| 3 | User authentication | 🔜 Upcoming |
| 4 | AI-based resume builder | 🔜 Upcoming |

---

## 🤝 Contributing

Contributions are welcome! To get started:

1. Fork the repository
2. Create a new branch: `git checkout -b feature/your-feature-name`
3. Make your changes and commit: `git commit -m "Add your message here"`
4. Push to your fork: `git push origin feature/your-feature-name`
5. Open a Pull Request

Please read [CONTRIBUTING.md](CONTRIBUTING.md) before submitting any changes.

---

## 👤 Author

**Ronit Maheshwari**


---

<div align="center">

Made with ❤️ for students, by a student &nbsp;|&nbsp; GirlScript Summer of Code 2026

</div>
