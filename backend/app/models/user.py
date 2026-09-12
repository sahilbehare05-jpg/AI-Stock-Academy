"""
User document shape stored in MongoDB (collection: users).
This is not an ORM model — MongoDB via Motor is schemaless — but this
documents the canonical field set every user document should have,
and provides a factory to build a new user document consistently.
"""
from datetime import datetime, timezone
from app.config import settings


def new_user_document(name: str, email: str, password_hash: str, preferred_language: str = "en") -> dict:
    now = datetime.now(timezone.utc)
    return {
        "name": name,
        "email": email.lower(),
        "password_hash": password_hash,
        "preferred_language": preferred_language,
        "training_score": 0,
        "virtual_balance": settings.starting_virtual_balance,
        "created_at": now,
        "updated_at": now,
    }


def serialize_user(doc: dict) -> dict:
    """Converts a MongoDB user document into the shape expected by UserPublic."""
    return {
        "id": str(doc["_id"]),
        "name": doc["name"],
        "email": doc["email"],
        "preferred_language": doc.get("preferred_language", "en"),
        "training_score": doc.get("training_score", 0),
        "virtual_balance": doc.get("virtual_balance", settings.starting_virtual_balance),
        "created_at": doc["created_at"],
    }
