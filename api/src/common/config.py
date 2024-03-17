from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")
    # log
    # log level
    log_level: str = "INFO"

    # app settings
    app_name: str = "Moonhub API - Takehome"
    debug: bool = False
    listen_address: str = "0.0.0.0"
    port: int = 3024
    reload: bool = False

    # qdrant settings
    # qdrant_host: str = "qdrant"
    # qdrant_port: int = 6333

    # redis settings
    redis_url: str = "redis://redis:6379"

    # postgres settings
    database_url: str = "postgresql://postgres:postgres@postgres:5432/postgres"

    # nylas
    nylas_client_id: str
    nylas_api_key: str
    nylas_api_region_uri: str


# export settings
settings = Settings()
