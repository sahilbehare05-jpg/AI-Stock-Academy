"""
MongoDB connection handler using Motor (async driver).
Exposes get_database() for dependency injection into routes/services.
"""
from motor.motor_asyncio import AsyncIOMotorClient
from app.config import settings

client: AsyncIOMotorClient | None = None


def connect_to_mongo():
    global client
    client = AsyncIOMotorClient(settings.mongo_uri)
    print(f"[db] Connected to MongoDB at {settings.mongo_uri}")


def close_mongo_connection():
    global client
    if client:
        client.close()
        print("[db] MongoDB connection closed")


def get_database():
    """Returns the database instance. Call connect_to_mongo() first (done on app startup)."""
    if client is None:
        raise RuntimeError("Database client not initialized. Did the app startup event run?")
    return client[settings.mongo_db_name]


# Collection name constants — used consistently across the app
class Collections:
    USERS = "users"
    STOCKS = "stocks"
    HISTORICAL_DATA = "historical_data"
    PREDICTIONS = "predictions"
    PORTFOLIO = "portfolio"
    TRANSACTIONS = "transactions"
    WATCHLISTS = "watchlists"
    LESSONS = "lessons"
    MODULES = "modules"
    QUIZZES = "quizzes"
    QUIZ_ATTEMPTS = "quiz_attempts"
    PRACTICE_QUESTIONS = "practice_questions"
    TRAINING_PROGRESS = "training_progress"
    ACHIEVEMENTS = "achievements"
    NOTIFICATIONS = "notifications"
    CHAT_HISTORY = "chat_history"
