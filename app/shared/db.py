"""
Configuración de SQLAlchemy 2.0 async con session management.
"""
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase
from app.config.settings import settings


# Declarative Base (la heredan tus modelos)
class Base(DeclarativeBase):
    pass


# Engine async
engine: AsyncEngine = create_async_engine(
    settings.DATABASE_URL,  # ej: postgresql+asyncpg://user:pass@localhost:5432/db
    echo=False,
    pool_pre_ping=True,
)

# Session maker async
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """Dependency para obtener sesión de BD en endpoints"""
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
