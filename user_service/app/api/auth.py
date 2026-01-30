from fastapi import APIRouter, Depends, Response
from sqlalchemy.ext.asyncio import AsyncSession
# from app.core.security import get_password_hash
from app.models.user import User
# from app.repositories.users import UserRepository
from app.schemas import user as schemas
from app.config.database import get_db
from app.services.auth import AuthService
from app.dependencies.auth import get_current_user


router = APIRouter(prefix="/auth", tags=["Auth"])


async def get_auth_service(db: AsyncSession = Depends(get_db)):
    return AuthService


@router.post("/register", response_model=schemas.UserResponse)
async def register_user(
    user_data: schemas.UserCreate,
    db: AsyncSession = Depends(get_db)
):
    service = AuthService(db)
    return await service.register_user(user_data)


@router.post("/login")
async def auth_user(
    response: Response,
    user: schemas.TokenCreate,
    db: AsyncSession = Depends(get_db)
):
    service = AuthService(db)
    return await service.authentificate_user(
        response=response,
        username=user.useranme,
        password=user.password
    )


@router.get("/me")
async def get_me(
    user_data: User = Depends(get_current_user)
):
    return user_data


@router.post("/logout/")
async def logout_user(response: Response, db: AsyncSession = Depends(get_db)):
    service = AuthService(db)
    return await service.logout_user(response)
