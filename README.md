# LLM Response Evaluation Pipeline

## Overview

This project evaluates AI-generated responses in real time using conversation history and retrieved context documents.

The goal is to automatically assess **answer quality, factual grounding, and operational efficiency** without relying on manual review.

---

## Metrics

* Response Relevance & Completeness
* Hallucination / Faithfulness
* Latency & Cost Estimation

---

## Pipeline Architecture

```wasm
conversation.json ─┐
                   ├──► Evaluation Pipeline
context.json ──────┘            │
                                ├─ Relevance & Completeness Scorer
                                ├─ Hallucination / Faithfulness Checker
                                ├─ Latency & Cost Tracker
                                │
                                ▼
                    evaluation_report.json
```

---

## Evaluation Strategy

### 1. Response Relevance & Completeness

**Objective:** Measure how well the AI answers the latest user query.

**Approach:**

* Extract the last user message
* Generate embeddings for:

  * User query
  * AI final response
* Compute cosine similarity

**Output:**

* `relevance_score` (0–1)

---

### 2. Hallucination / Factual Accuracy

**Key Idea:**

```
If the AI claims something that is NOT supported by retrieved context → hallucination
```

**Approach:**

* Split AI response into sentences
* Embed each sentence
* Compare against retrieved context chunks
* Flag sentences below a similarity threshold

**Output:**

* `hallucination_score`
* `unsupported_claims[]`

---

### 3. Latency & Costs

**Measured by:**

* Token count estimation
* Cost estimation per 1K tokens

---

## Why This Design?

This solution was designed to be **simple, fast, and scalable**.

* Embedding-based evaluation avoids expensive LLM-as-a-judge calls, reducing cost and latency
* Modular scorers allow independent tuning and easy extension
* No dependency on external APIs makes the pipeline reliable at scale
* Context-grounded evaluation ensures hallucinations are detected using actual retrieved data

This approach balances **accuracy, speed, and operational efficiency**, which is critical for real-time production systems.

---

## Scalability & Cost Efficiency

To support millions of daily evaluations:

* Lightweight embedding models minimize inference time
* Embeddings can be cached and batch-processed
* No additional LLM calls are required during evaluation
* The pipeline is async-ready and cloud-deployable

---

## Repository Structure

```wasm
llm-eval-pipeline/
│
├── evaluator.py
├── metrics/
│       ├── relevance.py
│       ├── hallucination.py
│       └── latency_cost.py
│
├── utils/
│       ├── embeddings.py
│       └── json_loader.py
│
├── sample_data/
│       ├── sample-chat-conversation-01.json
│       ├── sample-chat-conversation-02.json
│       ├── sample_context_vectors-01.json
│       └── sample_context_vectors-02.json
│
├── output/
│       └── evaluation_report.json
│
├── requirements.txt
└── README.md
```

---

## Local Setup

```bash
pip install -r requirements.txt
python evaluator.py
```
