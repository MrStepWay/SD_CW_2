from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    DATABASE_URL: str
    FILE_STORAGE_SERVICE_URL: str
    WORD_CLOUD_API_URL: str = "https://quickchart.io/wordcloud"
    IMAGE_STORAGE_PATH: str = "/images"

settings = Settings()