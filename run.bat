@echo off
echo Starting PM Internship Recommendation System...
echo.

REM Check if virtual environment exists
if not exist "venv" (
    echo Virtual environment not found. Please run setup first.
    echo Run: python setup_complete.py
    pause
    exit /b 1
)

REM Activate virtual environment and run the application
call venv\Scripts\activate
python app_with_rag.py

pause
