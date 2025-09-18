#!/usr/bin/env python3
"""
Complete setup script for PM Internship Recommendation System
This script automates the entire setup process for new users.
"""

import os
import sys
import subprocess
import platform
from pathlib import Path

def print_step(step, message):
    """Print a formatted step message"""
    print(f"\n{'='*60}")
    print(f"Step {step}: {message}")
    print('='*60)

def run_command(command, cwd=None, shell=True):
    """Run a command and return success status"""
    try:
        print(f"Running: {command}")
        result = subprocess.run(command, shell=shell, cwd=cwd, check=True, 
                              capture_output=True, text=True)
        print("✅ Success")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error: {e}")
        print(f"Output: {e.stdout}")
        print(f"Error: {e.stderr}")
        return False

def check_python_version():
    """Check if Python version is compatible"""
    print_step(1, "Checking Python Version")
    
    version = sys.version_info
    print(f"Python version: {version.major}.{version.minor}.{version.micro}")
    
    if version.major < 3 or (version.major == 3 and version.minor < 9):
        print("❌ Python 3.9+ is required")
        return False
    
    if version.major == 3 and version.minor >= 13:
        print("⚠️  Python 3.13 detected. Some dependencies might have compatibility issues.")
        print("   Consider using Python 3.11 or 3.12 for best compatibility.")
    
    print("✅ Python version is compatible")
    return True

def check_node_version():
    """Check if Node.js is installed"""
    print_step(2, "Checking Node.js Installation")
    
    try:
        result = subprocess.run(["node", "--version"], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ Node.js version: {result.stdout.strip()}")
            return True
    except FileNotFoundError:
        pass
    
    print("❌ Node.js is not installed or not in PATH")
    print("Please install Node.js from https://nodejs.org/")
    return False

def create_virtual_environment():
    """Create Python virtual environment"""
    print_step(3, "Creating Python Virtual Environment")
    
    if os.path.exists("venv"):
        print("✅ Virtual environment already exists")
        return True
    
    return run_command("python -m venv venv")

def activate_virtual_environment():
    """Get the activation command for the virtual environment"""
    if platform.system() == "Windows":
        return "venv\\Scripts\\activate"
    else:
        return "source venv/bin/activate"

def install_python_dependencies():
    """Install Python dependencies"""
    print_step(4, "Installing Python Dependencies")
    
    # Determine the correct pip path
    if platform.system() == "Windows":
        pip_path = "venv\\Scripts\\pip"
    else:
        pip_path = "venv/bin/pip"
    
    # Install setuptools and wheel first
    if not run_command(f"{pip_path} install setuptools wheel"):
        return False
    
    # Install requirements
    return run_command(f"{pip_path} install -r requirements_rag.txt")

def install_node_dependencies():
    """Install Node.js dependencies and build frontend"""
    print_step(5, "Installing Node.js Dependencies and Building Frontend")
    
    frontend_path = "twin-digital-copy-main/twin-digital-copy-main"
    
    if not os.path.exists(frontend_path):
        print(f"❌ Frontend directory not found: {frontend_path}")
        return False
    
    # Install dependencies
    if not run_command("npm install", cwd=frontend_path):
        return False
    
    # Build frontend
    if not run_command("npm run build", cwd=frontend_path):
        return False
    
    print("✅ Frontend built successfully")
    return True

def create_env_file():
    """Create .env file if it doesn't exist"""
    print_step(6, "Setting up Environment Configuration")
    
    env_file = ".env"
    if os.path.exists(env_file):
        print("✅ .env file already exists")
        return True
    
    env_content = """# OpenRouter API Configuration
OPENROUTER_API_KEY=your_openrouter_api_key_here
OPENROUTER_BASE_URL=https://openrouter.ai/api/v1
OPENROUTER_MODEL=mistralai/mistral-7b-instruct:free

# Optional: Ollama Configuration (for local LLM)
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama2

# Application Configuration
FLASK_ENV=development
FLASK_DEBUG=True
"""
    
    try:
        with open(env_file, 'w') as f:
            f.write(env_content)
        print("✅ Created .env file")
        print("⚠️  Please edit .env file and add your OpenRouter API key")
        return True
    except Exception as e:
        print(f"❌ Error creating .env file: {e}")
        return False

def test_application():
    """Test if the application can start"""
    print_step(7, "Testing Application")
    
    # Determine the correct python path
    if platform.system() == "Windows":
        python_path = "venv\\Scripts\\python"
    else:
        python_path = "venv/bin/python"
    
    print("Testing application startup...")
    print("(This will start the server - you can stop it with Ctrl+C)")
    
    try:
        # Start the application
        result = subprocess.run([python_path, "app_with_rag.py"], timeout=10)
        return True
    except subprocess.TimeoutExpired:
        print("✅ Application started successfully (timeout reached)")
        return True
    except Exception as e:
        print(f"❌ Error testing application: {e}")
        return False

def print_success_message():
    """Print success message with next steps"""
    print("\n" + "="*60)
    print("🎉 SETUP COMPLETE!")
    print("="*60)
    print("\nYour PM Internship Recommendation System is ready!")
    print("\nNext steps:")
    print("1. Edit .env file and add your OpenRouter API key")
    print("2. Start the application:")
    
    if platform.system() == "Windows":
        print("   venv\\Scripts\\activate")
        print("   python app_with_rag.py")
    else:
        print("   source venv/bin/activate")
        print("   python app_with_rag.py")
    
    print("\n3. Open your browser to: http://localhost:5000")
    print("\nFor detailed instructions, see SETUP_GUIDE.md")

def main():
    """Main setup function"""
    print("🚀 PM Internship Recommendation System - Automated Setup")
    print("This script will set up everything you need to run the application.")
    
    # Check prerequisites
    if not check_python_version():
        sys.exit(1)
    
    if not check_node_version():
        sys.exit(1)
    
    # Setup steps
    steps = [
        create_virtual_environment,
        install_python_dependencies,
        install_node_dependencies,
        create_env_file,
    ]
    
    for step_func in steps:
        if not step_func():
            print(f"\n❌ Setup failed at step: {step_func.__name__}")
            print("Please check the error messages above and try again.")
            sys.exit(1)
    
    # Test application
    print("\n" + "="*60)
    print("Testing application startup...")
    print("="*60)
    print("The application will start briefly to test if everything works.")
    print("You can stop it with Ctrl+C when you see the server running.")
    print("\nPress Enter to continue...")
    input()
    
    test_application()
    print_success_message()

if __name__ == "__main__":
    main()
