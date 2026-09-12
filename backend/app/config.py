"""
Central configuration for AI Stock Academy backend.
All secrets/config come from environment variables (.env file).
Never hard-code secrets here.
"""
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    mongo_uri: str = "mongodb://localhost:27017"
    mongo_db_name: str = "ai_stock_academy"

    jwt_secret_key: str = "change_me"
    jwt_algorithm: str = "HS256"
    jwt_expire_minutes: int = 1440

    cors_origins: str = "http://localhost:5173,http://localhost:5174,http://localhost:5175,http://localhost:5176"

    starting_virtual_balance: float = 100000.0

    alphavantage_api_key: str = ""
    gnews_api_key: str = ""
    openai_api_key: str = ""

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    @property
    def cors_origin_list(self) -> list[str]:
        return [o.strip() for o in self.cors_origins.split(",") if o.strip()]


settings = Settings()
