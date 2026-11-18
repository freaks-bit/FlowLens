
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # PostgreSQL configuration
    db_host: str = "localhost"
    db_port: int = 5432
    db_name: str = "flowlens"
    db_user: str = "flowlens_app"
    db_password: str
    db_sslmode: str = "prefer"

    # Approved frontend origins, separated by commas
    cors_origins: str = (
        "http://localhost:5173,"
        "http://127.0.0.1:5173"
    )

    # Secure default: reject database-changing API requests
    demo_read_only: bool = True

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()
