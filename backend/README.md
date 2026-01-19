# PDF Summary AI - Backend

FastAPI backend for uploading and summarizing PDF documents using OpenAI API.

## Features

- PDF Upload (up to 50MB)
- PDF Parsing with text, tables, and images (OCR)
- AI Summary Generation via OpenAI API
- History of last 5 processed documents
- Docker support

## Tech Stack

- **FastAPI** - Web framework
- **pdfplumber** - PDF text and table extraction
- **pdf2image + pytesseract** - OCR for images
- **OpenAI API** - Summary generation
- **SQLite** - Persistent storage for document history
- **Docker** - Containerization

## Installation

### Local Setup

1. Install system dependencies:
```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install -y poppler-utils tesseract-ocr tesseract-ocr-eng

# macOS
brew install poppler tesseract
```

2. Create virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # Linux/macOS
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create `.env` file in project root:
```bash
cp ../.env.example ../.env
# Edit .env and add your OPENAI_API_KEY
```

5. Run server:
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Docker

See main [README.md](../README.md) for Docker setup instructions.

## API Documentation

After starting the server, documentation is available at:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### Endpoints

- `POST /api/v1/upload` - Upload PDF and get summary
- `GET /api/v1/history` - Get last 5 documents
- `DELETE /api/v1/history/{doc_id}` - Delete document
- `GET /health` - Health check
- `GET /` - API information

## Project Structure

```
backend/
├── main.py                    # FastAPI entry point
├── app/
│   ├── api/routes/           # API endpoints
│   ├── core/                 # Configuration & dependencies
│   ├── models/               # Database models
│   ├── schemas/              # API schemas
│   └── services/             # Business logic
├── requirements.txt
└── Dockerfile
```

## Configuration

Environment variables (set in root `.env` file):
- `OPENAI_API_KEY` (required) - OpenAI API key
- `OPENAI_MODEL` (optional) - Model to use (default: `gpt-4o-mini`)
- `SAVE_PDF_FILES` (optional) - Save PDFs to disk (default: `false`)

## PDF Processing

The parser supports:
1. **Text** - Direct text extraction
2. **Tables** - Automatic table detection and formatting
3. **Images** - OCR via Tesseract for scanned PDFs

## Storage

- **SQLite database** (`documents.db`) - Stores document metadata
- **Uploads folder** (optional) - Stores PDF files if `SAVE_PDF_FILES=true`
- **Auto cleanup** - Old documents (beyond 5) are automatically removed

## Limitations

- Maximum file size: 50MB
- Maximum pages: 100 (recommended)
- History: Last 5 documents
