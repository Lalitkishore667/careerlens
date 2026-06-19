# 🎯 CareerLens — AI-Powered Career Intelligence Platform

> Built with FastAPI, LangChain, and Google Gemini AI

## 🚀 What is CareerLens?

CareerLens is an end-to-end AI platform that helps job seekers optimize their resume for any job description. Upload your resume, paste a job description, and get instant AI-powered insights.

## ✨ Features

- 📄 **Resume Parser** — Extracts text from PDF and DOCX resumes
- 🎯 **AI Match Scorer** — Scores your resume against any job description (0-100%)
- 🕳️ **Skill Gap Analyzer** — Identifies missing skills with learning roadmap
- ✍️ **Resume Rewriter** — Rewrites bullet points to match job description
- 🤖 **Interview Generator** — Generates role-specific interview questions

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | FastAPI, Python |
| AI Engine | Google Gemini AI, LangChain |
| Vector DB | FAISS |
| Resume Parsing | PyPDF2, python-docx |
| Deployment | Hugging Face Spaces |

## ⚙️ Setup & Installation

```bash
# Clone the repo
git clone https://github.com/Lalitkishore667/careerlens.git
cd careerlens

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Add your Gemini API key
echo "GEMINI_API_KEY=your_key_here" > backend/.env

# Run the server
cd backend
uvicorn main:app --reload
```

## 📡 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Health check |
| POST | `/upload-resume` | Upload PDF/DOCX resume |
| POST | `/match` | Match resume to job description |

## 🎯 Built For

This project was built as part of targeting **Salesforce's Futureforce** program — demonstrating real-world agentic AI development skills.

## 👨‍💻 Author

**Lalit Kishore** — B.Tech AI & Data Science
- GitHub: [@Lalitkishore667](https://github.com/Lalitkishore667)
- LinkedIn: [Lalit Kishore](https://linkedin.com/in/lalitkishore667)
