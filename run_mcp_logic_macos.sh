#!/bin/bash

# macOS run script for MCP-Logic
# This script runs the MCP server locally for testing

PROJECT_PATH="/Volumes/External/Code/mcp-logic"
PROVER9_PATH="$PROJECT_PATH/ladr/bin"

echo "Running MCP-Logic server on macOS"
echo "Project path: $PROJECT_PATH"
echo "Prover9 path: $PROVER9_PATH"
echo ""

# Check if virtual environment exists
if [ ! -d "$PROJECT_PATH/.venv" ]; then
    echo "Virtual environment not found. Please run the setup first."
    exit 1
fi

# Activate virtual environment
source "$PROJECT_PATH/.venv/bin/activate"

# Run the server
echo "Starting MCP server..."
uv --directory "$PROJECT_PATH/src/mcp_logic" run mcp_logic --prover-path "$PROVER9_PATH"
