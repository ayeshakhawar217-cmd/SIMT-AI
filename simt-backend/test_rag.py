from rag import search_programs


queries = [
    "I am unemployed and want to start an online clothing business. I need around 12 lakh rupees.",

    "I am a university student and need financial help for my education.",

    "I am a young person from Punjab looking for free IT training.",

    "I have an innovative startup idea and need funding."
]


for query in queries:

    print("\n" + "=" * 70)
    print("QUERY:")
    print(query)

    results = search_programs(query, limit=5)

    print("\nRESULTS:")

    for result in results:

        print(
            f"{result['program_name']} "
            f"→ similarity: {result['similarity']:.3f}"
        )