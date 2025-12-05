from typing import Self
from app.utils.normalize_datetime import NormalizeDateTime
from uuid import UUID
from pydantic import model_validator, Field, BaseModel
from datetime import datetime

from app.enums import TokenTypeEnum


class Token(NormalizeDateTime):
    token_owner: UUID = Field(..., description="Token owner (user_sid")
    token_type: TokenTypeEnum = Field(..., description="Token type")
    expired_at: datetime = Field(..., description="Token expired at")
    created_at: datetime = Field(..., description="Token created at")

    redis_key: str = Field(
        "", exclude=True, description="Token key for redis"
    )

    @staticmethod
    def build_redis_key(
        *,
        token_owner: UUID | None = None,
        token_type: TokenTypeEnum | None = None,
        sid: UUID | None = None,
    ) -> str:
        return (
            f"token:{token_owner or '*'}:"
            f"{token_type or '*'}:"
            f"{sid or '*'}"
        )

    @model_validator(mode="after")
    def create_redis_key(self) -> Self:
        self.redis_key = self.build_redis_key(
            token_owner=self.token_owner,
            token_type=self.token_type,
            sid=self.sid,
        )
        return self