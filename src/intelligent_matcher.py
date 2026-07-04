from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

from src.skills import load_skills_database, alias_exists_in_text


MODEL_NAME = "all-MiniLM-L6-v2"


def load_model():
    return SentenceTransformer(MODEL_NAME)


def extract_required_skills(job_description_text):
    skills_database = load_skills_database()
    required_skills = []

    for skill, aliases in skills_database.items():
        for alias in aliases:
            if alias_exists_in_text(alias, job_description_text):
                required_skills.append(skill)
                break

    return sorted(set(required_skills))


def exact_skill_match(skill, resume_text):
    skills_database = load_skills_database()
    aliases = skills_database.get(skill, [])

    for alias in aliases:
        if alias_exists_in_text(alias, resume_text):
            return True

    return False


def split_into_sentences(text):
    sentences = text.split(".")
    sentences = [sentence.strip() for sentence in sentences if sentence.strip()]
    return sentences


def semantic_skill_match(skill, resume_text, model, threshold=0.30):
    sentences = split_into_sentences(resume_text)

    if not sentences:
        return False, 0

    skill_embedding = model.encode([skill])
    sentence_embeddings = model.encode(sentences)

    scores = cosine_similarity(skill_embedding, sentence_embeddings)[0]
    best_score = max(scores)

    return best_score >= threshold, round(float(best_score) * 100, 2)


def analyse_resume_against_job(resume_text, job_description_text):
    model = load_model()

    required_skills = extract_required_skills(job_description_text)

    matched_skills = []
    missing_skills = []
    semantic_matches = []

    for skill in required_skills:
        if exact_skill_match(skill, resume_text):
            matched_skills.append(skill)
        else:
            semantic_match, semantic_score = semantic_skill_match(
                skill,
                resume_text,
                model
            )

            if semantic_match:
                matched_skills.append(skill)
                semantic_matches.append({
                    "skill": skill,
                    "semantic_score": semantic_score
                })
            else:
                missing_skills.append(skill)

    if required_skills:
        skill_score = len(matched_skills) / len(required_skills) * 100
    else:
        skill_score = 0

    return {
        "required_skills": required_skills,
        "matched_skills": sorted(set(matched_skills)),
        "missing_skills": sorted(set(missing_skills)),
        "semantic_matches": semantic_matches,
        "skill_score": round(skill_score, 2)
    }