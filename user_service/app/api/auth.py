from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.security import get_password_hash
from app.models.user import User
from app.repositories.users import UserRepository
from app.schemas import user as schemas
from app.config.database import get_db
from app.services.auth import AuthService


router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register", response_model=schemas.UserResponse)
async def register_user(
    user_data: schemas.UserCreate,
    db: AsyncSession = Depends(get_db)
):
    service = AuthService(db)
    return await service.create_user(user_data)






    # user = await UserRepository.get_user_by_email(db, email=user_data.email)
    # if user:
    #     raise HTTPException(
    #         status_code=status.HTTP_409_CONFLICT,
    #         detail="User already registered"
    #     )
    # user_dict = user_data.model_dump()
    # user_dict['password'] = get_password_hash(user_data.password)
    # await UserRepository.create_user(db, user_dict)
    # return {"message": "You have been registered successfully!"}
