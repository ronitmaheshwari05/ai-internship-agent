<div align="center">

# AI Internship Finder Agent

An AI-powered agent that helps students discover relevant internship opportunities based on their skills and preferred location.

![Python](https://img.shields.io/badge/Python-3.8+-blue?style=flat-square&logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-Frontend-red?style=flat-square&logo=streamlit)
![Mistral](https://img.shields.io/badge/Mistral-AI%20Model-orange?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)
![GSSoC 2026](https://img.shields.io/badge/GSSoC-2026-purple?style=flat-square)

*Built as part of the AI Agents for India track under GirlScript Summer of Code 2026*

</div>

---

## Table of Contents

- [Overview](#overview)
- [Problem Statement](#problem-statement)
- [Solution](#solution)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [System Workflow](#system-workflow)
- [Demo](#demo)
- [Getting Started](#getting-started)
- [Project Structure](#project-structure)
- [Roadmap](#roadmap)
- [Contributing](#contributing)
- [Developer](#developer)

---

## Overview

Finding the right internship is often slow, confusing, and filled with irrelevant listings. The AI Internship Finder Agent simplifies that process using AI.

Users provide their **skills** and **preferred location**, and the system returns structured internship recommendations including company names, work mode (remote/hybrid/onsite), compensation status, expected stipend, duration, and a searchable history of past queries — all presented through a clean card-based UI.

---

## Problem Statement

Students consistently face three core challenges in internship discovery:

| Challenge | Impact |
|---|---|
| Irrelevant listings | Wastes hours of research time |
| No skill-based filtering | Poor match with roles |
| Slow, generic suggestions | Reduces motivation to apply |

---

## Solution

This agent takes a simple two-input approach and converts it into intelligent, structured output.

1. **Input** — Skills + Location
2. **Process** — Mistral LLM processes an optimized prompt
3. **Output** — Structured internship recommendations with direct links to company careers pages

---

## Features

### Phase 1 — Core Agent (Completed)

- Skill-based internship recommendations
- Location-aware filtering
- Mistral LLM integration
- Clean Streamlit UI
- Structured output format

### Phase 2 — Database and User Experience (Completed)

**Backend**
- SQLite to PostgreSQL migration
- Search history storage
- Context-aware prompt memory
- Modular database architecture

**User Experience**
- Recent searches sidebar with one-click reload
- Delete search functionality
- Session state handling

**UI Improvements**
- Work mode filters: Remote / Hybrid / Onsite
- Compensation filters: Paid / Unpaid
- Enhanced internship cards

### Phase 3 — Evaluation (In Progress)

- Evaluation dashboard
- Skill match scoring
- Location relevance scoring
- Format accuracy validation
- Diversity scoring
- Response count validation
- Overall quality score

---

## Tech Stack

| Layer | Technology |
|---|---|
| Language | Python |
| Frontend | Streamlit |
| AI Model | Mistral API |
| Database | PostgreSQL (Neon) |
| Config | python-dotenv |
| Evaluation | Custom Metrics Engine |

---

## System Workflow

```
User Input (Skills + Location)
          |
          v
   Prompt Builder
          |
          v
  Mistral LLM API
          |
          v
  Response Parser
          |
          v
 Streamlit UI Cards
          |
          v
 User → Careers Page
```

---

## Demo

### Current Demo

[Watch the Demo on Google Drive](https://drive.google.com/file/d/18Hk-VCmsGPCC0ZezprhurC6YovvSwNp_/view?usp=sharing)

### Upcoming Demos

| Feature | Status |
|---|---|
| User Authentication Flow | Coming Soon |
| Resume Builder Walkthrough | Coming Soon |
| RAG Integration Preview | Coming Soon |

---

## Getting Started

### Prerequisites

- Python 3.8+
- Mistral API Key
- PostgreSQL database URL (e.g., Neon)

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/ai-internship-agent.git
cd ai-internship-agent
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Set up environment variables

Create a `.env` file in the project root:

```env
MISTRAL_API_KEY=your_api_key
DATABASE_URL=your_postgres_url
```

### 4. Run the application

```bash
streamlit run app.py
```

---

## Project Structure

```
ai-internship-agent/
│
├── app.py
├── README.md
├── requirements.txt
│
├── src/
│   ├── agent/
│   ├── database/
│   ├── evaluation/
│   └── features/
│
├── docs/
│   └── flowcharts/
│
└── tests/
```

---

## Roadmap

| Phase | Feature | Status |
|---|---|---|
| 1 | Core AI agent and Streamlit UI | Done |
| 2 | Database integration and search history | Done |
| 2 | Caching system | Done |
| 3 | Evaluation dashboard | Done |
| 3 | User authentication | Upcoming |
| 4 | Resume builder | Upcoming |
| 4 | RAG integration | Planned |

---

## Contributing

Contributions are welcome. To get started:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/your-feature`)
3. Commit your changes (`git commit -m 'Add your feature'`)
4. Push to the branch (`git push origin feature/your-feature`)
5. Open a Pull Request

---

## Developer

**Ronit Maheshwari**  
B.Tech, Computer Science Engineering (AI & ML)

---

<div align="center">

If you found this project useful, consider starring the repository.

Made with dedication under GirlScript Summer of Code 2026

</div>
