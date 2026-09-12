from fastapi import HTTPException, status
from bson import ObjectId
from bson.errors import InvalidId

from app.database.db import get_database, Collections
from app.services.stock_service import get_live_price


async def get_watchlist(user_id: str):
    try:
        user_oid = ObjectId(user_id)
    except InvalidId:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid user ID.",
        )

    db = get_database()
    watchlists = db[Collections.WATCHLISTS]

    cursor = watchlists.find(
        {"user_id": user_oid}
    ).sort("created_at", -1)

    items = []

    async for item in cursor:
        symbol = item.get("symbol", "")

        try:
            live = get_live_price(symbol)

            items.append({
                "id": str(item["_id"]),
                "symbol": symbol,
                "price": live["price"],
                "previous_close": live["previous_close"],
                "change": live["change"],
                "change_percent": live["change_percent"],
                "timestamp": live["timestamp"],
            })

        except Exception:
            items.append({
                "id": str(item["_id"]),
                "symbol": symbol,
                "price": None,
                "previous_close": None,
                "change": None,
                "change_percent": None,
                "timestamp": None,
            })

    return items


async def add_to_watchlist(user_id: str, symbol: str):
    try:
        user_oid = ObjectId(user_id)
    except InvalidId:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid user ID.",
        )

    symbol = symbol.strip().upper()

    if not symbol:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Stock symbol is required.",
        )

    # Validate that the stock exists
    try:
        get_live_price(symbol)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Unable to find stock {symbol}.",
        )

    db = get_database()
    watchlists = db[Collections.WATCHLISTS]

    existing = await watchlists.find_one({
        "user_id": user_oid,
        "symbol": symbol,
    })

    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"{symbol} is already in your watchlist.",
        )

    from datetime import datetime, timezone

    result = await watchlists.insert_one({
        "user_id": user_oid,
        "symbol": symbol,
        "created_at": datetime.now(timezone.utc),
    })

    return {
        "id": str(result.inserted_id),
        "symbol": symbol,
        "message": f"{symbol} added to watchlist.",
    }


async def remove_from_watchlist(user_id: str, symbol: str):
    try:
        user_oid = ObjectId(user_id)
    except InvalidId:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid user ID.",
        )

    symbol = symbol.strip().upper()

    db = get_database()
    watchlists = db[Collections.WATCHLISTS]

    result = await watchlists.delete_one({
        "user_id": user_oid,
        "symbol": symbol,
    })

    if result.deleted_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"{symbol} is not in your watchlist.",
        )

    return {
        "symbol": symbol,
        "message": f"{symbol} removed from watchlist.",
    }