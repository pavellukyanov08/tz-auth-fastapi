from pydantic import Field


class JwtSettings:
    SECRET_KEY: str = Field(
        ..., min_length=10, max_length=128, alias="JWT_SECRET_KEY"
    )
    ACCESS_TOKEN_TTL: int = Field(
        ..., ge=300, le=1800, alias="JWT_ACCESS_TOKEN_TTL"
    )
    REFRESH_TOKEN_TTL: int = Field(
        ..., ge=3600, le=2592000, alias="JWT_REFRESH_TOKEN_TTL"
    )