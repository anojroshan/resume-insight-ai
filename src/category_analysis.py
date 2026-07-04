import json

from src.config import SKILL_CATEGORIES_PATH


def load_skill_categories():
    with open(SKILL_CATEGORIES_PATH, "r", encoding="utf-8") as file:
        return json.load(file)


def calculate_category_scores(required_skills, matched_skills):
    categories = load_skill_categories()
    category_scores = {}

    required_set = set(required_skills)
    matched_set = set(matched_skills)

    for category, category_skills in categories.items():
        relevant_required = required_set.intersection(set(category_skills))

        if not relevant_required:
            continue

        relevant_matched = matched_set.intersection(relevant_required)

        score = len(relevant_matched) / len(relevant_required) * 100

        category_scores[category] = {
            "score": round(score, 2),
            "required": sorted(relevant_required),
            "matched": sorted(relevant_matched),
            "missing": sorted(relevant_required - relevant_matched)
        }

    return category_scores