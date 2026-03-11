from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

URL = "sqlite+aiosqlite:///./forum-fastapi.db"

engine = create_async_engine(
    url=URL,
    connect_args = {"check_same_thread": False}
)

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

class Base(DeclarativeBase):
    pass

async def get_db():
    with AsyncSessionLocal() as session:
        yield session

