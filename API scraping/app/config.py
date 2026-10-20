"""
Configurações da aplicação carregadas via variáveis de ambiente (.env).
"""

from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """Configurações da aplicação."""

    # Database
    DB_TYPE: str = "sqlite"  # "sqlite" ou "mysql"
    DB_HOST: str = "localhost"
    DB_PORT: int = 3306
    DB_USER: str = "root"
    DB_PASSWORD: str = ""
    DB_NAME: str = "sigaa_unb"
    DATABASE_URL_OVERRIDE: str | None = None

    # Scraper
    SCRAPER_DELAY: float = 1.5
    SIGAA_BASE_URL: str = "https://sigaa.unb.br/sigaa"

    @property
    def DATABASE_URL(self) -> str:
        if self.DATABASE_URL_OVERRIDE:
            return self.DATABASE_URL_OVERRIDE
        if self.DB_TYPE.lower() == "mysql":
            return (
                f"mysql+pymysql://{self.DB_USER}:{self.DB_PASSWORD}"
                f"@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
                "?charset=utf8mb4"
            )
        return "sqlite:///./sigaa_unb.db"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache()
def get_settings() -> Settings:
    return Settings()
