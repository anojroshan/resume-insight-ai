from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


MODEL_NAME = "all-MiniLM-L6-v2"


def load_embedding_model():
    return SentenceTransformer(MODEL_NAME)


def split_into_sentences(text):
    sentences = text.split(".")
    sentences = [sentence.strip() for sentence in sentences if sentence.strip()]
    return sentences


def calculate_text_similarity(resume_text, job_description_text, model):
    embeddings = model.encode(
        [resume_text, job_description_text],
        convert_to_tensor=False
    )

    score = cosine_similarity(
        [embeddings[0]],
        [embeddings[1]]
    )[0][0]

    return round(float(score) * 100, 2)


def find_semantic_skill_matches(resume_text, missing_skills, model, threshold=0.45):
    sentences = split_into_sentences(resume_text)
    semantic_matches = []

    if not sentences:
        return semantic_matches

    sentence_embeddings = model.encode(sentences)

    for skill in missing_skills:
        skill_embedding = model.encode([skill])
        scores = cosine_similarity(skill_embedding, sentence_embeddings)[0]

        best_index = scores.argmax()
        best_score = float(scores[best_index])

        if best_score >= threshold:
            semantic_matches.append(
                {
                    "skill": skill,
                    "score": round(best_score * 100, 2),
                    "evidence": sentences[best_index]
                }
            )

    return semantic_matches