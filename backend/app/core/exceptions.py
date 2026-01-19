"""Custom exceptions for the application."""
from fastapi import HTTPException, status


class DocumentProcessingError(HTTPException):
    """Exception raised when document processing fails."""
    def __init__(self, detail: str = "Failed to process document"):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=detail
        )


class PDFParseError(HTTPException):
    """Exception raised when PDF parsing fails."""
    def __init__(self, detail: str = "Failed to parse PDF file"):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=detail
        )


class FileValidationError(HTTPException):
    """Exception raised when file validation fails."""
    def __init__(self, detail: str = "File validation failed"):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=detail
        )


