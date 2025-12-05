from typing import Annotated
from fastapi import Depends, Request
# from redis import Redis

from app.services.auth import AuthService
from app.utils import LoggerDep
from app.common.deps import CommonPostgresDep
from app.adapters import RedisAdapter


# def _get_redis_client(request: Request) -> Redis:
#     redis_client: Redis | None = getattr(
#         request.state, "redis_client", None
#     )
#     if not redis_client:
#         raise RuntimeError("Missing required request state: redis_client")
#     return redis_client
#
#
# def _get_redis_adapter(
#     logger: LoggerDep,
#     redis_client: Annotated[Redis, Depends(_get_redis_client)],
# ) -> RedisAdapter:
#     return RedisAdapter(
#         logger=logger,
#         redis_client=redis_client,
#     )


def _get_auth_service(
    logger: LoggerDep,
    # redis_adapter: Annotated[RedisAdapter, Depends(_get_redis_adapter)],
    postgres_adapter: CommonPostgresDep,
) -> AuthService:
    return AuthService(
        logger=logger,
        # redis_adapter=redis_adapter,
        postgres_adapter=postgres_adapter
    )

AuthServiceDep = Annotated[AuthService, Depends(_get_auth_service)]
