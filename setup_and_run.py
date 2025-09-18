#!/usr/bin/env python3
"""
Setup and Run Script for PM Internship Recommendation System
This script handles the complete setup and running of both frontend and backend
"""

import subprocess
import sys
import os
import time
import webbrowser
from pathlib import Path

def run_command(command, cwd=None, shell=True):
    """Run a command and return the result"""
    try:
        result = subprocess.run(command, shell=shell, cwd=cwd, check=True, capture_output=True, text=True)
        return True, result.stdout
    except subprocess.CalledProcessError as e:
        return False, e.stderr

def check_python():
    """Check if Python is available"""
    success, output = run_command("python --version")
    if success:
        print(f"✅ Python found: {output.strip()}")
        return True
    else:
        print("❌ Python not found. Please install Python 3.8+")
        return False

def create_virtual_environment():
    """Create virtual environment if it doesn't exist"""
    venv_path = Path("venv")
    if venv_path.exists():
        print("✅ Virtual environment already exists")
        return True
    
    print("🔧 Creating virtual environment...")
    success, output = run_command("python -m venv venv")
    if success:
        print("✅ Virtual environment created successfully")
        return True
    else:
        print(f"❌ Failed to create virtual environment: {output}")
        return False

def activate_virtual_environment():
    """Activate virtual environment and return the activation command"""
    import platform
    if platform.system() == "Windows":
        return "venv\\Scripts\\activate"
    else:
        return "source venv/bin/activate"

def check_node():
    """Check if Node.js is available"""
    success, output = run_command("node --version")
    if success:
        print(f"✅ Node.js found: {output.strip()}")
        return True
    else:
        print("❌ Node.js not found. Please install Node.js 16+")
        return False

def install_python_dependencies():
    """Install Python dependencies in virtual environment"""
    print("\n🔧 Installing Python dependencies in virtual environment...")
    
    # Get the correct pip path for virtual environment
    import platform
    if platform.system() == "Windows":
        pip_path = "venv\\Scripts\\pip"
    else:
        pip_path = "venv/bin/pip"
    
    # Upgrade pip first
    success, output = run_command(f"{pip_path} install --upgrade pip")
    if not success:
        print(f"⚠️ Warning: Failed to upgrade pip: {output}")
    
    # Install setuptools and wheel first (fixes Windows issues)
    print("🔧 Installing setuptools and wheel...")
    success, output = run_command(f"{pip_path} install setuptools wheel")
    if not success:
        print(f"⚠️ Warning: Failed to install setuptools: {output}")
    
    # Install requirements
    success, output = run_command(f"{pip_path} install -r requirements.txt")
    if success:
        print("✅ Python dependencies installed successfully")
        return True
    else:
        print(f"❌ Failed to install Python dependencies: {output}")
        return False

def install_node_dependencies():
    """Install Node.js dependencies"""
    print("\n🔧 Installing Node.js dependencies...")
    frontend_dir = Path("twin-digital-copy-main/twin-digital-copy-main")
    if not frontend_dir.exists():
        print("❌ Frontend directory not found")
        return False
    
    success, output = run_command("npm install", cwd=frontend_dir)
    if success:
        print("✅ Node.js dependencies installed successfully")
        return True
    else:
        print(f"❌ Failed to install Node.js dependencies: {output}")
        return False

def build_frontend():
    """Build the React frontend"""
    print("\n🔧 Building React frontend...")
    frontend_dir = Path("twin-digital-copy-main/twin-digital-copy-main")
    
    success, output = run_command("npm run build", cwd=frontend_dir)
    if success:
        print("✅ Frontend built successfully")
        return True
    else:
        print(f"❌ Failed to build frontend: {output}")
        return False

def start_backend():
    """Start the Flask backend using virtual environment"""
    print("\n🚀 Starting Flask backend...")
    try:
        # Get the correct python path for virtual environment
        import platform
        if platform.system() == "Windows":
            python_path = "venv\\Scripts\\python"
        else:
            python_path = "venv/bin/python"
        
        # Start the backend in a separate process
        process = subprocess.Popen([python_path, "app.py"], 
                                 stdout=subprocess.PIPE, 
                                 stderr=subprocess.PIPE,
                                 text=True)
        
        # Wait a moment for the server to start
        time.sleep(3)
        
        # Check if the process is still running
        if process.poll() is None:
            print("✅ Backend started successfully on http://localhost:5000")
            return process
        else:
            stdout, stderr = process.communicate()
            print(f"❌ Backend failed to start: {stderr}")
            return None
    except Exception as e:
        print(f"❌ Error starting backend: {e}")
        return None

def main():
    """Main setup and run function"""
    print("🚀 PM Internship Recommendation System Setup")
    print("=" * 60)
    
    # Check prerequisites
    if not check_python():
        return False
    
    if not check_node():
        return False
    
    # Create virtual environment
    if not create_virtual_environment():
        return False
    
    # Install dependencies
    if not install_python_dependencies():
        return False
    
    if not install_node_dependencies():
        return False
    
    # Build frontend
    if not build_frontend():
        return False
    
    # Start backend
    backend_process = start_backend()
    if not backend_process:
        return False
    
    print("\n" + "=" * 60)
    print("🎉 Setup Complete!")
    print("=" * 60)
    print("📱 Frontend: http://localhost:5000")
    print("🔧 API: http://localhost:5000/api/")
    print("🔑 Set OPENROUTER_API_KEY environment variable for AI features")
    print("\n💡 The system will automatically fall back to ChromaDB + Ollama if API fails")
    print(f"\n🐍 Virtual environment created: {activate_virtual_environment()}")
    print("=" * 60)
    
    # Open browser
    try:
        webbrowser.open("http://localhost:5000")
        print("🌐 Opening browser...")
    except:
        print("🌐 Please open http://localhost:5000 in your browser")
    
    print("\n⏹️  Press Ctrl+C to stop the server")
    
    try:
        # Keep the script running
        backend_process.wait()
    except KeyboardInterrupt:
        print("\n🛑 Stopping server...")
        backend_process.terminate()
        backend_process.wait()
        print("✅ Server stopped")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
