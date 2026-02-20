#!/bin/bash
# Local development server for ARI

# Check if uvicorn is installed
if ! command -v uvicorn &> /dev/null; then
    echo "Installing uvicorn..."
    pip3 install uvicorn fastapi slowapi joblib numpy nltk pyphen scikit-learn pandas httpx pydantic
fi

# Start API server in background
echo "Starting ARI API on http://localhost:8080..."
cd "$(dirname "$0")"
ARI_DEV_MODE=true python3 -m uvicorn ari.api.main:app --host 127.0.0.1 --port 8080 --reload &
API_PID=$!

# Wait for API to start
sleep 3

# Start web server in background
echo "Starting web server on http://localhost:8000..."
cd ari/web
python3 -m http.server 8000 &
WEB_PID=$!

echo ""
echo "✓ ARI API running at: http://localhost:8080"
echo "✓ Web interface at: http://localhost:8000/index.html"
echo ""
echo "Press Ctrl+C to stop both servers"

# Wait for Ctrl+C
trap "kill $API_PID $WEB_PID 2>/dev/null; exit" INT TERM
wait
