"""Health check and system information routes."""
from fastapi import APIRouter

router = APIRouter(tags=["health"])


@router.get("/health")
async def health_check():
    """
    Health check endpoint.
    
    Returns the current status of the API.
    """
    return {
        "status": "healthy",
        "version": "1.0.0"
    }


@router.get("/")
async def root():
    """
    Root endpoint with API information.
    """
    return {
        "message": "PDF Summary AI API",
        "version": "1.0.0",
        "docs": "/docs"
    }
