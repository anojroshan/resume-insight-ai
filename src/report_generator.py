from io import BytesIO

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer


def generate_pdf_report(result, suggestions, questions):
    buffer = BytesIO()

    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        title="Resume Insight AI Report"
    )

    styles = getSampleStyleSheet()
    story = []

    story.append(Paragraph("Resume Insight AI", styles["Title"]))
    story.append(Paragraph("Recruiter-Style Resume Intelligence Report", styles["Heading2"]))
    story.append(Spacer(1, 12))

    story.append(Paragraph("Screening Scores", styles["Heading2"]))
    story.append(Paragraph(f"ATS Match Score: {result['final_score']:.2f}%", styles["Normal"]))
    story.append(Paragraph(f"Skill Match Score: {result['skill_score']:.2f}%", styles["Normal"]))
    story.append(Paragraph(f"Semantic Similarity: {result['semantic_score']:.2f}%", styles["Normal"]))
    story.append(Spacer(1, 12))

    story.append(Paragraph("Matched Skills", styles["Heading2"]))
    for skill in result["matched_skills"]:
        story.append(Paragraph(f"- {skill}", styles["Normal"]))
    story.append(Spacer(1, 12))

    story.append(Paragraph("Skills to Strengthen", styles["Heading2"]))
    for skill in result["missing_skills"]:
        story.append(Paragraph(f"- {skill}", styles["Normal"]))
    story.append(Spacer(1, 12))

    story.append(Paragraph("Matched Skill Evidence", styles["Heading2"]))
    for skill, evidence in result["evidence"].items():
        story.append(Paragraph(f"<b>{skill}</b>: {evidence}", styles["Normal"]))
    story.append(Spacer(1, 12))

    story.append(Paragraph("Resume Improvement Suggestions", styles["Heading2"]))
    for suggestion in suggestions:
        story.append(Paragraph(f"- {suggestion}", styles["Normal"]))
    story.append(Spacer(1, 12))

    story.append(Paragraph("Interview Preparation Questions", styles["Heading2"]))
    for question in questions:
        story.append(Paragraph(f"- {question}", styles["Normal"]))

    doc.build(story)

    buffer.seek(0)
    return buffer

def generate_executive_summary(result):

    score = result["final_score"]

    matched = len(result["matched_skills"])
    missing = len(result["missing_skills"])

    if score >= 75:
        return (
            f"The candidate demonstrates strong alignment with the role. "
            f"The resume provides evidence for {matched} important technical skills while only "
            f"{missing} role-specific skills require further strengthening. "
            f"The candidate appears suitable for interview consideration."
        )

    elif score >= 50:
        return (
            f"The candidate demonstrates partial alignment with the position. "
            f"Several required skills are present, however {missing} important requirements are "
            f"either missing or not clearly demonstrated. Resume tailoring is recommended."
        )

    else:
        return (
            f"The resume currently demonstrates limited alignment with this position. "
            f"Only {matched} required skills were identified while {missing} important skills "
            f"are missing or lack sufficient evidence. Significant resume tailoring is recommended before applying."
        )