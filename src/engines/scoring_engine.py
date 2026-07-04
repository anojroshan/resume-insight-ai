from src.category_analysis import calculate_category_scores

from src.engines.keyword_engine import (
    extract_required_skills,
    exact_match_required_skills
)
from src.engines.semantic_engine import (
    load_embedding_model,
    calculate_text_similarity,
    find_semantic_skill_matches
)
from src.engines.evidence_engine import find_keyword_evidence


def calculate_skill_score(matched_skills, required_skills):
    if not required_skills:
        return 0

    return round(len(matched_skills) / len(required_skills) * 100, 2)


def calculate_final_score(skill_score, semantic_score):
    final_score = (0.6 * skill_score) + (0.4 * semantic_score)
    return round(float(final_score), 2)


def analyse_resume(resume_text, job_description_text):
    model = load_embedding_model()

    required_skills = extract_required_skills(job_description_text)

    keyword_result = exact_match_required_skills(
        resume_text,
        required_skills
    )

    semantic_matches = find_semantic_skill_matches(
        resume_text,
        keyword_result["missing_skills"],
        model
    )

    semantic_skill_names = [
        item["skill"] for item in semantic_matches
    ]

    matched_skills = sorted(
        set(keyword_result["matched_skills"] + semantic_skill_names)
    )

    missing_skills = sorted(
        set(required_skills) - set(matched_skills)
    )

    skill_score = calculate_skill_score(
        matched_skills,
        required_skills
    )

    semantic_score = calculate_text_similarity(
        resume_text,
        job_description_text,
        model
    )

    final_score = calculate_final_score(
        skill_score,
        semantic_score
    )

    category_scores = calculate_category_scores(
        required_skills,
        matched_skills
    )

    keyword_evidence = find_keyword_evidence(
        resume_text,
        keyword_result["matched_skills"]
    )

    semantic_evidence = {
        item["skill"]: item["evidence"] for item in semantic_matches
    }

    evidence = {
        **keyword_evidence,
        **semantic_evidence
    }

    return {
        "final_score": final_score,
        "category_scores": category_scores,
        "skill_score": skill_score,
        "semantic_score": semantic_score,
        "required_skills": required_skills,
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "keyword_matches": keyword_result["matched_skills"],
        "semantic_matches": semantic_matches,
        "evidence": evidence
    }