import os
import google.generativeai as genai

def explain_score(lead: dict, score: int, reasons: list[str]) -> str:
    """Generate a short human-readable explanation using Gemini."""
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY is not set.")

    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-1.5-flash")
    prompt = f"""
Explain this sales lead score to a sales representative in 3 concise bullet points.
Do not invent facts, do not change the numeric score, and mention one sensible next action.
Lead fields: {lead}
Score: {score}/100
Scoring reasons: {reasons}
"""
    response = model.generate_content(prompt)
    return response.text or "Gemini returned an empty explanation."
