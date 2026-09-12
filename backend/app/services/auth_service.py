"""
Auth service: business logic for registering and authenticating users.
Kept separate from the route layer so it can be reused/tested independently.
"""
from bson import ObjectId
from bson.errors import InvalidId
from fastapi import HTTPException, status
from app.database.db import get_database, Collections
from app.models.user import new_user_document, serialize_user
from app.utils.security import hash_password, verify_password, create_access_token


async def register_user(name: str, email: str, password: str, preferred_language: str) -> dict:
    db = get_database()
    users = db[Collections.USERS]

    existing = await users.find_one({"email": email.lower()})
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="An account with this email already exists.",
        )

    doc = new_user_document(name, email, hash_password(password), preferred_language)
    result = await users.insert_one(doc)
    doc["_id"] = result.inserted_id

    token = create_access_token({"sub": str(doc["_id"])})
    return {"access_token": token, "token_type": "bearer", "user": serialize_user(doc)}


async def authenticate_user(email: str, password: str) -> dict:
    db = get_database()
    users = db[Collections.USERS]

    doc = await users.find_one({"email": email.lower()})
    if not doc or not verify_password(password, doc["password_hash"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password.",
        )

    token = create_access_token({"sub": str(doc["_id"])})
    return {"access_token": token, "token_type": "bearer", "user": serialize_user(doc)}


async def get_user_by_id(user_id: str) -> dict | None:
    db = get_database()
    users = db[Collections.USERS]
    try:
        oid = ObjectId(user_id)
    except InvalidId:
        return None
    doc = await users.find_one({"_id": oid})
    if not doc:
        return None
    return serialize_user(doc)
