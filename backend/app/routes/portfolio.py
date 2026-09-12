from bson import ObjectId
from fastapi import APIRouter, Depends

from app.database.db import get_database, Collections
from app.services.stock_service import get_live_price
from app.utils.deps import get_current_user


router = APIRouter(
    prefix="/api/portfolio",
    tags=["Portfolio"],
)


@router.get("")
async def get_portfolio(
    current_user: dict = Depends(get_current_user),
):
    db = get_database()

    user_id = ObjectId(current_user["id"])

    holdings_cursor = db[Collections.PORTFOLIO].find(
        {"user_id": user_id}
    )

    holdings = []

    total_invested = 0.0
    total_value = 0.0
    total_pnl = 0.0

    async for item in holdings_cursor:
        symbol = item["symbol"]
        quantity = int(item["quantity"])
        average_price = float(item["average_price"])

        # Get current LIVE market price
        try:
            live_data = get_live_price(symbol)
            current_price = float(live_data["price"])

        except Exception:
            # Fallback to average buy price if live data unavailable
            current_price = average_price

        invested_value = round(
            average_price * quantity,
            2,
        )

        market_value = round(
            current_price * quantity,
            2,
        )

        pnl = round(
            market_value - invested_value,
            2,
        )

        pnl_percent = round(
            (pnl / invested_value) * 100,
            2,
        ) if invested_value > 0 else 0.0

        total_invested += invested_value
        total_value += market_value
        total_pnl += pnl

        holdings.append(
            {
                "symbol": symbol,
                "quantity": quantity,

                "average_price": round(
                    average_price,
                    2,
                ),

                "current_price": round(
                    current_price,
                    2,
                ),

                "invested_value": invested_value,

                "market_value": market_value,

                "pnl": pnl,

                "pnl_percent": pnl_percent,
            }
        )

    total_invested = round(
        total_invested,
        2,
    )

    total_value = round(
        total_value,
        2,
    )

    total_pnl = round(
        total_pnl,
        2,
    )

    total_pnl_percent = round(
        (total_pnl / total_invested) * 100,
        2,
    ) if total_invested > 0 else 0.0

    return {
        "success": True,
        "data": {
            "user_id": current_user["id"],

            "holdings": holdings,

            "total_invested": total_invested,

            "total_value": total_value,

            "total_pnl": total_pnl,

            "total_pnl_percent": total_pnl_percent,
        },
    }