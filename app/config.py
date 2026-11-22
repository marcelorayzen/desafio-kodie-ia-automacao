from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    gemini_api_key: str = ""
    # Nome do modelo é configurável: confirme o vigente no Google AI Studio.
    gemini_model: str = "gemini-flash-latest"
    gemini_timeout_seconds: float = 30.0
    confidence_threshold: float = 0.6


def get_settings() -> Settings:
    return Settings()
