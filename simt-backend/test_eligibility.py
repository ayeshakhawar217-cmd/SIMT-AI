"""
test_eligibility.py
Run: python test_eligibility.py

Tries two sample profiles against programs.json and prints ranked results.
"""

import json
from eligibility import load_programs, rank_programs

programs = load_programs("programs.json")

# --- Profile 1: matches the Kamyab Jawan loan well, HEC scholarship is N/A ---
profile_1 = {
    "age": 28,
    "city": "Gujranwala",
    "province": "Punjab",
    "employment_status": "unemployed",
    "business_stage": "idea",
    "sector": "ecommerce",
    "goal": "start_business",
    "funding_required": 1200000,
    "education_level": None,
    "income": None,
    "flags": {},
}

# --- Profile 2: undergrad student, but on self-finance admission
#     (should be disqualified from the HEC scholarship specifically) ---
profile_2 = {
    "age": 20,
    "city": "Lahore",
    "province": "Punjab",
    "employment_status": None,
    "business_stage": None,
    "sector": None,
    "goal": "get_scholarship",
    "funding_required": None,
    "education_level": "Undergraduate",
    "income": None,
    "flags": {
        "on_self_finance_admission": True,
        "has_existing_scholarship": False,
        "in_affiliated_college": False,
    },
}


def show(profile_name, profile):
    print(f"\n===== Results for {profile_name} =====")
    results = rank_programs(profile, programs)
    for r in results:
        status = "ELIGIBLE" if r["eligible"] else "NOT ELIGIBLE"
        print(f"\n{r['program_name']}  —  {status}  ({r['score']}% match)")
        for p in r["passed"]:
            print(f"   [pass] {p}")
        for f in r["failed"]:
            print(f"   [fail] {f}")
        for n in r["not_applicable"]:
            print(f"   [n/a]  {n}")


show("Profile 1 (unemployed, wants business loan)", profile_1)
show("Profile 2 (undergrad, on self-finance)", profile_2)