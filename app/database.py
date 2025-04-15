from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base, sessionmaker

# Base class for SQLAlchemy models
Base = declarative_base()

# Global variables to be initialized
async_engine = None
AsyncSessionLocal = None

async def initialize_async_db(database_url: str):
    """
    Initializes the asynchronous database engine and sessionmaker.
    """
    global async_engine, AsyncSessionLocal
    async_engine = create_async_engine(database_url, echo=True, future=True)
    AsyncSessionLocal = sessionmaker(
        bind=async_engine, class_=AsyncSession, expire_on_commit=False, future=True
    )

async def get_async_db():
    """
    Dependency to yield a session for each request.
    """
    async with AsyncSessionLocal() as async_session:
        try:
            yield async_session
        finally:
            await async_session.close()

class Database:
    """
    Simple wrapper for dependency injection in FastAPI.
    """
    async def get_session(self):
        async for session in get_async_db():
            return session
