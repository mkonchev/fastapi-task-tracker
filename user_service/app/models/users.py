from sqlalchemy.sql import func, text
from sqlalchemy import Column, VARCHAR, Boolean, DateTime, UUID
from app.config.database import Base


class User(Base):
    __tablename__ = "user"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()")
    )
    email = Column(VARCHAR(255), unique=True, index=True, nullable=False)
    username = Column(VARCHAR(100), unique=True, index=True, nullable=False)
    hashed_password = Column(VARCHAR(255))
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now())
