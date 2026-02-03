from sqlalchemy.ext.asyncio import AsyncSession
# from jose import jwts
from fastapi import HTTPException, status, Response, Request
# from fastapi.security import OAuth2PasswordRequestForm
from app.repositories.users import UserRepository
from app.schemas import user as schemas
from app.core.security import verify_password, create_access_token
from app.core.security import decode_token, create_refresh_token
from app.models.user import User


class AuthService:
    def __init__(self, db: AsyncSession):
        self.crud = UserRepository(db)

    @staticmethod
    def get_token(request: Request):
        token = request.cookies.get('users_access_token')
        if not token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token not found"
            )
        return token

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

        refresh_token = create_refresh_token({"sub": str(user.id)})
        response.set_cookie(
            key="users_refresh_token",
            value=refresh_token,
            httponly=True
        )
        return {'access_token': access_token, 'refresh_token': refresh_token}

    async def logout_user(self, response: Response):
        response.delete_cookie(key="users_access_token")
        response.delete_cookie(key="users_refresh_token")
        return {"message": "User logout successfully"}

    async def refresh_token(
        self,
        request: Request,
        response: Response,
        user: User
    ):
        refresh_token = request.cookies.get('users_refresh_token')
        if not refresh_token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token not found"
            )
        decoded_token = decode_token(refresh_token)
        user_id = decoded_token.get('sub')
        if str(user_id) != str(user.id):
            raise HTTPException(
                status_code=401,
                detail=f"Invalid Token {user_id}   {user.id}"
            )

        access_token = create_access_token({"sub": str(user_id)})
        response.set_cookie(
            key="users_access_token",
            value=access_token,
            httponly=True
        )

        refresh_token = create_refresh_token({"sub": str(user_id)})
        response.set_cookie(
            key="users_refresh_token",
            value=refresh_token,
            httponly=True
        )
        return {'access_token': access_token, 'refresh_token': refresh_token}
