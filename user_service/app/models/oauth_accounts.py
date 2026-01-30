from sqlalchemy.sql import text
from sqlalchemy.orm import relationship
from sqlalchemy import Column, VARCHAR, TIMESTAMP
from sqlalchemy import UUID, ForeignKey, TEXT, UniqueConstraint
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
        ForeignKey('users.id', ondelete="CASCADE"),
        index=True
    )
    provider = Column(VARCHAR(50), nullable=False)
    provider_id = Column(VARCHAR(255), nullable=False)
    access_token = Column(TEXT)
    refresh_token = Column(TEXT)
    expires_at = Column(TIMESTAMP)

    user = relationship("User", back_populates="oauth_accounts")

    __table_args__ = (
        UniqueConstraint(
            'provider',
            'provider_id',
            name='uq_provider_provider_id'
        ),
        UniqueConstraint(
            'user_id',
            'provider',
            name='uq_user_provider'
        ),
    )
