from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from datetime import datetime
from app.schemas import user as schemas
from app.models import users as models


class UserRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_user(self, user: schemas.UserCreate):
        db_user = models.User(
            id=user.id,
            email=user.email,
            username=user.username,
            is_active=user.is_active,
            is_verified=user.is_verified,
        )

        self.db.add(db_user)
        await self.db.commit()
        await self.db.refresh(db_user)
        return db_user

    async def get_user_by_id(self, id: str) -> models.User:
        result = await self.db.execute(
            select(models.User).where(models.User.id == id)
        )
        return result.scalar_one_or_none()

    async def get_user_by_username(self, username: str) -> models.User:
        result = await self.db.execute(
            select(models.User).where(models.User.username == username)
        )
        return result.scalar_one_or_none()

    async def get_user_by_email(self, email: str) -> models.User:
        result = await self.db.execute(
            select(models.User).where(models.User.email == email)
        )
        return result.scalar_one_or_none()

    async def update_user_by_username(
            self,
            username: str,
            user_update: schemas.UserUpdate
        ):
        db_user = await self.get_user_by_username(username)

        if not db_user:
            return None

        db_user.updated_at = datetime.now()

        update_data = user_update.model_dump(exclude_unset=True)

        for field, value in update_data.items():
            setattr(db_user, field, value)
        await self.db.commit()
        await self.db.refresh(db_user)
        return db_user

    async def update_user_by_id(
            self,
            id: str,
            user_update: schemas.UserUpdate
        ):
        db_user = await self.get_user_by_id(id)

        if not db_user:
            return None

        db_user.updated_at = datetime.now()

        update_data = user_update.model_dump(exclude_unset=True)

        for field, value in update_data.items():
            setattr(db_user, field, value)
        await self.db.commit()
        await self.db.refresh(db_user)
        return db_user

    async def delete_user(self, username: str) -> models.Profile:
        db_user = await self.get_user_by_username(username)
        db_user.is_active = False
        db_user.updated_at = datetime.now()
        await self.db.commit()
        await self.db.refresh(db_user)
        return db_user
