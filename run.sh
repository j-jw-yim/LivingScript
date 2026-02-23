#!/bin/bash
# Run Living Script — starts backend and frontend.
# Usage: ./run.sh

set -e
cd "$(dirname "$0")"

echo "Living Script — starting..."
echo ""

# Check for Python
if ! command -v python3 &> /dev/null; then
  echo "Error: python3 required"
  exit 1
fi

# Check for Node
if ! command -v npm &> /dev/null; then
  echo "Error: npm required"
  exit 1
fi

# Kill anything on port 8000 from a previous run (including uvicorn reloader children)
if lsof -ti:8000 >/dev/null 2>&1; then
  echo "Clearing port 8000..."
  for pid in $(lsof -ti:8000 2>/dev/null); do
    kill -9 $pid 2>/dev/null || true
  done
  sleep 2
fi

# Install Python deps if needed
if ! python3 -c "import fastapi" 2>/dev/null; then
  echo "Installing Python deps..."
  pip install -r requirements.txt -q
fi

# Install UI deps if needed
if [ ! -d "ui/node_modules" ]; then
  echo "Installing UI deps..."
  (cd ui && npm install)
fi

echo "Starting API server on :8000..."
python3 run_server.py &
API_PID=$!
sleep 3
if ! lsof -ti:8000 >/dev/null 2>&1; then
  echo "Warning: API may not have started on port 8000. Checking..."
fi

echo "Starting UI dev server on :5173..."
(cd ui && npm run dev) &
UI_PID=$!

echo ""
echo "✓ Backend: http://localhost:8000"
echo "✓ Frontend: http://localhost:5173"
echo ""
echo "Press Ctrl+C to stop both"
cleanup() { kill $API_PID $UI_PID 2>/dev/null; exit 0; }
trap cleanup INT TERM
wait
