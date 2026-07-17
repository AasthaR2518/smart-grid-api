from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "postgres"
    POSTGRES_DB: str = "smartgrid"
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: int = 5432
    DATABASE_ASYNC_URL: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/smartgrid"
    DATABASE_SYNC_URL: str = "postgresql://postgres:postgres@localhost:5432/smartgrid"

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()
