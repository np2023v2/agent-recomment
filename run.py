#!/usr/bin/env python3
"""
Simple script to run the Article Recommendation System
Works on Windows, macOS, and Linux
"""

import subprocess
import sys
import os

def main():
    print("=" * 50)
    print("Article Recommendation System")
    print("=" * 50)
    print()
    
    print("Starting FastAPI server...")
    print("Server will be available at: http://localhost:8000")
    print("API Documentation: http://localhost:8000/docs")
    print()
    print("Press Ctrl+C to stop the server")
    print()
    
    try:
        # Run the server
        subprocess.run([
            sys.executable, "-m", "uvicorn",
            "app.main:app",
            "--host", "0.0.0.0",
            "--port", "8000",
            "--reload"
        ])
    except KeyboardInterrupt:
        print("\n\nServer stopped.")
    except Exception as e:
        print(f"\nError: {e}")
        print("\nMake sure you have installed the dependencies:")
        print("  pip install -r requirements.txt")

if __name__ == "__main__":
    main()
