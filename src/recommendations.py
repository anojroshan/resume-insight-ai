def generate_resume_suggestions(missing_skills, final_score):
    suggestions = []

    if final_score < 50:
        suggestions.append(
            "The resume has a low-to-moderate match with the job description. Consider tailoring the resume more closely to the role."
        )
    elif final_score < 75:
        suggestions.append(
            "The resume has a moderate match. Improving skill alignment and project descriptions may increase the score."
        )
    else:
        suggestions.append(
            "The resume has a strong match with the job description. Minor refinements may further improve clarity."
        )

    if missing_skills:
        suggestions.append(
            "Add relevant missing skills only if you genuinely have experience with them: "
            + ", ".join(missing_skills[:6])
        )

    suggestions.append(
        "Use clear project bullet points that mention the problem, tools used, model or method applied, and measurable outcome."
    )

    suggestions.append(
        "Include links to GitHub repositories, deployed applications, or portfolio projects where possible."
    )

    suggestions.append(
        "Use keywords from the job description naturally in the professional summary and project descriptions."
    )

    return suggestions


def generate_interview_questions(missing_skills, matched_skills):
    questions = []

    for skill in matched_skills[:5]:
        questions.append(f"Can you explain how you used {skill} in a project?")

    for skill in missing_skills[:5]:
        questions.append(f"The job mentions {skill}. What is your current understanding of it?")

    questions.append("Can you explain one end-to-end AI or machine learning project you have built?")
    questions.append("How would you improve this resume for the specific job description?")

    return questions