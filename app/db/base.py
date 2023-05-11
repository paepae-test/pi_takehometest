from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from app.core.config import settings


# Database connection string
SQLALCHEMY_DATABASE_URL = f"postgresql+asyncpg://{settings.POSTGRES_USERNAME}:{settings.POSTGRES_PASSWORD}@{settings.POSTGRES_SERVER}:{settings.POSTGRES_PORT}/{settings.POSTGRES_DB}"

# Create the database engine
engine = create_async_engine(SQLALCHEMY_DATABASE_URL, echo=True)

# Create a session factory
async_session = async_sessionmaker(engine, expire_on_commit=False)

# Base class for database models
class Base(DeclarativeBase):
    pass
