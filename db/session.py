"""
Contains SQLAlchemy Session Instance
"""
from sqlalchemy.exc import DBAPIError, InterfaceError, OperationalError
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from sqlalchemy.orm import Session

from instance.config import config


class RoutingSession(Session):
    """
    Responsible for query traffic routing to connection strings defined in SQLALCHEMY_ENGINES.
    This can be used to specify multiple DB binds, separate for reader, writer, master, proxies, etc.
    Or specifying different connections for multi-tenants configuration
    """

    bind_key = config.APP_ENVIRONMENT

    def get_bind(self, mapper=None, clause=None, **kw):
        engines = config.SQLALCHEMY_ENGINES
        if mapper is None:
            return engines[self.bind_key].sync_engine

        if hasattr(mapper.mapped_table, "info"):
            if "bind_key" in mapper.mapped_table.info:
                self.bind_key = mapper.mapped_table.info["bind_key"]
            return engines[self.bind_key].sync_engine

        return engines["development"].sync_engine

    def set_bind_key(self, bind_key: str):
        self.bind_key = bind_key


class RetryingSession(AsyncSession):
    retry_count: int = 3

    async def execute(self, statement, *args, **kwargs):
        retries: int = 0
        engine = self.get_bind()

        while retries < self.retry_count:
            try:
                return await super().execute(statement, *args, **kwargs)
            except (OperationalError, InterfaceError, DBAPIError) as e:
                # Raise this exception so that it is automatically handled
                # by the logging handlers
                retries += 1
                engine.dispose()
                if retries == self.retry_count:
                    raise e


# Bind Session to Async Session
AsyncSessionMaker = async_sessionmaker(
    sync_session_class=RoutingSession, class_=RetryingSession, expire_on_commit=False
)
