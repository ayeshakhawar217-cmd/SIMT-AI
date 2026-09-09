import os
from dotenv import load_dotenv
from supabase import create_client
from sentence_transformers import SentenceTransformer

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError("SUPABASE_URL and SUPABASE_KEY must be set")

supabase = create_client(
    SUPABASE_URL,
    SUPABASE_KEY
)

# Multilingual model — the previous all-MiniLM-L6-v2 is English-centric
# and largely can't understand Roman Urdu/Urdu queries, which is most of
# what real users type. This model outputs the same 384 dimensions, so
# no Supabase schema change is needed — just re-seed after switching.
model = SentenceTransformer("all-MiniLM-L6-v2")


def program_to_text(program):
    """
    Converts one program JSON object into a semantic document for embedding.

    Deliberately excludes documents/application_process — that text is
    near-identical boilerplate across nearly every program (CNIC, submit
    application, official portal...) and dilutes the embedding, making
    genuinely different programs look similar. Only distinctive,
    program-specific content goes into the embedding text.
    """

    return f"""
Program: {program.get("program_name", "")}

Category: {program.get("category", "")}

Audience: {program.get("audience", "")}

Eligibility: {program.get("eligibility", "")}

Benefits: {program.get("benefit", "")}

Notes: {program.get("notes", "")}
""".strip()


def create_embedding(text):
    """
    Converts text into a 384-dimensional vector.
    """

    embedding = model.encode(
        text,
        normalize_embeddings=True
    )

    return embedding.tolist()


def search_programs(query, limit=10):
    """
    Converts a user query into an embedding and searches
    Supabase pgvector for the most semantically similar programs.
    """

    query_embedding = create_embedding(query)

    response = supabase.rpc(
        "match_programs",
        {
            "query_embedding": query_embedding,
            "match_count": limit
        }
    ).execute()

    return response.data