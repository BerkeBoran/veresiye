import os
import sys
from pathlib import Path

from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

APP_NAME = "VeresiyeTakip"

IS_FROZEN = getattr(sys, "frozen", False)

BACKEND_DIR = Path(__file__).resolve().parents[2]


def get_data_dir() -> Path:
    if IS_FROZEN:
        data_dir = Path(os.environ.get("APPDATA")) / APP_NAME
    else:
        data_dir = BACKEND_DIR
    data_dir.mkdir(parents=True, exist_ok=True)
    return data_dir


def get_bundle_dir() -> Path:
    if IS_FROZEN:
        return Path(sys._MEIPASS)
    return BACKEND_DIR

DATA_DIR = get_data_dir()
BUNDLE_DIR = get_bundle_dir()

MIGRATIONS_DIR = BUNDLE_DIR / "migrations" if IS_FROZEN else BACKEND_DIR / "alembic"
FRONTEND_DIR = BUNDLE_DIR / "frontend" if IS_FROZEN else BACKEND_DIR.parent / "frontend" / "dist"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=DATA_DIR / ".env", env_file_encoding="utf-8")

    supabase_url: str | None = None
    supabase_service_key: SecretStr | None = None
    backup_bucket: str = "backups"
    backup_keep_days: int = 30
    backup_hour: int = 18
    database_path: Path = DATA_DIR / "veresiye.db"

    @property
    def backup_enabled(self) -> bool:
        return bool(self.supabase_url and self.supabase_service_key)


settings = Settings()