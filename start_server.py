#!/usr/bin/env python3
"""
Simple script to start the API server
Usage: python start_server.py
"""
import uvicorn

if __name__ == "__main__":
    print("Starting Business Info Retrieval Agent API Server...")
    print("Server will be available at http://localhost:8000")
    print("API documentation: http://localhost:8000/docs")
    print("\nPress Ctrl+C to stop the server\n")
    uvicorn.run("api:app", host="0.0.0.0", port=8000, reload=True)

