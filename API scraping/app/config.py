"""
Configurações da aplicação carregadas via variáveis de ambiente (.env).
"""

from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """Configurações da aplicação."""

    # Database
    DB_TYPE: str = "postgres" 
    DB_HOST: str = "localhost"
    DB_PORT: int = 5432
    DB_USER: str = "postgres"
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
        db_type = self.DB_TYPE.lower()
        if db_type == "mysql":
            return (
                f"mysql+pymysql://{self.DB_USER}:{self.DB_PASSWORD}"
                f"@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
                "?charset=utf8mb4"
            )
        if db_type in ("postgres", "postgresql"):
            port = self.DB_PORT if self.DB_PORT != 3306 else 5432
            return (
                f"postgresql+psycopg2://{self.DB_USER}:{self.DB_PASSWORD}"
                f"@{self.DB_HOST}:{port}/{self.DB_NAME}"
            )
        return "sqlite:///./sigaa_unb.db"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache()
def get_settings() -> Settings:
    return Settings()
