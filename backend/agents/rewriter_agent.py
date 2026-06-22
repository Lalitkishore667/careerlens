import os
import json
import asyncio
from dotenv import load_dotenv
from google import genai

load_dotenv()


class RewriterAgent:
    def __init__(self):
        self.client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
        self.model = "gemini-2.0-flash-lite"
    
    async def analyze(self, resume_text: str, job_description: str) -> dict:
        """Generate rewritten resume bullets optimized for job description"""
        prompt = f"""
You are an expert resume writer and ATS optimization specialist.

Rewrite the resume bullets to better match the job description. Return ONLY a valid JSON response with exactly this format:
{{
    "original_bullets": ["<original bullet 1>", "<original bullet 2>", ...],
    "rewritten_bullets": ["<rewritten bullet 1>", "<rewritten bullet 2>", ...],
    "improvements": "<2-3 sentence explanation of key improvements made>"
}}

For each original bullet point from the resume, provide an optimized version that:
1. Uses keywords from the job description
2. Emphasizes relevant achievements and metrics
3. Aligns with ATS scanning best practices
4. Maintains authenticity and accuracy

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
                "original_bullets": [],
                "rewritten_bullets": [],
                "improvements": "Unable to parse response"
            }
        except Exception as e:
            return {
                "original_bullets": [],
                "rewritten_bullets": [],
                "improvements": f"Error: {str(e)}"
            }
