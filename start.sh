#!/bin/bash

# Load environment variables
if [ -f .env ]; then
    export $(cat .env | grep -v '^#' | xargs)
fi

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    source venv/bin/activate
fi

# Check if MongoDB URI is set
if [ -z "$MONGODB_URI" ]; then
    echo "Error: MONGODB_URI environment variable is not set"
    echo "Please set your MongoDB connection string in .env file"
    exit 1
fi

echo "Starting Todo MCP Server..."
echo "MongoDB URI: ${MONGODB_URI}"
echo "Database: ${MONGODB_DATABASE:-todo_db}"

# Run the server
python -m todo_mcp_server.server