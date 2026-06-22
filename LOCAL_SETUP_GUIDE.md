# CareerLens — Local Development Setup Guide

Complete guide to run CareerLens on your local machine for learning and development.

---

## 📋 Prerequisites

Before starting, make sure you have installed:

1. **Python 3.11+** - [Download](https://www.python.org/downloads/)
2. **Node.js 18+** - [Download](https://nodejs.org/)
3. **Git** - [Download](https://git-scm.com/)
4. **VS Code** - [Download](https://code.visualstudio.com/)
5. **Google Gemini API Key** - [Get Free API Key](https://ai.google.dev/)

### Verify Installations

```bash
python --version
node --version
npm --version
git --version
```

---

## 🚀 Step 1: Clone the Repository

```bash
# Clone the repository
git clone https://github.com/Lalitkishore667/careerlens.git
cd careerlens

# Open in VS Code
code .
```

---

## 🔧 Step 2: Backend Setup (FastAPI)

### 2.1 Create Virtual Environment

```bash
# Navigate to backend folder
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate
```

### 2.2 Install Dependencies

```bash
# Install required packages
pip install fastapi uvicorn google-genai python-dotenv PyPDF2 python-docx python-multipart
```

### 2.3 Set Up Environment Variables

Create a `.env` file in the `backend/` folder:

```bash
# Create .env file
# On Windows (PowerShell):
New-Item -Path ".env" -ItemType File

# On macOS/Linux:
touch .env
```

Add your Google Gemini API key to `.env`:

```
GEMINI_API_KEY=your_actual_api_key_here
```

**How to get your API key:**
1. Go to [Google AI Studio](https://ai.google.dev/)
2. Click "Get API Key"
3. Create a new API key
4. Copy and paste it into `.env`

### 2.4 Create Uploads Folder

```bash
# Create uploads directory for storing resumes
mkdir uploads
```

### 2.5 Run Backend Server

```bash
# Make sure you're in the backend folder and venv is activated
python main.py
```

You should see:
```
INFO:     Uvicorn running on http://127.0.0.1:8000
```

**Test the backend:**
- Open browser: http://localhost:8000/docs
- You'll see interactive API documentation (Swagger UI)

---

## 💻 Step 3: Frontend Setup (React + Vite)

### 3.1 Install Node Packages

Open a **new terminal** (keep backend running in the first one):

```bash
# Navigate to frontend folder
cd careerlens-frontend

# Install dependencies
npm install
# or if you have pnpm:
pnpm install
```

### 3.2 Run Development Server

```bash
# Start the development server
npm run dev
# or with pnpm:
pnpm dev
```

You should see:
```
VITE v7.1.9 ready in XXX ms
➜  Local:   http://localhost:5173/
```

---

## ✅ Step 4: Test Everything

### 4.1 Open the Application

1. Open browser: http://localhost:5173/
2. You should see the CareerLens homepage with:
   - Purple/cyan gradient hero section
   - "Analyze My Resume" button
   - Feature cards below

### 4.2 Test the Full Flow

1. **Upload a Resume**
   - Click "Drag and drop your resume"
   - Select a PDF or DOCX file
   - You should see "Resume uploaded successfully!"

2. **Enter Job Description**
   - Paste a job description in the text area
   - Click "Analyze My Resume"
   - Wait for AI analysis (takes 10-30 seconds)

3. **View Results**
   - Match Score (animated circular progress)
   - Skill Gaps (expandable cards)
   - Resume Rewriter (side-by-side comparison)
   - Interview Prep (10 questions)

---

## 📁 Project Structure Explained

```
careerlens/
│
├── backend/
│   ├── agents/
│   │   ├── __init__.py
│   │   ├── match_agent.py          # AI agent for match score
│   │   ├── gap_agent.py            # AI agent for skill gaps
│   │   ├── rewriter_agent.py       # AI agent for resume rewriting
│   │   └── interview_agent.py      # AI agent for interview questions
│   │
│   ├── parser.py                   # Resume parsing logic (PDF/DOCX)
│   ├── main.py                     # FastAPI application (main entry point)
│   ├── uploads/                    # Folder where uploaded resumes are stored
│   ├── .env                        # Environment variables (API keys)
│   └── venv/                       # Virtual environment (created by you)
│
└── careerlens-frontend/
    ├── client/
    │   ├── src/
    │   │   ├── components/
    │   │   │   ├── Navbar.tsx       # Top navigation bar
    │   │   │   ├── Hero.tsx         # Hero section with gradient text
    │   │   │   ├── UploadSection.tsx # Resume upload & job description
    │   │   │   ├── MatchScore.tsx   # Match score visualization
    │   │   │   ├── SkillGap.tsx     # Skill gap analysis display
    │   │   │   ├── ResumeRewriter.tsx # Rewritten resume display
    │   │   │   ├── InterviewPrep.tsx # Interview questions display
    │   │   │   └── Footer.tsx       # Footer with credits
    │   │   │
    │   │   ├── pages/
    │   │   │   └── Home.tsx         # Main page (orchestrates all components)
    │   │   │
    │   │   ├── App.tsx              # React app root
    │   │   ├── main.tsx             # React entry point
    │   │   └── index.css            # Global styles & theme colors
    │   │
    │   ├── index.html               # HTML template
    │   └── package.json             # Node dependencies
    │
    └── README.md                    # Project documentation
```

---

## 🎓 Learning Path

### Week 1: Understand the Architecture
- [ ] Read `backend/main.py` - Understand FastAPI routing
- [ ] Read `backend/parser.py` - Learn resume parsing
- [ ] Read `backend/agents/match_agent.py` - Understand AI prompting

### Week 2: Modify Backend
- [ ] Change the AI prompt in `match_agent.py` to get different results
- [ ] Add a new endpoint (e.g., `/salary-estimate`)
- [ ] Implement error handling improvements

### Week 3: Understand Frontend
- [ ] Read `client/src/pages/Home.tsx` - Understand React state management
- [ ] Read `client/src/components/MatchScore.tsx` - Learn animations
- [ ] Understand TailwindCSS styling in components

### Week 4: Modify Frontend
- [ ] Change colors in `client/src/index.css`
- [ ] Add a new component (e.g., `SalaryEstimate.tsx`)
- [ ] Modify animations in Framer Motion

---

## 🔍 Debugging Tips

### Backend Issues

**Problem: `ModuleNotFoundError: No module named 'google'`**
```bash
# Solution: Install missing package
pip install google-genai
```

**Problem: `GEMINI_API_KEY not found`**
```bash
# Solution: Check .env file exists and has correct key
cat .env
```

**Problem: Port 8000 already in use**
```bash
# Solution: Run on different port
python main.py --port 8001
```

### Frontend Issues

**Problem: `npm: command not found`**
```bash
# Solution: Install Node.js from nodejs.org
```

**Problem: Port 5173 already in use**
```bash
# Solution: Run on different port
npm run dev -- --port 3000
```

**Problem: API calls failing (CORS error)**
```bash
# Solution: Make sure backend is running on http://localhost:8000
```

---

## 📡 API Testing

### Test Backend Endpoints with cURL

```bash
# Test health check
curl http://localhost:8000/health

# Test upload resume (requires actual file)
curl -X POST -F "file=@resume.pdf" http://localhost:8000/upload-resume

# Test match endpoint
curl -X POST http://localhost:8000/match \
  -H "Content-Type: application/json" \
  -d '{"session_id":"test-id","job_description":"Python developer"}'
```

### Use Swagger UI

1. Open: http://localhost:8000/docs
2. Click on any endpoint
3. Click "Try it out"
4. Fill in parameters
5. Click "Execute"

---

## 🎨 Customization Ideas

### Easy Modifications

1. **Change Colors**
   - Edit `client/src/index.css` (lines 45-114)
   - Change `#7c3aed` (purple) to your favorite color

2. **Change Fonts**
   - Edit `client/index.html`
   - Import different Google Font

3. **Add Your Logo**
   - Replace logo URL in `client/src/components/Navbar.tsx`

### Medium Modifications

1. **Add New Analysis Type**
   - Create `backend/agents/salary_agent.py`
   - Add endpoint in `backend/main.py`
   - Create component in `client/src/components/SalaryAnalysis.tsx`

2. **Change AI Model**
   - Edit `backend/agents/*.py`
   - Change `model="gemini-2.0-flash-lite"` to different model

3. **Add Database**
   - Install SQLAlchemy: `pip install sqlalchemy`
   - Create models for storing analyses
   - Save results to database

---

## 📚 Resources for Learning

### Backend (FastAPI)
- [FastAPI Official Docs](https://fastapi.tiangolo.com/)
- [Google Gemini API Docs](https://ai.google.dev/docs)
- [Python Async/Await](https://docs.python.org/3/library/asyncio.html)

### Frontend (React + Vite)
- [React Official Docs](https://react.dev/)
- [Vite Documentation](https://vitejs.dev/)
- [TailwindCSS Docs](https://tailwindcss.com/docs)
- [Framer Motion Docs](https://www.framer.com/motion/)

### AI & Prompting
- [Prompt Engineering Guide](https://www.promptingguide.ai/)
- [Google AI Studio](https://ai.google.dev/)
- [LLM Best Practices](https://github.com/brexhq/prompt-engineering)

---

## 🚀 Next Steps After Setup

1. **Run the application** and test all features
2. **Read through the code** and understand how it works
3. **Make small modifications** (change colors, text, etc.)
4. **Add new features** (salary estimation, cover letter generation, etc.)
5. **Deploy to production** (Hugging Face Spaces for backend, Manus for frontend)

---

## 💡 Pro Tips

- **Use VS Code Extensions**: Prettier, ESLint, Python, Thunder Client (for API testing)
- **Debug with Browser DevTools**: F12 to open, check Network tab for API calls
- **Use `console.log()` in React**: Check browser console for debugging
- **Use `print()` in Python**: Check terminal for backend debugging
- **Keep backend and frontend terminals open**: Makes it easy to see errors

---

## 🆘 Need Help?

1. Check error messages carefully - they usually tell you what's wrong
2. Google the error message - chances are someone else had the same issue
3. Check the GitHub repository for issues/discussions
4. Review the code comments for explanations

---

**Happy Learning! 🎓**

Built with ❤️ for students learning AI and full-stack development.
