from fastapi import APIRouter, Depends, HTTPException
from bson import ObjectId
from bson.errors import InvalidId

from app.services.wallet_service import get_wallet
from app.database.db import get_database, Collections
from app.utils.deps import get_current_user


router = APIRouter(
    prefix="/api/wallet",
    tags=["Virtual Wallet"],
)


@router.get("")
async def wallet(
    current_user: dict = Depends(get_current_user),
):
    user_id = current_user["id"]

    result = await get_wallet(user_id)

    if result is None:
        raise HTTPException(
            status_code=404,
            detail="User wallet not found.",
        )

    return {
        "success": True,
        "data": result,
    }


@router.get("/transactions")
async def wallet_transactions(
    current_user: dict = Depends(get_current_user),
):
    try:
        user_id = ObjectId(current_user["id"])
    except InvalidId:
        raise HTTPException(
            status_code=400,
            detail="Invalid user ID.",
        )

    db = get_database()

    cursor = (
        db[Collections.TRANSACTIONS]
        .find({"user_id": user_id})
        .sort("created_at", -1)
    )

    transactions = []

    async for transaction in cursor:
        transactions.append(
            {
                "id": str(transaction["_id"]),
                "type": transaction.get("type"),
                "symbol": transaction.get("symbol"),
                "quantity": int(
                    transaction.get("quantity", 0)
                ),
                "price": float(
                    transaction.get("price", 0)
                ),
                "total": float(
    transaction.get("total", 0)
),

"realized_pnl": float(
    transaction.get("realized_pnl", 0)
),

"realized_pnl_percent": float(
    transaction.get("realized_pnl_percent", 0)
),

"created_at": transaction.get(
    "created_at"
),
            }
        )

    return {
        "success": True,
        "data": transactions,
    }