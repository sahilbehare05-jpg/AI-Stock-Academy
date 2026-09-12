from fastapi import APIRouter, HTTPException, Query

from app.services.news_service import get_market_news


router = APIRouter(
    prefix="/api/news",
    tags=["Market News"],
)


@router.get("")
async def market_news(
    symbol: str | None = Query(
        default=None,
        description="Optional stock symbol, e.g. AAPL or RELIANCE.NS",
    ),
    limit: int = Query(
        default=20,
        ge=1,
        le=50,
    ),
):
    try:
        news = await get_market_news(
            symbol=symbol,
            limit=limit,
        )

        return {
            "success": True,
            "data": news,
        }

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to load market news: {str(e)}",
        )