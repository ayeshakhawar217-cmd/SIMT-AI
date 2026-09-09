"""
eligibility.py
SIMT AI — deterministic eligibility engine.

Takes a user profile + a program (with a "match_criteria" block) and
returns whether the user is eligible, which rules passed/failed, and a
0-100 match score. The LLM/RAG side never touches this logic — this is
the deterministic core the PRD requires.
"""

import json

# Ordinal education levels — used so "requires Matric" means Matric OR
# ANYTHING HIGHER qualifies, not an exact match.
EDUCATION_LEVELS = ["Matric", "Intermediate", "Undergraduate", "Graduate", "Postgraduate"]


def load_programs(path: str) -> list:
    """Load the programs.json file into a list of dicts."""
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def _check_range(value, min_val, max_val):
    """Generic range check. Returns True if unrestricted or value fits."""
    if min_val is None and max_val is None:
        return True
    if value is None:
        return None
    if min_val is not None and value < min_val:
        return False
    if max_val is not None and value > max_val:
        return False
    return True


def _check_list_membership(value, allowed_list):
    """Generic membership check. Empty allowed_list = no restriction."""
    if not allowed_list:
        return True
    if value is None:
        return None
    return value in allowed_list


def _check_province(user_province, allowed_provinces):
    """
    Province check with a special case: if the program lists
    'Nationwide' or 'Pakistan' as an allowed value, it's available
    everywhere regardless of the user's specific province.
    """
    if not allowed_provinces:
        return True
    if user_province is None:
        return None
    nationwide_terms = {"nationwide", "pakistan", "all provinces"}
    if any(p.lower() in nationwide_terms for p in allowed_provinces):
        return True
    return user_province in allowed_provinces


def _check_education_minimum(user_level, required_level):
    """
    Education check as a MINIMUM threshold, not exact match.
    A program requiring 'Matric' is satisfied by Matric, Intermediate,
    Undergraduate, Graduate, or Postgraduate — anything at or above it.
    """
    if not required_level:
        return True
    if user_level is None:
        return None
    if required_level not in EDUCATION_LEVELS or user_level not in EDUCATION_LEVELS:
        return user_level == required_level  # fallback: exact match
    return EDUCATION_LEVELS.index(user_level) >= EDUCATION_LEVELS.index(required_level)


def check_eligibility(profile: dict, program: dict) -> dict:
    """
    Evaluate one program against one user profile.

    Returns:
        {
          "eligible": bool,
          "score": int (0-100),
          "passed": [str, ...],
          "failed": [str, ...],
          "not_applicable": [str, ...],
          "disqualified_reason": str or None
        }
    """
    mc = program.get("match_criteria", {})
    flags = profile.get("flags", {}) or {}

    # 0. Closed programs — deadline has passed, don't show as eligible
    if mc.get("status") == "closed":
        reason = mc.get("closed_reason", "This program is not currently accepting applications.")
        return {
            "eligible": False,
            "score": 0,
            "passed": [],
            "failed": [reason],
            "not_applicable": [],
            "disqualified_reason": reason,
        }

    # 1. Hard disqualifiers first — flags that must NOT be true
    for exclusion in mc.get("exclude_if_true", []):
        flag = exclusion["flag"]
        if flags.get(flag) is True:
            return {
                "eligible": False,
                "score": 0,
                "passed": [],
                "failed": [exclusion["reason"]],
                "not_applicable": [],
                "disqualified_reason": exclusion["reason"],
            }

    passed = []
    failed = []
    not_applicable = []

    # 2. Requirements that must be true — but "unknown" is NOT the same as
    # "confirmed false". Only an explicit False hard-disqualifies. A null
    # (never asked / not mentioned) goes to not_applicable like every other
    # missing field — it shouldn't zero out an otherwise strong match.
    for requirement in mc.get("require_true", []):
        flag = requirement["flag"]
        flag_value = flags.get(flag)
        if flag_value is False:
            return {
                "eligible": False,
                "score": 0,
                "passed": [],
                "failed": [requirement["reason"]],
                "not_applicable": [],
                "disqualified_reason": requirement["reason"],
            }
        elif flag_value is True:
            passed.append(requirement["reason"])
        else:
            not_applicable.append(f"{requirement['reason']} (not confirmed)")

    # 3. Age
    age_result = _check_range(profile.get("age"), mc.get("age_min"), mc.get("age_max"))
    if age_result is True and (mc.get("age_min") or mc.get("age_max")):
        passed.append(f"Age {profile.get('age')} is within the allowed range")
    elif age_result is False:
        failed.append(f"Age {profile.get('age')} is outside the allowed range "
                       f"({mc.get('age_min')}-{mc.get('age_max')})")
    elif age_result is None and (mc.get("age_min") or mc.get("age_max")):
        not_applicable.append("Age requirement (not provided by user)")

    # 4. Income ceiling
    income_result = _check_range(profile.get("income"), None, mc.get("income_max"))
    if income_result is True and mc.get("income_max"):
        passed.append("Income is within the eligible limit")
    elif income_result is False:
        failed.append(f"Income exceeds the limit of {mc.get('income_max')}")
    elif income_result is None and mc.get("income_max"):
        not_applicable.append("Income limit (not provided by user)")

    # 5. Province / geography (domicile-restricted programs use the same field)
    province_result = _check_province(profile.get("province"), mc.get("provinces"))
    if province_result is True and mc.get("provinces"):
        passed.append(f"Available in {profile.get('province')}")
    elif province_result is False:
        failed.append(f"Not available in {profile.get('province')}")
    elif province_result is None and mc.get("provinces"):
        not_applicable.append("Location requirement (not provided by user)")

    # 6. Education level — MINIMUM threshold, not exact match
    edu_required = mc.get("education_level")
    edu_result = _check_education_minimum(profile.get("education_level"), edu_required)
    if edu_result is True and edu_required:
        passed.append(f"Meets the minimum education requirement ({edu_required})")
    elif edu_result is False:
        failed.append(f"Requires at least: {edu_required}")
    elif edu_result is None and edu_required:
        not_applicable.append("Education level requirement (not provided by user)")

    # 7. Gender
    gender_result = _check_list_membership(profile.get("gender"), mc.get("gender"))
    if gender_result is True and mc.get("gender"):
        passed.append(f"Open to {profile.get('gender')} applicants")
    elif gender_result is False:
        failed.append(f"This program is restricted to: {', '.join(mc.get('gender', []))}")
    elif gender_result is None and mc.get("gender"):
        not_applicable.append("Gender requirement (not provided by user)")

    # 8. Employment status
    emp_result = _check_list_membership(profile.get("employment_status"), mc.get("employment_status"))
    if emp_result is True and mc.get("employment_status"):
        passed.append(f"Employment status matches ({profile.get('employment_status')})")
    elif emp_result is False:
        failed.append(f"Employment status '{profile.get('employment_status')}' not accepted")
    elif emp_result is None and mc.get("employment_status"):
        not_applicable.append("Employment status requirement (not provided by user)")

    # 9. Business stage
    stage_result = _check_list_membership(profile.get("business_stage"), mc.get("business_stage"))
    if stage_result is True and mc.get("business_stage"):
        passed.append(f"Business stage matches ({profile.get('business_stage')})")
    elif stage_result is False:
        failed.append(f"Business stage '{profile.get('business_stage')}' not accepted")
    elif stage_result is None and mc.get("business_stage"):
        not_applicable.append("Business stage requirement (not provided by user)")

    # 10. Sector
    sector_result = _check_list_membership(profile.get("sector"), mc.get("sector"))
    if sector_result is True and mc.get("sector"):
        passed.append(f"Sector matches ({profile.get('sector')})")
    elif sector_result is False:
        failed.append(f"Sector '{profile.get('sector')}' not accepted")
    elif sector_result is None and mc.get("sector"):
        not_applicable.append("Sector requirement (not provided by user)")

    # 11. Funding amount fit
    funding_result = _check_range(profile.get("funding_required"), mc.get("min_funding"), mc.get("max_funding"))
    if funding_result is True and (mc.get("min_funding") or mc.get("max_funding")):
        passed.append("Requested amount is within the program's financing range")
    elif funding_result is False:
        failed.append(f"Requested amount is outside the range "
                       f"({mc.get('min_funding')}-{mc.get('max_funding')})")
    elif funding_result is None and (mc.get("min_funding") or mc.get("max_funding")):
        not_applicable.append("Funding amount fit (not provided by user)")

    # --- Final scoring ---
    total_checked = len(passed) + len(failed)
    eligible = len(failed) == 0

    if total_checked == 0:
        score = 50  # nothing concrete to check either way — neutral score
    else:
        score = round((len(passed) / total_checked) * 100)

    return {
        "eligible": eligible,
        "score": score,
        "passed": passed,
        "failed": failed,
        "not_applicable": not_applicable,
        "disqualified_reason": None,
    }


def rank_programs(profile: dict, programs: list) -> list:
    """
    Run check_eligibility against every program and return them
    sorted best-match first: eligible programs before ineligible ones,
    then by score descending.
    """
    results = []
    for program in programs:
        result = check_eligibility(profile, program)
        results.append({
            "program_name": program["program_name"],
            "provider": program.get("provider"),
            "category": program.get("category"),
            "official_source": program.get("official_source"),
            **result,
        })

    results.sort(key=lambda r: (r["eligible"], r["score"]), reverse=True)
    return results