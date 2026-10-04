from fastapi import FastAPI
from app.config import settings



app = FastAPI(
    title=settings.app_name,
    description="Backend Api for AI-Powered enterprie research agent",
    version="1.0.0"
)


@app.get("/")
def root():
    return {"message": f"{settings.app_name} App is running"}


@app.get("/health")
def health_check():
    return {"status":"health",
            "envirnment":settings.environment,
    }