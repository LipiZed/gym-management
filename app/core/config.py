from pydantic_settings import BaseSettings, SettingsConfigDict




class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    DATABASE_URL: str
    SECRET_KEY: str
    SYNC_DATABASE_URL: str
    ADMIN_EMAIL: str
    ADMIN_PASSWORD: str


settings = Settings()