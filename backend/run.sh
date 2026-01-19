#!/bin/bash
# Script to run backend locally

set -e

echo "🚀 Starting PDF Summary AI Backend..."

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔌 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install --upgrade pip -q
pip install -r requirements.txt -q

# Check .env file
if [ ! -f ".env" ]; then
    echo "⚠️  .env file not found!"
    echo "📝 Creating example .env file..."
    cat > .env << EOF
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-4o-mini
SAVE_PDF_FILES=false
EOF
    echo "❗ Please edit .env and add your OPENAI_API_KEY!"
    echo "📄 File: $(pwd)/.env"
    exit 1
fi

# Start server
echo "✅ Starting server on http://localhost:8000"
echo "📚 Documentation: http://localhost:8000/docs"
echo ""
uvicorn main:app --reload --host 0.0.0.0 --port 8000
