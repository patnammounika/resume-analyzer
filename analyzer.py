import json
import os
import streamlit as st
import anthropic

def analyze_resume(resume_text: str, job_role: str = "") -> dict:
    try:
        # Streamlit Cloud secrets first, fallback to env
        api_key = st.secrets.get("ANTHROPIC_API_KEY") or os.getenv("ANTHROPIC_API_KEY")
        client = anthropic.Anthropic(api_key=api_key)

        job_context = f"The candidate is targeting a {job_role} role." if job_role else ""

        prompt = f"""
You are an expert resume reviewer and career coach. Analyze the resume below.

{job_context}

Resume:
\"\"\"
{resume_text}
\"\"\"

Return ONLY valid JSON (no markdown, no explanation):
{{
  "score": <integer 1-10>,
  "ats_score": "<Poor/Fair/Good/Excellent>",
  "completeness": "<Incomplete/Partial/Complete>",
  "strengths": ["<strength 1>", "<strength 2>", "<strength 3>"],
  "weaknesses": ["<weakness 1>", "<weakness 2>", "<weakness 3>"],
  "recommendations": ["<tip 1>", "<tip 2>", "<tip 3>", "<tip 4>"],
  "missing_keywords": ["<keyword 1>", "<keyword 2>", "<keyword 3>"],
  "summary": "<2-3 sentence overall feedback>"
}}
"""
        response = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=1024,
            messages=[{"role": "user", "content": prompt}]
        )

        raw = response.content[0].text.strip()
        raw = raw.replace("```json", "").replace("```", "").strip()
        return json.loads(raw)

    except Exception as e:
        return {"error": str(e)}
