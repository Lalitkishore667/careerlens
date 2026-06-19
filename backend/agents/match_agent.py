import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def match_resume_to_job(resume_text, job_description):
    prompt = f"""
    You are an expert career coach and ATS system.
    
    Analyze this resume against the job description and return a JSON response with exactly this format:
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
    
    Return only the JSON, no extra text.
    """
    
    response = client.models.generate_content(
        model="gemini-1.5-flash",
        contents=prompt
    )
    return response.text