from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "EduGenie"

    host: str = "127.0.0.1"
    port: int = 8000

    gemini_api_key: str = ""
    gemini_model: str = "gemini-3.8-flash"

    local_explainer_enabled: bool = False
    local_explainer_model: str = "MBZUAI/LaMini-Flan-T5-783M"

    max_input_length: int = 20000
    request_timeout: int = 60

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()