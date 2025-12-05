from typing import Annotated
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.common.adapters import PostgresStorageAdapter
from app.core.database import get_db
from app.utils import LoggerDep


def _get_common_postgres_adapter(
    logger: LoggerDep,
    postgres_session: Annotated[AsyncSession, Depends(get_db)],
) -> PostgresStorageAdapter:
    return PostgresStorageAdapter(
        logger=logger,
        postgres_session=postgres_session
    )


CommonPostgresDep = Annotated[PostgresStorageAdapter, Depends(_get_common_postgres_adapter)]
