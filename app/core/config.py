from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file= ".env",
        env_file_encoding="utf-8",
    )

    db_name: str = "forum-fastapi.db"

    secret_key: SecretStr
    alghorithm: str = "HS256"
    token_expire_minutes: int = 30

    @property
    def db_url(self):
        return f"sqlite+aiosqlite:///./{self.db_name}"

settings = Settings()

