"""
Tiny test script — confirms your Groq API key and setup work.
Run this FIRST, before touching the real project files.

Setup:
    1. Go to https://console.groq.com -> sign up (free, no card needed)
    2. Create an API key
    3. Set it as an environment variable:
         export GROQ_API_KEY="your-key-here"      (Mac/Linux)
         set GROQ_API_KEY=your-key-here            (Windows)
    4. pip install groq
    5. python test_api.py
"""

import os
from groq import Groq

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

response = client.chat.completions.create(
    model="llama-3.3-70b-versatile",  # free, fast, good quality model on Groq
    max_tokens=100,
    messages=[
        {"role": "user", "content": "Say hello and tell me one fun fact about AI agents, in 2 sentences."}
    ],
)

# This is the standard OpenAI-style response shape that Groq also uses
print(response.choices[0].message.content)
