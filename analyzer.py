import json
import os
from openai import OpenAI

def analyze_resume(resume_text: str, job_role: str = "") -> dict:
    try:
        client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
        
        job_context = f"The candidate is targeting a **{job_role}** role." if job_role else ""

        prompt = f"""
You are an expert resume reviewer. Analyze the resume below.

{job_context}

Resume:
{resume_text}

Return ONLY valid JSON:
{{
  "score": <integer 1-10>,
  "ats_score": "<Poor/Fair/Good/Excellent>",
  "completeness": "<Incomplete/Partial/Complete>",
  "strengths": ["<strength 1>", "<strength 2>", "<strength 3>"],
  "weaknesses": ["<weakness 1>", "<weakness 2>", "<weakness 3>"],
  "recommendations": ["<tip 1>", "<tip 2>", "<tip 3>"],
  "missing_keywords": ["<keyword 1>", "<keyword 2>", "<keyword 3>"],
  "summary": "<2-3 sentence feedback>"
}}
"""
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.4,
            max_tokens=1000
        )
        raw = response.choices[0].message.content.strip()
        raw = raw.replace("```json", "").replace("```", "").strip()
        return json.loads(raw)
        
    except Exception as e:
        return {"error": str(e)}
