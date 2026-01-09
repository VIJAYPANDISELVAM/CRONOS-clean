import os
import google.generativeai as genai

genai.configure(api_key=os.getenv("AIzaSyAYNLY17mu0CH7qHvmvo4LGyST09sLOD8k"))

model = genai.GenerativeModel(
    model_name="gemini-1.5-pro",
    generation_config={
        "temperature": 0.0,   # 🔒 deterministic
        "top_p": 1.0,
        "top_k": 1
    }
)

def generate_human_explanation(payload: dict) -> str:
    prompt = build_prompt(payload)

    response = model.generate_content(prompt)

    return response.text.strip()


def build_prompt(payload: dict) -> str:
    return f"""
You are a static code analysis explanation engine.

STRICT RULES:
- Do NOT decide pass or fail.
- Do NOT change risk score.
- Do NOT invent behavior.
- Explain ONLY using the provided analysis signals.
- Be deterministic, factual, and concise.
- Do NOT mention AI, models, or assumptions.

Your task:
Explain in plain English:
1. What semantic behavior changed (if any)
2. Why the change violates or respects constraints
3. How the new behavior differs from the expected output

Analysis Data:
{payload}
"""