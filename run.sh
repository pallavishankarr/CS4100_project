#!/bin/bash

# Business Info Retrieval Agent - Run Script
# This script starts both the backend API server and frontend server

set -e

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Get the directory where the script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}Business Info Retrieval Agent${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo -e "${YELLOW}Error: python3 is not installed or not in PATH${NC}"
    exit 1
fi

# Check if required packages are installed
echo -e "${BLUE}Checking dependencies...${NC}"
if ! python3 -c "import fastapi, uvicorn" 2>/dev/null; then
    echo -e "${YELLOW}Warning: Some dependencies may be missing.${NC}"
    echo -e "${YELLOW}Run: pip install -r requirements.txt${NC}"
    echo ""
fi

# Function to cleanup on exit
cleanup() {
    echo ""
    echo -e "${YELLOW}Shutting down servers...${NC}"
    kill $BACKEND_PID $FRONTEND_PID 2>/dev/null || true
    exit 0
}

# Trap Ctrl+C
trap cleanup SIGINT SIGTERM

# Start backend API server
echo -e "${GREEN}Starting backend API server on http://localhost:8000${NC}"
python3 scripts/start_server.py &
BACKEND_PID=$!

# Wait a moment for backend to start
sleep 3

# Check if backend started successfully
if ! kill -0 $BACKEND_PID 2>/dev/null; then
    echo -e "${YELLOW}Error: Backend server failed to start${NC}"
    exit 1
fi

# Start frontend server
echo -e "${GREEN}Starting frontend server on http://localhost:3000${NC}"
(cd static && python3 -m http.server 3000 > /dev/null 2>&1) &
FRONTEND_PID=$!

# Wait a moment for frontend to start
sleep 2

echo ""
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}Servers are running!${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""
echo -e "Backend API:  ${BLUE}http://localhost:8000${NC}"
echo -e "API Docs:     ${BLUE}http://localhost:8000/docs${NC}"
echo -e "Frontend:     ${BLUE}http://localhost:3000/frontend.html${NC}"
echo ""
echo -e "${YELLOW}Press Ctrl+C to stop all servers${NC}"
echo ""

# Wait for both processes
wait $BACKEND_PID $FRONTEND_PID

