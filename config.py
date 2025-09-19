"""
Configuration file for RAG Internship Recommendation System
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# OpenRouter API Configuration
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "your_openrouter_api_key_here")
OPENROUTER_MODEL = os.getenv("OPENROUTER_MODEL", "mistralai/mistral-7b-instruct:free")

# System Configuration
DEBUG = os.getenv("DEBUG", "True").lower() == "true"
PORT = int(os.getenv("PORT", "8000"))

# File paths
CSV_FILE_PATH = "internships_all_streams_edited.csv"
REQUIREMENTS_FILE = "requirements.txt"

# API Configuration
API_TIMEOUT = 30
MAX_TOKENS = 1000
TEMPERATURE = 0.7

def get_api_key():
    """Get API key with proper error handling"""
    if OPENROUTER_API_KEY == "your_openrouter_api_key_here":
        print("⚠️  OpenRouter API key not set!")
        print("   Set it as environment variable: OPENROUTER_API_KEY")
        print("   Or create a .env file with: OPENROUTER_API_KEY=your_key_here")
        return None
    return OPENROUTER_API_KEY

def is_api_configured():
    """Check if API is properly configured"""
    return get_api_key() is not None
