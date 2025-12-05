from typing import Annotated
from fastapi import Depends

from app.services.auth import AuthService
from app.utils import LoggerDep
from app.common.deps import CommonPostgresDep


def _get_auth_service(
    logger: LoggerDep,
    postgres_adapter: CommonPostgresDep,
) -> AuthService:
    return AuthService(
        logger=logger,
        postgres_adapter=postgres_adapter
    )

AuthServiceDep = Annotated[AuthService, Depends(_get_auth_service)]
