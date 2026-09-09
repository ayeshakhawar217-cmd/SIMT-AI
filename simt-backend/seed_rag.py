import json
from rag import supabase, program_to_text, create_embedding


def load_programs():
    with open("programs.json", "r", encoding="utf-8") as f:
        return json.load(f)


def seed_database():

    programs = load_programs()

    print(f"Found {len(programs)} programs.")

    for index, program in enumerate(programs, start=1):

        print(
            f"[{index}/{len(programs)}] "
            f"Embedding: {program['program_name']}"
        )

        text = program_to_text(program)

        embedding = create_embedding(text)

        row = {
            "program_name": program.get("program_name"),
            "provider": program.get("provider"),
            "category": program.get("category"),
            "audience": program.get("audience"),
            "geography": program.get("geography"),
            "eligibility": program.get("eligibility"),
            "benefit": program.get("benefit"),
            "documents": program.get("documents"),
            "application_process": program.get("application_process"),
            "official_source": program.get("official_source"),
            "last_verified": program.get("last_verified"),
            "notes": program.get("notes"),
            "match_criteria": program.get("match_criteria"),
            "require_true": program.get("require_true"),
            "exclude_if_true": program.get("exclude_if_true"),
            "embedding": embedding
        }

        supabase.table("programs").insert(row).execute()

    print("Finished seeding Supabase.")


if __name__ == "__main__":
    seed_database()