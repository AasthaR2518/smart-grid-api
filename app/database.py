from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.config import settings

# Async database engine & session maker (used by FastAPI)
async_engine = create_async_engine(
    settings.DATABASE_ASYNC_URL, 
    pool_size=20, 
    max_overflow=10, 
    pool_pre_ping=True, 
    echo=False
)
AsyncSessionLocal = async_sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False
)

# Sync database engine & session maker (used by Celery tasks)
sync_engine = create_engine(
    settings.DATABASE_SYNC_URL,
    pool_size=10,
    max_overflow=5,
    pool_pre_ping=True,
    echo=False
)
SessionLocal = sessionmaker(
    bind=sync_engine,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False
)

# Base class for SQLAlchemy models
Base = declarative_base()

# FastAPI Dependency for obtaining an async session
async def get_async_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
