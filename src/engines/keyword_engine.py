from src.skills import load_skills_database, alias_exists_in_text


def extract_required_skills(job_description_text):
    skills_database = load_skills_database()
    required_skills = []

    for skill, aliases in skills_database.items():
        for alias in aliases:
            if alias_exists_in_text(alias, job_description_text):
                required_skills.append(skill)
                break

    return sorted(set(required_skills))


def exact_match_required_skills(resume_text, required_skills):
    skills_database = load_skills_database()

    matched_skills = []
    missing_skills = []

    for skill in required_skills:
        aliases = skills_database.get(skill, [])

        found = False
        for alias in aliases:
            if alias_exists_in_text(alias, resume_text):
                found = True
                break

        if found:
            matched_skills.append(skill)
        else:
            missing_skills.append(skill)

    return {
        "matched_skills": sorted(set(matched_skills)),
        "missing_skills": sorted(set(missing_skills))
    }