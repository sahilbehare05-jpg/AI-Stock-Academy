from datetime import datetime, timezone
from bson import ObjectId
from bson.errors import InvalidId

from app.database.db import get_database, Collections


async def get_wallet(user_id: str):
    db = get_database()

    try:
        oid = ObjectId(user_id)
    except InvalidId:
        return None

    user = await db[Collections.USERS].find_one(
        {"_id": oid}
    )

    if not user:
        return None

    return {
        "user_id": str(user["_id"]),
        "balance": float(
            user.get("virtual_balance", 0)
        ),
        "currency": "INR",
    }