from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    """
    The main configuration class for the bot.
    """

    bot_token: SecretStr

    postgres_host: str
    postgres_db: str
    postgres_password: str
    postgres_port: str
    postgres_user: str

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    @property
    def build_postgres_dsn(self) -> str:
        """
        :return: Build a DSN for the PostgreSQL database.
        """
        return (
            "postgresql+asyncpg://"
            f"{self.postgres_user}:{self.postgres_password}"
            f"@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
        )
