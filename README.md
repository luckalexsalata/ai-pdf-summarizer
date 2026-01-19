# PDF Summary AI

A full-stack web application that allows users to upload PDF documents (up to 50MB, 100 pages) and receive AI-generated summaries using OpenAI's API.

## Features

- PDF Upload with validation (max 50MB)
- PDF Parsing supporting text, tables, and images (via OCR)
- AI Summary Generation using OpenAI API
- History Display showing the last 5 processed documents

## Tech Stack

**Backend:** FastAPI, pdfplumber, pytesseract, OpenAI API, SQLite  
**Frontend:** Next.js 14, TypeScript, Tailwind CSS

## Quick Start

### Using Docker (Recommended)

1. Create `.env` file in project root:
   ```
   OPENAI_API_KEY=your_openai_api_key_here
   OPENAI_MODEL=gpt-4o-mini
   ```

2. Start the application:
   ```bash
   docker-compose up --build
   ```

3. Access:
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Docs: http://localhost:8000/docs

### Local Development

**Backend:**
```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
echo "OPENAI_API_KEY=your_key_here" > .env
uvicorn main:app --reload
```

**Frontend:**
```bash
cd frontend
npm install
npm run dev
```

## API Endpoints

- `POST /api/v1/upload` - Upload PDF and get summary
- `GET /api/v1/history` - Get last 5 documents
- `DELETE /api/v1/history/{doc_id}` - Delete document

Full API documentation available at http://localhost:8000/docs

## Configuration

- `OPENAI_API_KEY` (required) - Your OpenAI API key
- `OPENAI_MODEL` (optional) - Model to use (default: `gpt-4o-mini`)
- `SAVE_PDF_FILES` (optional) - Save PDFs to disk (default: `false`)

## Limitations

- Maximum file size: 50MB
- Maximum pages: 100 (recommended)
- History: Last 5 documents
