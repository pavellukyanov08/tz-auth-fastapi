from pydantic_settings import BaseSettings


class ApiSettings(BaseSettings):
    AUTH_USERS_PREFIX: str = '/auth'
    USERS_PREFIX: str = '/users'


api_settings = ApiSettings()