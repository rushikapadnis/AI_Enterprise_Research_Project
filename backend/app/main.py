
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.api.users import router as users_router
from app.api.research import router as research_router


app = FastAPI(
    title="AI Enterprise Research & Action Agent",
    description="Backend API for an AI-powered enterprise research agent.",
    version="1.0.0",
)

# Allow the local Next.js frontend to communicate with FastAPI.
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register each router exactly once.
app.include_router(users_router)
app.include_router(research_router)


@app.get("/")
def root():
    return {
        "message": f"{settings.app_name} API is running"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "environment": settings.environment,
    }
