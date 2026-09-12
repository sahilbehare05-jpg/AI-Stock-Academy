#!/usr/bin/env bash
# One-time setup for AI Stock Academy on macOS/Linux.
# Usage: bash setup.sh
set -e

echo "== Setting up backend =="
cd backend
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip -q
pip install -r requirements.txt -q
if [ ! -f .env ]; then
  cp .env.example .env
  echo "Created backend/.env from .env.example — edit MONGO_URI and JWT_SECRET_KEY before running."
fi
deactivate
cd ..

echo "== Setting up frontend =="
cd frontend
npm install --silent
if [ ! -f .env ]; then
  cp .env.example .env
fi
cd ..

echo ""
echo "Setup complete."
echo "Start backend:  cd backend && source venv/bin/activate && uvicorn app.main:app --reload --port 8000"
echo "Start frontend: cd frontend && npm run dev"
echo "Or in VS Code: Terminal > Run Task > 'Run Full Stack (Backend + Frontend)'"
