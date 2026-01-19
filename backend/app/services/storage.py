import os
import uuid
import aiosqlite
from typing import List, Optional
from datetime import datetime
from pathlib import Path
from app.models.document import Document
from app.schemas.documents import HistoryItem
from app.core.config import settings


class StorageService:
    """
    Storage service for document history.
    Uses SQLite for metadata and optional file storage on disk.
    """
    
    def __init__(self, db_path: str = "documents.db", storage_dir: str = "uploads"):
        self.db_path = db_path
        self.storage_dir = Path(storage_dir)
        self.storage_dir.mkdir(exist_ok=True)
        self.max_history = settings.max_history
        self._init_db_sync()
    
    def _init_db_sync(self):
        """Initialize database schema (sync for startup)"""
        import sqlite3
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS documents (
                id TEXT PRIMARY KEY,
                filename TEXT NOT NULL,
                file_path TEXT,
                summary TEXT NOT NULL,
                file_size_mb REAL NOT NULL,
                uploaded_at TIMESTAMP NOT NULL
            )
        """)
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_uploaded_at 
            ON documents(uploaded_at DESC)
        """)
        conn.commit()
        conn.close()
    
    async def add_to_history(
        self, 
        filename: str, 
        summary: str, 
        file_size: float,
        file_content: Optional[bytes] = None
    ) -> HistoryItem:
        """
        Add a new document to history.
        Optionally saves PDF file to disk.
        Maintains only the last max_history items.
        
        Args:
            filename: Original filename
            summary: Generated summary
            file_size: File size in MB
            file_content: Optional PDF file content to save
            
        Returns:
            HistoryItem with document information
        """
        doc_id = str(uuid.uuid4())
        uploaded_at = datetime.now()
        file_path = None
        
        if file_content:
            file_path = self._save_file(doc_id, filename, file_content)
        
        document = Document(
            id=doc_id,
            filename=filename,
            file_path=file_path,
            summary=summary,
            file_size_mb=file_size,
            uploaded_at=uploaded_at
        )
        
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute("""
                INSERT INTO documents (id, filename, file_path, summary, file_size_mb, uploaded_at)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                document.id,
                document.filename,
                document.file_path,
                document.summary,
                document.file_size_mb,
                document.uploaded_at.isoformat()
            ))
            await db.commit()
        
        # Clean up old documents (keep only last max_history)
        await self._cleanup_old_documents()
        
        return HistoryItem(
            id=document.id,
            filename=document.filename,
            summary=document.summary,
            uploaded_at=document.uploaded_at,
            file_size_mb=document.file_size_mb
        )
    
    def _save_file(self, doc_id: str, filename: str, content: bytes) -> str:
        """
        Save PDF file to disk and return file path.
        
        Args:
            doc_id: Document ID
            filename: Original filename
            content: File content bytes
            
        Returns:
            File path where the file was saved
        """
        # Sanitize filename to prevent path traversal
        safe_filename = "".join(c for c in filename if c.isalnum() or c in ".-_")[:100]
        file_path = self.storage_dir / f"{doc_id}_{safe_filename}"
        
        with open(file_path, 'wb') as f:
            f.write(content)
        
        return str(file_path)
    
    async def _cleanup_old_documents(self):
        """Remove old documents beyond max_history limit"""
        async with aiosqlite.connect(self.db_path) as db:
            # Get IDs of documents to keep (last max_history)
            cursor = await db.execute("""
                SELECT id, file_path FROM documents 
                ORDER BY uploaded_at DESC 
                LIMIT ?
            """, (self.max_history,))
            keep_ids = {row[0] for row in await cursor.fetchall()}
            
            # Get all document IDs
            cursor = await db.execute("SELECT id, file_path FROM documents")
            all_docs = await cursor.fetchall()
            
            # Delete old documents and their files
            for doc_id, file_path in all_docs:
                if doc_id not in keep_ids:
                    # Delete file from disk if exists
                    if file_path and os.path.exists(file_path):
                        try:
                            os.remove(file_path)
                        except Exception:
                            pass
                    
                    await db.execute("DELETE FROM documents WHERE id = ?", (doc_id,))
            
            await db.commit()
    
    async def get_history(self) -> List[HistoryItem]:
        """
        Get the history of processed documents (last 5).
        
        Returns:
            List of HistoryItem objects ordered by upload time (newest first)
        """
        async with aiosqlite.connect(self.db_path) as db:
            db.row_factory = aiosqlite.Row
            cursor = await db.execute("""
                SELECT id, filename, file_path, summary, file_size_mb, uploaded_at
                FROM documents
                ORDER BY uploaded_at DESC
                LIMIT ?
            """, (self.max_history,))
            
            rows = await cursor.fetchall()
            documents = [
                Document(
                    id=row["id"],
                    filename=row["filename"],
                    file_path=row["file_path"],
                    summary=row["summary"],
                    file_size_mb=row["file_size_mb"],
                    uploaded_at=datetime.fromisoformat(row["uploaded_at"])
                )
                for row in rows
            ]
            
            return [
                HistoryItem(
                    id=doc.id,
                    filename=doc.filename,
                    summary=doc.summary,
                    uploaded_at=doc.uploaded_at,
                    file_size_mb=doc.file_size_mb
                )
                for doc in documents
            ]
    
    async def delete_document(self, doc_id: str) -> bool:
        """
        Delete a document by ID.
        
        Args:
            doc_id: Document ID to delete
            
        Returns:
            True if document was deleted, False if not found
        """
        async with aiosqlite.connect(self.db_path) as db:
            cursor = await db.execute("""
                SELECT file_path FROM documents WHERE id = ?
            """, (doc_id,))
            row = await cursor.fetchone()
            
            # Delete from database
            cursor = await db.execute("DELETE FROM documents WHERE id = ?", (doc_id,))
            deleted = cursor.rowcount > 0
            await db.commit()
            
            # Delete file from disk if exists
            if deleted and row and row[0] and os.path.exists(row[0]):
                try:
                    os.remove(row[0])
                except Exception:
                    pass
            
            return deleted
