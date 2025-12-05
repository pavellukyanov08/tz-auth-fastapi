from pydantic import Field
from app.enums import TokenTypeEnum

from app.common.schemas import CamelDTO


class TokenPair(CamelDTO):
    access_token: str = Field(..., description="Access token")
    refresh_token: str = Field(..., description="Refresh token")
    token_type: TokenTypeEnum


class RefreshToken(CamelDTO):
    access_token: str = Field(..., description="Access token")
    token_type: TokenTypeEnum = Field(..., description="Token type")
