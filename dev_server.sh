#!/bin/bash

# Start Python web server in docs directory (for GitHub Pages testing)
cd "$(dirname "$0")/docs" || exit 1
python -m http.server 8080 > /dev/null 2>&1 &
SERVER_PID=$!

# Give the server a moment to start
sleep 1

# Open the URL in the default browser
open http://localhost:8080/international_movies_table.html

echo "Server started with PID $SERVER_PID"
echo "Press Ctrl+C to stop"

# Handle cleanup on interrupt
cleanup() {
    echo ""
    echo "Shutting down server (PID $SERVER_PID)..."
    kill $SERVER_PID 2>/dev/null
    exit 0
}

trap cleanup INT

# Keep script alive and waiting for interrupt
wait $SERVER_PID 2>/dev/null
