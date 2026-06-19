from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import shutil
import os
import json
from parser import parse_resume
from agents.match_agent import match_resume_to_job

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

resume_store = {}

class JobDescription(BaseModel):
    job_description: str

@app.get("/")
def home():
    return {"message": "CareerLens API is running!"}

@app.post("/upload-resume")
async def upload_resume(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    result = parse_resume(file_path)
    resume_store["latest"] = result["raw_text"]
    return result

@app.post("/match")
async def match_resume(job: JobDescription):
    if "latest" not in resume_store:
        return {"error": "Please upload a resume first!"}
    
    resume_text = resume_store["latest"]
    result = match_resume_to_job(resume_text, job.job_description)
    
    try:
        return json.loads(result)
    except:
        return {"raw_response": result}