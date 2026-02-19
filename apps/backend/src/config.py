from pydantic_settings import BaseSettings
from pathlib import Path


class Settings(BaseSettings):
    # API
    environment: str = "development"
    cors_origins: str = "http://localhost:5173"
    session_secret: str = "change-me-in-production"

    # Database
    database_url: str = "sqlite+aiosqlite:///./data/app.db"

    # Storage
    upload_dir: str = "./uploads"
    max_file_size_mb: int = 25
    max_session_size_mb: int = 100

    # AI
    google_api_key: str = ""
    gemini_model: str = "gemini-2.0-flash"

    # External APIs
    ep_online_api_key: str = ""

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}

    @property
    def upload_path(self) -> Path:
        path = Path(self.upload_dir)
        path.mkdir(parents=True, exist_ok=True)
        return path


settings = Settings()
