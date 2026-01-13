#!/bin/bash

# Start Ollama server in the background
ollama serve > ollama.log 2>&1 &

# Wait for Ollama to be ready
echo "Waiting for Ollama to start..."
sleep 3

# Pull the model
echo "Pulling model..."
ollama pull ministral-3:3b
# ollama pull smollm:135m

# Start the application
# exec gunicorn --bind 0.0.0.0:8000 -k uvicorn.workers.UvicornWorker server:app
exec python -m uvicorn server:app --host 0.0.0.0 --port 8000