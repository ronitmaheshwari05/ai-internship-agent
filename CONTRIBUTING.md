# Contributing to AI Internship Finder Agent

Thanks for your interest in contributing! This project is part of **GirlScript Summer of Code 2026** and welcomes contributions from everyone.

---

## 📋 Before You Start

- Check the [Issues](../../issues) tab for open tasks before starting anything new
- Comment on an issue to get it assigned to you — avoid working on unassigned issues
- One pull request per issue keeps reviews clean and fast

---

## 🛠️ Setting Up Locally

```bash
# 1. Fork the repo, then clone your fork
git clone https://github.com/your-username/ai-internship-finder.git
cd ai-internship-finder

# 2. Install dependencies
pip install -r requirements.txt

# 3. Add your API key
cp .env.example .env
# Then open .env and paste your MISTRAL_API_KEY

# 4. Run the app
streamlit run app.py
```

---

## 🔀 Contribution Workflow

```
1. Fork → 2. Branch → 3. Code → 4. Commit → 5. Push → 6. Pull Request
```

### Branch naming

| Type | Format | Example |
|------|--------|---------|
| New feature | `feature/short-description` | `feature/search-history` |
| Bug fix | `fix/short-description` | `fix/location-filter-crash` |
| Docs | `docs/short-description` | `docs/update-readme` |
| Refactor | `refactor/short-description` | `refactor/prompt-template` |

### Commit messages

Keep commits short and descriptive:

```
feat: add location autocomplete to search bar
fix: handle empty skill input gracefully
docs: add setup instructions to README
refactor: move prompt logic to separate module
```

---

## ✅ Pull Request Checklist

Before opening a PR, make sure:

- [ ] Your branch is up to date with `main`
- [ ] The app runs without errors (`streamlit run app.py`)
- [ ] No API keys or `.env` files are committed
- [ ] Code is clean and reasonably commented
- [ ] PR description explains **what** you changed and **why**

---

## 🚫 What to Avoid

- Don't push directly to `main`
- Don't include your `MISTRAL_API_KEY` anywhere in the code
- Don't open a PR for an issue that isn't assigned to you
- Don't make large sweeping changes without discussing in the issue first

---

## 💡 Ideas to Contribute

Not sure where to start? Here are some good first areas:

- Improving the prompt template for better suggestions
- Adding input validation to the Streamlit UI
- Writing tests for the agent logic
- Improving the card UI styling
- Adding a loading spinner or skeleton state

---

## 🙋 Need Help?

Open a [GitHub Discussion](../../discussions) or comment on the relevant issue. The maintainer will get back to you.

---

*Happy contributing! Every PR, big or small, makes this project better.* 🚀
