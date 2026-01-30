from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    DB_HOST: str = "localhost"
    DB_PORT: str = "5435"
    DB_NAME: str = "user_db"
    DB_USER: str = "postgres"
    DB_PASSWORD: str = "1111"
    SEKRET_KEY: str = "my-secret-key"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7


settings = Settings()


def get_db_url():
    return (f"postgresql+asyncpg://{settings.DB_USER}:{settings.DB_PASSWORD}@"
            f"{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}")


def get_db_url_docker():
    return (f"postgresql+asyncpg://{settings.DB_USER}:{settings.DB_PASSWORD}@"
            f"localhost:{settings.DB_PORT}/{settings.DB_NAME}")


def get_auth_data():
    return {
        "secret_key": settings.SEKRET_KEY,
        "algorithm": settings.ALGORITHM,
        "access_token_exp": settings.ACCESS_TOKEN_EXPIRE_MINUTES,
        "refresh_token_exp": settings.REFRESH_TOKEN_EXPIRE_DAYS,
    }
