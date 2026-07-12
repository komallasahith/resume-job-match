"""
Streamlit interface for the Resume-to-Job Match Agent.

Run with:
    streamlit run app.py
"""

import streamlit as st
from matcher import run_agent

st.set_page_config(page_title="Resume-to-Job Match Agent", layout="wide")

st.title("🎯 Resume-to-Job Match Agent")
st.caption(
    "Paste your resume and a few job descriptions. "
    "The agent scores each one, explains why, and drafts a cover note "
    "for the ones actually worth applying to."
)

col1, col2 = st.columns(2)

with col1:
    resume_text = st.text_area(
        "Paste your resume text here",
        height=300,
        placeholder="Paste your resume content (skills, projects, experience)...",
    )

with col2:
    jobs_raw = st.text_area(
        "Paste job descriptions — separate each one with a line containing only ---",
        height=300,
        placeholder="Job description 1...\n---\nJob description 2...\n---\nJob description 3...",
    )

threshold = st.slider(
    "Minimum match score to generate a cover note", min_value=0, max_value=100, value=60
)

if st.button("Run Agent", type="primary"):
    if not resume_text.strip() or not jobs_raw.strip():
        st.warning("Please paste both your resume and at least one job description.")
    else:
        job_list = [j.strip() for j in jobs_raw.split("---") if j.strip()]

        with st.spinner(f"Agent is analyzing {len(job_list)} job description(s)..."):
            results = run_agent(resume_text, job_list, threshold=threshold)

        st.success(f"Done — analyzed {len(results)} job(s).")

        for i, r in enumerate(results, start=1):
            with st.expander(
                f"#{i} — {r.get('job_title_guess', 'Unknown role')} — Match Score: {r['match_score']}/100"
            ):
                st.write("**Why this score:**")
                for reason in r.get("reasons", []):
                    st.write(f"- {reason}")

                if r.get("missing_skills"):
                    st.write("**Missing / weak skills for this role:**")
                    st.write(", ".join(r["missing_skills"]))

                if r.get("cover_note"):
                    st.write("**Drafted cover note:**")
                    st.info(r["cover_note"])
                else:
                    st.write(
                        f"_Score below threshold ({threshold}) — no cover note generated._"
                    )
