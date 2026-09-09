# SIMT AI API

Base URL:

```text
http://127.0.0.1:8000
```

Production URL should be configured according to the deployed backend.

Interactive API documentation:

```text
/docs
```

FastAPI automatically provides Swagger UI, which is the most up-to-date source for the request and response schemas.

---

## POST `/simt`

Main end-to-end recommendation endpoint.

### Request

```json
{
  "text": "I am unemployed and want to start an online clothing business. I need around 12 lakh rupees."
}
```

### Response

```json
{
  "profile": {},
  "matches": [],
  "total_programs_considered": 0
}
```

The actual `profile` and `matches` contain the extracted profile and ranked opportunity data.

### Processing

```text
Text
 ↓
LLM Profile Extraction
 ↓
Eligibility Ranking
 ↓
Semantic RAG Search
 ↓
Hybrid Ranking
 ↓
Top Matches
```

---

## GET `/`

Backend status endpoint.

Example response:

```json
{
  "status": "SIMT AI backend is running",
  "programs_loaded": 10
}
```

`programs_loaded` reflects the number of programs loaded from `programs.json`.

---

## POST `/recommend`

Accepts a structured profile directly and returns ranked program matches.

Example:

```json
{
  "age": 21,
  "province": "Punjab",
  "employment_status": "unemployed",
  "goal": "start a business"
}
```

---

## GET `/programs`

Returns the loaded opportunity catalog.

This endpoint is primarily useful for browsing, debugging, and development.

---

## Error Handling

Common responses include:

```text
400 — Invalid or empty input
500 — Backend matching error
502 — AI service / profile extraction failure
```

For development and testing, visit:

```text
http://127.0.0.1:8000/docs
```

to interact with the API directly.
