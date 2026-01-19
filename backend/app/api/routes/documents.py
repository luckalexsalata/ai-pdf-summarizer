"""Document-related API routes."""
from pathlib import Path
from fastapi import APIRouter, UploadFile, File, Depends, status, HTTPException
from typing import List

from app.schemas.documents import SummaryResponse, HistoryItem
from app.core.dependencies import (
    get_pdf_parser,
    get_openai_service,
    get_storage_service
)
from app.core.exceptions import FileValidationError, PDFParseError, DocumentProcessingError
from app.core.constants import ALLOWED_FILE_EXTENSIONS, MIN_TEXT_LENGTH, ERROR_FILE_NOT_PDF, ERROR_FILE_TOO_LARGE, ERROR_NO_TEXT_EXTRACTED
from app.services.pdf_parser import PDFParser
from app.services.openai_service import OpenAIService
from app.services.storage import StorageService
from app.core.config import settings

router = APIRouter(prefix="/api/v1", tags=["documents"])


@router.post("/upload", response_model=SummaryResponse, status_code=status.HTTP_201_CREATED)
async def upload_pdf(
    file: UploadFile = File(...),
    pdf_parser: PDFParser = Depends(get_pdf_parser),
    openai_service: OpenAIService = Depends(get_openai_service),
    storage_service: StorageService = Depends(get_storage_service),
):
    """
    Upload a PDF file and generate AI summary.
    
    Args:
        file: PDF file to upload (max 50MB, up to 100 pages)
        pdf_parser: PDF parser service (injected)
        openai_service: OpenAI service (injected)
        storage_service: Storage service (injected)
    
    Returns:
        SummaryResponse with filename, summary, and upload timestamp
    """
    if not file.filename:
        raise FileValidationError(ERROR_FILE_NOT_PDF)
    
    file_ext = Path(file.filename).suffix.lower()
    if file_ext not in ALLOWED_FILE_EXTENSIONS:
        raise FileValidationError(ERROR_FILE_NOT_PDF)
    
    file_content = await file.read()
    file_size_mb = len(file_content) / (1024 * 1024)
    
    if file_size_mb == 0:
        raise FileValidationError("PDF file is empty")
    
    if file_size_mb > settings.max_file_size_mb:
        raise FileValidationError(ERROR_FILE_TOO_LARGE.format(max_size=settings.max_file_size_mb))
    
    try:
        text_content = await pdf_parser.parse_pdf(file_content)
        
        if not text_content or len(text_content.strip()) < MIN_TEXT_LENGTH:
            raise PDFParseError(ERROR_NO_TEXT_EXTRACTED)
        
        summary = await openai_service.generate_summary(text_content)
        
        history_item = await storage_service.add_to_history(
            filename=file.filename,
            summary=summary,
            file_size=file_size_mb,
            file_content=file_content if settings.save_pdf_files else None
        )
        
        return SummaryResponse(
            filename=file.filename,
            summary=summary,
            uploaded_at=history_item.uploaded_at
        )
    
    except (FileValidationError, PDFParseError):
        raise
    except Exception as e:
        raise DocumentProcessingError(f"Error processing PDF: {str(e)}")


@router.get("/history", response_model=List[HistoryItem])
async def get_history(
    storage_service: StorageService = Depends(get_storage_service),
):
    """
    Get the last 5 processed documents.
    
    Returns a list of history items with filename, summary, upload time, and file size.
    """
    return await storage_service.get_history()


@router.delete("/history/{doc_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_document(
    doc_id: str,
    storage_service: StorageService = Depends(get_storage_service),
):
    """
    Delete a document by ID.
    
    - **doc_id**: Document ID (UUID)
    - Returns: 204 No Content on success, 404 Not Found if document doesn't exist
    """
    deleted = await storage_service.delete_document(doc_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Document with id {doc_id} not found"
        )
