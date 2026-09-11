"""
extract_profile.py
SIMT AI — turns a raw user sentence (English/Urdu/Roman Urdu mix) into
the structured Profile JSON that eligibility.py and main.py expect.

Uses Groq's free API (fast, no cost, generous rate limits — good fit
for a hackathon). Get a free key at https://console.groq.com/keys

Set it as an environment variable:
  Windows (PowerShell):  $env:GROQ_API_KEY="gsk_..."
  Mac/Linux:              export GROQ_API_KEY="gsk_..."

Install:
  pip install groq
"""

import os
import json
from dotenv import load_dotenv
from groq import Groq

load_dotenv()  # reads the .env file and loads GROQ_API_KEY into the environment

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise RuntimeError("GROQ_API_KEY is not set")

client = Groq(api_key=GROQ_API_KEY)

# llama-3.3-70b-versatile was deprecated by Groq (Aug 2026). Using their
# recommended replacement — strong at structured extraction, still free tier.
# If you hit rate limits during heavy testing, swap to "openai/gpt-oss-20b"
# — faster, higher limits, slightly less sharp on messy/ambiguous input.
MODEL = "openai/gpt-oss-20b"

SYSTEM_PROMPT = """You extract structured information from a Pakistani citizen's
description of their situation, for a system that matches them to government
programs. Read their message (which may mix English, Urdu, and Roman Urdu) and
output ONLY a JSON object — no explanation, no markdown fences, nothing else.

Use exactly this shape. Use null for anything not mentioned or unclear —
never guess or invent a value:

{
  "age": <integer or null>,
  "city": <string or null>,
  "province": <one of "Punjab","Sindh","Khyber Pakhtunkhwa","Balochistan","Islamabad","Gilgit-Baltistan","Azad Kashmir" or null>,
  "gender": <one of "man","woman" or null — only set if directly stated or clearly implied by the person's own words (e.g. "main rehti hoon" = feminine verb form = woman); never guess from a name alone>,
  "employment_status": <one of "employed","unemployed","student","self-employed" or null>,
  "business_stage": <one of "idea","startup","existing" or null>,
  "sector": <short lowercase string like "ecommerce","agriculture","retail" or null>,
  "goal": <one of "start_business","get_scholarship","find_job","get_training","get_financing" or null>,
  "funding_required": <integer PKR amount or null>,
  "education_level": <one of "Matric","Intermediate","Undergraduate","Graduate","Postgraduate" or null>,
  "income": <integer monthly PKR or null>,
  "flags": {
    "on_self_finance_admission": <true/false/null>,
    "has_existing_scholarship": <true/false/null>,
    "in_affiliated_college": <true/false/null>,
    "studies_at_private_institution": <true/false/null>,
    "receives_other_govt_assistance": <true/false/null>,
    "parent_is_govt_employee": <true/false/null>,
    "belongs_to_marginalized_group": <true/false/null — set true only if the person explicitly self-identifies as transgender, as having a disability/special needs, or as another marginalized group>,
    "graduated_within_4_years": <true/false/null>,
    "studied_it_related_discipline": <true/false/null>,
    "enrolled_in_hec_eligible_institution": <true/false/null — only set true if they name a specific public-sector university, otherwise null>,
    "has_overseas_job_offer": <true/false/null>,
    "confirmed_via_nser_survey": <true/false/null — almost always null unless they explicitly say they're already registered with BISP/NSER>
  }
}

Rules:
- Convert "lakh" to the actual number (e.g. "12 lakh" = 1200000).
- If province isn't stated but a well-known city is (e.g. Lahore, Gujranwala,
  Multan → Punjab; Karachi, Hyderabad → Sindh; Peshawar → KP; Quetta →
  Balochistan), infer the province from the city, but leave city as stated.
- Never fabricate age, income, funding, or any flag — leave null if not clearly stated.
  Flags default to null, not false — false means "explicitly ruled out," not "not mentioned."
- Gender-marked verb forms in Urdu/Roman Urdu (e.g. "rehti hoon" vs "rehta hoon",
  "chahti hoon" vs "chahta hoon") are a reliable signal for gender — use them.
"""


# A few examples the model can pattern-match against.
FEW_SHOT_EXAMPLES = [
    {
        "role": "user",
        "content": "Main 28 saal ka hoon, Gujranwala mein rehta hoon, currently "
                    "unemployed hoon aur online clothing business start karna "
                    "chahta hoon. Mujhe 12 lakh rupay chahiye.",
    },
    {
        "role": "assistant",
        "content": json.dumps({
            "age": 28,
            "city": "Gujranwala",
            "province": "Punjab",
            "gender": "man",
            "employment_status": "unemployed",
            "business_stage": "idea",
            "sector": "ecommerce",
            "goal": "start_business",
            "funding_required": 1200000,
            "education_level": None,
            "income": None,
            "flags": {
                "on_self_finance_admission": None,
                "has_existing_scholarship": None,
                "in_affiliated_college": None,
                "studies_at_private_institution": None,
                "receives_other_govt_assistance": None,
                "parent_is_govt_employee": None,
                "belongs_to_marginalized_group": None,
                "graduated_within_4_years": None,
                "studied_it_related_discipline": None,
                "enrolled_in_hec_eligible_institution": None,
                "has_overseas_job_offer": None,
                "confirmed_via_nser_survey": None,
            },
        }),
    },
    {
        "role": "user",
        "content": "Meri age 22 hai, main Lahore mein rehti hoon, Matric kiya hua "
                    "hai aur koi skill seekhna chahti hoon.",
    },
    {
        "role": "assistant",
        "content": json.dumps({
            "age": 22,
            "city": "Lahore",
            "province": "Punjab",
            "gender": "woman",
            "employment_status": None,
            "business_stage": None,
            "sector": None,
            "goal": "get_training",
            "funding_required": None,
            "education_level": "Matric",
            "income": None,
            "flags": {
                "on_self_finance_admission": None,
                "has_existing_scholarship": None,
                "in_affiliated_college": None,
                "studies_at_private_institution": None,
                "receives_other_govt_assistance": None,
                "parent_is_govt_employee": None,
                "belongs_to_marginalized_group": None,
                "graduated_within_4_years": None,
                "studied_it_related_discipline": None,
                "enrolled_in_hec_eligible_institution": None,
                "has_overseas_job_offer": None,
                "confirmed_via_nser_survey": None,
            },
        }),
    },
]


def extract_profile(user_text: str) -> dict:
    """
    Calls the LLM to turn raw user text into a structured profile dict.
    Returns a dict matching the Profile shape used by main.py.
    Raises ValueError if the model doesn't return valid JSON.
    """
    messages = (
        [{"role": "system", "content": SYSTEM_PROMPT}]
        + FEW_SHOT_EXAMPLES
        + [{"role": "user", "content": user_text}]
    )

    response = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        temperature=0,
        response_format={"type": "json_object"},  # forces valid JSON output
    )

    raw = response.choices[0].message.content.strip()

    # Safety net: strip markdown fences if the model adds them anyway
    if raw.startswith("```"):
        raw = raw.strip("`")
        if raw.startswith("json"):
            raw = raw[4:]
        raw = raw.strip()

    try:
        profile = json.loads(raw)
    except json.JSONDecodeError:
        raise ValueError(f"Model did not return valid JSON:\n{raw}")

    return profile