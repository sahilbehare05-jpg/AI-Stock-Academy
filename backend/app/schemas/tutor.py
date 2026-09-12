from pydantic import BaseModel, Field


class TutorChatRequest(BaseModel):
    question: str = Field(..., min_length=1, max_length=4000)
    level: str = "Beginner"
    context: str = ""


class TutorChatResponse(BaseModel):
    success: bool
    answer: str