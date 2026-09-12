"""
Authentication routes.
POST /api/auth/register
POST /api/auth/login
GET  /api/auth/me
"""
from fastapi import APIRouter, Depends
from app.schemas.user import UserRegister, UserLogin, TokenResponse, UserPublic
from app.services import auth_service
from app.utils.deps import get_current_user

router = APIRouter(prefix="/api/auth", tags=["Authentication"])


@router.post("/register", response_model=TokenResponse, status_code=201)
async def register(payload: UserRegister):
    result = await auth_service.register_user(
        name=payload.name,
        email=payload.email,
        password=payload.password,
        preferred_language=payload.preferred_language,
    )
    return result


@router.post("/login", response_model=TokenResponse)
async def login(payload: UserLogin):
    result = await auth_service.authenticate_user(payload.email, payload.password)
    return result


@router.get("/me", response_model=UserPublic)
async def me(current_user: dict = Depends(get_current_user)):
    return current_user
