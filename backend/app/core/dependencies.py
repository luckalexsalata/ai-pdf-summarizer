"""Dependency injection for services."""
from app.services.pdf_parser import PDFParser
from app.services.openai_service import OpenAIService
from app.services.storage import StorageService
from app.core.config import settings


# Service instances (singletons)
pdf_parser = PDFParser()
openai_service = OpenAIService()
storage_service = StorageService(
    db_path=settings.db_path,
    storage_dir=settings.storage_dir
)


def get_pdf_parser() -> PDFParser:
    """Get PDF parser service."""
    return pdf_parser


def get_openai_service() -> OpenAIService:
    """Get OpenAI service."""
    return openai_service


def get_storage_service() -> StorageService:
    """Get storage service."""
    return storage_service
