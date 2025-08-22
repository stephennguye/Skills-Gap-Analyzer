import streamlit as st
import pandas as pd
from core.config import AppConfig
from core.logger import get_logger
from core.exceptions import SkillGapError
from nlp.parse_resume import extract_text
from nlp.skill_extractor import load_taxonomy, extract_skills
from jobs.skill_profile_builder import synthesize_required_skills
from scoring.matcher import skill_match_scores, overall_match
from recommender.course_recommender import recommend_courses
from utils.plotting import overall_gauge

st.set_page_config(page_title="AI Skill Gap Analyzer", page_icon="🧭", layout="wide")
log = get_logger()
cfg = AppConfig()

st.title("🧭 AI Skill Gap Analyzer")
st.caption("Upload your resume and choose a target job to discover gaps and recommended learning paths")

with st.sidebar:
    st.header("Start here: Select & Upload")
    job = st.selectbox("Target role", ["Data Scientist", "Machine Learning Engineer", "Data Analyst"])
    uploaded = st.file_uploader("Upload your resume (PDF/DOCX/TXT)", type=["pdf", "docx", "doc", "txt"])
    run_btn = st.button("Analyze", type="primary")

if run_btn:
    if not uploaded:
        st.error("Please upload a resume file.")
        st.stop()
    try:
        resume_text = extract_text(uploaded.read(), uploaded.name)
        st.session_state["resume_text"] = resume_text
        st.success("Resume parsed successfully")
    except SkillGapError as e:
        st.exception(e)
        st.stop()

    # Required skills (synthesized)
    try:
        required_skills = synthesize_required_skills(job, cfg)
        st.session_state["required_skills"] = required_skills
    except Exception as e:
        st.exception(e)
        st.stop()

    # Extract skills from resume 
    taxonomy = load_taxonomy(cfg)
    resume_skill_counts = extract_skills(resume_text, taxonomy, extra_terms=required_skills)

    # Semantic matching
    scores = skill_match_scores(resume_text, required_skills, cfg)
    ovr = overall_match(scores)

    st.subheader("Overall Skill Match")
    st.plotly_chart(overall_gauge(ovr), use_container_width=True)

    st.progress(ovr)
    st.caption(f"Overall match: {round(ovr*100, 1)}%")

    st.subheader("Skill Gaps")
    gap_threshold = 0.6
    gaps = [s for s, v in scores.items() if v < gap_threshold]

    if gaps:
        st.write("⚠️ Missing or weak skills:")
        st.write(", ".join(sorted(gaps)))
    else:
        st.success("No major gaps detected 🎉")

    # Show lexical evidence
    with st.expander("Show detected skills from resume (keyword hits)"):
        if resume_skill_counts:
            df_hits = pd.DataFrame(
                [{"skill": k, "mentions": v} for k, v in sorted(resume_skill_counts.items(), key=lambda x: -x[1])]
            )
            st.dataframe(df_hits, use_container_width=True)
        else:
            st.write("No explicit skills detected from taxonomy. (Semantic match may still capture them.)")

    # Gaps & recommendations
    st.subheader("Recommendations to close gaps")
    recs = recommend_courses(gaps, cfg, top_k=10)
    if len(recs):
        st.dataframe(recs.assign(similarity=(recs["similarity"] * 100).round(1)), use_container_width=True)
    else:
        st.info("No course data available. Add more entries to data/courses_sample.csv.")

    st.divider()
    st.caption(
        "Tip: Turn on web enrichment in core/config.py and add connectors in web_enrichment/sources.py for live job skills & course crawling."
    )
else:
    st.info("Upload a resume and click **Analyze** to begin.")
