from pathlib import Path

from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

BACKEND_DIR = Path(__file__).resolve().parents[2]


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=BACKEND_DIR / ".env", env_file_encoding="utf-8")

    supabase_url: str
    supabase_service_key: SecretStr
    backup_bucket: str = "backups"
    backup_keep_days: int = 30
    backup_hour: int = 18
    database_path: Path = BACKEND_DIR / "veresiye.db"


settings = Settings()