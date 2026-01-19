import os
from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # OpenAI settings
    openai_api_key: str = ""
    openai_model: str = "gpt-4o-mini"
    
    # Storage settings
    save_pdf_files: bool = False
    db_path: str = "documents.db"
    storage_dir: str = "uploads"
    max_history: int = 5
    
    # File upload settings
    max_file_size_mb: int = 50
    max_pages: int = 100
    
    # CORS settings
    cors_origins: List[str] = ["*"]
    
    class Config:
        env_file = ".env"
        case_sensitive = False
        # Allow reading from environment even if .env doesn't exist
        env_file_encoding = "utf-8"
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Fallback to environment variables if not set
        if not self.openai_api_key:
            self.openai_api_key = os.getenv("OPENAI_API_KEY", "")
        if not self.openai_model or self.openai_model == "gpt-4o-mini":
            self.openai_model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
        # Convert string to bool for save_pdf_files
        if isinstance(self.save_pdf_files, str):
            self.save_pdf_files = self.save_pdf_files.lower() == "true"


# Global settings instance
settings = Settings()
