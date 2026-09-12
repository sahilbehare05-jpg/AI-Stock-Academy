# AI Stock Academy

**AI-Powered Stock Prediction, Virtual Trading & Trading Education Platform**

> Educational simulation platform. All trading is virtual (₹1,00,000 starting balance).
> AI predictions are not financial advice and do not guarantee profit. No real brokerage
> connection or real-money trading exists anywhere in this codebase.

This delivery covers **Phase 1 (project setup) + Phase 2 (authentication)** of the full
14-phase roadmap in `docs/ROADMAP.md`. It is a real, runnable full-stack app — not a mockup:
React frontend talking to a FastAPI backend, which reads/writes real users in MongoDB with
hashed passwords and JWT auth.

---

## Stack

- **Frontend:** React 18 + Vite + Tailwind CSS + React Router + Axios + Framer Motion + i18next (en/hi/mr)
- **Backend:** FastAPI + Pydantic + Motor (async MongoDB driver) + python-jose (JWT) + passlib (bcrypt)
- **Database:** MongoDB (local or Atlas)
- **ML (scaffolded, Phase 5+):** pandas, numpy, scikit-learn, XGBoost, TensorFlow/Keras, joblib

---

## Prerequisites

- Node.js 18+ and npm
- Python 3.11+
- MongoDB running locally (`mongodb://localhost:27017`) **or** a MongoDB Atlas connection string
- VS Code (recommended) with the Python and Tailwind CSS IntelliSense extensions

---

## Quickest Start (VS Code)

1. Unzip and open the `ai-stock-academy` folder in VS Code (or open
   `ai-stock-academy.code-workspace` for a clean 3-pane root/backend/frontend view).
2. VS Code will prompt to install the recommended extensions (Python, Pylance,
   Tailwind CSS IntelliSense, MongoDB) — accept it.
3. Open a terminal in VS Code (`` Ctrl+` ``) and run the setup script once:
   - macOS/Linux: `bash setup.sh`
   - Windows: `setup.bat`
4. Edit `backend/.env` — set `MONGO_URI` (and generate a real `JWT_SECRET_KEY`, see below).
5. Run both servers with one click: **Terminal → Run Task → "Run Full Stack (Backend + Frontend)"**
   (or run the two tasks "Backend: Run Dev Server" / "Frontend: Run Dev Server" separately).
   To debug the backend with breakpoints, use the **Run and Debug** panel → "FastAPI: Debug Backend".
6. Visit **http://localhost:5173**.

The manual, step-by-step equivalent of the above is below if you'd rather not use the script/tasks.

---

## 1. Backend Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt

cp .env.example .env
# Edit .env and set MONGO_URI, JWT_SECRET_KEY, etc.

uvicorn app.main:app --reload --port 8000
```

Backend will run at **http://localhost:8000**
Interactive API docs: **http://localhost:8000/docs**
Health check: **http://localhost:8000/api/health** (confirms MongoDB connectivity)

> ⚠️ Generate a real `JWT_SECRET_KEY` before anything but local dev, e.g.:
> `python -c "import secrets; print(secrets.token_hex(32))"`

---

## 2. Frontend Setup

```bash
cd frontend
npm install

cp .env.example .env
# VITE_API_BASE_URL=http://localhost:8000 (default already correct for local dev)

npm run dev
```

Frontend will run at **http://localhost:5173**

---

## 3. Test It

1. Open http://localhost:5173 → Landing page loads with hero, feature cards, disclaimer.
2. Click **Register** → create an account (name, email, password, preferred language).
3. On success you're redirected to `/app/dashboard`, showing your real virtual balance
   (₹1,00,000) pulled from MongoDB via the JWT-protected `/api/auth/me` endpoint.
4. Refresh the page — session persists (JWT stored, auto-restored).
5. Switch language (top-right globe icon) — sidebar, header, and dashboard labels
   switch between English / Hindi / Marathi instantly.
6. Click **Logout** → redirected to login; protected `/app/*` routes now redirect to `/login`.
7. Visit any other sidebar item (Stock Analysis, AI Prediction, Wallet, Academy, etc.) —
   each shows a clearly labeled "coming in a later phase" placeholder instead of a broken
   or fake screen, per the no-fake-data development rule.

**Expected result:** full register → login → persisted session → protected dashboard flow
works end-to-end against a real database, with no hard-coded users, prices, or fake data.

---

## Project Structure

```
ai-stock-academy/
├── frontend/           React + Vite + Tailwind SPA
│   └── src/
│       ├── components/ Sidebar, Header, ProtectedRoute, PlaceholderPage
│       ├── pages/       Landing, Login, Register, Dashboard
│       ├── layouts/     DashboardLayout (sidebar + header shell)
│       ├── context/     AuthContext (session state)
│       ├── services/    api.js (Axios client)
│       ├── locales/     en.json, hi.json, mr.json
│       └── utils/       i18n.js
├── backend/             FastAPI app
│   └── app/
│       ├── routes/      auth.py
│       ├── services/    auth_service.py
│       ├── models/      user.py (Mongo document shape)
│       ├── schemas/     user.py (Pydantic I/O contracts)
│       ├── database/    db.py (Motor connection + collection names)
│       ├── utils/       security.py (hashing/JWT), deps.py (auth dependency)
│       └── main.py      App entrypoint, CORS, lifespan, health check
├── ml/                   Scaffolded for Phase 5 (training/, models/, datasets/, notebooks/)
├── docs/
│   └── ROADMAP.md        Full 14-phase plan and what's left to build
└── README.md
```

---

## What's Next

See `docs/ROADMAP.md` for the remaining phases (stock data integration, ML pipeline,
AI prediction, virtual trading, Trading Academy, Practice Lab, AI Tutor, news,
notifications, testing, deployment). Reply with which phase to build next and it will
be delivered the same way: exact files, exact commands, and how to test it — one working
phase at a time, per the development method in the original spec.
