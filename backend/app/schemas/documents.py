"""Pydantic schemas for document-related API endpoints."""
from pydantic import BaseModel, Field
from datetime import datetime


class SummaryResponse(BaseModel):
    """Response schema for PDF upload and summary generation."""
    filename: str = Field(..., description="Original filename of the uploaded PDF")
    summary: str = Field(..., description="AI-generated summary of the document")
    uploaded_at: datetime = Field(..., description="Timestamp when the document was uploaded")
    
    class Config:
        json_schema_extra = {
            "example": {
                "filename": "document.pdf",
                "summary": "This document discusses...",
                "uploaded_at": "2024-01-01T12:00:00"
            }
        }


class HistoryItem(BaseModel):
    """Schema for document history item."""
    id: str = Field(..., description="Document ID")
    filename: str = Field(..., description="Filename of the processed document")
    summary: str = Field(..., description="Generated summary")
    uploaded_at: datetime = Field(..., description="Upload timestamp")
    file_size_mb: float = Field(..., description="File size in megabytes")
    
    class Config:
        json_schema_extra = {
            "example": {
                "filename": "document.pdf",
                "summary": "Summary text...",
                "uploaded_at": "2024-01-01T12:00:00",
                "file_size_mb": 2.5
            }
        }
