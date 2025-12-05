from datetime import timedelta

from app.core.auth import jwt_auth
from app.enums import TokenTypeEnum
from app.core.config import jwt_settings
from app.schemas.user import AuthLogin


def create_jwt(
    token_type: TokenTypeEnum,
    token_data: dict,
    expire_minutes: int = jwt_settings.jwt_access_token_ttl,
    expire_timedelta: timedelta | None = None,
) -> str:
    jwt_payload = {"token_type": token_type.value}
    jwt_payload.update(token_data)
    return jwt_auth.encode_token(
        payload=jwt_payload,
        expire_minutes=expire_minutes,
        expire_timedelta=expire_timedelta,
    )

def create_access_token(
    *,
    user_data: AuthLogin,
) -> str:
    jwt_payload = {
        "token_owner": user_data.email,
        "email": user_data.email,
    }
    return create_jwt(
        token_type=TokenTypeEnum.ACCESS,
        token_data=jwt_payload,
        expire_minutes=jwt_settings.jwt_access_token_ttl,
    )

def create_refresh_token(
    *,
    user_data: AuthLogin
) -> str:
    jwt_payload = {
        "token_owner": user_data.email,
    }
    return create_jwt(
        token_type=TokenTypeEnum.REFRESH,
        token_data=jwt_payload,
        expire_timedelta=timedelta(minutes=jwt_settings.jwt_refresh_token_ttl),
    )
