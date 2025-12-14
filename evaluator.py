import json
from utils.json_loader import load_json
from metrics.relevance import relevance_score
from metrics.hallucination import hallucination_check
from metrics.latency_cost import estimate_cost


conversation = load_json("sample_data/sample-chat-conversation-02.json")
context = load_json("sample_data/sample_context_vectors-02.json")


user_msg = [t for t in conversation['conversation_turns'] if t['role'] == 'User'][-1]['message']
ai_response = " ".join(context['data']['sources']['final_response'])


context_texts = [
    v.get("text", "")
    for v in context.get("data", {}).get("vector_data", [])
    if v.get("text")
]
ai_sentences = ai_response.split('.')


relevance = relevance_score(user_msg, ai_response)
hallu_score, unsupported = hallucination_check(ai_sentences, context_texts)


token_estimate = sum(len(s.split()) for s in ai_response.split())
cost = estimate_cost(token_estimate)


report = {
    "relevance_score": relevance,
    "hallucination_score": hallu_score,
    "unsupported_claims": unsupported,
    "estimated_tokens": token_estimate,
    "estimated_cost_usd": cost
}


with open("output/evaluation_report.json", "w") as f:
    json.dump(report, f, indent=2)


print("Evaluation completed")