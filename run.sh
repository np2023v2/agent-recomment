#!/bin/bash
# Script to run the Article Recommendation System

echo "=========================================="
echo "Article Recommendation System"
echo "=========================================="
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate 2>/dev/null || . venv/Scripts/activate 2>/dev/null

# Install dependencies if needed
if [ ! -f "venv/installed.flag" ]; then
    echo "Installing dependencies..."
    pip install -r requirements.txt
    touch venv/installed.flag
fi

echo ""
echo "Starting FastAPI server..."
echo "Server will be available at: http://localhost:8000"
echo "API Documentation: http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

# Run the server
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
