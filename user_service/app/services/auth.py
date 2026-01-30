from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from app.repositories.users import UserRepository
from app.schemas import user as schemas


class AuthService:
    def __init__(self, db: AsyncSession):
        self.crud = UserRepository(db)

    async def create_user(self, user: schemas.UserCreate):
        if await self.crud.get_user_by_username(user.username):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Username already exists",
            )

        if await self.crud.get_user_by_email(user.email):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Email already exists",
            )

        db_user = await self.crud.create_user(user)
        return schemas.UserResponse.model_validate(db_user)
