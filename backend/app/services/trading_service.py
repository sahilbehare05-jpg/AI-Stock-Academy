from datetime import datetime, timezone

from bson import ObjectId
from bson.errors import InvalidId
from fastapi import HTTPException, status

from app.database.db import get_database, Collections


async def buy_stock(user_id: str, symbol: str, quantity: int, price: float):
    if quantity <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Quantity must be greater than zero.",
        )

    if price <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Stock price must be greater than zero.",
        )

    try:
        user_oid = ObjectId(user_id)
    except InvalidId:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid user ID.",
        )

    symbol = symbol.strip().upper()
    total_cost = round(price * quantity, 2)

    db = get_database()
    users = db[Collections.USERS]
    portfolio = db[Collections.PORTFOLIO]
    transactions = db[Collections.TRANSACTIONS]

    user = await users.find_one({"_id": user_oid})

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found.",
        )

    current_balance = float(
        user.get("virtual_balance", 0)
        )
    

    if current_balance < total_cost:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Insufficient virtual balance.",
        )

    now = datetime.now(timezone.utc)

    # Deduct money from wallet
    await users.update_one(
        {"_id": user_oid},
        {
            "$set": {
                "virtual_balance": round(
                    current_balance - total_cost, 2
                ),
                "updated_at": now,
            }
        },
    )

    # Add/update portfolio holding
    existing = await portfolio.find_one(
        {
            "user_id": user_oid,
            "symbol": symbol,
        }
    )

    if existing:
        old_quantity = int(existing.get("quantity", 0))
        old_average_price = float(
            existing.get("average_price", 0)
        )

        new_quantity = old_quantity + quantity

        new_average_price = (
            (old_quantity * old_average_price)
            + (quantity * price)
        ) / new_quantity

        await portfolio.update_one(
            {"_id": existing["_id"]},
            {
                "$set": {
                    "quantity": new_quantity,
                    "average_price": round(new_average_price, 2),
                    "updated_at": now,
                }
            },
        )

    else:
        await portfolio.insert_one(
            {
                "user_id": user_oid,
                "symbol": symbol,
                "quantity": quantity,
                "average_price": round(price, 2),
                "created_at": now,
                "updated_at": now,
            }
        )

    # Save transaction
    await transactions.insert_one(
        {
            "user_id": user_oid,
            "type": "BUY",
            "symbol": symbol,
            "quantity": quantity,
            "price": round(price, 2),
            "total": total_cost,
            "created_at": now,
        }
    )

    new_balance = round(current_balance - total_cost, 2)

    return {
        "symbol": symbol,
        "quantity": quantity,
        "price": round(price, 2),
        "total": total_cost,
        "balance": new_balance,
        "message": f"Successfully bought {quantity} shares of {symbol}.",
    }
async def sell_stock(user_id: str, symbol: str, quantity: int, price: float):
    if quantity <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Quantity must be greater than zero.",
        )

    if price <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Stock price must be greater than zero.",
        )

    try:
        user_oid = ObjectId(user_id)
    except InvalidId:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid user ID.",
        )

    symbol = symbol.strip().upper()
    total_amount = round(price * quantity, 2)

    db = get_database()
    users = db[Collections.USERS]
    portfolio = db[Collections.PORTFOLIO]
    transactions = db[Collections.TRANSACTIONS]

    holding = await portfolio.find_one(
        {
            "user_id": user_oid,
            "symbol": symbol,
        }
    )

    if not holding:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"You do not own any shares of {symbol}.",
        )

    owned_quantity = int(holding.get("quantity", 0))

    if quantity > owned_quantity:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Insufficient shares. You own {owned_quantity} shares of {symbol}.",
        )

    user = await users.find_one({"_id": user_oid})

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found.",
        )
    current_balance = float(user.get("virtual_balance", 0))
    new_balance = round(current_balance + total_amount, 2)

    # Calculate realized P&L for the sold shares
    average_price = float(
        holding.get("average_price", 0)
    )

    invested_amount = round(
        average_price * quantity,
        2,
    )

    realized_pnl = round(
        (price - average_price) * quantity,
        2,
    )

    realized_pnl_percent = round(
        (
            realized_pnl / invested_amount
        ) * 100,
        2,
    ) if invested_amount > 0 else 0.0

    now = datetime.now(timezone.utc)

    # Add sale amount to wallet
    await users.update_one(
        {"_id": user_oid},
        {
            "$set": {
                "virtual_balance": new_balance,
                "updated_at": now,
            }
        },
    )

    remaining_quantity = owned_quantity - quantity

    if remaining_quantity == 0:
        await portfolio.delete_one(
            {"_id": holding["_id"]}
        )
    else:
        await portfolio.update_one(
            {"_id": holding["_id"]},
            {
                "$set": {
                    "quantity": remaining_quantity,
                    "updated_at": now,
                }
            },
        )

    # Save SELL transaction
    await transactions.insert_one(
        {
            "user_id": user_oid,
            "type": "SELL",
            "symbol": symbol,
            "quantity": quantity,
            "price": round(price, 2),
            "total": total_amount,
            "realized_pnl": realized_pnl,
            "realized_pnl_percent": realized_pnl_percent,
            "created_at": now,
        }
    )

    return {
        "symbol": symbol,
        "quantity": quantity,
        "price": round(price, 2),
        "total": total_amount,
        "balance": new_balance,
        "realized_pnl": realized_pnl,
        "realized_pnl_percent": realized_pnl_percent,
        "message": f"Successfully sold {quantity} shares of {symbol}.",
    }