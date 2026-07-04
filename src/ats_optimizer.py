def calculate_skill_impact(skill, result):
    category_scores = result.get("category_scores", {})

    impact = 3

    core_high_impact = {
        "Python",
        "SQL",
        "Machine Learning",
        "Data Engineering",
        "Cloud Platforms",
        "AWS",
        "Azure",
        "RAG",
        "API",
        "Power BI"
    }

    medium_impact = {
        "Docker",
        "YAML",
        "Data Pipeline",
        "Data Quality",
        "ETL",
        "REST API",
        "Dashboard"
    }

    if skill in core_high_impact:
        impact += 6
    elif skill in medium_impact:
        impact += 4
    else:
        impact += 2

    for category, details in category_scores.items():
        if skill in details["missing"]:
            if details["score"] < 50:
                impact += 3
            elif details["score"] < 75:
                impact += 2
            else:
                impact += 1

    return min(impact, 12)


def get_ats_optimization_priorities(result):
    missing_skills = result.get("missing_skills", [])

    priorities = []

    for skill in missing_skills:
        impact = calculate_skill_impact(skill, result)

        priorities.append(
            {
                "skill": skill,
                "estimated_impact": impact,
                "recommendation": (
                    f"Add evidence of {skill} if you genuinely have experience with it."
                )
            }
        )

    priorities = sorted(
        priorities,
        key=lambda item: item["estimated_impact"],
        reverse=True
    )

    return priorities[:5]