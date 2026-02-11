#!/bin/bash

# Run script for Image Optimization Flask app

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}Starting Image Optimization Flask App...${NC}"

# Activate virtual environment
source venv/bin/activate

# Check if uploads directory exists
if [ ! -d "uploads" ]; then
    echo -e "${BLUE}Creating uploads directory...${NC}"
    mkdir -p uploads
fi

# Run the Flask app
echo -e "${GREEN}Flask app starting on http://localhost:5000${NC}"
echo -e "${GREEN}Press Ctrl+C to stop${NC}\n"

python app.py
