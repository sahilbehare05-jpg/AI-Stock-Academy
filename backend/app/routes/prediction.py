from fastapi import APIRouter, HTTPException, Depends
from datetime import datetime, timezone
from bson import ObjectId

from app.services.prediction_service import (
    get_prediction,
    get_prediction_explanation,
)
from app.utils.deps import get_current_user
from app.database.db import get_database, Collections


router = APIRouter(
    prefix="/api/prediction",
    tags=["AI Prediction"],
)


@router.get("/explain/{symbol}")
async def explain_prediction(symbol: str):
    try:
        result = get_prediction_explanation(symbol)

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
            detail=f"Explanation failed: {str(e)}",
        )


@router.get("/history")
async def prediction_history(
    current_user: dict = Depends(get_current_user),
):
    try:
        db = get_database()

        user_id = ObjectId(current_user["id"])

        cursor = (
            db[Collections.PREDICTIONS]
            .find({"user_id": user_id})
            .sort("created_at", -1)
        )

        history = []

        async for prediction in cursor:
            history.append(
                {
                    "id": str(prediction["_id"]),
                    "symbol": prediction.get("symbol"),
                    "prediction": prediction.get("prediction"),
                    "confidence": float(
                        prediction.get("confidence", 0)
                    ),
                    "model": prediction.get("model"),
                    "features": prediction.get(
                        "features", {}
                    ),
                    "created_at": prediction.get(
                        "created_at"
                    ),
                }
            )

        return {
            "success": True,
            "data": history,
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to load prediction history: {str(e)}",
        )


@router.get("/{symbol}")
async def predict(
    symbol: str,
    current_user: dict = Depends(get_current_user),
):
    try:
        result = get_prediction(symbol)

        db = get_database()

        user_id = ObjectId(current_user["id"])

        prediction_document = {
            "user_id": user_id,
            "symbol": result["symbol"],
            "prediction": result["prediction"],
            "confidence": result["confidence"],
            "model": result["model"],
            "features": result["features"],
            "created_at": datetime.now(timezone.utc),
        }

        await db[Collections.PREDICTIONS].insert_one(
            prediction_document
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
            detail=f"Prediction failed: {str(e)}",
        )