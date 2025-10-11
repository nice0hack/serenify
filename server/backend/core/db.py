from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from core.settings import settings

SQLALCHEMY_DATABASE_URL = "postgresql+asyncpg://{}:{}@{}/{}".format(
    settings.db_username,
    settings.db_password,
    settings.db_host,
    settings.db_name
)

engine = create_async_engine(SQLALCHEMY_DATABASE_URL, future=True, echo=True)
async_session_factory = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False) # type: ignore

Base = declarative_base()

async def get_session():
    async with async_session_factory() as session: # type: ignore
        yield session