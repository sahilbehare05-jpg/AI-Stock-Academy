from fastapi import APIRouter, HTTPException, Query

from app.services.stock_service import (
    get_stock_data,
    get_live_price,
)


router = APIRouter(
    prefix="/api/stocks",
    tags=["Stocks"],
)

@router.get("/{symbol}/live")
async def live_stock_price(symbol: str):
    try:
        data = get_live_price(symbol)

        return {
            "success": True,
            "data": data,
        }

    except ValueError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e),
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Unable to fetch live price: {str(e)}",
        )
@router.get("/{symbol}")
async def stock_analysis(
    symbol: str,
    period: str = Query("1mo"),
    interval: str = Query("1D"),
):
    try:
        data = get_stock_data(
            symbol=symbol,
            period=period,
            interval=interval,
        )

        return {
            "success": True,
            "data": data,
        }

    except ValueError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e),
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Unable to fetch stock data: {str(e)}",
        )