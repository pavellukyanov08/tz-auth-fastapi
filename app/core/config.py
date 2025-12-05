import os
from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv

load_dotenv()


class JWTSettings(BaseModel):
    jwt_secret_key: str = os.getenv("JWT_SECRET_KEY")
    jwt_access_token_ttl: int = int(os.getenv("JWT_ACCESS_TOKEN_TTL"))
    jwt_refresh_token_ttl: int = int(os.getenv("JWT_REFRESH_TOKEN_TTL"))


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    DB_HOST: str
    DB_PORT: str
    DB_NAME: str
    DB_USER: str
    DB_PASS: str
    SECRET_KEY: str
    redis_host: str
    redis_port: int
    redis_user: str
    redis_password: str


    @property
    def async_database_url(self) -> str:
        return (
            f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )

    @property
    def sync_database_url(self) -> str:
        return (
            f"postgresql://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )



jwt_settings = JWTSettings()
settings = Settings()
