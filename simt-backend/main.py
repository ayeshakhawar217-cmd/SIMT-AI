"""
main.py
SIMT AI — backend API.
Run with: uvicorn main:app --reload
Then open: http://127.0.0.1:8000/docs to test it in the browser.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, Dict
from eligibility import load_programs, rank_programs
from extract_profile import extract_profile
from rag import search_programs

app = FastAPI(title="SIMT AI Backend")

# Allows your frontend (running on a different port) to call this API.
# Fine to leave wide open for the hackathon build.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

PROGRAMS = load_programs("programs.json")

# Never dump the whole catalog back at the user — that's what makes an
# AI product feel like an unfiltered database instead of a curated
# recommendation. Cap results, and drop anything too weak a match to
# be worth showing, while always guaranteeing a minimum of 3 results
# so a real answer never comes back empty.
MAX_RESULTS = 8
MIN_SCORE = 30
MIN_RESULTS_FLOOR = 3


def select_top_matches(results, max_results=MAX_RESULTS, min_score=MIN_SCORE, floor=MIN_RESULTS_FLOOR):
    """results must already be sorted best-first by blend_with_semantic_scores."""
    filtered = [r for r in results if r["score"] >= min_score]
    if len(filtered) < floor:
        filtered = results[:floor]
    return filtered[:max_results]


class Profile(BaseModel):
    age: Optional[int] = None
    city: Optional[str] = None
    province: Optional[str] = None
    gender: Optional[str] = None
    employment_status: Optional[str] = None
    business_stage: Optional[str] = None
    sector: Optional[str] = None
    goal: Optional[str] = None
    funding_required: Optional[int] = None
    education_level: Optional[str] = None
    income: Optional[int] = None
    flags: Optional[Dict[str, bool]] = {}


class SituationInput(BaseModel):
    text: str


def blend_with_semantic_scores(eligibility_results, semantic_matches):
    """
    Combines deterministic eligibility scores with RAG semantic relevance.
    eligibility_results: output of rank_programs() — full list, all programs
    semantic_matches: raw rows from rag.search_programs() — may be a
                       partial top-N list, not necessarily all programs

    Weighting: 70% eligibility, 30% semantic. Eligibility stays the
    dominant signal — semantic relevance nudges ranking within it,
    never overrides a hard disqualification (eligible:false always
    sorts after eligible:true).
    """
    # Confirmed against match_programs SQL: returns "similarity" as
    # 1 - cosine_distance, in the 0-1 range.
    semantic_lookup = {}
    for row in semantic_matches:
        name = row.get("program_name")
        raw_score = row.get("similarity", 0.5)
        normalized = raw_score * 100 if raw_score <= 1 else raw_score
        semantic_lookup[name] = max(0, min(100, normalized))

    for result in eligibility_results:
        sem_score = semantic_lookup.get(result["program_name"], 50)  # neutral default if not in top-N
        result["eligibility_score"] = result["score"]
        result["semantic_score"] = round(sem_score)
        # 55/45 instead of a heavier eligibility weight — many programs
        # have loose criteria and trivially score 100% eligibility
        # regardless of topical fit, which was drowning out genuine
        # semantic relevance. Semantic signal needs real room to matter.
        result["score"] = round(result["score"] * 0.55 + sem_score * 0.45)

    eligibility_results.sort(key=lambda r: (r["eligible"], r["score"]), reverse=True)
    return eligibility_results


@app.post("/simt")
def simt(input: SituationInput):
    """
    The main end-to-end endpoint: takes raw user text, extracts a
    structured profile via the LLM, runs it through the deterministic
    eligibility engine, then blends in RAG semantic relevance for
    final ranking.
    """
    if not input.text or not input.text.strip():
        raise HTTPException(status_code=400, detail="Please describe your situation first.")

    try:
        profile = extract_profile(input.text)
    except ValueError as e:
        raise HTTPException(status_code=502, detail=f"Could not understand the situation: {e}")
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(
             status_code=502,
             detail=f"AI service is unavailable right now: {type(e).__name__}: {e}"
        )
    
    try:
        results = rank_programs(profile, PROGRAMS)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error matching programs: {e}")

    try:
        semantic_matches = search_programs(input.text, limit=len(PROGRAMS))
        results = blend_with_semantic_scores(results, semantic_matches)
    except Exception as e:
        # RAG is an enhancement, not a hard dependency — if Supabase is
        # unreachable, fall back to eligibility-only results rather than
        # failing the whole request.
        print(f"RAG search failed, falling back to eligibility-only ranking: {e}")

    total_considered = len(results)
    top_matches = select_top_matches(results)

    return {
        "profile": profile,
        "matches": top_matches,
        "total_programs_considered": total_considered,
    }


@app.get("/")
def health_check():
    return {"status": "SIMT AI backend is running", "programs_loaded": len(PROGRAMS)}


@app.post("/recommend")
def recommend(profile: Profile):
    """
    Takes a user profile, returns ranked program matches.
    This is the main endpoint the frontend will call.
    """
    results = rank_programs(profile.dict(), PROGRAMS)
    return {"matches": results}


@app.get("/programs")
def list_programs():
    """Returns all programs as-is — useful for the frontend to browse/debug."""
    return PROGRAMS