from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import os
import json
from pathlib import Path

app = FastAPI()

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Session storage
sessions = {}

@app.post("/upload-resume")
async def upload_resume(file: UploadFile = File(...)):
    """Upload resume and create session"""
    session_id = f"session_{len(sessions) + 1}"
    sessions[session_id] = {"filename": file.filename}
    return {"session_id": session_id, "message": "Resume uploaded successfully"}

@app.post("/full-analysis")
async def full_analysis(data: dict):
    """Return mock analysis data"""
    return {
        "match": {
            "match_score": 82,
            "matched_skills": ["Python", "FastAPI", "React", "Machine Learning", "Data Analysis", "REST APIs", "Git"],
            "missing_skills": ["Kubernetes", "Docker", "AWS", "GraphQL", "CI/CD"],
            "summary": "Excellent match! Your skills align well with this role. You have strong fundamentals in Python, FastAPI, and React. Focus on cloud technologies to boost your competitiveness."
        },
        "gaps": {
            "gaps": [
                {
                    "skill": "Docker",
                    "importance": "High",
                    "how_to_learn": "Learn containerization through Docker's official tutorial and build projects",
                    "resources": ["Docker Official Tutorial", "Docker Hub", "Play with Docker"]
                },
                {
                    "skill": "Kubernetes",
                    "importance": "High",
                    "how_to_learn": "Take the Linux Foundation Kubernetes course and practice on Minikube",
                    "resources": ["Linux Foundation CKA Course", "Kubernetes Official Docs", "Play with Kubernetes"]
                },
                {
                    "skill": "AWS",
                    "importance": "Medium",
                    "how_to_learn": "Complete AWS Solutions Architect Associate course",
                    "resources": ["AWS Free Tier", "A Cloud Guru", "Pluralsight AWS Courses"]
                },
                {
                    "skill": "CI/CD Pipelines",
                    "importance": "Medium",
                    "how_to_learn": "Learn GitHub Actions and Jenkins through hands-on projects",
                    "resources": ["GitHub Actions Docs", "Jenkins Tutorial", "GitLab CI Documentation"]
                }
            ]
        },
        "rewrite": {
            "original_bullets": [
                "Built a machine learning model using Python",
                "Developed REST APIs with FastAPI",
                "Created responsive UI with React"
            ],
            "rewritten_bullets": [
                "Engineered a production-grade ML model achieving 94% accuracy, processing 1M+ data points using Python, scikit-learn, and pandas",
                "Architected and deployed 5+ high-performance REST APIs using FastAPI, handling 10K+ requests/day with sub-100ms latency and 99.9% uptime",
                "Designed and implemented responsive web interfaces using React and Tailwind CSS, improving user engagement by 35% and reducing load time by 40%"
            ],
            "improvements": "Your resume bullets are solid, but they lack quantifiable impact. The rewritten versions include specific metrics (94% accuracy, 10K requests/day), technologies used, and business outcomes. This makes your achievements more compelling to recruiters."
        },
        "interview": {
            "questions": [
                {
                    "question": "Tell me about a time you optimized a machine learning model. What was the challenge and how did you solve it?",
                    "difficulty": "Medium",
                    "category": "Technical",
                    "hint": "Focus on the problem, your approach, tools used, and measurable results. Mention hyperparameter tuning, feature engineering, or algorithm selection."
                },
                {
                    "question": "How do you handle API rate limiting and caching in your FastAPI applications?",
                    "difficulty": "Medium",
                    "category": "Backend",
                    "hint": "Discuss Redis for caching, middleware for rate limiting, and explain trade-offs between performance and consistency."
                },
                {
                    "question": "Describe your experience with React hooks. When would you use useEffect vs useCallback?",
                    "difficulty": "Medium",
                    "category": "Frontend",
                    "hint": "Explain the purpose of each hook, dependency arrays, and performance optimization scenarios."
                },
                {
                    "question": "How do you approach debugging a slow API endpoint?",
                    "difficulty": "Medium",
                    "category": "Problem Solving",
                    "hint": "Mention profiling tools, database query optimization, caching strategies, and monitoring."
                },
                {
                    "question": "What's your experience with CI/CD pipelines? How have you used them?",
                    "difficulty": "Hard",
                    "category": "DevOps",
                    "hint": "Discuss GitHub Actions, Jenkins, or GitLab CI. Explain testing, deployment, and rollback strategies."
                },
                {
                    "question": "How do you ensure code quality in your projects?",
                    "difficulty": "Easy",
                    "category": "Best Practices",
                    "hint": "Mention linting, testing (unit, integration), code reviews, and documentation."
                },
                {
                    "question": "Tell me about a project where you had to learn a new technology quickly.",
                    "difficulty": "Easy",
                    "category": "Soft Skills",
                    "hint": "Show your learning ability, problem-solving approach, and how you applied the new knowledge."
                },
                {
                    "question": "How do you handle technical debt in a codebase?",
                    "difficulty": "Hard",
                    "category": "Architecture",
                    "hint": "Discuss prioritization, refactoring strategies, and balancing new features with code quality."
                },
                {
                    "question": "What's your approach to testing? How do you decide what to test?",
                    "difficulty": "Medium",
                    "category": "Quality Assurance",
                    "hint": "Discuss unit tests, integration tests, coverage targets, and testing pyramid concept."
                },
                {
                    "question": "Describe a time you worked in a team on a complex project. How did you communicate and collaborate?",
                    "difficulty": "Easy",
                    "category": "Soft Skills",
                    "hint": "Emphasize communication, collaboration tools, code reviews, and how you handled disagreements."
                }
            ]
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
