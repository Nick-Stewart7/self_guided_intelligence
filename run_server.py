#!/usr/bin/env python3
"""
Simple script to run the Aria FastAPI server
"""

import uvicorn
import sys
import os

if __name__ == "__main__":
    # Add current directory to Python path
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    
    print("Starting Aria Mind API server...")
    print("Frontend will be available at: file:///frontend.html")
    print("API documentation at: http://localhost:8000/docs")
    print("Press Ctrl+C to stop the server")
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )