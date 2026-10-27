from pydantic import BaseModel, Field
from typing import Optional
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Create the JobGuard SA application
app = FastAPI(
    title="JobGuard SA",
    description="AI-powered job scam detection and verification API",
    version="1.0.0"
)

# Allow the React frontend to communicate with the backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ],
    allow_credentials=False,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type", "Authorization"]
)


# Home endpoint
@app.get("/")
def home():
    return {
        "application": "JobGuard SA",
        "message": "Welcome to JobGuard SA API",
        "status": "running"
    }


# Health check endpoint
@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "JobGuard SA Backend"
    }

from pydantic import BaseModel


# Information sent by the website
class JobRequest(BaseModel):
    job_text: str = Field(
        ...,
        min_length=10,
        max_length=10000
    )

    job_url: Optional[str] = None
    company_name: Optional[str] = None


# Analyse the job advert for common warning signs
def analyse_job(job_text: str):
    text = job_text.lower()
    warning_signs = []

    payment_phrases = [
        "registration fee",
        "application fee",
        "processing fee",
        "pay upfront",
        "pay before you start",
        "pay a fee",
    ]

    suspicious_phrases = [
        "guaranteed job",
        "no interview required",
        "send your password",
        "send your id number",
        "urgent hiring",
    ]

    for phrase in payment_phrases:
        if phrase in text:
            warning_signs.append(
                f"Possible upfront payment request: '{phrase}'"
            )

    for phrase in suspicious_phrases:
        if phrase in text:
            warning_signs.append(
                f"Suspicious wording found: '{phrase}'"
            )

    if warning_signs:
        risk_level = "High"
        advice = (
            "This advert contains warning signs. Verify the employer "
            "independently before paying money or sharing personal details."
        )
    else:
        risk_level = "Uncertain"
        advice = (
            "No warning phrases from our checklist were found. "
            "This does not prove the job is legitimate."
        )

    return {
        "risk_level": risk_level,
        "warning_signs": warning_signs,
        "advice": advice,
    }


# API endpoint for checking a job advert
@app.post("/check-job")
def check_job(request: JobRequest):
    return analyse_job(request.job_text)
