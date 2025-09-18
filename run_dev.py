#!/usr/bin/env python3
"""
Development Run Script for PM Internship Recommendation System
Quick start for development with hot reload
"""

import subprocess
import sys
import os
import time
import threading
from pathlib import Path

def run_backend():
    """Run the Flask backend using virtual environment"""
    print("🚀 Starting Flask backend...")
    import platform
    if platform.system() == "Windows":
        python_path = "venv\\Scripts\\python"
    else:
        python_path = "venv/bin/python"
    
    subprocess.run([python_path, "app.py"])

def run_frontend():
    """Run the React frontend in development mode"""
    print("🚀 Starting React frontend...")
    frontend_dir = Path("twin-digital-copy-main/twin-digital-copy-main")
    subprocess.run(["npm", "run", "dev"], cwd=frontend_dir)

def main():
    """Main function to run both frontend and backend"""
    print("🚀 PM Internship Recommendation System - Development Mode")
    print("=" * 60)
    print("📱 Frontend: http://localhost:8080")
    print("🔧 Backend API: http://localhost:5000")
    print("=" * 60)
    
    # Start backend in a separate thread
    backend_thread = threading.Thread(target=run_backend, daemon=True)
    backend_thread.start()
    
    # Wait a moment for backend to start
    time.sleep(2)
    
    # Start frontend (this will block)
    try:
        run_frontend()
    except KeyboardInterrupt:
        print("\n🛑 Stopping development servers...")
        print("✅ Development servers stopped")

if __name__ == "__main__":
    main()
