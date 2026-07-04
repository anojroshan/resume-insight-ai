from src.skills import load_skills_database, alias_exists_in_text


def split_into_sentences(text):
    sentences = text.split(".")
    sentences = [sentence.strip() for sentence in sentences if sentence.strip()]
    return sentences


def find_keyword_evidence(resume_text, matched_skills):
    skills_database = load_skills_database()
    sentences = split_into_sentences(resume_text)

    evidence = {}

    for skill in matched_skills:
        aliases = skills_database.get(skill, [])

        for sentence in sentences:
            for alias in aliases:
                if alias_exists_in_text(alias, sentence):
                    evidence[skill] = sentence
                    break

            if skill in evidence:
                break

    return evidence