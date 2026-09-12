@echo off
REM One-time setup for AI Stock Academy on Windows.
REM Usage: setup.bat

echo == Setting up backend ==
cd backend
python -m venv venv
call venv\Scripts\activate
pip install --upgrade pip
pip install -r requirements.txt
if not exist .env (
    copy .env.example .env
    echo Created backend\.env from .env.example — edit MONGO_URI and JWT_SECRET_KEY before running.
)
call venv\Scripts\deactivate
cd ..

echo == Setting up frontend ==
cd frontend
call npm install
if not exist .env (
    copy .env.example .env
)
cd ..

echo.
echo Setup complete.
echo Start backend:  cd backend ^&^& venv\Scripts\activate ^&^& uvicorn app.main:app --reload --port 8000
echo Start frontend: cd frontend ^&^& npm run dev
echo Or in VS Code: Terminal ^> Run Task ^> "Run Full Stack (Backend + Frontend)"
