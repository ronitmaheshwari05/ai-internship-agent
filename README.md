<div align="center">

# AI Internship Finder Agent

### An AI-powered internship discovery platform with authentication, ATS resume generation, and intelligent internship recommendations.

<br/>

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-Frontend-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![Firebase](https://img.shields.io/badge/Firebase-Authentication-FFCA28?style=for-the-badge&logo=firebase&logoColor=black)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-NeonDB-4169E1?style=for-the-badge&logo=postgresql&logoColor=white)
![Groq](https://img.shields.io/badge/Groq-AI_API-FF6B00?style=for-the-badge)
![Mistral](https://img.shields.io/badge/Mistral-AI_Model-F7631B?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-22C55E?style=for-the-badge)
![GSSoC 2026](https://img.shields.io/badge/GSSoC-2026-8B5CF6?style=for-the-badge)

<br/>

> Built under the AI Agents for India track during GirlScript Summer of Code 2026

</div>

---

# Table of Contents

- [Overview](#overview)
- [Problem Statement](#problem-statement)
- [Solution](#solution)
- [Core Features](#core-features)
- [Authentication System](#authentication-system)
- [Resume Builder](#resume-builder)
- [Evaluation Dashboard](#evaluation-dashboard)
- [Tech Stack](#tech-stack)
- [System Workflow](#system-workflow)
- [Architecture](#architecture)
- [Installation](#installation)
- [Environment Variables](#environment-variables)
- [Project Structure](#project-structure)
- [Roadmap](#roadmap)
- [Contributing](#contributing)
- [Developer](#developer)
- [License](#license)

---

# Overview

AI Internship Finder Agent is an AI-powered internship discovery platform designed to help students find relevant internship opportunities based on their technical skills, preferred location, and career interests.

The platform combines modern AI workflows, authentication systems, resume generation, and evaluation metrics into a single application.

The system provides:

- Skill-based internship recommendations
- AI-generated structured internship listings
- Firebase authentication
- PostgreSQL-based search history
- ATS-friendly resume generation
- Resume evaluation and ATS scoring
- Personalized user experience
- Modern Streamlit interface

---

# Problem Statement

Students often face multiple challenges during internship discovery:

| Challenge | Impact |
|---|---|
| Irrelevant internship listings | Wasted application effort |
| Generic recommendations | Low role relevance |
| Lack of personalization | Poor user experience |
| Weak resume quality | Reduced ATS compatibility |
| No centralized workflow | Fragmented internship search process |

---

# Solution

The platform provides a complete AI-assisted internship workflow.

## Workflow

1. User authentication using Firebase
2. Skills and location input
3. AI-powered internship recommendation generation
4. Structured internship presentation
5. Search history storage in PostgreSQL
6. ATS resume generation
7. Resume quality evaluation

The system combines AI reasoning with structured filtering to improve recommendation quality and user experience.

---

# Core Features

## AI Internship Recommendation Engine

- Skill-based internship recommendations
- Location-aware filtering
- Work mode filtering
- Structured internship formatting
- AI-generated recommendations
- Career page linking

---

## Search History System

- PostgreSQL-based storage
- Persistent recent searches
- Cached search responses
- Search deletion support
- Sidebar search management

---

## Streamlit User Interface

- Responsive dashboard
- Card-based internship UI
- Session state management
- Sidebar controls
- Interactive filters
- Clean professional layout

---

# Authentication System

The platform integrates Firebase Authentication for secure user access.

## Features

- User signup
- User login
- Secure session handling
- Protected dashboard access
- Logout functionality
- Firebase-backed authentication flow

---

# Resume Builder

The application includes a built-in ATS-friendly resume generation system.

## Features

- Resume generation using structured inputs
- Multiple resume templates
- Live HTML preview
- PDF export functionality
- ATS optimization support

---

# Evaluation Dashboard

The platform includes a custom evaluation engine for both recommendations and resumes.

## Internship Recommendation Evaluation

- Skill match score
- Location relevance score
- Diversity score
- Format accuracy validation
- Response count analysis
- Overall recommendation quality score

## ATS Resume Evaluation

- ATS score calculation
- Keyword matching
- Missing keyword detection
- Resume optimization feedback

---

# Tech Stack

| Layer | Technology |
|---|---|
| Programming Language | Python |
| Frontend | Streamlit |
| AI Models | Mistral AI, Groq API |
| Authentication | Firebase Authentication |
| Database | PostgreSQL (Neon DB) |
| Resume Generation | HTML + PDF |
| Environment Management | python-dotenv |
| Version Control | Git + GitHub |

---

# System Workflow

```text
User Authentication
        ↓
Firebase Authentication
        ↓
Skills + Location Input
        ↓
AI Recommendation Engine
        ↓
Mistral + Groq Processing
        ↓
Structured Internship Generation
        ↓
PostgreSQL Search Storage
        ↓
ATS Resume Builder + Evaluation
```

---

# Architecture

```text
Frontend Layer
└── Streamlit UI

Authentication Layer
└── Firebase Authentication

AI Layer
├── Prompt Engineering
├── Internship Recommendation Engine
├── Evaluation Engine
└── ATS Resume Scoring

LLM Integration
├── Mistral AI
└── Groq API

Database Layer
└── Neon PostgreSQL
```

---

# Installation

## Clone Repository

```bash
git clone https://github.com/YOUR_USERNAME/ai-internship-agent.git

cd ai-internship-agent
```

---

## Create Virtual Environment

### Windows

```bash
python -m venv .venv

.venv\Scripts\activate
```

### macOS/Linux

```bash
python3 -m venv .venv

source .venv/bin/activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Run Application

```bash
streamlit run app.py
```

---

# Environment Variables

Create a `.env` file in the root directory.

```env
MISTRAL_API_KEY=your_mistral_api_key

GROQ_API_KEY=your_groq_api_key

DATABASE_URL=your_neon_postgresql_url

FIREBASE_API_KEY=your_firebase_api_key
FIREBASE_AUTH_DOMAIN=your_auth_domain
FIREBASE_PROJECT_ID=your_project_id
FIREBASE_STORAGE_BUCKET=your_storage_bucket
FIREBASE_MESSAGING_SENDER_ID=your_sender_id
FIREBASE_APP_ID=your_app_id
```

---

# Project Structure

```text
ai-internship-agent/
│
├── app.py
├── requirements.txt
├── README.md
├── .env.example
├── .gitignore
│
├── src/
│
│   ├── agent/
│   │   ├── agent.py
│   │   └── prompts.py
│   │
│   ├── database/
│   │   ├── db.py
│   │   └── models.py
│   │
│   ├── evaluation/
│   │   ├── evaluator.py
│   │   └── metrics.py
│   │
│   └── features/
│       │
│       ├── auth/
│       │   └── auth.py
│       │
│       ├── internship/
│       │   └── fetcher.py
│       │
│       ├── resume_builder/
│       │   ├── builder.py
│       │   ├── ats_score.py
│       │   ├── pdf_generator.py
│       │   └── templates/
│       │
│       └── utils/
│
├── generated_resumes/
│
├── logs/
│
└── tests/
```

---

# Roadmap

| Feature | Status |
|---|---|
| AI Internship Recommendation Engine | Completed |
| PostgreSQL Integration | Completed |
| Search History System | Completed |
| Firebase Authentication | Completed |
| ATS Resume Builder | Completed |
| Evaluation Dashboard | Completed |
| Personalized User Search History | In Progress |
| Internship Bookmarking System | Planned |
| Resume Storage System | Planned |
| Google Authentication | Planned |
| RAG-based Recommendations | Planned |
| Deployment | Planned |

---

# Contributing

Contributions are welcome.

## Contribution Workflow

1. Fork the repository
2. Create a feature branch

```bash
git checkout -b feature/your-feature
```

3. Commit changes

```bash
git commit -m "Added new feature"
```

4. Push changes

```bash
git push origin feature/your-feature
```

5. Open a Pull Request

---

# Developer

## Ronit Maheshwari

B.Tech Computer Science Engineering (AI & ML)

AI/ML Developer and Open Source Contributor

---

# License

This project is licensed under the MIT License.

---

<div align="center">

If you found this project useful, consider starring the repository.

Built during GirlScript Summer of Code 2026.

</div>
