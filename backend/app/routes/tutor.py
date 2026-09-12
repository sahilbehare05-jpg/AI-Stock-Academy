from fastapi import APIRouter, Depends, HTTPException

from app.schemas.tutor import TutorChatRequest, TutorChatResponse
from app.services.tutor_service import ask_tutor
from app.utils.deps import get_current_user


router = APIRouter(
    prefix="/api/tutor",
    tags=["AI Trading Tutor"],
)


@router.post("/chat", response_model=TutorChatResponse)
async def tutor_chat(
    request: TutorChatRequest,
    current_user: dict = Depends(get_current_user),
):
    try:
        answer = ask_tutor(
            question=request.question,
            level=request.level,
            context=request.context,
        )

        return {
            "success": True,
            "answer": answer,
        }

    except Exception as e:
        print(f"Tutor error: {e}")

        raise HTTPException(
            status_code=500,
            detail="Unable to get a response from the AI Trading Tutor.",
        )