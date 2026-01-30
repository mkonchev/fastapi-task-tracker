from sqlalchemy.sql import text
from sqlalchemy.orm import relationship
from sqlalchemy import Column, VARCHAR
from sqlalchemy import UUID, ForeignKey, JSON, TEXT
from app.config.database import Base


class Profile(Base):
    __tablename__ = "profiles"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()")
    )
    user_id = Column(UUID, ForeignKey('users.id', ondelete="CASCADE"))
    full_name = Column(VARCHAR(255))
    avatar_url = Column(TEXT)
    timezone = Column(VARCHAR(50), server_default="UTC")
    settings = Column(
        JSON,
        default='{"notifications": true, "theme": "light"}'
    )

    user = relationship("User", back_populates="profile")
