"""
Core agent logic for Resume-to-Job Match Agent.

This module does the "thinking" part:
1. Takes a resume + a job description
2. Asks an LLM to score the match, explain why, and list missing skills
3. If the match is good enough, generates a tailored cover note

This is the "agent" piece — it loops over multiple jobs on its own,
decides which ones are worth acting on, and only then generates
a cover note (instead of doing it for every single job blindly).
"""

import os
import json
from groq import Groq

# Reads your API key from an environment variable so you never
# hardcode it into the file. Set it before running:
#   export GROQ_API_KEY="your-key-here"
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

MODEL = "llama-3.3-70b-versatile"  # free model on Groq

MATCH_PROMPT = """You are a strict, no-nonsense career advisor. Compare the RESUME below
against the JOB DESCRIPTION. Be honest, not encouraging for the sake of it.

RESUME:
{resume}

JOB DESCRIPTION:
{job_description}

Respond ONLY with valid JSON, no extra text, in this exact format:
{{
  "match_score": <integer 0-100>,
  "reasons": ["reason 1", "reason 2", "reason 3"],
  "missing_skills": ["skill 1", "skill 2"],
  "job_title_guess": "short guessed job title from the description"
}}
"""

COVER_NOTE_PROMPT = """Write a short, specific, non-generic cover note (max 120 words) for this candidate
applying to this job. Use details from their resume. Do not use cliches like
"I am excited to apply" or "team player". Be direct and specific.

RESUME:
{resume}

JOB DESCRIPTION:
{job_description}
"""


def _ask_llm(prompt: str) -> str:
    """Single helper to call the Groq API and return plain text."""
    response = client.chat.completions.create(
        model=MODEL,
        max_tokens=1000,
        messages=[{"role": "user", "content": prompt}],
    )
    return response.choices[0].message.content


def score_match(resume: str, job_description: str) -> dict:
    """Ask the LLM to score one resume against one job description."""
    prompt = MATCH_PROMPT.format(resume=resume, job_description=job_description)
    raw = _ask_llm(prompt)

    # Clean up in case the model wraps JSON in ```json fences
    cleaned = raw.strip().removeprefix("```json").removeprefix("```").removesuffix("```").strip()

    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        # Fallback if the model didn't return clean JSON
        return {
            "match_score": 0,
            "reasons": ["Could not parse model response"],
            "missing_skills": [],
            "job_title_guess": "Unknown",
        }


def generate_cover_note(resume: str, job_description: str) -> str:
    """Generate a tailored cover note for a good match."""
    prompt = COVER_NOTE_PROMPT.format(resume=resume, job_description=job_description)
    return _ask_llm(prompt)


def run_agent(resume: str, job_descriptions: list[str], threshold: int = 60) -> list[dict]:
    """
    The actual 'agent loop':
    - Scores every job description
    - Only generates a cover note for jobs above the threshold score
    - Returns everything ranked by match score, highest first

    This loop + conditional decision-making (skip low matches,
    act only on good ones) is what makes this an agent rather than
    a single one-shot prompt.
    """
    results = []

    for jd in job_descriptions:
        jd = jd.strip()
        if not jd:
            continue

        match = score_match(resume, jd)
        match["job_description"] = jd

        if match["match_score"] >= threshold:
            match["cover_note"] = generate_cover_note(resume, jd)
        else:
            match["cover_note"] = None  # not worth writing one

        results.append(match)

    # Rank best matches first
    results.sort(key=lambda x: x["match_score"], reverse=True)
    return results
