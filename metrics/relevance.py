from sklearn.metrics.pairwise import cosine_similarity
from utils.embeddings import embed


def relevance_score(user_query, ai_response):
    q_emb = embed(user_query)
    r_emb = embed(ai_response)
    score = cosine_similarity(q_emb, r_emb)[0][0]
    return round(float(score), 3)