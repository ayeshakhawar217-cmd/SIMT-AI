# Eligibility Engine

The eligibility engine evaluates structured user profiles against program requirements.

## Input

The engine receives attributes such as:

* age
* city
* province
* gender
* employment status
* business stage
* sector
* goal
* funding required
* education level
* income
* additional flags

## Evaluation

Each program contains eligibility requirements.

The engine compares the user's profile against these requirements and produces:

```text
Eligible / Not Eligible
Eligibility Score
Program Match Information
```

Programs are then ranked based on eligibility.

## Why Deterministic Rules?

Eligibility should not depend on an LLM guessing whether someone qualifies.

For example:

```text
Required age: 18–30
User age: 21
→ Pass
```

This makes the decision:

* reproducible
* explainable
* easier to test
* less vulnerable to hallucination

## Final Ranking

Eligibility is combined with semantic relevance in the main `/simt` pipeline.

The system returns a maximum of **8 top matches**, while maintaining a minimum result floor so users are not unnecessarily given an empty recommendation list.
