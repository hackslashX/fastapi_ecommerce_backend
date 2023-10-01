from sqlalchemy.ext.asyncio import AsyncSession

from .session import AsyncSessionMaker
from instance.config import config


async def get_db() -> AsyncSession:
    """
    Dependency function that yields db sessions
    """
    db: AsyncSession = AsyncSessionMaker()
    try:
        db.sync_session.set_bind_key(config.APP_ENVIRONMENT)
        yield db
    finally:
        await db.close()
