from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status, Response
from app.repositories.users import UserRepository
from app.schemas import user as schemas
from app.core.security import verify_password, create_access_token


class AuthService:
    def __init__(self, db: AsyncSession):
        self.crud = UserRepository(db)

    async def register_user(self, user: schemas.UserCreate):
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

    async def authentificate_user(
            self,
            response: Response,
            username: str,
            password: str
    ):
        user = await self.crud.get_user_by_username(username)
        if not user or not verify_password(password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password"
            )
        access_token = create_access_token({"sub": str(user.id)})
        response.set_cookie(
            key="users_access_token",
            value=access_token,
            httponly=True
        )
        return {'access_token': access_token, 'refresh_token': None}
