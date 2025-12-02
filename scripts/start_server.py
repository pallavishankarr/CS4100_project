#!/usr/bin/env python3
"""
Simple script to start the API server
Usage: python scripts/start_server.py
"""
import os
import sys
import uvicorn

# Add src directory to path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
src_path = os.path.join(project_root, "src")
sys.path.insert(0, src_path)

if __name__ == "__main__":
    print("Starting Business Info Retrieval Agent API Server...")
    print("Server will be available at http://localhost:8000")
    print("API documentation: http://localhost:8000/docs")
    print("\nPress Ctrl+C to stop the server\n")
    uvicorn.run("api:app", host="0.0.0.0", port=8000, reload=True)

