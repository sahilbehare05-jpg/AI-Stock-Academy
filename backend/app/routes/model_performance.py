from fastapi import APIRouter, Depends, HTTPException

from app.services.model_performance_service import (
    get_model_performance,
)
from app.utils.deps import get_current_user


router = APIRouter(
    prefix="/api/model-performance",
    tags=["Model Performance"],
)


@router.get("/{symbol}")
async def model_performance(
    symbol: str,
    period: str = "1y",
    current_user: dict = Depends(get_current_user),
):
    try:
        result = get_model_performance(
            symbol=symbol,
            period=period,
        )

        return {
            "success": True,
            "data": result,
        }

    except ValueError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e),
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Model performance evaluation failed: {str(e)}",
        )