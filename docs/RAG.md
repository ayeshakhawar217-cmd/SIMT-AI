# Retrieval-Augmented Opportunity Matching

SIMT AI uses semantic retrieval to understand whether a program is relevant to what the user actually wants.

## Pipeline

```text
Program Data
    ↓
Text Representation
    ↓
Sentence Transformer Embeddings
    ↓
Supabase / pgvector
    ↓
Similarity Search
    ↓
Semantic Relevance Score
```

The user's original situation is embedded and compared against stored program representations.

## Why RAG?

Keyword search can miss relevant programs when the user uses different wording.

For example:

> "I want money to start a clothing business"

may be relevant to a program described as:

> "financing support for small-scale textile entrepreneurs."

Semantic search can recognize this relationship even without exact keyword matches.

## Hybrid Ranking

SIMT combines:

* **Eligibility score:** whether the user satisfies program criteria
* **Semantic score:** how relevant the program is to the user's stated situation

Current final score:

```text
55% Eligibility
45% Semantic Relevance
```

Eligible programs are always prioritized over ineligible programs.

RAG is an enhancement to the eligibility engine rather than a replacement for it.

