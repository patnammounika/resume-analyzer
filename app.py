import streamlit as st
import PyPDF2
import docx2txt
import os
from analyzer import analyze_resume

# Load API key
if "OPENAI_API_KEY" in st.secrets:
    os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]

st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="📄",
    layout="centered"
)

st.markdown("""
    <style>
        .main-title { font-size: 2rem; font-weight: 700; color: #1A56A0; }
        .sub-title  { font-size: 1rem; color: #555; margin-bottom: 1.5rem; }
        .section-header { font-size: 1.1rem; font-weight: 600; color: #1A56A0;
                          border-bottom: 2px solid #1A56A0; padding-bottom: 4px; margin-top: 1.5rem; }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">📄 AI Resume Analyzer</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Upload your resume and get instant AI-powered feedback.</div>', unsafe_allow_html=True)

with st.sidebar:
    st.header("⚙️ Settings")
    job_role = st.text_input("Target Job Role (optional)", placeholder="e.g. Software Engineer")
    st.markdown("---")
    st.markdown("**Supported formats:** PDF, DOCX, TXT")
    st.markdown("**Powered by:** OpenAI GPT-4o Mini")

uploaded_file = st.file_uploader("Upload Your Resume", type=["pdf", "docx", "txt"])

def extract_text(file):
    if file.name.endswith(".pdf"):
        reader = PyPDF2.PdfReader(file)
        return "\n".join(page.extract_text() or "" for page in reader.pages)
    elif file.name.endswith(".docx"):
        return docx2txt.process(file)
    elif file.name.endswith(".txt"):
        return file.read().decode("utf-8")
    return ""

def format_report(result, filename):
    lines = [
        "RESUME ANALYSIS REPORT",
        f"File: {filename}",
        "=" * 50,
        f"Overall Score     : {result.get('score', 'N/A')}/10",
        f"ATS Compatibility : {result.get('ats_score', 'N/A')}",
        f"Completeness      : {result.get('completeness', 'N/A')}",
        "\nSTRENGTHS:",
        *[f"  + {s}" for s in result.get("strengths", [])],
        "\nAREAS TO IMPROVE:",
        *[f"  - {w}" for w in result.get("weaknesses", [])],
        "\nRECOMMENDATIONS:",
        *[f"  * {r}" for r in result.get("recommendations", [])],
        "\nMISSING KEYWORDS:",
        f"  {', '.join(result.get('missing_keywords', []))}",
        "\nSUMMARY:",
        f"  {result.get('summary', '')}",
    ]
    return "\n".join(lines)

if uploaded_file:
    with st.spinner("Reading your resume..."):
        resume_text = extract_text(uploaded_file)

    if not resume_text.strip():
        st.error("Could not extract text. Please try a different format.")
    else:
        st.success(f"✅ Resume loaded: **{uploaded_file.name}**")

        with st.expander("📋 View Extracted Text"):
            st.text_area("Resume Content", resume_text, height=200)

        if st.button("🔍 Analyze Resume", use_container_width=True, type="primary"):
            with st.spinner("Analyzing with AI..."):
                result = analyze_resume(resume_text, job_role)

            if "error" in result:
                st.error(f"Analysis failed: {result['error']}")
            else:
                st.markdown("---")
                st.markdown("## 📊 Analysis Results")

                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Overall Score", f"{result.get('score', 'N/A')}/10")
                with col2:
                    st.metric("ATS Compatibility", result.get('ats_score', 'N/A'))
                with col3:
                    st.metric("Completeness", result.get('completeness', 'N/A'))

                st.markdown('<div class="section-header">✅ Strengths</div>', unsafe_allow_html=True)
                for s in result.get("strengths", []):
                    st.markdown(f"- {s}")

                st.markdown('<div class="section-header">⚠️ Areas to Improve</div>', unsafe_allow_html=True)
                for w in result.get("weaknesses", []):
                    st.markdown(f"- {w}")

                st.markdown('<div class="section-header">💡 Recommendations</div>', unsafe_allow_html=True)
                for r in result.get("recommendations", []):
                    st.markdown(f"- {r}")

                st.markdown('<div class="section-header">🔑 Missing Keywords</div>', unsafe_allow_html=True)
                keywords = result.get("missing_keywords", [])
                if keywords:
                    st.markdown(" ".join([f"`{k}`" for k in keywords]))
                else:
                    st.markdown("No major keywords missing!")

                st.markdown('<div class="section-header">📝 Summary Feedback</div>', unsafe_allow_html=True)
                st.info(result.get("summary", ""))

                st.download_button(
                    label="📥 Download Report",
                    data=format_report(result, uploaded_file.name),
                    file_name="resume_analysis_report.txt",
                    mime="text/plain"
                )
