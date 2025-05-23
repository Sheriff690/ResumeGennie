from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi import Request
from pydantic import BaseModel
from openai import OpenAI
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = FastAPI(
    title="Resume Generator API",
    description="Generate professional resumes using AI",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure this properly for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize templates
templates = Jinja2Templates(directory="templates")

# Initialize OpenAI client for Groq
client = OpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=os.getenv("GROQ_API_KEY"),
)


# Pydantic models
class ResumeRequest(BaseModel):
    description: str
    additional_details: str = ""
    resume_style: str = "professional"  # professional, modern, creative


class ResumeResponse(BaseModel):
    resume: str
    success: bool
    message: str = ""


@app.get("/", response_class=HTMLResponse)
async def serve_frontend(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/api")
async def api_info():
    return {
        "message": "Resume Generator API",
        "version": "1.0.0",
        "endpoints": ["/generate-resume", "/health", "/api"]
    }


@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "resume-generator"}


@app.post("/generate-resume", response_model=ResumeResponse)
async def generate_resume(request: ResumeRequest):
    try:
        # Validate input
        if not request.description.strip():
            raise HTTPException(status_code=400, detail="Description cannot be empty")

        # Create the prompt based on user input and style
        prompt = create_resume_prompt(request.description, request.additional_details, request.resume_style)

        # Make API call to Groq
        response = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[
                {
                    "role": "system",
                    "content": "You are a professional resume writer with expertise in creating compelling resumes for various industries. Create well-structured, ATS-friendly resumes."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            max_tokens=1500,
            temperature=0.7
        )

        resume_content = response.choices[0].message.content

        return ResumeResponse(
            resume=resume_content,
            success=True,
            message="Resume generated successfully"
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate resume: {str(e)}"
        )


def create_resume_prompt(description: str, additional_details: str, style: str) -> str:
    """Create a detailed prompt for resume generation"""

    style_instructions = {
        "professional": "Create a traditional, professional resume format with clear sections and conservative formatting.",
        "modern": "Create a modern resume with a clean design, using contemporary formatting while maintaining professionalism.",
        "creative": "Create a creative resume that stands out while remaining professional and readable."
    }

    prompt = f"""
Based on the following information, create a comprehensive and professional resume:

User Description: {description}

Additional Details: {additional_details if additional_details else "None provided"}

Style: {style_instructions.get(style, style_instructions["professional"])}

Please include the following sections where relevant:
1. Professional Summary/Objective
2. Work Experience (with specific achievements and responsibilities)
3. Technical Skills
4. Education
5. Projects (if applicable)
6. Certifications (if applicable)

Guidelines:
- Use strong action verbs
- Include quantifiable achievements where possible
- Make it ATS (Applicant Tracking System) friendly
- Ensure proper formatting and structure
- Keep it concise but comprehensive
- Use industry-relevant keywords

If specific company names or details are not provided, create realistic examples that fit the described experience level and role.

Format the resume in a clean, readable text format that can be easily copied and used.
"""

    return prompt


# Error handlers
@app.exception_handler(404)
async def not_found_handler(request, exc):
    return {"error": "Endpoint not found", "status_code": 404}


@app.exception_handler(500)
async def internal_error_handler(request, exc):
    return {"error": "Internal server error", "status_code": 500}