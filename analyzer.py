import json
import os
from openai import OpenAI

def analyze_resume(resume_text: str, job_role: str = "") -> dict:
    try:
        api_key = os.getenv("OPENAI_API_KEY")
        client = OpenAI(api_key=api_key)

        job_context = f"The candidate is targeting a {job_role} role." if job_role else ""

        prompt = f"""
You are an expert resume reviewer.
{job_context}
Resume:
{resume_text}

Return ONLY valid JSON:
{{
  "score": 1-10,
  "ats_score": "",
  "completeness": "",
  "strengths": [],
  "weaknesses": [],
  "recommendations": [],
  "missing_keywords": [],
  "summary": ""
}}
"""
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3
        )
        raw = response.choices[0].message.content.strip()
        raw = raw.replace("```json", "").replace("```", "").strip()
        return json.loads(raw)

    except Exception as e:
        return {"error": str(e)}
