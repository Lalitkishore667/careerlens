from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import os
import json
import uuid
from pathlib import Path
from dotenv import load_dotenv
import asyncio
import shutil

# Import AI agents
from agents.match_agent import MatchAgent
from agents.gap_agent import GapAgent
from agents.rewriter_agent import RewriterAgent
from agents.interview_agent import InterviewAgent
from parser import parse_resume

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

# Create uploads directory if it doesn't exist
UPLOADS_DIR = Path("uploads")
UPLOADS_DIR.mkdir(exist_ok=True)

# Initialize AI agents
match_agent = MatchAgent()
gap_agent = GapAgent()
rewriter_agent = RewriterAgent()
interview_agent = InterviewAgent()

# In-memory session storage (maps session_id to resume data)
sessions = {}


class JobDescriptionRequest(BaseModel):
    session_id: str
    job_description: str


@app.get("/")
def home():
    return {"message": "CareerLens API is running!"}


@app.post("/upload-resume")
async def upload_resume(file: UploadFile = File(...)):
    """Upload and parse resume file (PDF or DOCX)"""
    try:
        # Validate file type
        if file.content_type not in [
            "application/pdf",
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            "application/msword"
        ]:
            raise HTTPException(status_code=400, detail="Only PDF and DOCX files are supported")
        
        # Generate session ID
        session_id = str(uuid.uuid4())
        
        # Save file to uploads folder
        file_path = UPLOADS_DIR / f"{session_id}_{file.filename}"
        with open(file_path, "wb") as f:
            shutil.copyfileobj(file.file, f)
        
        # Parse resume text
        raw_text = parse_resume(str(file_path))
        
        # Store session data
        sessions[session_id] = {
            "file_path": str(file_path),
            "file_name": file.filename,
            "file_type": file.content_type,
            "raw_text": raw_text
        }
        
        return JSONResponse({
            "session_id": session_id,
            "raw_text": raw_text,
            "file_name": file.filename,
            "file_type": file.content_type
        })
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/match")
async def match_resume(request: JobDescriptionRequest):
    """Calculate match score between resume and job description"""
    try:
        session_id = request.session_id
        job_description = request.job_description
        
        if not session_id or session_id not in sessions:
            raise HTTPException(status_code=400, detail="Invalid session ID")
        
        resume_text = sessions[session_id]["raw_text"]
        
        # Get match analysis from AI agent
        result = await match_agent.analyze(resume_text, job_description)
        
        return JSONResponse(result)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/gap-analysis")
async def gap_analysis(request: JobDescriptionRequest):
    """Analyze skill gaps between resume and job description"""
    try:
        session_id = request.session_id
        job_description = request.job_description
        
        if not session_id or session_id not in sessions:
            raise HTTPException(status_code=400, detail="Invalid session ID")
        
        resume_text = sessions[session_id]["raw_text"]
        
        # Get gap analysis from AI agent
        result = await gap_agent.analyze(resume_text, job_description)
        
        return JSONResponse(result)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/rewrite-resume")
async def rewrite_resume(request: JobDescriptionRequest):
    """Generate rewritten resume bullets optimized for job description"""
    try:
        session_id = request.session_id
        job_description = request.job_description
        
        if not session_id or session_id not in sessions:
            raise HTTPException(status_code=400, detail="Invalid session ID")
        
        resume_text = sessions[session_id]["raw_text"]
        
        # Get rewritten resume from AI agent
        result = await rewriter_agent.analyze(resume_text, job_description)
        
        return JSONResponse(result)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/interview-questions")
async def interview_questions(request: JobDescriptionRequest):
    """Generate interview questions based on job description and resume"""
    try:
        session_id = request.session_id
        job_description = request.job_description
        
        if not session_id or session_id not in sessions:
            raise HTTPException(status_code=400, detail="Invalid session ID")
        
        resume_text = sessions[session_id]["raw_text"]
        
        # Get interview questions from AI agent
        result = await interview_agent.analyze(resume_text, job_description)
        
        return JSONResponse(result)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/full-analysis")
async def full_analysis(request: JobDescriptionRequest):
    """Run all 4 analyses in parallel"""
    try:
        session_id = request.session_id
        job_description = request.job_description
        
        if not session_id or session_id not in sessions:
            raise HTTPException(status_code=400, detail="Invalid session ID")
        
        resume_text = sessions[session_id]["raw_text"]
        
        # Run all analyses in parallel
        results = await asyncio.gather(
            match_agent.analyze(resume_text, job_description),
            gap_agent.analyze(resume_text, job_description),
            rewriter_agent.analyze(resume_text, job_description),
            interview_agent.analyze(resume_text, job_description)
        )
        
        return JSONResponse({
            "match": results[0],
            "gaps": results[1],
            "rewrite": results[2],
            "interview": results[3]
        })
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return JSONResponse({"status": "healthy"})


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
