#!/usr/bin/env python3
"""
Fix script for Python 3.13 compatibility issues
"""

import subprocess
import sys
import os
from pathlib import Path

def run_command(command, cwd=None, shell=True):
    """Run a command and return the result"""
    try:
        result = subprocess.run(command, shell=shell, cwd=cwd, check=True, capture_output=True, text=True)
        return True, result.stdout
    except subprocess.CalledProcessError as e:
        return False, e.stderr

def fix_python313():
    """Fix Python 3.13 compatibility issues"""
    print("🔧 Fixing Python 3.13 compatibility issues...")
    
    # Get the correct pip path for virtual environment
    import platform
    if platform.system() == "Windows":
        pip_path = "venv\\Scripts\\pip"
    else:
        pip_path = "venv/bin/pip"
    
    # Upgrade pip to latest version
    print("Upgrading pip...")
    success, output = run_command(f"{pip_path} install --upgrade pip")
    if not success:
        print(f"⚠️ Warning: Failed to upgrade pip: {output}")
    
    # Install setuptools and wheel with specific versions
    print("Installing compatible setuptools and wheel...")
    success, output = run_command(f"{pip_path} install 'setuptools>=68.0.0' 'wheel>=0.40.0'")
    if not success:
        print(f"❌ Failed to install setuptools: {output}")
        return False
    
    # Install packages one by one to avoid conflicts
    packages = [
        "pandas>=2.0.0",
        "numpy>=1.24.0", 
        "requests>=2.31.0",
        "openai>=1.3.0",
        "python-dotenv>=1.0.0",
        "scikit-learn>=1.3.0",
        "flask>=2.3.0",
        "flask-cors>=4.0.0",
        "chromadb>=0.4.15",
        "ollama>=0.1.7",
        "pdfplumber>=0.10.3",
        "docx2txt>=0.8"
    ]
    
    print("Installing packages individually...")
    for package in packages:
        print(f"Installing {package}...")
        success, output = run_command(f"{pip_path} install '{package}'")
        if not success:
            print(f"⚠️ Warning: Failed to install {package}: {output}")
            # Continue with other packages
    
    print("✅ Package installation completed")
    return True

def main():
    """Main fix function"""
    print("🚀 Fixing Python 3.13 Compatibility Issues")
    print("=" * 60)
    
    # Check if virtual environment exists
    venv_path = Path("venv")
    if not venv_path.exists():
        print("❌ Virtual environment not found. Please run setup_and_run.py first.")
        return False
    
    # Fix Python 3.13 issues
    if fix_python313():
        print("\n🎉 Fix completed successfully!")
        print("You can now run: python app.py")
        return True
    else:
        print("\n❌ Fix failed. Please check the error messages above.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
