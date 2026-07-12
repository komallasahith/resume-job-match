"""
Quick test to see matcher.py working with a real (tiny) example,
before we connect it to the Streamlit UI.

Run with:
    python test_matcher.py
"""

from matcher import run_agent

sample_resume = """
Sahith Komalla
B.Tech CSE (AI & ML), 3rd year

Skills: Python, Java, C, HTML, CSS, SQL
Projects: Full-stack web app (IoT dashboard), Financial tracker app,
Database design project.
Currently learning: Machine Learning, building AI agent projects.
"""

sample_jobs = [
    """Software Engineer Intern - Backend
We need someone comfortable with Python, SQL, and building REST APIs.
Experience with databases is a plus. Freshers welcome.""",

    """Senior Machine Learning Engineer
Requires 5+ years experience with PyTorch, deploying ML models at scale,
and leading a team of engineers. PhD preferred.""",
]

if __name__ == "__main__":
    results = run_agent(sample_resume, sample_jobs, threshold=50)

    for r in results:
        print("=" * 50)
        print(f"Job: {r['job_title_guess']}")
        print(f"Match Score: {r['match_score']}")
        print(f"Reasons: {r['reasons']}")
        print(f"Missing skills: {r['missing_skills']}")
        if r["cover_note"]:
            print(f"\nCover note:\n{r['cover_note']}")
        print()
