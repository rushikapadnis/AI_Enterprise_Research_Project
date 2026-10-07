from fastapi import FastAPI
from app.config import settings
from app.api.users import router as users_router
from app.api.research import router as research_router
from app.api.users import router as auth_router
from app.api.research import router as research_router
from app.api.users import router as users_router




app = FastAPI(
    title="AI Enterprise Research & Action Agent",
    description="Backend API for an AI-powered enterprise research agent.",
    version="1.0.0",
)

app.include_router(users_router)
app.include_router(auth_router)
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
        "environment": settings.environment
    }