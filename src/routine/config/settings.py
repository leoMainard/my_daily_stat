from pydantic_settings import BaseSettings
from functools import lru_cache
from dotenv import load_dotenv
import os

load_dotenv()

class Settings(BaseSettings):
    DB_HOST: str = os.getenv("DB_HOST")
    DB_PORT: int = 5432
    DB_NAME: str = os.getenv("DB_NAME")
    DB_USER: str = os.getenv("DB_USER")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD")

    # App
    APP_NAME: str = "Mon App Streamlit"
    DEBUG: bool = False
    LOG_LEVEL: str = "INFO"

    @property
    def database_url(self) -> str:
        """URL de connexion pour SQLAlchemy/Alembic"""
        return (
            f"postgresql://{self.DB_USER}:{self.DB_PASSWORD}"
            f"@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )
    
    # class Config:
    #     env_file = ".env"
    #     env_file_encoding = 'utf-8'
    #     case_sensitive = True
    #     extra = "ignore"

@lru_cache()
def get_settings() -> Settings:
    return Settings()

settings = get_settings()