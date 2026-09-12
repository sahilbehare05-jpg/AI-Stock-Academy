from fastapi import APIRouter, Depends
from pydantic import BaseModel

from app.services import watchlist_service
from app.utils.deps import get_current_user


router = APIRouter(
    prefix="/api/watchlist",
    tags=["Watchlist"],
)


class WatchlistRequest(BaseModel):
    symbol: str


@router.get("")
async def get_watchlist(
    current_user: dict = Depends(get_current_user),
):
    user_id = str(current_user["id"])

    data = await watchlist_service.get_watchlist(user_id)

    return {
        "success": True,
        "data": data,
    }


@router.post("")
async def add_watchlist(
    payload: WatchlistRequest,
    current_user: dict = Depends(get_current_user),
):
    user_id = str(current_user["id"])

    data = await watchlist_service.add_to_watchlist(
        user_id,
        payload.symbol,
    )

    return {
        "success": True,
        "data": data,
    }


@router.delete("/{symbol}")
async def remove_watchlist(
    symbol: str,
    current_user: dict = Depends(get_current_user),
):
    user_id = str(current_user["id"])

    data = await watchlist_service.remove_from_watchlist(
        user_id,
        symbol,
    )

    return {
        "success": True,
        "data": data,
    }