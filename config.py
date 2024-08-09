from pydantic_settings import BaseSettings, SettingsConfigDict





class Settings(BaseSettings):
    TOKEN_BOT: str
    LIST_ADMINS: list[str]
    CHANNEL_ID: str

    model_config = SettingsConfigDict(env_file=".env")

settings: Settings = Settings()