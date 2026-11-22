from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    gemini_api_key: str = ""
    # Modelo fixado (não um apelido "-latest"): escolha e medição em docs/ARQUITETURA.md.
    gemini_model: str = "gemini-3.5-flash"
    # Raciocínio interno do modelo: "low" mantém a resposta em ~2 s; vazio usa o padrão do modelo.
    gemini_thinking_level: str = "low"
    gemini_timeout_seconds: float = 30.0
    confidence_threshold: float = 0.6


def get_settings() -> Settings:
    return Settings()
