"""Database models for documents."""
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class Document(BaseModel):
    """
    Database model representing a document in the system.
    This model represents the structure of the 'documents' table.
    """
    id: str = Field(..., description="Unique document identifier (UUID)")
    filename: str = Field(..., description="Original filename of the uploaded PDF")
    file_path: Optional[str] = Field(None, description="Path to saved PDF file (if saved)")
    summary: str = Field(..., description="AI-generated summary of the document")
    file_size_mb: float = Field(..., description="File size in megabytes")
    uploaded_at: datetime = Field(..., description="Timestamp when the document was uploaded")
    
    class Config:
        """Pydantic configuration."""
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": "550e8400-e29b-41d4-a716-446655440000",
                "filename": "document.pdf",
                "file_path": "uploads/550e8400-e29b-41d4-a716-446655440000_document.pdf",
                "summary": "This document discusses...",
                "file_size_mb": 2.5,
                "uploaded_at": "2024-01-01T12:00:00"
            }
        }
