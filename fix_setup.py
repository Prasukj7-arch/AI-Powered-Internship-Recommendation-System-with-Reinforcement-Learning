#!/usr/bin/env python3
"""
Quick fix script for setuptools issues on Windows
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

def fix_setuptools():
    """Fix setuptools issue in virtual environment"""
    print("🔧 Fixing setuptools issue...")
    
    # Get the correct pip path for virtual environment
    import platform
    if platform.system() == "Windows":
        pip_path = "venv\\Scripts\\pip"
    else:
        pip_path = "venv/bin/pip"
    
    # Install setuptools and wheel
    print("Installing setuptools and wheel...")
    success, output = run_command(f"{pip_path} install --upgrade setuptools wheel")
    if success:
        print("✅ setuptools and wheel installed successfully")
    else:
        print(f"❌ Failed to install setuptools: {output}")
        return False
    
    # Install requirements
    print("Installing requirements...")
    success, output = run_command(f"{pip_path} install -r requirements.txt")
    if success:
        print("✅ Requirements installed successfully")
        return True
    else:
        print(f"❌ Failed to install requirements: {output}")
        return False

def main():
    """Main fix function"""
    print("🚀 Fixing PM Internship Recommendation System Setup")
    print("=" * 60)
    
    # Check if virtual environment exists
    venv_path = Path("venv")
    if not venv_path.exists():
        print("❌ Virtual environment not found. Please run setup_and_run.py first.")
        return False
    
    # Fix setuptools
    if fix_setuptools():
        print("\n🎉 Fix completed successfully!")
        print("You can now run: python app.py")
        return True
    else:
        print("\n❌ Fix failed. Please check the error messages above.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
