from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    # URL внутренних сервисов,
    FILE_STORAGE_SERVICE_URL: str
    FILE_ANALYSIS_SERVICE_URL: str

settings = Settings()