"""
test_extract.py
Run: python test_extract.py

Requires GROQ_API_KEY to be set as an environment variable first.
Get a free key at https://console.groq.com/keys
"""

import json
from extract_profile import extract_profile

test_sentences = [
    "Main 28 saal ka hoon, Gujranwala mein rehta hoon, unemployed hoon aur "
    "online clothing business start karna chahta hoon. Mujhe 12 lakh chahiye.",

    "I'm a 20 year old undergrad student in Lahore, studying on self finance. "
    "I need help finding a scholarship.",

    "Meri age 35 hai, main Karachi mein rehti hoon, mera chota sa boutique hai "
    "aur main expand karna chahti hoon.",
]

for sentence in test_sentences:
    print("\nINPUT:", sentence)
    try:
        profile = extract_profile(sentence)
        print("OUTPUT:", json.dumps(profile, indent=2))
    except Exception as e:
        print("ERROR:", e)