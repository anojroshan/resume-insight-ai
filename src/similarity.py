from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


MODEL_NAME = "all-MiniLM-L6-v2"


def load_embedding_model():
    model = SentenceTransformer(MODEL_NAME)
    return model


def calculate_similarity(resume_text, job_description_text):
    model = load_embedding_model()

    embeddings = model.encode(
        [resume_text, job_description_text],
        convert_to_tensor=False
    )

    similarity_score = cosine_similarity(
        [embeddings[0]],
        [embeddings[1]]
    )[0][0]

    return round(similarity_score * 100, 2)