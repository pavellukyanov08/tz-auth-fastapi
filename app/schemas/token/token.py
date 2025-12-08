from pydantic import Field, BaseModel
from app.enums import TokenTypeEnum


class TokenPair(BaseModel):
    access_token: str = Field(..., description="Access token")
    refresh_token: str = Field(..., description="Refresh token")
    token_type: TokenTypeEnum


class RefreshToken(BaseModel):
    access_token: str = Field(..., description="Access token")
    token_type: TokenTypeEnum = Field(..., description="Token type")
