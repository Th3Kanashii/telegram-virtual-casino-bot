from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy.engine.url import URL


class Config(BaseSettings):
    """
    The main configuration class for the bot.
    """

    bot_token: SecretStr

    postgres_host: str
    postgres_db: str
    postgres_password: SecretStr
    postgres_port: int
    postgres_user: str

    redis_host: str
    redis_port: int
    redis_db: int

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    @property
    def build_postgres_dsn(self) -> URL:
        """
        :return: Build a DSN for the PostgreSQL database.
        """
        return URL.create(
            drivername="postgresql+asyncpg",
            username=self.postgres_user,
            password=self.postgres_password.get_secret_value(),
            host=self.postgres_host,
            port=self.postgres_port,
            database=self.postgres_db,
        )
