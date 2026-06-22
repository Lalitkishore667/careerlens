import os
import json
import asyncio
from dotenv import load_dotenv
from google import genai

load_dotenv()


class InterviewAgent:
    def __init__(self):
        self.client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
        self.model = "gemini-2.0-flash-lite"
    
    async def analyze(self, resume_text: str, job_description: str) -> dict:
        """Generate interview questions based on job description and resume"""
        prompt = f"""
You are an expert interview coach and hiring manager.

Generate 10 role-specific interview questions based on the resume and job description. Return ONLY a valid JSON response with exactly this format:
{{
    "questions": [
        {{
            "question": "<interview question>",
            "hint": "<brief hint or approach to answer>",
            "difficulty": "<Easy/Medium/Hard>",
            "category": "<Technical/Behavioral/Experience>"
        }}
    ]
}}

Questions should:
1. Be specific to the role and job description
2. Reference the candidate's experience from the resume
3. Mix technical, behavioral, and experience-based questions
4. Range from Easy to Hard difficulty
5. Help the candidate prepare thoroughly

RESUME:
{resume_text}

JOB DESCRIPTION:
{job_description}

Return ONLY the JSON, no extra text or markdown.
"""
        
        try:
            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt
            )
            
            # Parse JSON response
            response_text = response.text.strip()
            # Remove markdown code blocks if present
            if response_text.startswith("```"):
                response_text = response_text.split("```")[1]
                if response_text.startswith("json"):
                    response_text = response_text[4:]
            
            result = json.loads(response_text)
            return result
        except json.JSONDecodeError:
            # Return default structure if JSON parsing fails
            return {
                "questions": []
            }
        except Exception as e:
            return {
                "questions": []
            }
