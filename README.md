# 📄 AI Resume Analyzer

An intelligent resume analysis tool built with **Python**, **Streamlit**, and **OpenAI GPT-4o**. Upload your resume and get instant AI-powered feedback including an overall score, ATS compatibility check, strengths, weaknesses, keyword suggestions, and actionable recommendations.

---

## 🚀 Features

- 📤 Upload resume in **PDF**, **DOCX**, or **TXT** format
- 🤖 AI-powered analysis using **OpenAI GPT-4o**
- 📊 Overall score out of 10
- ✅ ATS (Applicant Tracking System) compatibility rating
- 💡 Specific recommendations to improve your resume
- 🔑 Missing keywords detection
- 🎯 Target a specific job role for tailored feedback
- 📥 Download analysis report as a text file

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|------------|
| Frontend UI | Streamlit |
| AI Engine | OpenAI GPT-4o |
| PDF Parsing | PyPDF2 |
| DOCX Parsing | docx2txt |
| Language | Python 3.10+ |

---

## ⚙️ Setup & Installation

### 1. Clone the Repository
```bash
git clone https://github.com/patnammounika/resume-analyzer.git
cd resume-analyzer
```

### 2. Create a Virtual Environment
```bash
python -m venv venv
source venv/bin/activate        # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Set Up Environment Variables
```bash
cp .env.example .env
```
Open `.env` and add your OpenAI API key:
```
OPENAI_API_KEY=your_openai_api_key_here
```
> Get your API key from: https://platform.openai.com/api-keys

### 5. Run the App
```bash
streamlit run app.py
```
Open your browser and go to `http://localhost:8501`

---

## 📁 Project Structure

```
resume-analyzer/
│
├── app.py              # Main Streamlit application
├── analyzer.py         # OpenAI GPT-4o integration & analysis logic
├── requirements.txt    # Python dependencies
├── .env.example        # Environment variable template
├── .gitignore          # Git ignore rules
└── README.md           # Project documentation
```

---

## 📸 Screenshots

> Upload your resume → Click Analyze → Get instant AI feedback with score, strengths, weaknesses, and keyword suggestions.

---

## 🔍 How It Works

1. User uploads a PDF, DOCX, or TXT resume
2. Text is extracted using PyPDF2 / docx2txt
3. Resume text is sent to OpenAI GPT-4o with a structured prompt
4. GPT-4o returns a JSON response with score, strengths, weaknesses, and recommendations
5. Results are displayed in a clean Streamlit UI
6. User can download the full analysis report

---

## 📌 Future Improvements

- [ ] Support for multiple resume comparison
- [ ] Job description matching (paste JD → get tailored feedback)
- [ ] LinkedIn profile analysis
- [ ] Resume rewriting suggestions
- [ ] Cover letter generator

---

## 👩‍💻 Author

**Mounika Patnam**  
 Python | AWS | GenAI  
[LinkedIn](https://linkedin.com/in/mounika-patnam) | [GitHub](https://github.com/patnammounika)

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).
