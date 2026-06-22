import os
import json
import asyncio
from dotenv import load_dotenv
from google import genai

load_dotenv()


class GapAgent:
    def __init__(self):
        self.client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
        self.model = "gemini-2.0-flash-lite"
    
    async def analyze(self, resume_text: str, job_description: str) -> dict:
        """Analyze skill gaps between resume and job description"""
        prompt = f"""
You are an expert career coach specializing in skill development.

Analyze the skill gaps between this resume and job description. Return ONLY a valid JSON response with exactly this format:
{{
    "gaps": [
        {{
            "skill": "<skill name>",
            "importance": "<Critical/High/Medium>",
            "how_to_learn": "<brief 1-2 sentence explanation of how to learn this skill>",
            "resources": ["<resource 1>", "<resource 2>", "<resource 3>"]
        }}
    ]
}}

Identify 5-8 key skill gaps. For each gap, provide practical learning resources (online courses, certifications, projects, etc.).

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
                "gaps": []
            }
        except Exception as e:
            return {
                "gaps": []
            }
