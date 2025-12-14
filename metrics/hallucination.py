from sklearn.metrics.pairwise import cosine_similarity
from utils.embeddings import embed


def hallucination_check(ai_sentences, context_chunks, threshold=0.65):
    hallucinations = []


    context_embs = embed(context_chunks)


    for sent in ai_sentences:
        sent_emb = embed(sent)
        sims = cosine_similarity(sent_emb, context_embs)[0]
        if max(sims) < threshold:
            hallucinations.append(sent)


    score = 1 - (len(hallucinations) / max(len(ai_sentences), 1))
    return round(score, 3), hallucinations