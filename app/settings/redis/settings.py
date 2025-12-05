from pydantic import Field
from app.settings import EnvSettings


class RedisSettings(EnvSettings):
    USER: str = Field(..., max_length=64, alias="REDIS_USER")
    PASSWORD: str = Field(..., max_length=64, alias="REDIS_PASSWORD")