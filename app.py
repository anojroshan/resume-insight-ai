import streamlit as st

from src.parser import extract_text
from src.preprocessing import clean_text
from src.ats_optimizer import get_ats_optimization_priorities
from src.report_generator import generate_pdf_report,generate_executive_summary
from src.engines.scoring_engine import analyse_resume
from src.recommendations import (
    generate_resume_suggestions,
    generate_interview_questions
)

def get_hiring_recommendation(final_score):
    if final_score >= 75:
        return "Proceed to Interview", "Strong alignment with the role requirements."
    elif final_score >= 50:
        return "Consider After Tailoring", "Candidate shows partial alignment but should tailor the resume."
    else:
        return "Not Ready for This Role", "Resume has limited alignment with the current job description."


def get_resume_strengths(result):

    strengths = []

    if "Python" in result["matched_skills"]:
        strengths.append("Strong evidence of Python programming experience.")

    if "Machine Learning" in result["matched_skills"]:
        strengths.append("Machine Learning experience is demonstrated.")

    if "Cloud Platforms" in result["matched_skills"]:
        strengths.append("Cloud platform experience identified.")

    if result["semantic_score"] > 60:
        strengths.append("Resume wording closely aligns with the job description.")

    if len(result["evidence"]) >= 3:
        strengths.append("Multiple technical skills are supported with resume evidence.")

    if not strengths:
        strengths.append("Some transferable skills were identified.")

    return strengths


def get_resume_risks(result):

    risks = []

    if result["missing_skills"]:

        top_missing = result["missing_skills"][:5]

        risks.append(
            "Highest priority skill gaps: "
            + ", ".join(top_missing)
        )

    if result["semantic_score"] < 50:

        risks.append(
            "Resume wording could better align with the job description."
        )

    if result["skill_score"] < 40:

        risks.append(
            "Technical skill coverage is below recruiter expectations."
        )

    return risks

def get_score_label(score):
    if score >= 75:
        return "Strong", "🟢"
    elif score >= 50:
        return "Moderate", "🟡"
    else:
        return "Needs Improvement", "🔴"


def get_resume_health(score):
    if score >= 90:
        return "★★★★★"
    elif score >= 75:
        return "★★★★☆"
    elif score >= 60:
        return "★★★☆☆"
    elif score >= 40:
        return "★★☆☆☆"
    else:
        return "★☆☆☆☆"


def calculate_analysis_confidence(result):
    evidence_count = len(result["evidence"])
    matched_count = len(result["matched_skills"])
    required_count = max(len(result["required_skills"]), 1)

    evidence_factor = min(evidence_count / required_count, 1) * 40
    match_factor = min(matched_count / required_count, 1) * 40
    semantic_factor = min(result["semantic_score"] / 100, 1) * 20

    confidence = evidence_factor + match_factor + semantic_factor

    return round(confidence, 2)

def estimate_skill_impact(skill):

    impact = {
        "Python": 5,
        "SQL": 8,
        "AWS": 12,
        "Azure": 12,
        "Power BI": 15,
        "RAG": 18,
        "Docker": 10,
        "Kubernetes": 15,
        "API": 8,
        "YAML": 6,
        "Machine Learning": 10,
        "Data Pipeline": 15,
        "Data Engineering": 18
    }

    return impact.get(skill, 7)

st.set_page_config(
    page_title="Resume Insight AI",
    layout="wide"
)

st.title("Resume Insight AI")
st.caption("AI-powered Resume Intelligence and ATS Optimization Platform")

st.write(
    "Upload a resume and paste a job description to generate a recruiter-style intelligence report "
    "including ATS score, skill coverage, matched evidence, Priority Skills to Develop, improvement suggestions, "
    "and interview preparation questions."
)

st.divider()

st.header("Upload Resume and Job Description")

col1, col2 = st.columns(2)

with col1:
    uploaded_resume = st.file_uploader(
        "Upload Resume",
        type=["pdf", "docx", "txt"]
    )

with col2:
    job_description = st.text_area(
        "Paste Job Description",
        height=250,
        placeholder="Paste the job description here..."
    )

if st.button("Generate Resume Intelligence Report"):
    if uploaded_resume is None:
        st.error("Please upload a resume file.")

    elif not job_description.strip():
        st.error("Please paste a job description.")

    else:
        with st.spinner("Analysing resume..."):
            resume_text = extract_text(uploaded_resume)

            resume_clean = clean_text(resume_text)
            job_clean = clean_text(job_description)

            result = analyse_resume(
                resume_clean,
                job_clean
            )

            suggestions = generate_resume_suggestions(
                result["missing_skills"],
                result["final_score"]
            )

            questions = generate_interview_questions(
                result["missing_skills"],
                result["matched_skills"]
            )
            optimization_priorities = get_ats_optimization_priorities(result)

        st.divider()

        st.header("📊 Resume Intelligence Report")

        score_label, score_icon = get_score_label(result["final_score"])
        confidence = calculate_analysis_confidence(result)
        resume_health = get_resume_health(result["final_score"])

        st.subheader("📋 Executive Summary")
        st.info(generate_executive_summary(result))

        metric1, metric2, metric3, metric4 = st.columns(4)

        metric1.metric("ATS Match Score", f"{result['final_score']:.2f}%")
        metric2.metric("Hiring Fit", f"{score_icon} {score_label}")
        metric3.metric("Resume Health", resume_health)
        if confidence >= 80:
            confidence_label = "High"
        elif confidence >= 60:
            confidence_label = "Medium"
        else:
            confidence_label = "Low"

        metric4.metric(
            "Analysis Confidence",
            f"{confidence:.2f}%",
            confidence_label
        )
        st.progress(float(result["final_score"]) / 100)

        if result["final_score"] >= 75:
            st.success("Strong match for this role.")
        elif result["final_score"] >= 50:
            st.warning("Moderate match. Resume tailoring is recommended.")
        else:
            st.error("Low-to-moderate match. Significant tailoring may be needed.")

        st.divider()

        st.subheader("🎯 Recruiter Summary")

        recommendation, recommendation_reason = get_hiring_recommendation(
            result["final_score"]
        )

        summary_col1, summary_col2 = st.columns(2)

        with summary_col1:
            st.metric("Hiring Recommendation", recommendation)

        with summary_col2:
            st.write("**Reason**")
            st.write(recommendation_reason)

        strengths_col, risks_col = st.columns(2)

        with strengths_col:
            st.subheader("Candidate Strengths")
            for strength in get_resume_strengths(result):
                st.write(f"- {strength}")

        with risks_col:
            st.subheader("Risk Areas")
            for risk in get_resume_risks(result):
                st.write(f"- {risk}")

        st.divider()

        st.subheader("📈 Skill Category Coverage")

        if result["category_scores"]:
            for category, details in result["category_scores"].items():
                st.write(f"**{category}: {details['score']:.2f}%**")
                st.progress(float(details["score"]) / 100)
        else:
            st.write("No skill categories detected.")

        st.divider()

        col_required, col_matched, col_missing = st.columns(3)

        with col_required:
            st.subheader("Required Skills")
            if result["required_skills"]:
                for skill in result["required_skills"]:
                    st.write(f"- {skill}")
            else:
                st.write("No required skills detected.")

        with col_matched:
            st.subheader("✅ Matched Skills")
            if result["matched_skills"]:
                for skill in result["matched_skills"]:
                    st.write(f"- {skill}")
            else:
                st.write("No matched skills found.")

        with col_missing:
            st.subheader("Skills to strengthen")
            if result["missing_skills"]:
                for skill in result["missing_skills"]:
                    st.write(f"- {skill}")
            else:
                st.write("No major skills to strengthen found.")

        st.divider()

        st.header("Evidence Found in Resume")

        if result["evidence"]:
            for skill, evidence in result["evidence"].items():
                st.write(f"**{skill}**")
                st.write(f"> {evidence}")
        else:
            st.write("No supporting evidence found.")

        if result["semantic_matches"]:
            with st.expander("View Semantic Matches"):
                for item in result["semantic_matches"]:
                    st.write(
                        f"**{item['skill']}** matched semantically "
                        f"with score {item['score']}%"
                    )
                    st.write(f"> {item['evidence']}")

        st.divider()

        st.divider()

        st.header("🚀 ATS Optimization Priorities")

        if optimization_priorities:
            st.write(
                "These are the highest-impact improvements based on missing role requirements and skill category gaps."
            )

            priority_cols = st.columns(len(optimization_priorities))

            for col, item in zip(priority_cols, optimization_priorities):
                with col:
                    skill = item["skill"]
                    impact = estimate_skill_impact(skill)

                    st.metric(
                        label=skill,
                        value=f"+{impact}%"
                    )
                    st.write(item["recommendation"])
        else:
            st.write("No major ATS optimization priorities detected.")
        st.header("💡Recommended Resume Improvements")

        for suggestion in suggestions:
            st.write(f"- {suggestion}")

        st.divider()

        st.header("Interview Preparation Questions")

        for question in questions:
            st.write(f"- {question}")
        st.info(
            "This report is intended as a decision-support tool. Results should be reviewed with human judgement and should not be treated as a final hiring decision."
        )
        with st.expander("View Extracted Resume Text"):
            st.write(resume_text[:4000])

        st.divider()

        st.header("⬇️ Download Recruiter Report")

        pdf_report = generate_pdf_report(
            result,
            suggestions,
            questions
        )

        st.download_button(
            label="Download PDF Report",
            data=pdf_report,
            file_name="resume_insight_ai_report.pdf",
            mime="application/pdf"
        )
st.divider()

st.caption(
    """
Resume Insight AI • Version 1.0

Built with Python, Streamlit, Sentence Transformers,
scikit-learn, NLP and ReportLab.

This application provides AI-assisted resume analysis and should be
used as a decision-support tool rather than a replacement for human review.
"""
)