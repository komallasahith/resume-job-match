# Resume-to-Job Match Agent
🔗 **Live demo:** [resume-job-match-p1.streamlit.app](https://resume-job-match-p1.streamlit.app)

An AI agent that compares your resume against multiple job descriptions,
scores each match, explains its reasoning, and drafts tailored cover notes
for the roles actually worth applying to.

## Why this is an "agent" and not just a chatbot

Instead of a single one-shot prompt, this tool:
1. Loops through multiple job descriptions on its own
2. Makes a decision at each step (is this match good enough to act on?)
3. Only generates a cover note for jobs above a score threshold — it
   doesn't waste effort writing notes for weak matches

This planning + conditional action loop is what separates an "agent"
from a plain LLM call.

## How it works

1. Paste your resume text and a batch of job descriptions
2. The agent scores each job (0-100) with reasoning and missing skills
3. For strong matches, it drafts a short, specific cover note
4. Results are ranked best-match first

## Setup

```bash
pip install -r requirements.txt
export GROQ_API_KEY="your-api-key-here"
streamlit run app.py
```

Get a free API key at [console.groq.com](https://console.groq.com) — no credit card required.

## Tech stack

- Python
- Groq API (free LLM inference — Llama 3.3 70B) for reasoning + scoring
- Streamlit (UI)

## Possible v2 upgrades

- Pull job descriptions automatically from a job board API (e.g. Adzuna)
  instead of manual paste
- Store results in a spreadsheet/SQLite so you can track applications
  over time
- Add a Playwright script to auto-fill (not auto-submit) application
  forms on sites that allow it
