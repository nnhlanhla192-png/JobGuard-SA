
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
