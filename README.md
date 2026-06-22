# CareerLens — AI-Powered Career Intelligence Platform

A full-stack AI web application that transforms your resume and job search journey. Upload your resume, paste a job description, and get a complete career intelligence report with match score, skill gaps, rewritten resume, and interview questions.

## 🚀 Features

- **Match Score**: Get an AI-calculated match percentage between your resume and the job description
- **Skill Gap Analysis**: Identify missing skills with importance levels and learning resources
- **Resume Rewriter**: Get AI-optimized resume bullets tailored to the job description
- **Interview Prep**: 10 role-specific interview questions with difficulty levels and hints
- **Beautiful UI**: Premium dark theme with purple/cyan gradients, glassmorphism, and smooth animations
- **Session-based Storage**: Resume persists across API calls within a session

## 🛠️ Tech Stack

### Frontend
- **React 19** + **Vite** - Fast, modern frontend framework
- **TailwindCSS 4** - Utility-first CSS framework
- **Framer Motion** - Smooth animations and transitions
- **shadcn/ui** - Pre-built, customizable components
- **TypeScript** - Type-safe development

### Backend
- **FastAPI** - Modern, fast Python web framework
- **Google Gemini 2.0 Flash Lite** - AI engine for analysis
- **PyPDF2 + python-docx** - Resume parsing

## 📋 Project Structure

```
careerlens/
├── backend/
│   ├── agents/
│   │   ├── match_agent.py
│   │   ├── gap_agent.py
│   │   ├── rewriter_agent.py
│   │   └── interview_agent.py
│   ├── parser.py
│   ├── main.py
│   └── uploads/
│
└── careerlens-frontend/
    └── client/src/
        ├── components/
        ├── pages/
        └── App.tsx
```

## 🚀 Getting Started

### Backend Setup

```bash
cd careerlens/backend
pip install fastapi uvicorn google-genai python-dotenv PyPDF2 python-docx python-multipart
```

Create `.env` file:
```
GEMINI_API_KEY=your_api_key
```

Run:
```bash
python main.py
```

### Frontend Setup

```bash
cd careerlens-frontend
pnpm install
pnpm dev
```

## 📡 API Endpoints

- `POST /upload-resume` - Upload resume file
- `POST /match` - Calculate match score
- `POST /gap-analysis` - Analyze skill gaps
- `POST /rewrite-resume` - Generate rewritten bullets
- `POST /interview-questions` - Generate interview questions
- `POST /full-analysis` - Run all analyses in parallel

## 🎨 Design

Premium Tech SaaS aesthetic with dark theme, purple/cyan gradients, glassmorphism, and smooth Framer Motion animations.

## 👨‍💻 Developer

**Lalit Kishore** - B.Tech AI & Data Science, Velammal Institute of Technology, Chennai

---

Built with React, FastAPI, and Google Gemini AI
