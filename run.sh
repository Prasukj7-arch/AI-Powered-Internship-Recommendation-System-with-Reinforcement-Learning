#!/bin/bash

echo "Starting PM Internship Recommendation System..."
echo

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Virtual environment not found. Please run setup first."
    echo "Run: python setup_complete.py"
    exit 1
fi

# Activate virtual environment and run the application
source venv/bin/activate
python app_with_rag.py
