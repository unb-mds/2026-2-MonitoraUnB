"""
Configurações da aplicação carregadas via variáveis de ambiente (.env).
"""

from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache
from sqlalchemy.engine import URL



class Settings(BaseSettings):
    """Configurações da aplicação."""

    model_config = SettingsConfigDict(
            env_file=".env",
            env_file_encoding="utf-8",
            extra="ignore",
        )
    # Database
    DB_HOST: str = "localhost"
    DB_PORT: int = 5432
    DB_USER: str = "monitora_app"
    DB_PASSWORD: str = ""
    DB_NAME: str = "monitora_unb"


    # Scraper
    SCRAPER_DELAY: float = 1.5
    SIGAA_BASE_URL: str = "https://sigaa.unb.br/sigaa"

    # Email (SMTP)
    SMTP_HOST: str = "smtp.gmail.com"
    SMTP_PORT: int = 587
    SMTP_USER: str = ""
    SMTP_PASSWORD: str = ""
    SMTP_FROM: str = ""
    SMTP_USE_TLS: bool = True

    # Auth do professor (login exclusivo — uma credencial)
    PROFESSOR_USERNAME: str = ""
    PROFESSOR_PASSWORD_HASH: str = ""
    SESSION_SECRET: str = ""

    @property
    def DATABASE_URL(self) -> str:
        return URL.create(
            drivername="postgresql+psycopg",
            username=self.DB_USER,
            password=self.DB_PASSWORD,
            host=self.DB_HOST,
            port=self.DB_PORT,
            database=self.DB_NAME,
        ).render_as_string(hide_password=False)

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache()
def get_settings() -> Settings:
    return Settings()

# comentario de teste
