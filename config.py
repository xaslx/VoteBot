from pydantic_settings import BaseSettings, SettingsConfigDict





class Settings(BaseSettings):
    TOKEN_BOT: str
    CHANNEL_ID: str
    REDIS_HOST: str
    REDIS_PORT: int
    ID_ADMINS_GROUP: str

    model_config = SettingsConfigDict(env_file=".env")

settings: Settings = Settings()