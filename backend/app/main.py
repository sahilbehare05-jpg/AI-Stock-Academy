"""
AI Stock Academy — Backend Entrypoint

Run locally:
    uvicorn app.main:app --reload --port 8000

Phase 1 scope: app setup, CORS, MongoDB connection lifecycle, health check,
and authentication routes (register/login/me). Further routers (stocks,
prediction, portfolio, academy, quiz, practice, progress, tutor, watchlist)
are added in later phases per the development roadmap in docs/ROADMAP.md.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.config import settings
from app.database.db import connect_to_mongo, close_mongo_connection, get_database
from app.routes import auth ,stocks ,prediction,wallet,portfolio,trading ,watchlist ,news ,academy ,tutor,model_performance


@asynccontextmanager
async def lifespan(app: FastAPI):
    connect_to_mongo()
    yield
    close_mongo_connection()


app = FastAPI(
    title="AI Stock Academy API",
    description="AI-Powered Stock Prediction, Virtual Trading & Trading Education Platform — backend API",
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(stocks.router)
app.include_router(prediction.router)
app.include_router(wallet.router)
app.include_router(portfolio.router)
app.include_router(trading.router)
app.include_router(watchlist.router)
app.include_router(news.router)
app.include_router(academy.router)
app.include_router(tutor.router)
app.include_router(model_performance.router)


@app.get("/api/health", tags=["System"])
async def health_check():
    """Simple liveness + DB connectivity check."""
    db_status = "unknown"
    try:
        db = get_database()
        await db.command("ping")
        db_status = "connected"
    except Exception as e:
        db_status = f"error: {e}"

    return {
        "status": "ok",
        "service": "AI Stock Academy API",
        "database": db_status,
    }


@app.get("/", tags=["System"])
async def root():
    return {
        "message": "AI Stock Academy API is running.",
        "docs": "/docs",
        "health": "/api/health",
    }
