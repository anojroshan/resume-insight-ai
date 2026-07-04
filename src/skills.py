import json
import re

from src.config import SKILLS_PATH


def load_skills_database():
    with open(SKILLS_PATH, "r", encoding="utf-8") as file:
        return json.load(file)


def normalise_text(text):
    text = text.lower()
    text = text.replace("-", " ")
    text = re.sub(r"\s+", " ", text).strip()
    return text


def alias_exists_in_text(alias, text):
    alias = normalise_text(alias)
    text = normalise_text(text)

    pattern = r"(?<![a-zA-Z0-9])" + re.escape(alias) + r"(?![a-zA-Z0-9])"

    return re.search(pattern, text) is not None


def extract_skills(text):
    skills_database = load_skills_database()
    found_skills = []

    for skill, aliases in skills_database.items():
        for alias in aliases:
            if alias_exists_in_text(alias, text):
                found_skills.append(skill)
                break

    return sorted(set(found_skills))


def compare_skills(resume_text, job_description_text):
    resume_skills = extract_skills(resume_text)
    job_skills = extract_skills(job_description_text)

    matched_skills = sorted(set(resume_skills).intersection(set(job_skills)))
    missing_skills = sorted(set(job_skills).difference(set(resume_skills)))

    return {
        "resume_skills": resume_skills,
        "job_skills": job_skills,
        "matched_skills": matched_skills,
        "missing_skills": missing_skills
    }