import json
import os
import streamlit as st
from openai import OpenAI

def analyze_resume(resume_text: str, job_role: str = "") -> dict:
    
    # Get API key from streamlit secrets or environment
    api_key = st.secrets.get("OPENAI_API_KEY") or os.getenv("OPENAI_API_KEY")
    
    client = OpenAI(api_key=api_key)
    
    job_context = f"The candidate is targeting a **{job_role}** role." if job_role else ""

    prompt = f"""
You are an expert resume reviewer and career coach. Analyze the resume below and return a JSON object.

{job_context}

Resume:
\"\"\"
{resume_text}
\"\"\"

Return ONLY valid JSON (no markdown, no explanation) with this exact structure:
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

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.4,
            max_tokens=1000
        )
        raw = response.choices[0].message.content.strip()
        raw = raw.replace("```json", "").replace("```", "").strip()
        return json.loads(raw)
    except json.JSONDecodeError as e:
        return {"error": f"Failed to parse AI response: {str(e)}"}
    except Exception as e:
        return {"error": str(e)}
