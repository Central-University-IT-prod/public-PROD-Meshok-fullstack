from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import computed_field
from sqlalchemy import URL


class Settings(BaseSettings):
    # database_url: str = "sqlite+aiosqlite:///./feedbacker.db"
    secret: str = "SECRET"

    host: str = "localhost"
    port: int = 5432
    user_name: str
    password: str
    database: str

    @computed_field  # type: ignore[misc]
    @property
    def database_url(self) -> str:
        return URL.create(
            drivername="postgresql+asyncpg",
            host=self.host,
            port=self.port,
            username=self.user_name,
            password=self.password,
            database=self.database
        ).render_as_string(hide_password=False)

    model_config = SettingsConfigDict(env_file='.env')


settings = Settings()
