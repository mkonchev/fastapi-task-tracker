from sqlalchemy.sql import text
from sqlalchemy import Column, VARCHAR, TIMESTAMP
from sqlalchemy import UUID, ForeignKey, JSON, TEXT
from app.config.database import Base


class OAuthAccounts(Base):
    __tablename__ = "oauth_accounts"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()")
    )
    user_id = Column(
        UUID,
        ForeignKey('user.id'),
        ondelete="CASCADE",
        index=True
    )
    provider = Column(VARCHAR(50), nullable=False, unique=True)
    provider_id = Column(VARCHAR(255), nullable=False, unique=True)
    access_token = Column(TEXT)
    refresh_token = Column(TEXT)
    expires_at = Column(TIMESTAMP)
