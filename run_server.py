#!/usr/bin/env python3
"""
Simple script to run the Aria FastAPI server
"""

import uvicorn
import sys
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import config after loading env vars
from config import config

if __name__ == "__main__":
    # Add current directory to Python path
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    
    # Validate configuration
    if not config.validate():
        print("Configuration validation failed. Please check your environment variables.")
        sys.exit(1)
    
    print("Starting Aria Mind API server...")
    print(f"Frontend will be available at: file://{os.path.abspath('frontend.html')}")
    print(f"API documentation at: http://{config.aria.host}:{config.aria.port}/docs")
    print("Press Ctrl+C to stop the server")
    
    uvicorn.run(
        "main:app",
        host=config.aria.host,
        port=config.aria.port,
        reload=config.aria.reload,
        log_level=config.aria.log_level
    )