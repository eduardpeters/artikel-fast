from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    cors_origins: str
    environment: str

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()  # type: ignore will be instanced with environment variables
