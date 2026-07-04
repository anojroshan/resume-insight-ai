from src.skills import compare_skills
from src.similarity import calculate_similarity


def calculate_skill_match_score(matched_skills, job_skills):
    if not job_skills:
        return 0

    score = len(matched_skills) / len(job_skills) * 100
    return round(score, 2)


def calculate_final_score(resume_text, job_description_text):
    skill_result = compare_skills(resume_text, job_description_text)

    skill_score = calculate_skill_match_score(
        skill_result["matched_skills"],
        skill_result["job_skills"]
    )

    semantic_score = calculate_similarity(
        resume_text,
        job_description_text
    )

    final_score = (0.6 * skill_score) + (0.4 * semantic_score)

    return {
        "final_score": round(final_score, 2),
        "skill_score": skill_score,
        "semantic_score": semantic_score,
        "resume_skills": skill_result["resume_skills"],
        "job_skills": skill_result["job_skills"],
        "matched_skills": skill_result["matched_skills"],
        "missing_skills": skill_result["missing_skills"]
    }