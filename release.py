#!/usr/bin/env python3
"""
Release script for the sagely package.
This script helps prepare and upload the package to PyPI.
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def run_command(cmd, check=True):
    """Run a command and return the result."""
    print(f"Running: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if check and result.returncode != 0:
        print(f"Error: {result.stderr}")
        sys.exit(1)
    return result

def clean_build():
    """Clean build artifacts."""
    print("Cleaning build artifacts...")
    dirs_to_clean = ['build', 'dist', 'src/sagely.egg-info']
    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
            print(f"Removed {dir_name}")

def build_package():
    """Build the package."""
    print("Building package...")
    run_command("python -m build")

def check_package():
    """Check the package for common issues."""
    print("Checking package...")
    run_command("python -m twine check dist/*")

def upload_to_testpypi():
    """Upload to TestPyPI."""
    print("Uploading to TestPyPI...")
    run_command("python -m twine upload --repository testpypi dist/*")

def upload_to_pypi():
    """Upload to PyPI."""
    print("Uploading to PyPI...")
    run_command("python -m twine upload dist/*")

def main():
    """Main function."""
    if len(sys.argv) < 2:
        print("Usage: python release.py [clean|build|check|test-upload|upload]")
        print("  clean       - Clean build artifacts")
        print("  build       - Build the package")
        print("  check       - Check the package")
        print("  test-upload - Upload to TestPyPI")
        print("  upload      - Upload to PyPI")
        sys.exit(1)

    action = sys.argv[1]

    if action == "clean":
        clean_build()
    elif action == "build":
        clean_build()
        build_package()
    elif action == "check":
        clean_build()
        build_package()
        check_package()
    elif action == "test-upload":
        clean_build()
        build_package()
        upload_to_testpypi()
    elif action == "upload":
        clean_build()
        build_package()
        upload_to_pypi()
    else:
        print(f"Unknown action: {action}")
        sys.exit(1)

if __name__ == "__main__":
    main() 