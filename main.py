from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import os
import json
from pathlib import Path
from dotenv import load_dotenv
import google.generativeai as genai
import PyPDF2
from docx import Document

load_dotenv()

app = FastAPI()

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure Gemini API
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY not found in .env file")

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-2.0-flash-lite")

# Session storage
sessions = {}

def extract_text_from_pdf(file_path):
    """Extract text from PDF"""
    text = ""
    with open(file_path, 'rb') as f:
        reader = PyPDF2.PdfReader(f)
        for page in reader.pages:
            text += page.extract_text()
    return text

def extract_text_from_docx(file_path):
    """Extract text from DOCX"""
    doc = Document(file_path)
    text = "\n".join([para.text for para in doc.paragraphs])
    return text

@app.post("/upload-resume")
async def upload_resume(file: UploadFile = File(...)):
    """Upload resume and create session"""
    try:
        session_id = f"session_{len(sessions) + 1}"
        file_path = f"/tmp/{session_id}_{file.filename}"
        
        # Save file
        with open(file_path, 'wb') as f:
            content = await file.read()
            f.write(content)
        
        # Extract text
        if file.filename.endswith('.pdf'):
            resume_text = extract_text_from_pdf(file_path)
        elif file.filename.endswith('.docx'):
            resume_text = extract_text_from_docx(file_path)
        else:
            raise ValueError("Unsupported file format")
        
        sessions[session_id] = {
            "filename": file.filename,
            "resume_text": resume_text,
            "file_path": file_path
        }
        
        return {"session_id": session_id, "message": "Resume uploaded successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/full-analysis")
async def full_analysis(data: dict):
    """Perform full analysis using Gemini AI"""
    try:
        session_id = data.get("session_id")
        job_description = data.get("job_description")
        
        if session_id not in sessions:
            raise ValueError("Invalid session ID")
        
        resume_text = sessions[session_id]["resume_text"]
        
        # Match Analysis
        match_prompt = f"""
        Analyze how well this resume matches the job description.
        
        RESUME:
        {resume_text}
        
        JOB DESCRIPTION:
        {job_description}
        
        Provide a JSON response with:
        {{
            "match_score": (0-100),
            "matched_skills": [list of skills from resume that match job],
            "missing_skills": [list of skills required but missing from resume],
            "summary": "brief analysis"
        }}
        """
        
        match_response = model.generate_content(match_prompt)
        match_data = json.loads(match_response.text)
        
        # Skill Gap Analysis
        gap_prompt = f"""
        Based on this resume and job description, identify skill gaps and provide learning roadmap.
        
        RESUME:
        {resume_text}
        
        JOB DESCRIPTION:
        {job_description}
        
        Provide a JSON response with:
        {{
            "gaps": [
                {{
                    "skill": "skill name",
                    "importance": "High/Medium/Low",
                    "how_to_learn": "learning approach",
                    "resources": ["resource 1", "resource 2"]
                }}
            ]
        }}
        """
        
        gap_response = model.generate_content(gap_prompt)
        gap_data = json.loads(gap_response.text)
        
        # Resume Rewriter
        rewrite_prompt = f"""
        Rewrite the resume bullets to be more impactful and aligned with this job description.
        
        RESUME:
        {resume_text}
        
        JOB DESCRIPTION:
        {job_description}
        
        Provide a JSON response with:
        {{
            "original_bullets": ["bullet 1", "bullet 2"],
            "rewritten_bullets": ["improved bullet 1", "improved bullet 2"],
            "improvements": "explanation of improvements"
        }}
        """
        
        rewrite_response = model.generate_content(rewrite_prompt)
        rewrite_data = json.loads(rewrite_response.text)
        
        # Interview Prep
        interview_prompt = f"""
        Generate 10 interview questions for this role based on the resume and job description.
        
        RESUME:
        {resume_text}
        
        JOB DESCRIPTION:
        {job_description}
        
        Provide a JSON response with:
        {{
            "questions": [
                {{
                    "question": "question text",
                    "difficulty": "Easy/Medium/Hard",
                    "category": "Technical/Soft Skills/etc",
                    "hint": "hint for answering"
                }}
            ]
        }}
        """
        
        interview_response = model.generate_content(interview_prompt)
        interview_data = json.loads(interview_response.text)
        
        return {
            "match": match_data,
            "gaps": gap_data,
            "rewrite": rewrite_data,
            "interview": interview_data
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
