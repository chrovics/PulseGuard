from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    PROJECT_NAME: str = "PulseGuard API"
    VERSION: str = "1.0.0"
    
    # Baza de date
    DATABASE_URL: str
    
    # Securitate
    SECRET_KEY: str
    ALGORITHM: str = "HS256"

    # Alerte Telegram
    TELEGRAM_BOT_TOKEN: str | None = None
    TELEGRAM_CHAT_ID: str | None = None

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

settings = Settings()
