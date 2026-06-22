# CareerLens — Code Walkthrough for Learning

A detailed explanation of how the code works, perfect for understanding the architecture.

---

## 🏗️ Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    React Frontend (Port 5173)               │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  Hero Section → Upload Resume → View Results        │   │
│  │  (Framer Motion animations, TailwindCSS styling)    │   │
│  └──────────────────────────────────────────────────────┘   │
└──────────────────────┬──────────────────────────────────────┘
                       │ HTTP Requests (JSON)
                       │
┌──────────────────────▼──────────────────────────────────────┐
│                   FastAPI Backend (Port 8000)               │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  /upload-resume → Parse Resume → Store Session      │   │
│  │  /match → Match Agent → Gemini AI → JSON Response   │   │
│  │  /gap-analysis → Gap Agent → Gemini AI → JSON       │   │
│  │  /rewrite-resume → Rewriter Agent → Gemini AI       │   │
│  │  /interview-questions → Interview Agent → Gemini AI │   │
│  └──────────────────────────────────────────────────────┘   │
└──────────────────────┬──────────────────────────────────────┘
                       │ API Calls
                       │
┌──────────────────────▼──────────────────────────────────────┐
│              Google Gemini 2.0 Flash Lite API               │
│  (AI Model that generates all analysis and recommendations) │
└──────────────────────────────────────────────────────────────┘
```

---

## 📝 Backend Code Walkthrough

### File: `backend/main.py`

This is the **main entry point** for the backend. It defines all API endpoints.

```python
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware

# Create FastAPI app
app = FastAPI()

# Enable CORS (allows frontend to make requests)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow requests from any origin
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

# In-memory storage for sessions
# Key: session_id, Value: {file_path, raw_text, etc.}
sessions = {}
```

**Key Concepts:**
- **FastAPI**: Modern Python web framework for building APIs
- **CORS**: Allows frontend (different port) to communicate with backend
- **Sessions**: Store resume data so it persists across multiple API calls

### Endpoint 1: `/upload-resume`

```python
@app.post("/upload-resume")
async def upload_resume(file: UploadFile = File(...)):
    """
    User uploads a resume file (PDF or DOCX)
    Returns: session_id (unique identifier for this session)
    """
    
    # Validate file type
    if file.content_type not in ["application/pdf", "application/vnd.openxmlformats-officedocument.wordprocessingml.document"]:
        raise HTTPException(status_code=400, detail="Only PDF and DOCX files are supported")
    
    # Generate unique session ID
    session_id = str(uuid.uuid4())
    
    # Save file to uploads/ folder
    file_path = UPLOADS_DIR / f"{session_id}_{file.filename}"
    with open(file_path, "wb") as f:
        shutil.copyfileobj(file.file, f)
    
    # Parse resume text from file
    raw_text = parse_resume(str(file_path))
    
    # Store in session
    sessions[session_id] = {
        "file_path": str(file_path),
        "file_name": file.filename,
        "file_type": file.content_type,
        "raw_text": raw_text
    }
    
    return {
        "session_id": session_id,
        "raw_text": raw_text,
        "file_name": file.filename,
        "file_type": file.content_type
    }
```

**What's Happening:**
1. User uploads a file
2. We validate it's PDF or DOCX
3. Create unique session ID
4. Save file to disk
5. Extract text from file
6. Store session data in memory
7. Return session_id to frontend

### Endpoint 2: `/match`

```python
@app.post("/match")
async def match_resume(request: JobDescriptionRequest):
    """
    Analyze match between resume and job description
    Input: session_id, job_description
    Output: match_score, matched_skills, missing_skills, etc.
    """
    
    # Get resume text from session
    session_id = request.session_id
    resume_text = sessions[session_id]["raw_text"]
    job_description = request.job_description
    
    # Call AI agent to analyze
    result = await match_agent.analyze(resume_text, job_description)
    
    return result
```

**What's Happening:**
1. Frontend sends session_id and job description
2. We retrieve the resume text from session storage
3. Call MatchAgent (AI agent) to analyze
4. Return results to frontend

### File: `backend/agents/match_agent.py`

This is where the **AI magic happens**.

```python
class MatchAgent:
    def __init__(self):
        # Initialize Google Gemini API client
        self.client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
        self.model = "gemini-2.0-flash-lite"
    
    async def analyze(self, resume_text: str, job_description: str) -> dict:
        """
        Send resume and job description to Gemini AI
        AI analyzes and returns structured JSON response
        """
        
        # Create the prompt (instructions for AI)
        prompt = f"""
You are an expert career coach and ATS system.

Analyze this resume against the job description and return ONLY a valid JSON response with exactly this format:
{{
    "match_score": <number between 0-100>,
    "matched_skills": [<list of skills that match>],
    "missing_skills": [<list of skills missing from resume>],
    "experience_match": "<Strong/Moderate/Weak>",
    "summary": "<2-3 sentence summary of the match>"
}}

RESUME:
{resume_text}

JOB DESCRIPTION:
{job_description}

Return ONLY the JSON, no extra text or markdown.
"""
        
        # Send to Gemini AI
        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt
        )
        
        # Parse JSON response
        response_text = response.text.strip()
        result = json.loads(response_text)
        
        return result
```

**Key Concepts:**
- **Prompt Engineering**: The prompt tells AI exactly what to do
- **JSON Response**: AI returns structured data, not just text
- **Async/Await**: Non-blocking operations (doesn't freeze the server)

### File: `backend/parser.py`

This file **extracts text from resume files**.

```python
def extract_text_from_pdf(file_path):
    """Extract text from PDF file"""
    text = ""
    with open(file_path, "rb") as f:
        reader = PyPDF2.PdfReader(f)
        for page in reader.pages:
            text += page.extract_text()
    return text

def extract_text_from_docx(file_path):
    """Extract text from DOCX file"""
    doc = docx.Document(file_path)
    text = ""
    for paragraph in doc.paragraphs:
        text += paragraph.text + "\n"
    return text

def parse_resume(file_path):
    """Determine file type and extract text"""
    ext = os.path.splitext(file_path)[1].lower()
    
    if ext == ".pdf":
        text = extract_text_from_pdf(file_path)
    elif ext == ".docx":
        text = extract_text_from_docx(file_path)
    else:
        return {"error": "Unsupported file type"}
    
    return {
        "raw_text": text,
        "file_name": os.path.basename(file_path),
        "file_type": ext
    }
```

**What's Happening:**
1. Check file extension (.pdf or .docx)
2. Use appropriate library to extract text
3. Return extracted text

---

## 💻 Frontend Code Walkthrough

### File: `client/src/pages/Home.tsx`

This is the **main page** that orchestrates everything.

```typescript
export default function Home() {
  // State management
  const [isLoading, setIsLoading] = useState(false);
  const [results, setResults] = useState<AnalysisResults | null>(null);
  const [showResults, setShowResults] = useState(false);

  // Handle analyze button click
  const handleAnalyze = async (sessionId: string, jobDescription: string) => {
    setIsLoading(true);
    
    try {
      // Make API call to backend
      const response = await fetch("http://localhost:8000/full-analysis", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          session_id: sessionId,
          job_description: jobDescription,
        }),
      });

      const data = await response.json();
      setResults(data);
      setShowResults(true);

      // Trigger confetti if score > 80
      if (data.match.match_score >= 80) {
        triggerConfetti();
      }

      toast.success("Analysis complete!");
    } catch (error) {
      toast.error("Failed to analyze resume");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div>
      <Navbar />
      
      {!showResults ? (
        <>
          <Hero onAnalyzeClick={...} />
          <UploadSection onAnalyze={handleAnalyze} isLoading={isLoading} />
        </>
      ) : (
        <div>
          <MatchScore {...results.match} />
          <SkillGap gaps={results.gaps.gaps} />
          <ResumeRewriter {...results.rewrite} />
          <InterviewPrep questions={results.interview.questions} />
        </div>
      )}
      
      <Footer />
    </div>
  );
}
```

**Key Concepts:**
- **useState**: React hook for managing component state
- **Conditional Rendering**: Show different UI based on state
- **Async/Await**: Wait for API response before updating UI
- **Error Handling**: Catch errors and show toast notifications

### File: `client/src/components/UploadSection.tsx`

This component handles **resume upload and job description input**.

```typescript
export default function UploadSection({ onAnalyze, isLoading }: UploadSectionProps) {
  const [resumeFile, setResumeFile] = useState<File | null>(null);
  const [jobDescription, setJobDescription] = useState("");
  const [sessionId, setSessionId] = useState<string | null>(null);

  // Handle file selection
  const handleFileSelect = async (file: File) => {
    setResumeFile(file);
    
    // Create FormData for file upload
    const formData = new FormData();
    formData.append("file", file);

    // Upload to backend
    const response = await fetch("http://localhost:8000/upload-resume", {
      method: "POST",
      body: formData,
    });

    const data = await response.json();
    setSessionId(data.session_id);  // Save session ID
    toast.success("Resume uploaded successfully!");
  };

  // Handle drag and drop
  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    const file = e.dataTransfer.files[0];
    if (file) handleFileSelect(file);
  };

  // Handle analyze button
  const handleAnalyze = () => {
    if (!sessionId || !jobDescription.trim()) {
      toast.error("Please upload resume and enter job description");
      return;
    }
    onAnalyze(sessionId, jobDescription);
  };

  return (
    <div>
      {/* Resume Upload Area */}
      <div onDrop={handleDrop} onDragOver={handleDragOver}>
        {resumeFile ? (
          <p>{resumeFile.name}</p>
        ) : (
          <p>Drag and drop your resume here</p>
        )}
      </div>

      {/* Job Description Input */}
      <textarea
        value={jobDescription}
        onChange={(e) => setJobDescription(e.target.value)}
        placeholder="Paste the job description here..."
      />

      {/* Analyze Button */}
      <button onClick={handleAnalyze} disabled={isLoading}>
        {isLoading ? "Analyzing..." : "Analyze My Resume"}
      </button>
    </div>
  );
}
```

**Key Concepts:**
- **FormData**: Special object for uploading files
- **Drag and Drop**: HTML5 API for better UX
- **Controlled Components**: Input value controlled by React state

### File: `client/src/components/MatchScore.tsx`

This component **displays the match score** with animations.

```typescript
export default function MatchScore({
  score,
  matchedSkills,
  missingSkills,
  summary,
  experienceMatch,
}: MatchScoreProps) {
  const [displayScore, setDisplayScore] = useState(0);

  // Animate score counting from 0 to final score
  useEffect(() => {
    let interval: NodeJS.Timeout;
    if (displayScore < score) {
      interval = setInterval(() => {
        setDisplayScore((prev) => Math.min(prev + 2, score));
      }, 20);
    }
    return () => clearInterval(interval);
  }, [score]);

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      whileInView={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.6 }}
    >
      {/* Circular SVG Progress Ring */}
      <svg viewBox="0 0 200 200">
        <circle cx="100" cy="100" r="90" fill="none" stroke="#ffffff10" strokeWidth="8" />
        <motion.circle
          cx="100"
          cy="100"
          r="90"
          fill="none"
          stroke="url(#scoreGradient)"
          strokeWidth="8"
          strokeDasharray={`${(displayScore / 100) * 565.48} 565.48`}
          animate={{ strokeDasharray: `${(displayScore / 100) * 565.48} 565.48` }}
        />
      </svg>

      {/* Display Score */}
      <div>{displayScore}%</div>

      {/* Skills */}
      <div>
        <h4>Matched Skills</h4>
        {matchedSkills.map((skill) => (
          <Badge key={skill} className="bg-green-500/20">
            ✓ {skill}
          </Badge>
        ))}
      </div>

      <div>
        <h4>Missing Skills</h4>
        {missingSkills.map((skill) => (
          <Badge key={skill} className="bg-red-500/20">
            ✗ {skill}
          </Badge>
        ))}
      </div>
    </motion.div>
  );
}
```

**Key Concepts:**
- **useEffect**: Run side effects (animations) after render
- **SVG**: Scalable Vector Graphics for circular progress
- **Framer Motion**: Smooth animations
- **Array Mapping**: Render lists of skills

### File: `client/src/index.css`

This file defines **all colors and global styles**.

```css
:root {
  /* Colors */
  --primary: #7c3aed;           /* Purple */
  --secondary: #06b6d4;         /* Cyan */
  --background: #0a0a0a;        /* Deep black */
  --card: #1a1a1a;              /* Card background */
  --foreground: #ffffff;        /* White text */
  
  /* Other colors */
  --accent: #f59e0b;            /* Amber */
  --success: #10b981;           /* Green */
  --error: #ef4444;             /* Red */
}

/* Global styles */
body {
  background-color: var(--background);
  color: var(--foreground);
  font-family: Inter, sans-serif;
}

/* Custom components */
.container {
  max-width: 1280px;
  margin: 0 auto;
  padding: 0 1rem;
}
```

**Key Concepts:**
- **CSS Variables**: Reusable color values
- **Dark Theme**: All colors are dark-friendly
- **Tailwind Integration**: Works with Tailwind utilities

---

## 🔄 Data Flow Example

Let's trace what happens when a user clicks "Analyze My Resume":

### Step 1: Frontend - Upload Resume
```
User clicks upload → handleFileSelect() → FormData → fetch("/upload-resume")
```

### Step 2: Backend - Receive Upload
```
Backend receives file → validate → parse resume → store in sessions → return session_id
```

### Step 3: Frontend - Store Session ID
```
setSessionId(data.session_id) → User can now analyze
```

### Step 4: Frontend - Click Analyze
```
User clicks "Analyze" → handleAnalyze() → fetch("/full-analysis")
```

### Step 5: Backend - Run All Analyses
```
Backend receives session_id + job_description
→ Get resume from sessions[session_id]
→ Call match_agent.analyze()
→ Call gap_agent.analyze()
→ Call rewriter_agent.analyze()
→ Call interview_agent.analyze()
→ Return all results as JSON
```

### Step 6: AI Processing (Inside Each Agent)
```
Agent receives resume + job_description
→ Create prompt
→ Send to Gemini API
→ Receive AI response
→ Parse JSON
→ Return structured data
```

### Step 7: Frontend - Display Results
```
setResults(data) → setShowResults(true)
→ React re-renders with MatchScore, SkillGap, etc.
→ Components animate in with Framer Motion
```

---

## 🎓 Learning Exercises

### Exercise 1: Change Colors
**Difficulty**: Easy

1. Open `client/src/index.css`
2. Change `--primary: #7c3aed` to `#ff00ff` (magenta)
3. Refresh browser - all purple elements are now magenta!

### Exercise 2: Add New AI Agent
**Difficulty**: Medium

1. Create `backend/agents/salary_agent.py`
2. Copy structure from `match_agent.py`
3. Change prompt to analyze salary expectations
4. Add endpoint in `backend/main.py`
5. Create component in frontend

### Exercise 3: Modify AI Prompt
**Difficulty**: Easy

1. Open `backend/agents/match_agent.py`
2. Change the prompt text
3. Run backend again
4. Test with new prompt

---

## 📚 Key Technologies Explained

### FastAPI
- Modern Python web framework
- Automatic API documentation (Swagger UI)
- Type hints for validation
- Async support for performance

### React
- Component-based UI library
- State management with hooks
- Virtual DOM for efficient rendering
- Reusable components

### TailwindCSS
- Utility-first CSS framework
- No need to write custom CSS
- Responsive design built-in
- Dark mode support

### Framer Motion
- Animation library for React
- Smooth transitions and entrance effects
- Physics-based animations
- Easy to use API

### Google Gemini AI
- Large Language Model (LLM)
- Understands and generates text
- Can analyze resumes and job descriptions
- Free API tier available

---

## 🚀 Next Learning Steps

1. **Understand async/await** - How backend handles multiple requests
2. **Learn React hooks** - useState, useEffect, useContext
3. **Study prompt engineering** - How to write better AI prompts
4. **Explore TailwindCSS** - Build custom UI components
5. **Deploy to production** - Hugging Face Spaces + Manus

---

**Happy Learning! 🎓**

This code is designed to be educational. Feel free to modify, experiment, and break things - that's how you learn!
