from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field

from app.services.trading_service import buy_stock, sell_stock
from app.utils.deps import get_current_user


router = APIRouter(
    prefix="/api/trading",
    tags=["Virtual Trading"],
)


class BuyRequest(BaseModel):
    symbol: str = Field(min_length=1, max_length=20)
    quantity: int = Field(gt=0)
    price: float = Field(gt=0)


@router.post("/buy")
async def buy(
    payload: BuyRequest,
    current_user: dict = Depends(get_current_user),
):
    result = await buy_stock(
        user_id=current_user["id"],
        symbol=payload.symbol,
        quantity=payload.quantity,
        price=payload.price,
    )

    return {
        "success": True,
        "data": result,
    }
class SellRequest(BaseModel):
    symbol: str = Field(min_length=1, max_length=20)
    quantity: int = Field(gt=0)
    price: float = Field(gt=0)


@router.post("/sell")
async def sell(
    payload: SellRequest,
    current_user: dict = Depends(get_current_user),
):
    result = await sell_stock(
        user_id=current_user["id"],
        symbol=payload.symbol,
        quantity=payload.quantity,
        price=payload.price,
    )

    return {
        "success": True,
        "data": result,
    }